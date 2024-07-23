import json
import threading
from typing import Optional, Callable, List, Union, Any

from . import globals
from .interface_network import IStreamingListeners
from .statsig_network import _StatsigNetwork
from .statsig_options import StatsigOptions
from .interface_data_store import IDataStore
from .diagnostics import Diagnostics, Marker, Context, Key
from .evaluation_details import EvaluationReason
from .statsig_error_boundary import _StatsigErrorBoundary
from .statsig_errors import StatsigValueError, StatsigNameError
from .thread_util import spawn_background_thread, THREAD_JOIN_TIMEOUT
from .utils import djb2_hash


RULESETS_SYNC_INTERVAL = 10
IDLISTS_SYNC_INTERVAL = 60
SYNC_OUTDATED_MAX_S = 120
STORAGE_ADAPTER_KEY = "statsig.cache"

class SpecUpdater:
    def __init__(self, network: _StatsigNetwork, data_adapter: Optional[IDataStore], options: StatsigOptions,
                 diagnostics: Diagnostics, sdk_key: str, error_boundary: _StatsigErrorBoundary, statsig_metadata: dict,
                 shutdown_event: threading.Event):
        self._shutdown_event = shutdown_event
        self._sync_failure_count = 0
        self._network = network
        self._options = options
        self._diagnostics = diagnostics
        self._sdk_key = sdk_key
        self._error_boundary = error_boundary
        self._statsig_metadata = statsig_metadata
        self._background_download_configs = None
        self._background_download_id_lists = None

        self.initialized = False
        self.last_update_time = 0
        self.initial_update_time = 0
        self.dcs_listener: Optional[Callable] = None
        self.id_lists_listener: Optional[Callable] = None
        self.data_adapter = data_adapter

    def register_process_network_id_lists_listener(self, listener: Callable):
        self.id_lists_listener = listener

    def register_process_dcs_listener(self, listener: Callable):
        self.dcs_listener = listener

    def load_config_specs_from_storage_adapter(self) -> bool:
        self._log_process("Loading specs from adapter")
        if self._options.data_store is None:
            return False

        self._diagnostics.add_marker(Marker().data_store_config_specs().process().start())

        cache_string = self._options.data_store.get(STORAGE_ADAPTER_KEY)
        if not isinstance(cache_string, str):
            return False

        cache = json.loads(cache_string)
        if not isinstance(cache, dict):
            globals.logger.warning(
                "Invalid type returned from StatsigOptions.data_store")
            return False
        adapter_time = cache.get("time", None)
        if not isinstance(adapter_time,
                          int) or adapter_time < self.last_update_time:
            return False

        self._log_process("Done loading specs")
        if self.dcs_listener and self.dcs_listener(cache, EvaluationReason.data_adapter):
            self._diagnostics.add_marker(Marker().data_store_config_specs().process().end(
                {'success': True}))
            return True

        self._diagnostics.add_marker(Marker().data_store_config_specs().process().end(
            {'success': False}))
        self._diagnostics.log_diagnostics(Context.CONFIG_SYNC, Key.DATA_STORE_CONFIG_SPECS)
        return False

    def download_config_specs(self, for_initialize: bool = False):
        def on_complete(specs: dict, error: Optional[Exception]):
            if error is not None:
                result[0], result[1] = False, error
                return

            if specs is None:
                self._sync_failure_count += 1
                result[0], result[1] = False, StatsigValueError(
                    "Failed to download specs from network")
                return

            try:
                self._diagnostics.add_marker(Marker().download_config_specs().process().start())
                self._log_process("Done loading specs")
                if self.dcs_listener and self.dcs_listener(specs, EvaluationReason.network):
                    result[0] = True
                    self._save_to_storage_adapter(specs)
            except Exception as err:
                result[0], result[1] = False, err
                return
            finally:
                self._diagnostics.add_marker(Marker().download_config_specs().process().end(
                    {'success': result[0]}))

        self._log_process("Loading specs from network...")

        timeout: Optional[int] = None
        if for_initialize:
            timeout = self._options.init_timeout

        result: List[Union[bool, Optional[Exception]]] = [False, None]
        try:
            self._network.get_dcs(on_complete,
                                  self.last_update_time, False, timeout)
            if result[0] is False:
                self._network.get_dcs_fallback(on_complete, self.last_update_time, False, timeout)

        except Exception as e:
            result[0], result[1] = False, e
        finally:
            self._diagnostics.log_diagnostics(Context.CONFIG_SYNC, Key.DOWNLOAD_CONFIG_SPECS)
        return result[0], result[1]


    def _log_process(self, msg, process=None):
        if process is None:
            process = "Initialize" if not self.initialized else "Sync"
        globals.logger.log_process(process, msg)

    def _save_to_storage_adapter(self, specs):
        if not self.is_specs_json_valid(specs):
            return

        if self._options.data_store is None:
            return

        if self.last_update_time == 0:
            return

        self._options.data_store.set(STORAGE_ADAPTER_KEY, json.dumps(specs))

    def is_specs_json_valid(self, specs_json):
        if specs_json is None or specs_json.get("time") is None:
            return False
        hashed_sdk_key_used = specs_json.get("hashed_sdk_key_used", None)
        if hashed_sdk_key_used is not None and hashed_sdk_key_used != djb2_hash(self._sdk_key):
            return False
        if specs_json.get("has_updates", False) is False:
            return False
        return True

    def bootstrap_config_specs(self):
        self._diagnostics.add_marker(Marker().bootstrap().process().start())
        if self._options.bootstrap_values is None:
            return

        success = False

        try:
            specs = json.loads(self._options.bootstrap_values)
            if specs is None or not self.is_specs_json_valid(specs):
                return
            if self.dcs_listener is not None:
                success = self.dcs_listener(specs, EvaluationReason.bootstrap)

        except ValueError:
            # JSON decoding failed, just let background thread update rulesets
            globals.logger.error(
                'Failed to parse bootstrap_values')
        finally:
            self._diagnostics.add_marker(Marker().bootstrap().process().end(
                {'success': success}))

    def download_id_lists(self, for_initialize=False):
        def on_complete(id_lists: list, error: Exception):
            if error is not None:
                self._error_boundary.log_exception("_download_id_lists", error)
                return
            if id_lists is None:
                return
            result[0] = True
            if self.id_lists_listener is not None:
                self.id_lists_listener(id_lists)

        result: List[bool] = [False]

        try:
            timeout: Optional[int] = None
            if for_initialize:
                timeout = self._options.init_timeout

            self._network.get_id_lists(on_complete, False, timeout)
            if result[0] is False:
                self._network.get_id_lists_fallback(on_complete, False, timeout)

        except Exception as e:
            raise e
        finally:
            self._diagnostics.log_diagnostics(Context.CONFIG_SYNC, Key.GET_ID_LIST)

    def download_single_id_list(
            self, url, list_name, local_list, all_lists, start_index):
        def on_complete(resp: Any):
            if resp is None:
                return
            threw_error = False
            try:
                self._diagnostics.add_marker(Marker().get_id_list().process().start({'url': url}))
                content_length_str = resp.headers.get('content-length')
                if content_length_str is None:
                    raise StatsigValueError("Content length invalid.")
                content_length = int(content_length_str)
                content = resp.text
                if content is None:
                    return
                first_char = content[0]
                if first_char not in ('+', '-'):
                    raise StatsigNameError("Seek range invalid.")
                lines = content.splitlines()
                for line in lines:
                    if len(line) <= 1:
                        continue
                    op = line[0]
                    id = line[1:].strip()
                    if op == "+":
                        local_list.get("ids", set()).add(id)
                    elif op == "-":
                        local_list.get("ids", set()).discard(id)
                local_list["readBytes"] = start_index + content_length
                all_lists[list_name] = local_list
            except Exception as e:
                threw_error = True
                self._error_boundary.log_exception("_download_single_id_list", e)
            finally:
                self._diagnostics.add_marker(Marker().get_id_list().process().end({
                    'url': url,
                    'success': not threw_error,
                }))

        self._network.get_id_list(on_complete,
                                  url, headers={"Range": f"bytes={start_index}-"})

    def start_background_threads(self):
        if self._options.local_mode:
            return
        self._diagnostics.set_context(Context.CONFIG_SYNC)
        if self._network.is_pull_worker("download_config_specs"):
            if self._background_download_configs is None or not self._background_download_configs.is_alive():
                self._spawn_bg_poll_dcs()
        else:
            def on_update_dcs(specs: dict, lcut: int):
                if self.last_update_time > lcut:
                    return
                if self.dcs_listener is not None:
                    self.dcs_listener(specs, EvaluationReason.network)

            def on_error_dcs(e: Exception):
                # pylint: disable=unused-argument
                pass

            self._network.listen_for_dcs(IStreamingListeners(
                on_error=on_error_dcs,
                on_update=on_update_dcs
            ))

        if self._network.is_pull_worker("download_id_lists"):
            if self._background_download_id_lists is None or not self._background_download_id_lists.is_alive():
                self._spawn_bg_poll_id_lists()
        else:
            def on_update_id_list(id_lists: list, lcut: int):
                if self.last_update_time > lcut:
                    return
                if self.id_lists_listener is not None:
                    self.id_lists_listener(id_lists)

            def on_error_id_list(e: Exception):
                self._error_boundary.log_exception("_listen_for_id_list", e)

            self._network.listen_for_id_lists(IStreamingListeners(
                on_error=on_error_id_list,
                on_update=on_update_id_list
            ))

    def _spawn_bg_poll_dcs(self):
        interval = self._options.rulesets_sync_interval or RULESETS_SYNC_INTERVAL
        fast_start = self._sync_failure_count > 0

        if self._options.data_store is not None and self._options.data_store.should_be_used_for_querying_updates(
                STORAGE_ADAPTER_KEY):
            self._background_download_configs = spawn_background_thread(
                "bg_download_config_specs_from_storage_adapter",
                self._sync,
                (self.load_config_specs_from_storage_adapter, interval, fast_start),
                self._error_boundary)
        else:
            self._background_download_configs = spawn_background_thread(
                "bg_download_config_specs",
                self._sync,
                (self.download_config_specs, interval, fast_start),
                self._error_boundary)

    def _spawn_bg_poll_id_lists(self):
        interval = self._options.idlists_sync_interval or IDLISTS_SYNC_INTERVAL
        self._background_download_id_lists = spawn_background_thread(
            "bg_download_id_lists",
            self._sync,
            (self.download_id_lists, interval),
            self._error_boundary)

    def _sync(self, sync_func, interval, fast_start=False):
        if fast_start:
            sync_func()

        while True:
            try:
                if self._shutdown_event.wait(interval):
                    break
                sync_func()
            except Exception as e:
                self._error_boundary.log_exception("_sync", e)

    def shutdown(self):
        if self._background_download_configs is not None:
            self._background_download_configs.join(THREAD_JOIN_TIMEOUT)

        if self._background_download_id_lists is not None:
            self._background_download_id_lists.join(THREAD_JOIN_TIMEOUT)
