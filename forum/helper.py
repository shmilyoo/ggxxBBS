# -*- coding: utf-8 -*-
import datetime
from django.core.paginator import Paginator, PageNotAnInteger
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.html import strip_tags
from account.helper import get_read_level_from_request
from account.models import MyUser
from forum.models import Forum, Subject, ModeratorRelation
from ggxxBBS import config


def list_forum(bbs_id):
    """
    将某个bbs下面的版块以树形方式列表进行排序输出
    :param bbs_id: 论坛id字符串
    :return:[{'id':id,...,'children':[{..},{..},...]},{},...]
    """
    forums_list = Forum.objects.filter(belong=bbs_id).values('id', 'parent_id', 'display_order', 'name', 'tag', 'descr',
                                                             'path_list', 'allow_topic').order_by('parent_id',
                                                                                                  'display_order')
    if not forums_list:
        return []
    root = {'id': '0' * 32, 'name': u'首页', 'children': []}
    dic = {root['id']: root}
    for f in forums_list:
        # 为每一个forum字典添加children键，值为一个集合；
        # 将id:forum 键值对添加到总字典dic中
        f['children'] = []
        dic[f['id']] = f
    for f in forums_list:
        # 再一次轮询forums_list 确保加入children的forum是按照display_order排列的
        parent_id = f['parent_id']
        dic[parent_id]['children'].append(dic[f['id']])
    result = dic['0' * 32]['children']
    return result


def step_order_forum(result, forum):
    forum['step_name'] = '&nbsp;&nbsp;&nbsp;&nbsp;' * (forum['path_list'].count(',') + 1) + forum['name']
    result.append(forum)
    if forum['children']:
        for child in forum['children']:
            step_order_forum(result, child)


# def list_forum1(bbs_id):
# list0 = []
# list1 = []
# forums = Forum.objects.filter(belong=bbs_id).order_by('-parent_id', '-display_order')
#     if forums:
#         for forum in forums:
#             name_prefix = '&nbsp;&nbsp;&nbsp;&nbsp;' * (forum.path_list.count(',') + 1)
#             forum.name = name_prefix + forum.name
#             list0.append((forum.parent_id, forum.display_order, forum))
#         sort_list(list0, list1)
#     return list1
#
#
# def sort_list(lista, listb, i=0):
#     """
#     lista格式[(forum.parent_id, forum.display_order, {...}),(...)]
#     listb格式[{},{},..]
#     :param lista: 未排序版面列表
#     :param listb: 已经按照树形结构排序的版面列表
#     """
#     if not lista:
#         return
#     if listb:
#         parent_id = listb[i].id
#         j = len(lista) - 1
#         k = i
#         while j >= 0:
#             if lista[j][0] == parent_id:
#                 listb.insert(k + 1, lista[j][2])
#                 k += 1
#                 del lista[j]
#             j -= 1
#         i += 1
#         return sort_list(lista, listb, i)
#     else:
#         # temp = [f for f in lista if f[0] == '0' * 32]
#         j = len(lista) - 1
#         while j >= 0:
#             if lista[j][0] == '0' * 32:
#                 listb.append(lista[j][2])
#                 del lista[j]
#             j -= 1
#         i = 0
#         return sort_list(lista, listb, i)


def get_sorted_forum_list(bbs_id):
    """
    返回排序后的树状版块列表，只包含一级和二级版块
    :param bbs_id:论坛id的字符串形式
    :return:返回列表，类似[{'id':id,'name':name.....,'children':[{'id':id,'name':name},{}...]},{}]格式
    """
    forums = Forum.objects.values().raw(
        'SELECT f.id,f.name,f.descr,f.parent_id,f.tag,f.display_order,f.allow_topic,f.icon,' +
        'if(date(update_time)=date(now()),today_posts,0) today_posts,ifnull(Count(distinct t.id),0) as topics,' +
        'ifnull(count(p.id),0) as posts,t.title as last_topic_title,last_topic_id,last_topic_title,update_time,' +
        'last_username,last_nickname FROM forum as f LEFT JOIN topic as t ON f.id = t.forum_id LEFT JOIN post ' +
        'as p ON t.id = p.topic_id WHERE f.belong = %s GROUP BY f.id ORDER BY f.parent_id,f.display_order',[bbs_id])

    # forums = Forum.objects.values().raw(
    #     'SELECT f.id,f.name,f.descr,f.parent_id,f.tag,f.display_order,f.allow_topic,f.icon,' +
    #     'ifnull(Count(distinct t.id),0) as topics,ifnull(count(p.id),0) as posts,t.title as last_topic_title,' +
    #     't.id as last_topic_id,t.post_time as last_topic_time,u.name as last_topic_username,' +
    #     'u.nick_name as last_topic_user_nickname FROM forum as f LEFT JOIN ' +
    #     '(select * from topic order by post_time desc) as t ON f.id = t.forum_id LEFT JOIN post as ' +
    #     'p ON t.id = p.topic_id left join user as u on t.author_id = u.id WHERE f.belong = %s GROUP BY f.id ' +
    #     'ORDER BY f.parent_id,f.display_order',
    #     [bbs_id])
    moderators_dict = get_all_moderators()
    result = []
    forums_clone = forums[:]  # 不复制一份的话，在下面的循环中每for一下就查询一下数据库。。。
    for forum in forums:
        if forum.parent_id == '0' * 32:
            result.append(forum)
            forum.children = []
            if forum.id in moderators_dict:
                forum.moderators_list = moderators_dict[forum.id]
            for f in forums_clone:
                if f.parent_id == forum.id:
                    forum.children.append(f)
                    if f.id in moderators_dict:
                        f.moderators_list = moderators_dict[f.id]
    return result


def get_all_moderators():
    """
    返回所有版块的信息字典{'forum_id':[版主姓名列表],....}
    :return:
    """
    result = {}
    for m in ModeratorRelation.objects.values('forum_id', 'moderator__name', 'moderator__nick_name'):
        if m['forum_id'] in result:
            result[m['forum_id']].append({'name': m['moderator__name'], 'nick_name': m['moderator__nick_name']})
        else:
            result[m['forum_id']] = [{'name': m['moderator__name'], 'nick_name': m['moderator__nick_name']}]
    return result


def get_remote_ip(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        return request.META['HTTP_X_FORWARDED_FOR']
    else:
        return request.META['REMOTE_ADDR']


class MyPaginator(Paginator):
    def __init__(self, object_list, per_page, range_num=3, orphans=0, allow_empty_first_page=True):
        """
        per_page: 每页显示几个；
        """
        Paginator.__init__(self, object_list, per_page, orphans, allow_empty_first_page)
        self.range_num = range_num  # 本页页码左右各显示几页
        self.show_first = False
        self.show_first_dot = False
        self.show_last = False
        self.show_last_dot = False
        self.num_count = 2 * self.range_num + 1

    def page(self, number):
        self.page_num = number  # 显示第几页
        self.page_base_num = (number - 1) * self.per_page  # 用于显示本页序号，代表之前所有页的元素个数

        if self.num_pages > self.num_count:
            if self.page_num - 1 > self.range_num:
                self.show_first = True
                self.show_first_dot = True
            if self.page_num - 1 == self.range_num + 1:
                self.show_first_dot = False
            if self.num_pages - self.page_num > self.range_num:
                self.show_last = True
                self.show_last_dot = True
            if self.num_pages - self.page_num == self.range_num + 1:
                self.show_last_dot = False
        return super(MyPaginator, self).page(number)

    def _page_range_ext(self):
        if self.num_pages <= self.num_count:
            # 总页数小于等于 2 * self.range_num + 1 时，直接显示所有页
            return range(1, self.num_pages + 1)
        num_list = [self.page_num]
        for i in range(1, self.range_num + 1):
            if self.page_num - i <= 0:
                num_list.append(self.num_count + self.page_num - i)
            else:
                num_list.append(self.page_num - i)
            if self.page_num + i <= self.num_pages:
                num_list.append(self.page_num + i)
            else:
                num_list.append(self.page_num + i - self.num_count)
        num_list.sort()
        return num_list

    page_range_ext = property(_page_range_ext)

def paginator_action(p_list,per_page,page_str):
    p = MyPaginator(p_list, per_page)
    try:
        result = p.page(int(page_str))
        page = int(page_str)
    except PageNotAnInteger:
        result = p.page(1)
        page = 1
    except:
        result = p.page(p.num_pages)
        page = p.num_pages
    return result,page

def check_and_add_recycle_forum():
    """
    当伪删除帖子时，帖子会被移动到回收站版块下，此时应检查是否有这个版块，如果返回为空时，应提示用户手动添加这个版块
    :return:
    """
    try:
        f = Forum.objects.get(belong=1, name=u'回收站')
        return f
    except Exception as e:
        return None


def get_or_create_default_subject(forum_id):
    """
    获取或创建默认的主题，name为空
    :return:获取或创建的指定forum的默认subject，其name为空
    """
    try:
        s = Subject.objects.get(forum_id=forum_id, name='')
    except Exception as e:
        s = Subject.objects.create(name='', forum_id=forum_id)
        # 待办 同步
    return s


# def cut_list_to_lists(list_a):
#     """
#     将一个列表按照指定的长度等分为数个列表
#     """
#     per_row = config.child_forum_num_per_row
#     list_b = []
#     i = len(list_a)
#     row_count = (i - 1) / per_row + 1
#     j = 1
#     while j <= row_count:
#         if j < row_count:
#             list_b.append(list_a[(j - 1) * per_row:j * per_row])
#         else:
#             list_b.append(list_a[(j - 1) * per_row:])
#         j += 1
#     return list_b

def get_path_lists(path_list, bbs_id):
    tag_lists = path_list.rstrip(',').split(',')
    path_lists = []  # 论坛版块层级列表信息
    for tag in tag_lists:
        if tag:
            f = Forum.objects.values('name', 'tag').get(tag=tag, belong=bbs_id)
            path_lists.append({'tag': f['tag'], 'name': f['name']})
    return path_lists


def check_manager(request, forum_id):
    """
    判断用户对页面是否具有管理权限，如果是管理员或者相应版块版主则返回true
    """
    if not hasattr(request, 'user'):
        return False
    user = request.user
    if not isinstance(user, MyUser):
        return False
    if user.is_staff:
        return True
    relations = ModeratorRelation.objects.filter(forum_id=forum_id, moderator=user)
    if relations:
        return True
    return False


def check_visit_level(request, visit_level):
    """
    如果权限不够，return不为none，返回response为自定义错误页面
    """
    user_visit_level = get_read_level_from_request(request)
    if user_visit_level < visit_level:
        error = {'message': u'访问权限不够'}
        return render_to_response('common/custom_error.html', {'error': error, 'config': config},
                                  context_instance=RequestContext(request))

def check_empty(content):
    """
    发帖的内容不能为空，检查是否为空
    """
    if 'img' in content:
        return False
    else:
        s = strip_tags(content).replace('\n','').replace('\r','').replace('&nbsp;','')
        return not bool(s)

def update_after_topic_post(user,forum,time,topic,is_topic):
    """
    在用户发帖或者回贴后更新用户积分、用户组、论坛最后回复等信息
    """
    user.refresh_ug()
    if is_topic:
        forum.new_topic_credits(user)
    else:
        forum.new_post_credits(user)
    forum.update_statistics(time, topic.id, topic.title, user.name, user.nick_name)

def get_or_create_subjects(forum):
    """
    获取或创建版块的主题列表，如果为空，创建默认主题，返回主题列表
    """
    list = forum.get_subjects()
    if not list:
        subject = Subject(name='',color='#000000',forum=forum)
        subject.save()
        list = [subject]
    return list