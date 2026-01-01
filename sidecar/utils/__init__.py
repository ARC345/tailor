"""
Tailor - Utilities Package

Utility modules for the Tailor sidecar application.
"""

from .logging_config import (
    configure_logging,
    get_logger,
    get_plugin_logger,
    set_log_level,
    setup_dev_logging,
)
from .json_rpc import (
    build_request,
    build_response,
    build_error,
    build_parse_error,
    build_invalid_request_error,
    build_method_not_found_error,
    build_invalid_params_error,
    build_internal_error,
    validate_jsonrpc_message,
    is_request,
    is_response,
    is_notification,
    get_request_id,
    get_method,
    get_params,
)
from .path_utils import (
    validate_vault_path,
    validate_plugin_structure,
    safe_path_join,
    ensure_directory,
    get_vault_config_path,
    get_memory_dir,
    get_plugins_dir,
    get_lib_dir,
    discover_plugins,
    is_safe_filename,
    get_relative_path,
)

__all__ = [
    # Logging
    "configure_logging",
    "get_logger",
    "get_plugin_logger",
    "set_log_level",
    "setup_dev_logging",
    # JSON-RPC
    "build_request",
    "build_response",
    "build_error",
    "build_parse_error",
    "build_invalid_request_error",
    "build_method_not_found_error",
    "build_invalid_params_error",
    "build_internal_error",
    "validate_jsonrpc_message",
    "is_request",
    "is_response",
    "is_notification",
    "get_request_id",
    "get_method",
    "get_params",
    # Path utilities
    "validate_vault_path",
    "validate_plugin_structure",
    "safe_path_join",
    "ensure_directory",
    "get_vault_config_path",
    "get_memory_dir",
    "get_plugins_dir",
    "get_lib_dir",
    "discover_plugins",
    "is_safe_filename",
    "get_relative_path",
]
