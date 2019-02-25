# -*- coding: utf-8 -*-
# from django.http import HttpResponse
import json
import datetime
import os
from PIL import Image
import pickle
from django.contrib.auth.hashers import check_password, make_password
from django.core.files.storage import default_storage
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.utils.html import remove_tags, strip_tags
from account.forms import RegForm, UserInfoForm, AvatarForm
from account.helper import my_login, get_unread_message_num, get_unread_notification_num

from account.models import MyUser
from forum.helper import get_remote_ip, paginator_action
from forum.models import Message, Notification, Topic, Post
from ggxxBBS import config, settings
from django.http.response import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404

# Create your views here.

def user_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('choose_bbs'))
    else:
        if request.method == 'GET':
            return render_to_response('account/login.html', {'config': config},
                                      context_instance=RequestContext(request))
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is None:
                messages.add_message(request, messages.ERROR, u'用户名或密码错误')
                return HttpResponseRedirect(reverse('login'))

            if not user.is_active:
                error = {'message': u'用户被禁用，请联系管理员。'}
                return render_to_response('common/custom_error.html', {'config': config, 'error': error})
            my_login(request, user)
            if 'next' in request.GET:
                url = request.GET['next']
                return HttpResponseRedirect(url)  # goto index
            else:
                return HttpResponseRedirect(reverse('choose_bbs'))  # choosebbs


def user_logout(request):
    user = request.user
    user.is_logout = True
    user.save(update_fields=['is_logout'])
    # 待办 同步
    logout(request)
    if request.method == 'GET' and 'from' in request.GET:
        # for v in config.bbs_names.values():
        # if v['name'] == request.GET['from']:
        return HttpResponseRedirect(reverse('index', args=(request.GET['from'],)))
    return HttpResponseRedirect(reverse('choose_bbs'))


def user_reg(request):
    if request.method == 'POST':
        form = RegForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            name = data['name']
            password = data['password']
            gender = data['gender']
            ip = get_remote_ip(request)
            MyUser.objects.create_user(name, password, name, gender, ip)
            user = authenticate(username=name, password=password)
            my_login(request, user)
            res = render_to_response('account/auth_success.html', {'config': config, 'flag': 'reg'},
                                     context_instance=RequestContext(request))
            return res
    else:
        if request.user.is_authenticated():
            return render_to_response('account/auth_success.html', {'config': config, 'flag': 'reg'},
                                      context_instance=RequestContext(request))
        form = RegForm()
    return render_to_response('account/reg.html', {'config': config, 'form': form},
                              context_instance=RequestContext(request))


def user_panel_name(request, name):
    pass


def user_search(request):
    if request.method == 'GET':
        raise Http404
    if 'user_name' not in request.POST:
        raise Http404
    user_name = request.POST['user_name']
    users = MyUser.objects.values('name').filter(name__icontains=user_name)
    data = json.dumps(list(users), ensure_ascii=False)
    return HttpResponse(data, content_type='application/json')


def get_unread_list(user):
    return [get_unread_message_num(user), get_unread_notification_num(user)]


@login_required
def get_unread_json(request):
    unread_list = get_unread_list(request.user)
    return HttpResponse(json.dumps(unread_list, ensure_ascii=False), content_type='application/json')


@login_required
def uc_inform(request, inform_type):
    """
    用户中心-消息管理功能，type分为message用户间短消息,notice系统通知,send_message发送消息,send_notice发送通知
    """
    menu = 'inform'
    unread = get_unread_list(request.user)
    page = request.GET.get('page','1')
    if inform_type == 'send_notice':
        return inform_send_notice_view(request, menu, inform_type, unread)
    elif inform_type == 'notice':
        # 显示收到的通知
        notice_list = Notification.objects.filter(to_user=request.user, is_show=True).order_by('-time')
        notice_list,page_int = paginator_action(notice_list,config.message_per_page,page)
        return render_to_response('account/inform_notification.html',
                                  {'config': config, 'menu': menu, 'inform_type': inform_type,
                                   'notice_list': notice_list, 'unread': unread, 'page':page_int},
                                  context_instance=RequestContext(request))
    elif inform_type == 'send_message':
        return inform_send_message_view(request, menu, inform_type, unread)
    elif inform_type == 'sent_message':
        # 显示已发送消息
        message_list = Message.objects.select_related('to_user').filter(from_user=request.user,
                                                                        show_at_from=True).order_by('-time')
        message_list,page_int = paginator_action(message_list,config.message_per_page,page)
        return render_to_response('account/inform_sent_message.html',
                                  {'config': config, 'menu': menu, 'inform_type': inform_type,
                                   'message_list': message_list, 'unread': unread, 'page':page_int},
                                  context_instance=RequestContext(request))
    else:
        # message,显示用户消息
        message_list = Message.objects.select_related('from_user').filter(to_user=request.user,
                                                                          show_at_to=True).order_by('-time')
        message_list,page_int = paginator_action(message_list,config.message_per_page,page)
        return render_to_response('account/inform_message.html',
                                  {'config': config, 'menu': menu, 'inform_type': inform_type,
                                   'message_list': message_list, 'unread': unread, 'page':page_int},
                                  context_instance=RequestContext(request))


def inform_send_message_view(request, menu, inform_type, unread):
    if request.method == 'POST':
        result = {'success': False, 'message': ''}
        to_user_str = request.POST['to_user'].strip().strip(';')
        message = strip_tags(request.POST['message'].strip()).replace('\n', '<br>')
        name_type = request.POST['name_type']
        if not to_user_str or not message:
            result['message'] = u'收件人和消息内容是必填内容'
        else:
            names = set(to_user_str.split(';'))
            if name_type == 'name':
                to_user = MyUser.objects.filter(name__in=names)
            else:
                to_user = MyUser.objects.filter(nick_name__in=names)
            if len(to_user) == 0:
                result['message'] = u'找不到符合条件的收件人'
            elif len(to_user) != len(names):
                result['message'] = u'找不到收件人，一个或多个收件人姓名(昵称)不正确'
            elif request.user in to_user:
                result['message'] = u'不能发送给自己'
            else:
                data_list = []
                time = datetime.datetime.now()
                # message = pickle.dumps(message)
                for user in to_user:
                    data_list.append(Message(from_user=request.user, to_user=user, time=time, content=message))
                Message.objects.bulk_create(data_list)
                result['success'] = True
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')
    to = request.GET.get('to', '')
    to_user = None
    if to:
        to_user = MyUser.objects.values('id', 'name', 'nick_name').get(name=to)
    return render_to_response('account/inform_send_message.html',
                              {'config': config, 'menu': menu, 'inform_type': inform_type, 'to_user': to_user,
                               'unread': unread},
                              context_instance=RequestContext(request))


def inform_send_notice_view(request, menu, inform_type, unread):
    if request.method == 'POST':
        result = {'success': False, 'message': ''}
        to_user_str = request.POST['to_user'].strip().strip(';')
        message = strip_tags(request.POST['message'].strip()).replace('\n', '<br>')
        name_type = request.POST['name_type']
        if not to_user_str or not message:
            result['message'] = u'收件人和消息内容是必填内容'
        else:
            names = set(to_user_str.split(';'))
            if name_type == 'name':
                to_user = MyUser.objects.filter(name__in=names)
            else:
                to_user = MyUser.objects.filter(nick_name__in=names)
            if len(to_user) == 0:
                result['message'] = u'找不到符合条件的收件人'
            elif len(to_user) != len(names):
                result['message'] = u'找不到收件人，一个或多个收件人姓名(昵称)不正确'
            else:
                data_list = []
                time = datetime.datetime.now()
                for user in to_user:
                    data_list.append(Notification(to_user=user, time=time, content=message))
                Notification.objects.bulk_create(data_list)
                result['success'] = True
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')
    return render_to_response('account/inform_send_message.html',
                              {'config': config, 'menu': menu, 'inform_type': inform_type, 'unread': unread},
                              context_instance=RequestContext(request))


def set_message_read(request):
    if request.method == 'GET':
        raise Http404
    result = {'success': False, 'message': '', 'count': [0, 0]}
    id = request.POST['id']
    flag = Message.objects.filter(id=id).update(has_read=True)
    if flag == 1:
        result['success'] = True
        result['count'] = get_unread_list(request.user)
    else:
        result['message'] = u'更新短消息已读状态失败'
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')


def set_message_bulk_read(request):
    if request.method == 'GET':
        raise Http404
    result = {'success': False, 'message': '', 'count': [0, 0]}
    id_list_str = request.POST['id_list']
    id_list = json.loads(id_list_str)
    flag = Message.objects.filter(id__in=id_list).update(has_read=True)
    if flag > 0:
        result['success'] = True
        result['count'] = get_unread_list(request.user)
    else:
        result['message'] = u'更新短消息已读状态失败'
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')


def set_notice_read(request):
    if request.method == 'GET':
        raise Http404
    result = {'success': False, 'message': '', 'count': [0, 0]}
    id = request.POST['id']
    flag = Notification.objects.filter(id=id).update(has_read=True)
    if flag == 1:
        result['success'] = True
        result['count'] = get_unread_list(request.user)
    else:
        result['message'] = u'更新通知已读状态失败'
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')


def set_notice_bulk_read(request):
    if request.method == 'GET':
        raise Http404
    result = {'success': False, 'message': '', 'count': [0, 0]}
    id_list_str = request.POST['id_list']
    id_list = json.loads(id_list_str)
    flag = Notification.objects.filter(id__in=id_list).update(has_read=True)
    if flag > 0:
        result['success'] = True
        result['count'] = get_unread_list(request.user)
    else:
        result['message'] = u'更新通知已读状态失败'
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')


def bulk_del_notice(request):
    if request.method == 'GET':
        raise Http404
    result = {'success': False, 'message': ''}
    id_list_str = request.POST['id_list']
    id_list = json.loads(id_list_str)
    flag = Notification.objects.filter(id__in=id_list).update(is_show=False)
    if flag > 0:
        result['success'] = True
    else:
        result['message'] = u'删除失败'
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')


def bulk_del_receive_message(request):
    if request.method == 'GET':
        raise Http404
    result = {'success': False, 'message': ''}
    id_list_str = request.POST['id_list']
    id_list = json.loads(id_list_str)
    flag = Message.objects.filter(id__in=id_list).update(show_at_to=False)
    if flag > 0:
        result['success'] = True
    else:
        result['message'] = u'删除失败'
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')


def bulk_del_sent_message(request):
    if request.method == 'GET':
        raise Http404
    result = {'success': False, 'message': ''}
    id_list_str = request.POST['id_list']
    id_list = json.loads(id_list_str)
    flag = Message.objects.filter(id__in=id_list).update(show_at_from=False)
    if flag > 0:
        result['success'] = True
    else:
        result['message'] = u'删除失败'
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')


def uc_info(request, info_type):
    """
    查看个人信息，get中name为空即为查看自己
    """
    menu = 'info'
    unread = get_unread_list(request.user)
    if 'name' in request.GET:
        viewer = get_object_or_404(MyUser, name=request.GET['name'])
        name = viewer.name
    else:
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login') + '?next=' + request.path)
        else:
            viewer = request.user
            name = ''
    bbs = None
    page_int = 1
    if info_type == 'summary':
        template = 'account/info_summary.html'
        viewer = MyUser.objects.raw(
            'SELECT user.*,ug.name AS ug_name,ug.can_ip AS ug_can_ip,ug.id AS ug_id,Count(distinct t.id) AS t_num,'
            'Count(distinct p.id) AS p_num FROM user inner JOIN user_group ug ON user.user_group_id = ug.id '
            'left JOIN topic t ON t.author_id = user.id left JOIN post p ON p.author_id = user.id '
            'where user.name = %s', [viewer.name])[0]
    else:
        if 'bbs' in request.GET:
            bbs = config.test_bbs_name(request.GET['bbs'])
            if not bbs:
                raise Http404
        else:
            bbs = config.bbs_names['1']
        page = request.GET.get('page','1')
        if info_type == 'topic':
            template = 'account/info_topic.html'
            viewer.topics = Topic.objects.raw(
                'SELECT t.*,s.name subject_name,s.color subject_color,s.id subject_id,%s author_name,%s author_nickname,'
                'ifnull(p.post_time,t.post_time) last_reply_time,ifnull(pu.name,%s) last_reply_name,f.name f_name,'
                'f.tag f_tag,f.belong bbs_id,ifnull(pu.nick_name,%s) last_reply_nickname,count(p.id) replies FROM topic t '
                'INNER JOIN subject s ON s.id = t.subject_id INNER JOIN forum f ON t.forum_id = f.id left JOIN '
                '(select id,post_time,topic_id,author_id from post order by post_time desc) p ON p.topic_id = t.id '
                'left JOIN user pu ON p.author_id = pu.id where t.author_id = %s and f.belong = %s and t.is_visible = true '
                'group by t.id order by t.post_time desc',
                [viewer.name, viewer.nick_name, viewer.name, viewer.nick_name, viewer.id, bbs['id']])
            viewer.topics,page_int = paginator_action(list(viewer.topics),config.topics_per_page,page)
        elif info_type == 'post':
            template = 'account/info_post.html'
            viewer.posts = Post.objects.raw(
                'SELECT p.id,p.post_time p_time, p.content p_content, p.id p_id, t.id t_id, t.title t_title, t.is_digest '
                't_is_digest,t.read_level t_read_level,t.title_color t_title_color,t.post_time t_time,t.is_poll t_is_poll, '
                't.is_locked t_is_locked, t.has_attachment t_has_attach, t.has_img t_has_img, t.title_bold t_title_bold, '
                'tu.name tu_name, tu.nick_name tu_nick_name, tu.id tu_id, s.id s_id, s.name s_name, s.color s_color, f.id f_id, '
                'f.name f_name, f.tag f_tag FROM post p INNER JOIN topic t ON p.topic_id = t.id '
                'INNER JOIN forum f ON t.forum_id = f.id INNER JOIN subject s ON t.subject_id = s.id '
                'INNER JOIN user tu ON t.author_id = tu.id WHERE p.is_visible = TRUE AND t.is_visible = TRUE '
                'AND f.belong = %s AND p.author_id = %s ORDER BY p_time DESC',[bbs['id'],viewer.id])
            viewer.posts,page_int = paginator_action(list(viewer.posts),config.topics_per_page,page)
        else:
            # info_type == 'fav':
            if viewer != request.user:
                raise Http404
            template = 'account/info_topic.html'
            viewer.topics = Topic.objects.raw(
                'SELECT t.*,s.name subject_name,s.color subject_color,s.id subject_id,%s author_name,%s author_nickname,'
                'ifnull(p.post_time,t.post_time) last_reply_time,ifnull(pu.name,%s) last_reply_name,f.name f_name,'
                'f.tag f_tag,f.belong bbs_id,ifnull(pu.nick_name,%s) last_reply_nickname,count(p.id) replies FROM topic t '
                'INNER JOIN favorite fav ON t.id = fav.topic_id and fav.user_id = %s '
                'INNER JOIN subject s ON s.id = t.subject_id INNER JOIN forum f ON t.forum_id = f.id left JOIN '
                '(select id,post_time,topic_id,author_id from post order by post_time desc) p ON p.topic_id = t.id '
                'left JOIN user pu ON p.author_id = pu.id where t.author_id = %s and f.belong = %s and t.is_visible = true '
                'group by t.id order by fav.add_time desc',
                [viewer.name, viewer.nick_name, viewer.name, viewer.nick_name,viewer.id, viewer.id, bbs['id']])
            viewer.topics,page_int = paginator_action(list(viewer.topics),config.topics_per_page,page)
    return render_to_response(template,
                              {'config': config, 'menu': menu, 'unread': unread, 'viewer': viewer,
                               'info_type': info_type, 'name': name, 'bbs': bbs,'page':page_int},
                              context_instance=RequestContext(request))


@login_required
def uc_data(request):
    """
    用户中心-个人资料
    """
    menu = 'data'
    unread = get_unread_list(request.user)
    if request.method == 'POST':
        form = UserInfoForm(request.POST, instance=request.user)
        if form.is_valid():
            # form.save(update_fields=['nick_name','email','gender','bio','signature'])
            f = form.save(commit=False)
            f.save(update_fields=['nick_name', 'email', 'gender', 'bio', 'signature'])
    else:
        form = UserInfoForm(instance=request.user)

    return render_to_response('account/data.html',
                              {'config': config, 'menu': menu, 'unread': unread, 'form': form},
                              context_instance=RequestContext(request))


@login_required
def uc_avatar(request):
    """
    用户中心-修改头像
    """
    menu = 'avatar'
    unread = get_unread_list(request.user)
    form = AvatarForm()
    return render_to_response('account/avatar.html',
                              {'config': config, 'menu': menu, 'unread': unread, 'form': form},
                              context_instance=RequestContext(request))


def avatar_select_pic(request):
    """
    修改头像界面选择图片，使前台显示
    """
    result = {'success': False, 'message': '', 'url': '', 'width': 0, 'height': 0}
    form = AvatarForm(request.POST, request.FILES)
    if form.is_valid():
        data = form.cleaned_data
        avatar = data['avatar']
        path = default_storage.save(os.path.join(config.temp_path, avatar.name), avatar)
        storage_name_ext = os.path.split(path)[1]
        temp_path = os.path.join(config.temp_url, storage_name_ext)
        file = Image.open(path)
        result['width'] = file.size[0]
        result['height'] = file.size[1]
        result['success'] = True
        result['url'] = temp_path
    else:
        result['message'] = form.errors['avatar']
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')


def avatar_save_avatar(request):
    result = {'success': False, 'message': '', 'url': ''}
    x1 = request.POST['x1']
    y1 = request.POST['y1']
    x2 = request.POST['x2']
    y2 = request.POST['y2']
    path = request.POST['path'].lstrip('/')
    real_path = os.path.join(settings.BASE_DIR, path)
    image = Image.open(real_path)
    w, h = image.size
    scale = round(w / 250.0, 3)   # 小数精确度从1改为3,太小了的时候，当图片分辨率比较小时，误差会放大
    box = (int(int(x1) * scale), int(int(y1) * scale), int(int(x2) * scale), int(int(y2) * scale))
    image2 = image.crop(box)
    if image2.size[0] > 200:
        image2 = image2.resize((120, 120))
    ext = os.path.splitext(path)[1]
    name_ext = request.user.name + datetime.datetime.now().strftime("-%Y%m%d%H%M%S%f") + ext
    avatar_path2 = os.path.join(config.avatar_directory, name_ext)
    image2.save(avatar_path2)
    url = os.path.join(config.avatar_url, name_ext)
    MyUser.objects.filter(id=request.user.id).update(avatar=url)
    result['url'] = url
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')


@login_required
def uc_password(request):
    """
    用户中心-修改密码
    """
    menu = 'password'
    unread = get_unread_list(request.user)
    if request.method == 'POST':
        original_pwd = request.POST['original_pwd']
        pwd1 = request.POST['new_pwd1']
        pwd2 = request.POST['new_pwd2']
        if not check_password(original_pwd, request.user.password):
            messages.add_message(request, messages.ERROR, u'原密码输入错误')
        elif pwd1.strip() == '':
            messages.add_message(request, messages.ERROR, u'新密码不能为空')
        elif pwd1 != pwd2:
            messages.add_message(request, messages.ERROR, u'两次输入密码不一致')
        else:
            pwd = make_password(pwd1)
            request.user.password = pwd
            request.user.save(update_fields=['password'])
            messages.add_message(request, messages.SUCCESS, u'修改成功')
    return render_to_response('account/password.html',
                              {'config': config, 'menu': menu, 'unread': unread},
                              context_instance=RequestContext(request))

