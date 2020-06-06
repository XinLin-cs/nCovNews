# -*- coding: utf-8 -*-
# @Time    : 2019/11/27 23:00
# @Author  : Leon
# @Email   : 1446684220@qq.com
# @File    : test.py
# @Desc    : 
# @Software: PyCharm

from WechatPCAPI.WechatPCAPI import WechatPCAPI
import time
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


# 消息处理示例 仅供参考
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
                        wx_inst.send_text(to_user=msg_from_id, msg='小助手让你发指令，您还真就只发‘指令’啊(>_ <)')
                        time.sleep(1)
                else:
                    wx_inst.send_text(to_user=msg_from_id, msg='小助手还不懂得怎么聊天呢，发送‘#指令’来和小助手互动吧')
                    msg = '指令列表\n'
                    msg += '#疫情小助手\n'
                    msg += '#今日疫情\n'
                    msg += '#疫情新闻\n'
                    wx_inst.send_text(to_user=msg_from_id, msg=msg)
                    time.sleep(1)
        
                    



def main():
    wx_inst = WechatPCAPI(on_message=on_message, log=logging)
    wx_inst.start_wechat(block=True)

    while not wx_inst.get_myself():
        time.sleep(5)

    print('登陆成功')
    print(wx_inst.get_myself())

    #threading.Thread(target=thread_handle_message, args=(wx_inst,)).start()

    #time.sleep(10)
    #wx_inst.send_text(to_user='filehelper', msg='777888999')
    # time.sleep(1)
    # wx_inst.send_link_card(
    #     to_user='filehelper',
    #     title='博客',
    #     desc='我的博客，红领巾技术分享网站',
    #     target_url='http://www.honglingjin.online/',
    #     img_url='http://honglingjin.online/wp-content/uploads/2019/07/0-1562117907.jpeg'
    # )
    # time.sleep(1)
    #
    # wx_inst.send_img(to_user='filehelper', img_abspath=r'C:\Users\Leon\Pictures\1.jpg')
    # time.sleep(1)
    #
    # wx_inst.send_file(to_user='filehelper', file_abspath=r'C:\Users\Leon\Desktop\1.txt')
    # time.sleep(1)
    #
    # wx_inst.send_gif(to_user='filehelper', gif_abspath=r'C:\Users\Leon\Desktop\08.gif')
    # time.sleep(1)
    #
    # wx_inst.send_card(to_user='filehelper', wx_id='gh_6ced1cafca19')

    # 这个是获取群具体成员信息的，成员结果信息也从上面的回调返回
    #wx_inst.get_member_of_chatroom('22941059407@chatroom')

    # 新增@群里的某人的功能
    #wx_inst.send_text(to_user='22941059407@chatroom', msg='test for at someone', at_someone='wxid_6ij99jtd6s4722')

    # 这个是更新所有好友、群、公众号信息的，结果信息也从上面的回调返回
    # wx_inst.update_frinds()

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

if __name__ == '__main__':
    init()