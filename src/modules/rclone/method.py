from enum import Enum


class Method(Enum):
    CORE_VERSION = "core/version"
    LIST_REMOTES = "config/listremotes"
    JOB_LIST = "job/list"
    JOB_STOP = "job/stop"
