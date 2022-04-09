from enum import Enum


class Method(Enum):
    ADD_URI = "aria2.addUri"
    REMOVE = "aria2.remove"
    PAUSE = "aria2.pause"
    UNPAUSE = "aria2.unpause"
    TELL_STATUS = "aria2.tellStatus"
    TELL_ACTIVE = "aria2.tellActive"
    TELL_WAITING = "aria2.tellWaiting"
    TELL_STOPPED = "aria2.tellStopped"
    GET_GLOBAL_STAT = "aria2.getGlobalStat"
    PURGE_DOWNLOAD_RESULT = "aria2.purgeDownloadResult"
    GET_VERSION = "aria2.getVersion"
