# -*- coding: utf-8 -*-
import os
import datetime
import random
from ggxxBBS import settings

bbs_sysName = u'公共信息网论坛系统'
# bbs_id 编号按照1,2,3,4... 依次增加，程序中有个别地方直接调用了bbs_names['1']
bbs_names = {'1': {'id':'1','name': 'jyxc', 'cnName': u'建言献策', 'syncIP': '', 'syncUserName': '', 'syncPwd': ''},
             '2': {'id':'2','name': 'jsjl', 'cnName': u'技术交流', 'syncIP': '', 'syncUserName': '', 'syncPwd': ''}}


allow_image_type = ('jpg', 'jpeg', 'bmp', 'png', 'gif', 'rar', 'zip')  # 允许用户上传文件类型
allow_flash_type = ('swf','flv')
allow_attachment_type = ('rar','zip','tar','7zip')
attachment_path = 'attachment/' + datetime.datetime.now().strftime('%Y%m')
temp_path = os.path.join(settings.MEDIA_ROOT,'temp')
temp_url = os.path.join(settings.MEDIA_URL,'temp')
max_attach_size = 2 * 10 ** 6  # byte 允许上传附件大小限制 2M
max_image_size = 1 * 10 ** 6  # 允许帖子中上传图片大小限制1M
max_avatar_size = 200 * 10 ** 3  # 允许头像图标最大 200K
max_icon_size = 200 * 10 ** 3  # 允许最大普通图标大小 200K
avatar_directory = os.path.join(settings.MEDIA_ROOT,'avatar')
avatar_url = os.path.join(settings.MEDIA_URL,'avatar')
default_avatar_path = settings.STATIC_URL + 'images/default_avatar2.gif'
default_forum_icon_path = settings.MEDIA_URL + 'forumIcon/default.gif'
media_url = settings.MEDIA_URL

topics_per_page = 2    # 版块页面每页显示多少帖子
replies_per_page = 2    # 每页多少楼，第一页计数包括topic(楼主)
message_per_page = 2    # 用户中心消息、通知等信件列表，每页显示多少个

colors = ['#f59595','#e89025','#e0da16','#84e615','#3ae09b','#5350e6','#cb4ae8','#757475','#b1e681','#e60000','#bbedea']
poll_option_max_length = 300  # 投票选项显示长度最长为300px

def test_bbs_name(name):
    """
    如果存在论坛名，则返回论坛信息字典，反之返回空
    :param name: 论坛名称
    :return:论坛信息字典
    """
    for k,v in bbs_names.items():
        if name == v['name']:
            return bbs_names[k]
    return None

def random_color():
    """
    用来显示投票结果柱状图的随机颜色
    """
    return random.choice(colors)