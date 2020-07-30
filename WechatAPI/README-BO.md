# WechatPCAPI稳定付费版
微信PC版的API接口，可通过Python调用微信获取好友、群、公众号列表，并收发消息等功能。可用于二次开发在线微信机器人、微信消息监控、群控软件、开发界面作多个微信控制软件等用途。

**当前版本:@博@**  

该版本为收费版本，新用户可免费试用半个月15天，需要购买的请联系我。

**该版本和免费版本有什么不同？**

1. 更稳定。连续测试3个月，未出现账号退出和崩溃等异常现象。
2. 更准确。不漏消息，经过测试，连续转发大量消息，保证消息不遗漏。
3. 更可靠。付费版本由我维护和更新，购买的不仅仅是代码，还有服务。

**如果帮到你，帮我点个star。**
遇到问题可以提Issues，或联系我。

**联系我**
1. 关注公众号“燕幕自安”，回复作者即可得到联系方式。
2. 邮件到：mocha_lee@qq.com
3. QQ加讨论群联系我（**QQ群：579737590**(广告实在太多了，加了1元付费入群)）


## 功能列表

目前支持：

1. 微信多开
2. 获取好友、群、公众号列表
3. 接收消息（包括好友、群、公众号消息，支持文本、图片、视频、文件、语音等）
4. 发送消息（支持文本、图片、分享链接、文件、视频等格式，支持@群成员）
5. 删除好友
6. 接受好友转账
7. 同意群聊邀请、同意添加好友请求
8. 进群提醒和退群提醒、邀请进群提醒
9. 获取群成员详细信息

## 版本功能区别

<img src="https://github.com/Mocha-L/WechatPCAPI/blob/master/%E5%85%8D%E8%B4%B9%E7%89%88%E4%BB%98%E8%B4%B9%E7%89%88%E5%8C%BA%E5%88%AB.png" width="660px" />


## 怎么用？

1. clone/下载源码到本地(src-BO这个目录是付费版)
2. 安装源码包里的微信客户端WeChatSetup2.6.8.52.exe（和免费版微信客户端版本不同，请注意）
3. 执行源码中的test.py

**依赖库**
  
  pip install pycryptodomex
  
  pip install requests
  
  
目前提供pyd和依赖的相关文件，通过python直接import即可使用，目录里的test.py即是调用示例。

## 环境支持情况

windows 7/10 测试通过

python 3.6 3.7 3.8 三个python版本均是64位，不是这些版本可能会报错dll load 错误

**微信版本 付费版本目前仅支持V2.6.8.52版本，目录包里有该微信版本，直接下载安装即可。**

## 国内下载慢？

请进群获取最新版本代码和相关文件，有问题也可以在群里咨询讨论。

**QQ群：579737590**(广告实在太多了，加了1元付费入群)

![QQ群](https://github.com/Mocha-L/wechat_wegoing/blob/master/image/qq.png)

## 遇到问题？

0. 加群解决一切蛇皮问题。
1. 请保证微信版本是从我的包里装的。
2. 出现“找不到指定模块”，请安装支持的python版本运行（python 3.6 3.7 3.8 三个python版本均是64位），还不行的话，大致是因为windows相关运行库的缺失，请自行打开windows更新，或安装各个版本的运行时库。
3. 其他问题和接口问题请在Issues中提问。

## 函数文档注释

不知道怎么调用的话，可以使用``help(类名)``查看函数文档，如下：

    class WechatPCAPI(builtins.object)
     |  WechatPCAPI(on_message=None, on_wx_exit_handle=None, log=None)
     |  
     |  微信PC版的API接口--当前版本:@博@
     |  
     |  Methods defined here:
     |  
     |  __init__(self, on_message=None, on_wx_exit_handle=None, log=None)
     |      类初始化函数
     |      :param on_message: 收到微信消息时的回调函数
     |      :param on_wx_exit_handle: 微信退出的回调函数，可空
     |      :param log: 日志句柄
     |  
     |  delete_frinds(self, wx_id)
     |      删除好友（包括好友，公众号）
     |      :return: 无
     |  
     |  get_friends(self)
     |      获取全体好友信息(包括好友、群组、公众号)，如发现该好友信息不准确，可以先调用update_frinds接口后，再调用该接口。大多时候是准的^^
     |      :return:
     |  
     |  get_member_of_chatroom(self, chatroom_wxid)
     |      获取某群的成员信息
     |      :param chatroom_wxid: 群ID
     |      :return: 无
     |  
     |  get_myself(self)
     |      获取我的信息，即所登录账号的信息
     |      :return: 尚未登陆成功时为None, 登陆成功后为dict格式返回
     |  
     |  send_img(self, to_user, img_abspath)
     |      发送图片消息
     |      :param to_user: 发给谁（wx_id）
     |      :param img_abspath: 图片绝对路径
     |      :return: 无
     |  
     |  send_link_card(self, to_user, title, desc, target_url, img_url='')
     |      发送链接分享
     |      :param to_user: 发给谁（wx_id）
     |      :param title: 链接标题
     |      :param desc: 链接描述
     |      :param target_url: 链接URL
     |      :param img_url: 显示图片的URL
     |      :return: 无
     |  
     |  send_text(self, to_user, msg)
     |      发送文本消息
     |      :param to_user: 发给谁（wx_id）
     |      :param msg: 文本消息内容
     |      :return: 无
     |  
     |  start_wechat(self, block=True)
     |      启动微信，目前仅支持微信版本v2.6.8.52
     |      :param block: 是否阻塞，默认阻塞
     |      :return: 无
     |  
     |  update_frinds(self)
     |      更新全局好友信息（包括好友，群组，公众号），该函数不会直接返回好友信息，调用该函数后，所有好友信息在回调函数中返回
     |      :return: 无
     |  ----------------------------------------------------------------------


## 赞赏我

支持作者继续更新，请我喝杯咖啡

<img src="https://github.com/Mocha-L/findtheone/blob/master/pic/ali.png" width="230px" /><img src="https://github.com/Mocha-L/findtheone/blob/master/pic/wechat.png" width="230px" />

## 声明

**本项目仅供技术研究，请勿用于非法用途，如有任何人凭此做何非法事情，均于作者无关，特此声明。**
