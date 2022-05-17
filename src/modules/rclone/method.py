from enum import Enum, auto


class Method(Enum):
    CORE_VERSION = "core/version"
    LIST_REMOTES = "config/listremotes"
    JOB_LIST = "job/list"
    JOB_STOP = "job/stop"
    SYNC_COPY = "sync/copy"
    SYNC_MOVE = "sync/move"
    SYNC_SYNC = "sync/sync"
    OPERATIONS_COPYFILE = "operations/copyfile"
    OPERATIONS_MOVEFILE = "operations/movefile"
    OPERATIONS_LIST = "operations/list"
    CORE_STATS = "core/stats"


class Operation(Enum):
    COPY = auto()
    MOVE = auto()
    SYNC = auto()
