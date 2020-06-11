# -*- coding: utf-8 -*-
# @Time    : 2019/11/27 23:00
# @Author  : Leon
# @Email   : 1446684220@qq.com
# @File    : test.py
# @Desc    : 
# @Software: PyCharm

from WechatPCAPI.WechatPCAPI import WechatPCAPI
import time
import datetime
import logging
from queue import Queue
import threading
from flask import url_for
from nCovNews import app,db
from nCovNews import datatype
from sqlalchemy import func


logging.basicConfig(level=logging.INFO)
queue_recved_message = Queue()


def on_message(message):
    queue_recved_message.put(message)

def thread_handle_message(wx_inst):
    while True:
        message = queue_recved_message.get()
        print(message)
        if 'msg' in message.get('type'):
            # 这里是判断收到的是消息 不是别的响应
            send_or_recv = message.get('data', {}).get('send_or_recv', '')
            if send_or_recv[0] == '0':
                msg_from_id = message.get('data', {}).get('from_wxid', '')
                msg_from_nickname =  message.get('data', {}).get('from_nickname', '')
                msg_time = message.get('data', {}).get('time', '')
                msg_content = message.get('data', {}).get('msg', '')
                # 0是收到的消息 1是发出的 对于1不要再回复了 不然会无限循环回复
                if '#' in msg_content:
                    if '#疫情小助手' in msg_content:
                        wx_inst.send_link_card(
                        to_user=msg_from_id,
                        title='疫情小助手',
                        desc='关注实时疫情数据及分析预测',
                        target_url='https://covnews.herokuapp.com/',
                        img_url='https://images.unsplash.com/photo-1516841273335-e39b37888115?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&dpr=1&auto=format&fit=crop&w=140&h=200&q=60')
                        time.sleep(1)
                    if '#订阅小助手' in msg_content:
                        session = db.session
                        user = datatype.WXUSER.query.first()
                        if user is None:
                            newuser = datatype.WXUSER(wxid=msg_from_id)
                            session.add(newuser)
                            wx_inst.send_text(to_user=msg_from_id, msg='订阅小助手成功(^-^)☆,每天中午12点小助手会将第一手数据发送给关注疫情的您')
                        else:
                            wx_inst.send_text(to_user=msg_from_id, msg='您已经订阅过小助手了哦')
                        session.commit()
                        time.sleep(1)
                    if '#取消订阅' in msg_content:
                        session = db.session
                        user = datatype.WXUSER.query.first()
                        if user is not None:
                            session.delete(user)
                            wx_inst.send_text(to_user=msg_from_id, msg='取消订阅成功，希望将来还能和小助手再会QAQ')
                        else:
                            wx_inst.send_text(to_user=msg_from_id, msg='您还没订阅小助手呢，用‘#订阅小助手’订阅我吧')
                        session.commit()
                        time.sleep(1)
                    if '#今日疫情' in msg_content:
                        # 中国数据查询
                        chinatotal = datatype.CHINATOTAL.query.order_by(datatype.CHINATOTAL.date.desc()).first()
                        # 世界数据查询
                        worldtotal = datatype.WORLDTOTAL.query.order_by(datatype.WORLDTOTAL.date.desc()).first()
                        # 国内疫情
                        msg1 = '今日国内疫情\n'
                        msg1 +='确诊：'+str(chinatotal.confirmed)+'\n'
                        msg1 +='疑似：'+str(chinatotal.suspected)+'\n'
                        msg1 +='治愈：'+str(chinatotal.cures)+'\n'
                        msg1 +='死亡：'+str(chinatotal.deaths)+'\n'
                        msg1 +='无症状感染：'+str(chinatotal.asymptomatic)+'\n'
                        msg1 +='更新时间：'+str(chinatotal.date)
                        wx_inst.send_text(to_user=msg_from_id, msg=msg1)
                        time.sleep(1)
                        # 国外疫情
                        msg2 = '今日海外疫情\n'
                        msg2 +='确诊：'+str(worldtotal.confirmed)+'\n'
                        msg2 +='治愈：'+str(worldtotal.cures)+'\n'
                        msg2 +='死亡：'+str(worldtotal.deaths)+'\n'
                        msg2 +='更新时间：'+str(chinatotal.date)
                        wx_inst.send_text(to_user=msg_from_id, msg=msg2)
                        time.sleep(1)
                    if '#疫情新闻' in msg_content:
                        wx_inst.send_text(to_user=msg_from_id, msg='小助手随机为您推荐')
                        time.sleep(1)
                        # 新闻查询
                        item = datatype.NEWS.query.order_by(func.random()).first()
                        wx_inst.send_link_card(
                        to_user=msg_from_id,
                        title=item.title,
                        desc=item.summary,
                        target_url=item.url)
                        time.sleep(1)
                    if '#指令' in msg_content:
                        msg = '指令列表\n'
                        msg += '#疫情小助手\n'
                        msg += '#订阅小助手\n'
                        msg += '#取消订阅\n'
                        msg += '#今日疫情\n'
                        msg += '#疫情新闻'
                        wx_inst.send_text(to_user=msg_from_id, msg=msg)
                        time.sleep(1)
                else:
                    wx_inst.send_text(to_user=msg_from_id, msg='小助手还不懂得怎么聊天呢，发送‘#指令’来和小助手互动吧')
                    time.sleep(1)
        
def init():
    wx_inst = WechatPCAPI(on_message=on_message, log=logging)
    wx_inst.start_wechat(block=True)

    while not wx_inst.get_myself():
        time.sleep(5)

    print('登陆成功')
    wx_inst.get_myself()
    time.sleep(1)

    threading.Thread(target=thread_handle_message, args=(wx_inst,)).start()
    time.sleep(1)

    while True:
        clock = datetime.datetime.today()
        print(clock)
        time.sleep(1)

if __name__ == '__main__':
    init()