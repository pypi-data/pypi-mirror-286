from copy import deepcopy

from intelliw.utils.intelliwapi import _data_pool_context_storage, _request_traceid_context_storage
from contextvars import copy_context, ContextVar


class _Context:
    def __init__(self, instance: ContextVar):
        self.ctx = instance

    def get(self):
        try:
            return self.ctx.get()
        except LookupError as e:
            raise RuntimeError(
                "You didn't use ContextMiddleware or "
                "you're trying to access `context` object "
                "outside of the request-response cycle."
            ) from e

    def copy_set(self, data):
        return self.ctx.set(
            deepcopy(data)
        )

    def set(self, data):
        return self.ctx.set(
            data
        )

    def exists(self) -> bool:
        return self.ctx in copy_context()


# context = _Context(_data_pool_context_storage)
traceid_ctx = _Context(_request_traceid_context_storage)
