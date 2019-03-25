from enum import Enum


class PendingStatus(Enum):
    """
    定义交易状态的4种属性的枚举值
    """
    Waiting = 1  # 等待
    Success = 2  # 成功
    Reject = 3  # 拒绝
    Redraw = 4  # 已寄
    pass
