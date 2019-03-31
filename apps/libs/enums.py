from enum import Enum


class PendingStatus(Enum):
    """
    定义交易状态的4种属性的枚举值
    """
    Waiting = 1  # 等待
    Success = 2  # 成功
    Reject = 3  # 拒绝
    Redraw = 4  # 已寄

    @classmethod
    def get_pending_status_str(cls, status, user):
        """根据stauts 和 user 来综合返回所需要的状态"""
        r = {
            1 : {
                'requester': '等待对方邮寄',
                'gifter': '等待你邮寄'
            },
            2 : {
                'requester': '对方已同意',
                'gifter': '您已同意'
            },
            3 : {
                'requester': '对方已拒绝',
                'gifter': '您已拒绝'
            },
            4 : {
                'requester': '对方已邮寄',
                'gifter': '您已邮寄'
            }
        }
        return r[status][user]
