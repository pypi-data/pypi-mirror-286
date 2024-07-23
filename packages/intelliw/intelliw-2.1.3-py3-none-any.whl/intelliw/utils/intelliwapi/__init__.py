from contextvars import ContextVar
from intelliw.utils.intelliwapi.request import Request

_data_pool_context_storage: ContextVar = ContextVar(
    "data-pool", default=None
)


_request_traceid_context_storage: ContextVar = ContextVar(
    "request-traceid", default='0'
)