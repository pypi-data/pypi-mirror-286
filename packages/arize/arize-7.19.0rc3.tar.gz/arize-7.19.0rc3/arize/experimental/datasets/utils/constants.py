import os
from enum import Enum
from pathlib import Path

from openinference.semconv import resource, trace

from .. import requests_pb2 as request_pb

"""Environmental configuration"""

# Override ARIZE Default Profile when reading from the config-file in a session.
ARIZE_PROFILE = os.getenv("ARIZE_PROFILE")

# Override ARIZE API Token when creating a session.
ARIZE_API_KEY = os.getenv("ARIZE_API_KEY")

INFERENCES = request_pb.INFERENCES
GENERATIVE = request_pb.GENERATIVE

"""Internal Use"""

# Default API endpoint when not provided through env variable nor profile
DEFAULT_ARIZE_FLIGHT_HOST = "flight.arize.com"
DEFAULT_ARIZE_FLIGHT_PORT = 443

# Name of the current package.
DEFAULT_PACKAGE_NAME = "arize_python_datasets_client"

# Default config keys for the Arize config file. Created via the CLI.
DEFAULT_ARIZE_API_KEY_CONFIG_KEY = "api_key"

# Default headers to trace and help identify requests. For debugging.
DEFAULT_ARIZE_SESSION_ID = "x-arize-session-id"  # Generally the session name.
DEFAULT_ARIZE_TRACE_ID = "x-arize-trace-id"
DEFAULT_PACKAGE_VERSION = "x-package-version"

# File name for profile configuration.
PROFILE_FILE_NAME = "profiles.ini"

# Default profile to be used.
DEFAULT_PROFILE_NAME = "default"

# Default path where any configuration files are written.
DEFAULT_CONFIG_PATH = os.path.join(str(Path.home()), ".arize")

# Default initial wait time for retries in seconds.
DEFAULT_RETRY_INITIAL_WAIT_TIME = 0.25

# Default maximum wait time for retries in seconds.
DEFAULT_RETRY_MAX_WAIT_TIME = 10.0

# Default to use grpc + tls scheme.
DEFAULT_TRANSPORT_SCHEME = "grpc+tls"


class FLIGHT_ACTION_KEY(Enum):
    GET_DATASET_VERSION = "get_dataset_version"
    LIST_DATASETS = "list_datasets"
    DELETE_DATASET = "delete_dataset"


OPEN_INFERENCE_JSON_STR_TYPES = frozenset(
    [
        trace.DocumentAttributes.DOCUMENT_METADATA,
        trace.SpanAttributes.LLM_FUNCTION_CALL,
        trace.SpanAttributes.LLM_INVOCATION_PARAMETERS,
        trace.SpanAttributes.LLM_PROMPT_TEMPLATE_VARIABLES,
        trace.MessageAttributes.MESSAGE_FUNCTION_CALL_ARGUMENTS_JSON,
        trace.SpanAttributes.METADATA,
        trace.SpanAttributes.TOOL_PARAMETERS,
        trace.ToolCallAttributes.TOOL_CALL_FUNCTION_ARGUMENTS_JSON,
    ]
)
