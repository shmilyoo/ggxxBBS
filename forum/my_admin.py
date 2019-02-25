# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from account.forms import UserGroupForm
from account.models import MyUser, UserGroup
from forum.forms import ForumForm
from forum.models import Forum, Subject, Topic
from forum.helper import list_forum, MyPaginator, get_or_create_default_subject, step_order_forum, paginator_action
from ggxxBBS import config
from django.contrib.sessions.backends.db import SessionStore

import json


def index(request):
    return render_to_response('admin/admin_base.html', {'config': config}, context_instance=RequestContext(request))


def get_forums_from_bbs(request):
    """
    后台添加版块，下拉版块列表异步请求函数。后因使用zTree来做下拉树状表，此函数废弃
    :param request:
    :return:
    """
    if 'bbs_id' in request.POST:
        bbs_id = request.POST['bbs_id']
        forum_list = list_forum(bbs_id)
        sorted_forum_list = [{'id': forum.id, 'tag': forum.tag, 'name': forum.name, 'parent': forum.parent_id,
                              'order': forum.display_order} for forum in forum_list]
        data = json.dumps(sorted_forum_list, ensure_ascii=False)
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404


def get_forum_ztree_json(request):
    """
    返回版块列表信息，提供给zTree树状表使用
    :param request:
    :return:
    """
    if 'bbs_id' in request.POST:
        bbs_id = request.POST['bbs_id']
        forums = Forum.objects.values('id', 'parent_id', 'name').filter(belong=bbs_id)
        ff = list(forums)
        ff.append({'id': '0' * 32, 'parent_id': '0', 'name': u'首页'})
        for f in ff:
            f['open'] = True
        data = json.dumps(ff, ensure_ascii=False)
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404


def add_forum(request):
    # 'belong','parent_id','name','tag','path_list','allow_topic','icon','topic_credit',
    # 'post_credit','visit_level','topic_level','post_level']
    if request.method == 'GET':
        form = ForumForm()
    else:
        if not request.is_ajax():
            pass
        form = ForumForm(request.POST, request.FILES)
        if form.is_valid():
            forum = Forum()
            data = form.cleaned_data
            forum.belong = data['belong']
            forum.parent_id = data['parent_id']
            forum.name = data['name']
            forum.tag = data['tag']
            forum.descr = data['descr']
            forum.content = data['content']
            count = len(forum.parent_id)
            if count == 32:
                forum.count = count
            if forum.parent_id == '0' * 32:
                forum.path_list = ''
            else:
                parent = Forum.objects.get(id=forum.parent_id)
                forum.path_list = parent.path_list + parent.tag + ','
            parents = Forum.objects.filter(parent_id=forum.parent_id).aggregate(Max('display_order'))
            if parents['display_order__max']:
                forum.display_order = parents['display_order__max'] + 1
            else:
                forum.display_order = 1
            forum.allow_topic = data['allow_topic']
            forum.icon = data['icon']
            forum.topic_credit = data['topic_credit']
            forum.post_credit = data['post_credit']
            forum.visit_level = data['visit_level']
            forum.topic_level = data['topic_level']
            forum.post_level = data['post_level']
            forum.save()
            # 同时添加默认主题
            subjects = [Subject(name='',color='#000000',forum=forum)]
            subject_list = json.loads(request.POST['subject_list_str'])
            for subject in subject_list:
                subjects.append(Subject(name=subject['name'],color=subject['color'],forum=forum))
            Subject.objects.bulk_create(subjects)
            return HttpResponseRedirect(reverse('choose_bbs'))

    return render_to_response('admin/add_forum.html', {'config': config, 'form': form},
                              context_instance=RequestContext(request))


def manage_forum(request, bbs_id='1'):
    forum_dic = {}
    for num, value in config.bbs_names.items():
        forum_list = list_forum(num)
        step_order_forum_list = []
        for forum in forum_list:
            step_order_forum(step_order_forum_list,forum)
        forum_dic[value['cnName']] = (num, step_order_forum_list)
    return render_to_response('admin/manage_forum.html', {'config': config, 'forum_dic': forum_dic, 'bbs_id': bbs_id},
                              context_instance=RequestContext(request))


def seq_forum(request):
    if request.method == "GET":
        raise Http404
    # forum_id direction
    if not ('forum_id' in request.POST and 'direction' in request.POST):
        raise Http404
    forum_id = request.POST['forum_id']
    direction = request.POST['direction']
    f = Forum.objects.get(id=forum_id)
    bbs_id = f.belong
    parent_id = f.parent_id
    forums_same_level = Forum.objects.filter(parent_id=parent_id, belong=bbs_id).order_by('display_order')
    count = len(forums_same_level)
    try:
        index_of = list(forums_same_level).index(f)
    except:
        raise Http404
    if (index_of == 0 and direction == 'up') or (index_of == count - 1 and direction == 'down'):
        return HttpResponseRedirect(reverse('admin_manage_forum_id', args=(bbs_id,)))
    this_order = f.display_order
    this_id = f.id
    if direction == 'up':
        pre_forum = forums_same_level[index_of - 1]
        pre_order = pre_forum.display_order
        pre_id = pre_forum.id
        Forum.objects.filter(id=pre_id).update(display_order=this_order)
        Forum.objects.filter(id=this_id).update(display_order=pre_order)
    if direction == 'down':
        suf_forum = forums_same_level[index_of + 1]
        suf_order = suf_forum.display_order
        suf_id = suf_forum.id
        Forum.objects.filter(id=suf_id).update(display_order=this_order)
        Forum.objects.filter(id=this_id).update(display_order=suf_order)
    return HttpResponseRedirect(reverse('admin_manage_forum_id', args=(bbs_id,)))


def edit_forum(request, forum_id):
    this_forum = get_object_or_404(Forum, id=forum_id)
    subjects = Subject.objects.values('id','name','color').filter(forum_id=forum_id)
    if request.method == 'POST':
        form = ForumForm(request.POST, request.FILES, instance=this_forum)
        if form.is_valid():
            data = form.cleaned_data
            this_forum.name = data['name']
            this_forum.descr = data['descr']
            this_forum.content = data['content']
            this_forum.allow_topic = data['allow_topic']
            this_forum.icon = data['icon']
            this_forum.topic_credit = data['topic_credit']
            this_forum.post_credit = data['post_credit']
            this_forum.visit_level = data['visit_level']
            this_forum.topic_level = data['topic_level']
            this_forum.post_level = data['post_level']
            this_forum.save(update_fields=['name', 'descr', 'content', 'allow_topic', 'icon', 'topic_credit',
                                           'post_credit', 'visit_level', 'topic_level', 'post_level'])
            return HttpResponseRedirect(reverse('admin_manage_forum_id', args=(this_forum.belong,)))
    else:
        form = ForumForm(instance=this_forum)
    try:
        parent = Forum.objects.values('id', 'name').get(id=this_forum.parent_id)
    except:
        parent = {'id': '0' * 32, 'name': u'首页'}
    return render_to_response('admin/edit_forum.html', {'config': config, 'form': form, 'parent': parent,
                                                        'subjects':subjects}, context_instance=RequestContext(request))


def edit_forum_moderator(request, forum_id):
    if request.method == 'POST':
        if 'moderators' not in request.POST:
            raise Http404
        moderators = request.POST['moderators']
        if len(moderators):
            moderator_list = moderators.split(',')
        else:
            moderator_list = []
        try:
            Forum.objects.get(id=forum_id).moderators = moderator_list
            flag = u'更新成功'
        except Exception as e:
            flag = u'更新失败'
        result = {'flag': flag}
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')
    else:
        forum = Forum.objects.get(id=forum_id)
        users = forum.moderators.values('name')
        forum_name = forum.name
        return render_to_response('admin/edit_moderator.html', {'config': config, 'forum_name': forum_name,
                                                                'forum_id': forum_id, 'users': users},
                                  context_instance=RequestContext(request))


def user_manage_filter(request, num="1", field='name', order='asc'):
    if request.method == 'POST':
        raise Http404
    if order == 'asc':
        orderBy = field
    else:
        orderBy = '-' + field
    search_user_name = ''
    if 'search_user_name' in request.GET and len(request.GET['search_user_name']):
        search_user_name = request.GET['search_user_name']
        if field != 'name':
            users_all = MyUser.objects.values('id', 'name', 'gender', 'last_visit', 'reg_time', 'reg_ip',
                                              'last_visit_ip', 'is_active',
                                              'is_admin').filter(name__icontains=search_user_name).order_by(orderBy,
                                                                                                            'name')
        else:
            users_all = MyUser.objects.values('id', 'name', 'gender', 'last_visit', 'reg_time', 'reg_ip',
                                              'last_visit_ip', 'is_active',
                                              'is_admin').filter(name__icontains=search_user_name).order_by(orderBy)
    else:
        if field != 'name':
            users_all = MyUser.objects.values('id', 'name', 'gender', 'last_visit', 'reg_time', 'reg_ip',
                                              'last_visit_ip', 'is_active',
                                              'is_admin').order_by(orderBy, 'name')
        else:
            users_all = MyUser.objects.values('id', 'name', 'gender', 'last_visit', 'reg_time', 'reg_ip',
                                              'last_visit_ip', 'is_active',
                                              'is_admin').order_by(orderBy)

    # p = MyPaginator(users_all, 1)
    # try:
    #     users = p.page(int(num))
    # except PageNotAnInteger:
    #     users = p.page(1)
    # except:
    #     users = p.page(p.num_pages)

    users,page_int = paginator_action(users_all,1,num)

    return render_to_response('admin/user_manage.html',
                              {'config': config, 'users': users, 'field': field, 'order': order,'page':page_int,
                               'search_user_name': search_user_name}, context_instance=RequestContext(request))




def user_active(request):
    """
    用户管理界面勾选设置用户是否活动禁用
    """
    if request.method == 'GET':
        raise Http404
    result = {'success': False, 'message': ''}
    if 'name' in request.POST and 'check' in request.POST:
        name = request.POST['name']
        check = request.POST['check']
        # if request.user.name == name:
        # result['message'] = u'不能修改自己'
        # else:
        active = True
        if check == 'true':
            active = False
        flag = MyUser.objects.filter(name=name).update(is_active=active)
        if flag == 1:
            result['success'] = True
        else:
            result['message'] = u'更新失败'
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')


def user_admin(request):
    """
    用户管理界面勾选设置用户是否为管理员
    """
    if request.method == 'GET':
        raise Http404
    result = {'success': False, 'message': ''}
    # if request.user.is_admin:     必须为管理员且名称为admin才能添加和解除管理员 相当于admin为超级管理员
    # pass
    # if request.user.name == 'admin':
    # pass
    if 'name' in request.POST and 'check' in request.POST:
        name = request.POST['name']
        check = request.POST['check']
        is_admin = False
        if check == 'true':
            is_admin = True

        flag = MyUser.objects.filter(name=name).update(is_admin=is_admin)
        if flag == 1:
            result['success'] = True
        else:
            result['message'] = u'更新失败'
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')


def user_groups(request):
    if request.method == 'POST':
        pass
    else:
        groups = UserGroup.objects.order_by('need_credits')
        return render_to_response('admin/user_groups.html', {'config': config, 'groups': groups},
                                  context_instance=RequestContext(request))

def del_user_groups(request):
    if not request.method == "POST":
        raise Http404
    result = {'success': False, 'message': ''}
    ug_id = request.POST['id']
    try:
        # 删除用户组的时候，把属于此用户组的用户的用户组更改为低一个级别的用户组
        ug = UserGroup.objects.get(id=ug_id)
        ug_low = UserGroup.objects.filter(need_credits__lt=ug.need_credits).order_by('-need_credits')[0]
        MyUser.objects.filter(user_group=ug).update(user_group=ug_low)
        ug.delete()
        # 待办  事务，同步
        result['success'] = True
    except Exception as e:
        result['message'] = e.message
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')


def add_user_groups(request):
    if request.method == "POST":
        form = UserGroupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            name = data['name']
            need_credits = data['need_credits']
            icon = data['icon']
            read_level = data['read_level']
            # 添加用户组，将对应这个用户组积分的用户进行更新
            ug = UserGroup.objects.create(name=name, need_credits=need_credits, icon=icon, read_level=read_level)
            ug_low = UserGroup.objects.filter(need_credits__lt=need_credits).order_by('-need_credits')[0]
            MyUser.objects.filter(user_group=ug_low).filter(credits__gte=need_credits).update(user_group=ug)
            # 待办 事务，同步
            return HttpResponseRedirect(reverse('admin_user_groups'))
    else:
        form = UserGroupForm()
    return render_to_response('admin/user_groups_add.html', {'config': config, 'form': form},
                              context_instance=RequestContext(request))


def edit_user_groups(request):
    if request.method == 'POST':
        ug_id = request.POST['ug_id']
        ug = get_object_or_404(UserGroup, pk=ug_id)
        credits_original = ug.need_credits
        form = UserGroupForm(request.POST, instance=ug)
        if form.is_valid():
            name = request.POST['name']
            need_credits = request.POST['need_credits']
            icon = request.POST['icon']
            flag = UserGroup.objects.filter(pk=ug_id).update(name=name, need_credits=need_credits, icon=icon)
            # 待办 同步
            if flag == 1:
                if credits_original != need_credits:
                    # 此处需要更新的用户的用户组太复杂，直接把除了当前管理员外所有服务器session删除，强制用户重新登录，登录时更新用户组信息
                    # 此处删除session数据表，不需要同步，用户登录更新时会同步用户组信息
                    session_id = request.COOKIES['sessionid']
                    from django.db import connections
                    cursor = connections['default'].cursor()
                    cursor.execute("delete from django_session where session_key != %s", [session_id])  # 防止自身管理用户被踢掉线
                return HttpResponseRedirect(reverse('admin_user_groups'))
        return HttpResponseRedirect(reverse('admin_edit_user_groups'))
    else:
        ug_id = request.GET['id']
        ug = get_object_or_404(UserGroup, pk=ug_id)
        form = UserGroupForm(instance=ug)
        return render_to_response('admin/user_groups_edit.html', {'form': form},
                                  context_instance=RequestContext(request))


def announcements(request):
    pass


def add_announcements(request):
    pass


def edit_announcements(request):
    pass


def del_announcements(request):
    pass

def subject_list(request):
    result = {'success':False,'message':''}
    if request.method == 'GET':
        pass
    else:
        forum_id = request.POST['forum_id']
        subjects = Subject.objects.values('id','name','color').filter(forum_id=forum_id).order_by('name')
        result['success'] = True
        result['data'] = list(subjects)
    return HttpResponse(json.dumps(result,ensure_ascii=False), content_type='application/json')

def subject_del(request):
    result = {'success':False,'message':''}
    if request.method == 'GET':
        result['message'] = u'信息提交错误'
    else:
        forum_id = request.POST['forum_id']
        subject_id = request.POST['subject_id']
        default_subject = get_or_create_default_subject(forum_id)
        try:
            Topic.objects.filter(subject_id=subject_id).update(subject_id=default_subject.id)
            Subject.objects.filter(id=subject_id).delete()
            # 待办 同步
            result['success'] = True
        except Exception as e:
            result['message'] = e.args[1]
    return HttpResponse(json.dumps(result,ensure_ascii=False), content_type='application/json')

def subject_modify(request):
    result = {'success':False,'message':''}
    if request.method == 'GET':
        result['message'] = u'信息提交错误'
    else:
        forum_id = request.POST['forum_id']
        subject_name = request.POST['subject_name']
        subject_color = '#' + request.POST['subject_color']
        subject_id = request.POST['subject_id']
        btn_text = request.POST['btn_text']
        try:
            if btn_text == u'加入':
                Subject.objects.create(forum_id=forum_id,name=subject_name,color=subject_color)
            else:
                Subject.objects.filter(pk=subject_id).update(name=subject_name,color=subject_color)
            result['success'] = True
        except Exception as e:
            result['message'] = e.args[1]
    return HttpResponse(json.dumps(result,ensure_ascii=False), content_type='application/json')

def topic_manage(request):
    if request.method == 'GET':
        pass
    else:
        pass
    return render_to_response('admin/topic_manage.html',{'config':config},
                              context_instance=RequestContext(request))

def topic_batch_del(request):
    pass

def topic_transfer(request):
    pass
