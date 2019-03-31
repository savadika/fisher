# -*- coding: utf-8 -*-#

# -------------------------------------------------------------------------------
# Name:         drift
# Description:  drift模型的viewModel显示
# Author:       ylf
# Date:         2019-03-30
# -------------------------------------------------------------------------------
from apps.libs import my_time
from apps.libs.enums import PendingStatus



class DriftViewModel():
    """根据传入的drift显示自己需要的数据模型"""
    """最终需要返回的是一个【】列表组，里面是一组的drift对象"""

    def __init__(self, drifts, current_user_id):
        """根据传入的drifts以及当前用户的id来生成显示的模型"""
        self.data = []
        self.muliti_drift(drifts, current_user_id)

    def muliti_drift(self, drifts, current_user_id):
        """组装多本书籍所组成的列表"""
        for drift in drifts:
            single = self.single_drift(drift, current_user_id)
            self.data.append(single)

    def single_drift(self, drift, current_user_id):
        """显示单本书籍需要显示的信息"""
        """难点：根据不同的用户的信息判断他到底是赠送者还是索要者"""
        you_are = self.who_are_you(drift, current_user_id)
        status_str = PendingStatus.get_pending_status_str(
            drift.pending, you_are)
        r = {
            'you_are': you_are,
            'drift_id': drift.id,
            'book_title': drift.book_title,
            'book_author': drift.book_author,
            'book_img': drift.book_img,
            'date': my_time.timestamp_to_time(drift.create_time),
            'operator': drift.requester_nickname if you_are != 'requester'
            else drift.gifter_nickname,
            'message': drift.message,
            'address': drift.address,
            'status_str': status_str,
            'recipient_name': drift.recipient_name,
            'mobile': drift.mobile,
            'status': drift.pending
        }
        return r

    def who_are_you(self, drift, current_user_id):
        """根据给定的drift 和当前登陆用户 ，判断用户是赠送者还是请求者"""
        you_are = ''
        if drift.requester_id == current_user_id:
            you_are = 'requester'
        if drift.gifter_id == current_user_id:
            you_are = 'gifter'
        return you_are
