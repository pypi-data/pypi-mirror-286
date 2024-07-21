# pyright: reportIncompatibleVariableOverride=false
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict

from yiriob.event.base import EventBase
from yiriob.message.message_chain import MessageChain

# Attention!
# All the code are from nonebot/adapter-onebot.
# We use and modify the code under MIT license.


class Sender(BaseModel):
    user_id: Optional[int] = None
    nickname: Optional[str] = None
    sex: Optional[str] = None
    age: Optional[int] = None
    card: Optional[str] = None
    area: Optional[str] = None
    level: Optional[str] = None
    role: Optional[str] = None
    title: Optional[str] = None

    model_config = ConfigDict(extra="allow")


class Reply(BaseModel):
    time: int
    message_type: str
    message_id: int
    real_id: int
    sender: Sender
    message: MessageChain

    model_config = ConfigDict(extra="allow")


class Anonymous(BaseModel):
    id: int
    name: str
    flag: str

    model_config = ConfigDict(extra="allow")


class File(BaseModel):
    id: str
    name: str
    size: int
    busid: int

    model_config = ConfigDict(extra="allow")


class Status(BaseModel):
    online: bool
    good: bool

    model_config = ConfigDict(extra="allow")


# Message Events
class MessageEvent(EventBase):
    """消息事件"""

    post_type: Literal["message"]
    sub_type: str
    user_id: int
    message_type: str
    message_id: int
    message: MessageChain
    original_message: Optional[MessageChain] = None
    raw_message: str
    font: int
    sender: Sender
    to_me: bool = False
    """
    :说明: 消息是否与机器人有关
    """
    reply: Optional[Reply] = None
    """
    :说明: 消息中提取的回复消息，内容为 ``get_msg`` API 返回结果
    """


class PrivateMessageEvent(MessageEvent):
    """私聊消息"""

    message_type: Literal["private"]


class GroupMessageEvent(MessageEvent):
    """群消息"""

    message_type: Literal["group"]
    group_id: int
    anonymous: Optional[Anonymous] = None


# Notice Events
class NoticeEvent(EventBase):
    """通知事件"""

    post_type: Literal["notice"]
    notice_type: str


class GroupUploadNoticeEvent(NoticeEvent):
    """群文件上传事件"""

    notice_type: Literal["group_upload"]
    user_id: int
    group_id: int
    file: File


class GroupAdminNoticeEvent(NoticeEvent):
    """群管理员变动"""

    notice_type: Literal["group_admin"]
    sub_type: str
    user_id: int
    group_id: int


class GroupDecreaseNoticeEvent(NoticeEvent):
    """群成员减少事件"""

    notice_type: Literal["group_decrease"]
    sub_type: str
    user_id: int
    group_id: int
    operator_id: int


class GroupIncreaseNoticeEvent(NoticeEvent):
    """群成员增加事件"""

    notice_type: Literal["group_increase"]
    sub_type: str
    user_id: int
    group_id: int
    operator_id: int


class GroupBanNoticeEvent(NoticeEvent):
    """群禁言事件"""

    notice_type: Literal["group_ban"]
    sub_type: str
    user_id: int
    group_id: int
    operator_id: int
    duration: int


class FriendAddNoticeEvent(NoticeEvent):
    """好友添加事件"""

    notice_type: Literal["friend_add"]
    user_id: int


class GroupRecallNoticeEvent(NoticeEvent):
    """群消息撤回事件"""

    notice_type: Literal["group_recall"]
    user_id: int
    group_id: int
    operator_id: int
    message_id: int


class FriendRecallNoticeEvent(NoticeEvent):
    """好友消息撤回事件"""

    notice_type: Literal["friend_recall"]
    user_id: int
    message_id: int


class NotifyEvent(NoticeEvent):
    """提醒事件"""

    notice_type: Literal["notify"]
    sub_type: str
    user_id: int
    group_id: int


class PokeNotifyEvent(NotifyEvent):
    """戳一戳提醒事件"""

    sub_type: Literal["poke"]
    target_id: int
    group_id: Optional[int] = None


class LuckyKingNotifyEvent(NotifyEvent):
    """群红包运气王提醒事件"""

    sub_type: Literal["lucky_king"]
    target_id: int


class HonorNotifyEvent(NotifyEvent):
    """群荣誉变更提醒事件"""

    sub_type: Literal["honor"]
    honor_type: str


# Request Events
class RequestEvent(EventBase):
    """请求事件"""

    post_type: Literal["request"]
    request_type: str


class FriendRequestEvent(RequestEvent):
    """加好友请求事件"""

    request_type: Literal["friend"]
    user_id: int
    flag: str
    comment: Optional[str] = None


class GroupRequestEvent(RequestEvent):
    """加群请求/邀请事件"""

    request_type: Literal["group"]
    sub_type: str
    group_id: int
    user_id: int
    flag: str
    comment: Optional[str] = None


# Meta Events
class MetaEvent(EventBase):
    """元事件"""

    post_type: Literal["meta_event"]
    meta_event_type: str


class LifecycleMetaEvent(MetaEvent):
    """生命周期元事件"""

    meta_event_type: Literal["lifecycle"]
    sub_type: str


class HeartbeatMetaEvent(MetaEvent):
    """心跳元事件"""

    meta_event_type: Literal["heartbeat"]
    status: Status
    interval: int


__all__ = [
    "MessageEvent",
    "PrivateMessageEvent",
    "GroupMessageEvent",
    "NoticeEvent",
    "GroupUploadNoticeEvent",
    "GroupAdminNoticeEvent",
    "GroupDecreaseNoticeEvent",
    "GroupIncreaseNoticeEvent",
    "GroupBanNoticeEvent",
    "FriendAddNoticeEvent",
    "GroupRecallNoticeEvent",
    "FriendRecallNoticeEvent",
    "NotifyEvent",
    "PokeNotifyEvent",
    "LuckyKingNotifyEvent",
    "HonorNotifyEvent",
    "RequestEvent",
    "FriendRequestEvent",
    "GroupRequestEvent",
    "MetaEvent",
    "LifecycleMetaEvent",
    "HeartbeatMetaEvent",
]
