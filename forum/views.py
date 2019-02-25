# -*- coding: utf-8 -*-
import datetime
import json
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.files.storage import default_storage
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from django.db import transaction
from django.db.models.aggregates import Count, Sum
from django.db.models import Q
from django.db.models import F
from django.http import Http404, HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.defaultfilters import truncatechars_html
from account.helper import get_read_level_from_request
from account.models import MyUser
from forum.forms import TopicForm, AttachmentForm, PollForm, PostFormSimple, PostFormFull
from forum.helper import get_sorted_forum_list, get_all_moderators, get_path_lists, check_manager, check_visit_level, \
    get_remote_ip, update_after_topic_post, get_or_create_default_subject, get_or_create_subjects, paginator_action
from forum.models import Forum, Topic, Post, Poll, PollOption, Attachment, Favorite
from ggxxBBS import config, settings
import os


def redirect(request):
    return render_to_response('common/chooseBBS.html', {'config': config}, context_instance=RequestContext(request))


# Create your views here.
def index(request, bbs_name):
    if request.method == 'POST':
        raise Http404
    bbs = config.test_bbs_name(bbs_name)
    if not bbs:
        raise Http404
    forums = get_sorted_forum_list(bbs['id'])
    # moderators_dict = get_all_moderators()  # {'forum_id':[moderator_name_list],....} 格式
    return render_to_response(bbs_name + '/index.html',
                              {'config': config, 'bbs': bbs, 'forums': forums},
                              context_instance=RequestContext(request))


def forum_index(request, bbs_name, forum_tag):
    bbs = config.test_bbs_name(bbs_name)
    if not bbs:
        raise Http404
    # forum = get_object_or_404(Forum, tag=forum_tag, belong=bbs['id'])
    try:
        forum = Forum.objects.raw(
            'SELECT f.id,f.name,f.tag,f.visit_level,f.descr,f.path_list,f.allow_topic,f.icon,f.visit_level,f.content,' +
            'f.today_posts,Count(distinct t.id) topics,Count(p.id) posts FROM forum f LEFT JOIN topic t ON t.forum_id' +
            '=f.id LEFT JOIN post p ON p.topic_id = t.id where f.belong = %s and f.tag = %s', [bbs['id'], forum_tag])[0]
    except:
        raise Http404
    is_manager = check_manager(request, forum.id)
    # 判断访问权限
    result = check_visit_level(request, forum.visit_level)
    if result:
        return result
    if request.method == 'GET':
        # 生成版块层级导航条   1 > 2 > 3 > 4
        forum.path_lists = get_path_lists(forum.path_list, bbs['id'])
        # 获取版主
        forum.moderator_names = forum.moderators.values('name', 'nick_name')
        # 获取主题 主题贴数   用raw sql 来做left  join 主题为0也可以显示
        forum.subjects_count = Topic.objects.values('subject__name', 'subject__id').annotate(
            sub_num=Count('subject')).filter(forum=forum).order_by('subject__name')
        # 如果有下级论坛，显示下级论坛信息
        children = Forum.objects.values().raw(
            'SELECT f.id,f.name,f.descr,f.tag,f.display_order,f.allow_topic,f.icon,' +
            'if(date(update_time)=date(now()),today_posts,0) today_posts,ifnull(Count(distinct t.id),0) as topics,' +
            'ifnull(count(p.id),0) as posts,t.title as last_topic_title,last_topic_id,last_topic_title,update_time,' +
            'last_username,last_nickname FROM forum as f LEFT JOIN topic as t ON f.id = t.forum_id LEFT JOIN post ' +
            'as p ON t.id = p.topic_id WHERE f.parent_id = %s GROUP BY f.id ORDER BY f.display_order',
            [forum.id])
        forum.children = list(children)
        get = {'subject': '', 'digest': '', 'page': '', 'order_by': '', 'order': ''}
        # 获取帖子列表
        filter = ''

        if 'subject' in request.GET:
            get['subject'] = request.GET['subject']
            # topics = topics.filter(subject_id=get['subject'])
            # parameters['filter':'subject_id = ' + get['subject'] + ' and']
            filter = 'subject_id = "' + get['subject'] + '" and '
        if 'digest' in request.GET:
            get['digest'] = request.GET['digest']
            # parameters['filter':'is_digest = true' + ' and']
            filter = 'is_digest = true' + ' and '
        if 'order_by' in request.GET:
            get['order_by'] = request.GET['order_by']
            get['order'] = request.GET['order']
            # parameters['order'] = get['order_by'] + ' ' + get['order']
            order = get['order_by'] + ' ' + get['order']
        else:
            order = 'last_reply_time desc'
        s = 'SELECT t.*,s.name subject_name,s.color subject_color,s.id subject_id,' + \
            'ifnull(p.post_time,t.post_time) last_reply_time,tu.name author_name,tu.nick_name author_nickname,' + \
            'ifnull(pu.name,tu.name) last_reply_name,ifnull(pu.nick_name,tu.nick_name) last_reply_nickname,' + \
            'count(p.id) replies FROM topic t INNER JOIN subject s ON s.id = t.subject_id left JOIN ' + \
            '(select id,post_time,topic_id,author_id from post order by post_time desc) p ON p.topic_id = t.id ' + \
            'INNER JOIN user tu ON t.author_id = tu.id left JOIN user pu ON p.author_id = pu.id where ' + filter + \
            't.is_visible = true and t.forum_id = %s group by t.id order by t.is_top_all desc,t.is_top desc,' + \
            't.is_bottom asc,' + order
        topics = Topic.objects.raw(s, [forum.id])
        get['page'] = request.GET.get('page','1')
        topics,page_int = paginator_action(list(topics),config.topics_per_page,get['page'])

        return render_to_response(bbs_name + '/forum/index.html',
                                  {'config': config, 'forum': forum, 'bbs': bbs, 'get': get, 'topics': topics,
                                   'is_manager': is_manager,'page':page_int},
                                  context_instance=RequestContext(request))
    else:
        pass

    return render_to_response(bbs_name + '/forum/index.html', {'config': config, 'forum': forum},
                              context_instance=RequestContext(request))


@login_required
@transaction.atomic()
def forum_new_topic(request, bbs_name, forum_tag):
    bbs = config.test_bbs_name(bbs_name)
    if not bbs:
        raise Http404
    forum = get_object_or_404(Forum, tag=forum_tag, belong=bbs['id'])
    is_manager = check_manager(request, forum.id)
    # 判断访问权限
    result = check_visit_level(request, forum.visit_level)
    if result:
        return result
    # 生成版块层级导航条   1 > 2 > 3 > 4
    forum.path_lists = get_path_lists(forum.path_list, bbs['id'])
    # 获取主题信息
    forum.subjects = get_or_create_subjects(forum)
    attach_form = AttachmentForm()
    if request.method == 'GET':
        topic_form = TopicForm()
        poll_form = PollForm()
    else:
        user = request.user
        topic_form = TopicForm(request.POST)
        poll_form = PollForm(request.POST)
        if topic_form.is_valid():
            topic_data = topic_form.cleaned_data
            now = datetime.datetime.now()
            subject_id = request.POST['subject']
            read_level = topic_data['read_level']
            author = user
            title = topic_data['title']
            content = topic_data['content']
            if is_manager:
                title_color = '#' + request.POST['title_color']
                title_bold = topic_data['title_bold']
            else:
                title_color = "#000000"
                title_bold = False
            post_time = now
            is_hide = topic_data['is_hide']
            is_poll = topic_data['is_poll']
            has_img = '<img' in content
            ip = get_remote_ip(request)
            attachments = json.loads(request.POST['attachments'])
            # 在此添加topic到数据库
            topic = Topic.objects.create(forum=forum, subject_id=subject_id, read_level=read_level, author=author,
                                         title=title, content=content, title_bold=title_bold, title_color=title_color,
                                         post_time=post_time, last_edit_time=post_time, is_hide=is_hide, is_poll=is_poll
                                         , ip=ip, has_attachment=bool(attachments),has_img=has_img)
            if is_poll:
                if poll_form.is_valid():
                    poll_data = poll_form.cleaned_data
                    # 如果是投票贴，获取投票各项参数，若未设置过期时间，默认为7天
                    poll_descr = poll_data['descr']
                    is_multi = poll_data['is_multi']
                    is_poll_visible = poll_data['is_visible']
                    expiry = poll_data['expiry']
                    max_choices = poll_data['max_choices']
                    poll_options_str = request.POST['poll_options']
                    # 前台使用jquery保证只要勾选了is_poll，就必须填写至少两项options
                    poll_options = json.loads(poll_options_str)  # 包含投票选项字符串的集合
                    # 有poll 在此添加topic到数据库
                    poll = Poll.objects.create(topic=topic, descr=poll_descr, is_multi=is_multi,
                                               is_visible=is_poll_visible,
                                               max_choices=max_choices, expiry=expiry)
                    options = []
                    i = 1
                    for option in poll_options:
                        options.append(PollOption(poll=poll, option=option, display_order=i))
                        i += 1
                    PollOption.objects.bulk_create(options)
                else:
                    # rollback 事务
                    return render_to_response(bbs_name + '/forum/new_topic.html',
                                              {'bbs': bbs, 'forum': forum, 'config': config,
                                               'topic_form': topic_form, 'is_manager': is_manager,
                                               'attach_form': attach_form, 'poll_form': poll_form},
                                              context_instance=RequestContext(request))
            # topic创建成功后，如果有附件，创建附件
            if attachments:
                # 上传附件不为空，获取附件信息
                attachs = []
                for attach in attachments:
                    file_name = attach['file_name']
                    file_type = attach['type']
                    file_size = attach['size']
                    file_path = attach['file_path']
                    attach_download_level = attach['download_level']
                    attachs.append(Attachment(user=author, tp_id=topic.id, file=file_path, file_name=file_name,
                                              file_type=file_type, file_size=file_size,
                                              download_level=attach_download_level))
                Attachment.objects.bulk_create(attachs)
            # 所属论坛信息更新,根据最后一次发帖/回帖时间是不是今天选择不同sql命令

            update_after_topic_post(request.user, forum, post_time, topic, True)

            return HttpResponseRedirect(reverse('topic', args=(bbs['name'], topic.id)))
    return render_to_response(bbs_name + '/forum/new_topic.html', {'bbs': bbs, 'forum': forum, 'config': config,
                                                                   'topic_form': topic_form, 'is_manager': is_manager,
                                                                   'attach_form': attach_form, 'poll_form': poll_form},
                              context_instance=RequestContext(request))


@login_required
def forum_edit_tp(request, bbs_name, tp_id, t_or_p):
    bbs = config.test_bbs_name(bbs_name)
    if not bbs:
        raise Http404
    if t_or_p == 't':
        tp = Topic.objects.select_related('forum', 'author', 'subject').get(id=tp_id)
        forum = tp.forum
        topic_id = tp.id
    else:
        tp = Post.objects.select_related('topic__forum', 'author').get(id=tp_id)
        forum = tp.topic.forum
        topic_id = tp.topic.id
    is_manager = check_manager(request, forum.id)
    is_author = tp.author_id == request.user.id
    # 判断访问权限
    if not (is_manager or is_author):
        error = {'message': u'只有帖子本人、版主、管理员可以编辑'}
        return render_to_response('common/custom_error.html', {'config': config, 'error': error})
    # 生成版块层级导航条   1 > 2 > 3 > 4
    forum.path_lists = get_path_lists(forum.path_list, bbs['id'])
    # 获取主题信息
    forum.subjects = forum.subject_set.all().order_by('name')
    if tp.has_attachment:
        tp.attachments = Attachment.objects.filter(tp_id=tp_id)
    attach_form = AttachmentForm()
    if request.method == 'POST':
        if tp.is_topic():
            tp_form = TopicForm(request.POST, instance=tp)
        else:
            tp_form = PostFormFull(request.POST, instance=tp)
        if tp_form.is_valid():
            new_attachments = json.loads(request.POST['new_attachments'])
            del_original_attachments = json.loads(request.POST['del_original_attachments'])

            topic_data = tp_form.cleaned_data
            tp.has_attachment = bool(int(request.POST['attachments_num']))
            now = datetime.datetime.now()
            tp.last_edit_time = now
            tp.content = topic_data['content']
            tp.remark = u'本帖最后由 {0} 于 {1} 编辑'.format(request.user.nick_name, now.strftime('%Y-%m-%d %H:%M'))
            if tp.is_topic():
                if is_manager:
                    tp.title_color = '#' + request.POST['title_color']
                    tp.title_bold = topic_data['title_bold']
                else:
                    tp.title_color = tp.title_color
                    tp.title_bold = tp.title_bold
                tp.subject_id = request.POST['subject']
                tp.read_level = topic_data['read_level']
                tp.title = topic_data['title']
                tp.is_hide = topic_data['is_hide']
                tp.save(force_update=True, update_fields=['last_edit_time', 'content', 'subject', 'read_level',
                                                          'title', 'is_hide', 'title_color', 'title_bold',
                                                          'has_attachment', 'remark'])
            else:
                tp.save(force_update=True, update_fields=['last_edit_time', 'content', 'has_attachment', 'remark'])

            if new_attachments:
                # 添加新加的附件到数据库
                attachs = []
                for attach in new_attachments:
                    file_name = attach['file_name']
                    file_type = attach['type']
                    file_size = attach['size']
                    file_path = attach['file_path']
                    attach_download_level = attach['download_level']
                    attachs.append(Attachment(user=request.user, tp_id=tp.id, file=file_path, file_name=file_name,
                                              file_type=file_type, file_size=file_size,
                                              download_level=attach_download_level))
                Attachment.objects.bulk_create(attachs)
            if del_original_attachments:
                # 删除已经存在附件
                del_id_list = [attach['storage_name'] for attach in del_original_attachments]
                Attachment.objects.filter(id__in=del_id_list).delete()
            return HttpResponseRedirect(reverse('topic', args=(bbs['name'], topic_id)))
    else:
        if tp.is_topic():
            tp_form = TopicForm(instance=tp)
        else:
            tp_form = PostFormFull(instance=tp)

    return render_to_response(bbs_name + '/forum/edit_topic.html', {'config': config, 'tp_form': tp_form,
                                                                    'forum': forum, 'tp': tp, 'is_manager': is_manager,
                                                                    'is_author': is_author, 'bbs': bbs,
                                                                    'attach_form': attach_form},
                              context_instance=RequestContext(request))


def upload_attachment(request):
    if request.method == 'GET':
        raise Http404
    result = {'success': False, 'message': ''}
    if not request.user.is_authenticated():
        result['message'] = u'您还未登录'
    else:
        form = AttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            file_name = data['file_name']
            upload_file = data['file']
            download_level = data['download_level']
            name, ext = os.path.splitext(upload_file.name)
            size = upload_file.size
            if not (ext.startswith('.') and ext.lstrip('.') in config.allow_attachment_type):
                result['message'] = u'上传文件格式不正确，允许的格式为' + u'、'.join(config.allow_attachment_type)
                return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')
            if size > config.max_attach_size:
                result['message'] = u'上传文件不能大于' + config.max_attach_size + u'字节'
            attachment_path = config.attachment_path  # 存储在数据库中的地址，不包括文件名后缀
            attachment_full_path = os.path.join(settings.MEDIA_ROOT, attachment_path)  # 绝对地址，完全的，不包括文件名后缀
            path = default_storage.save(os.path.join(attachment_full_path, upload_file.name), upload_file)
            storage_name_ext = os.path.split(path)[1]
            storage_name = storage_name_ext.split('.')[0]
            file_path = os.path.join(attachment_path, storage_name_ext)
            result['success'] = True
            result['data'] = {'file_name': file_name, 'download_level': download_level, 'file_path': file_path,
                              'storage_name': storage_name, 'size': size, 'type': ext.lstrip('.'), 'flag': 'insert'}
        else:
            request['message'] = u'上传出错'
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')


def topic(request, bbs_name, topic_id, page='1'):
    """
    帖子显示页面
    """
    bbs = config.test_bbs_name(bbs_name)
    if not bbs:
        raise Http404
    try:
        topic = Topic.objects.raw(
            'SELECT t.*,Count(DISTINCT ut.id) t_num,Count(DISTINCT up.id) p_num,s.id AS s_id,s.name AS s_name,' +
            's.color AS s_color,u.name u_name,u.nick_name u_nickname,u.is_active u_is_active, u.avatar u_avatar, '
            'u.credits u_credits,u.bio u_bio,u.signature u_signature, u.gender u_gender, ug.name ug_name, '
            'ug.icon ug_icon,ug.id ug_id FROM topic t '
            'INNER JOIN subject s ON t.subject_id = s.id INNER JOIN user u ON t.author_id = u.id '
            'INNER JOIN topic ut ON ut.author_id = u.id INNER JOIN post up ON up.author_id = u.id '
            'INNER JOIN user_group ug ON ug.id = u.user_group_id WHERE t.id = %s', [topic_id])[0]
    except:
        raise Http404
    posts = Post.objects.raw(
        'SELECT p.*,Count(DISTINCT ut.id) t_num,Count(DISTINCT up.id) p_num,u.name u_name,u.nick_name u_nickname,' +
        'u.is_active u_is_active,u.avatar u_avatar,u.bio u_bio,u.signature u_signature,u.gender u_gender,'
        'u.credits u_credits,ug.name ug_name,ug.icon ug_icon,ug.id ug_id '
        'FROM post p INNER JOIN user u ON p.author_id = u.id '
        'INNER JOIN topic ut ON ut.author_id = u.id INNER JOIN post up ON up.author_id = u.id '
        'INNER JOIN user_group ug ON ug.id = u.user_group_id WHERE p.topic_id = %s group by p.id '
        'order by p.post_time', [topic_id])
    forum = get_object_or_404(Forum, id=topic.forum_id)
    is_manager = check_manager(request, forum.id)
    # 判断访问权限
    result = check_visit_level(request, max(forum.visit_level, topic.read_level))
    if result:
        return result
    if request.method == 'GET':
        # 生成版块层级导航条   1 > 2 > 3 > 4
        forum.path_lists = get_path_lists(forum.path_list, bbs['id'])
        posts_list = list(posts)
        topic.reply_num = len(posts_list)
        if topic.is_poll:
            try:
                topic.poll = Poll.objects.raw(
                    'SELECT poll.*,SUM(poll_option.votes) AS voters_num FROM poll INNER JOIN poll_option '
                    'ON poll_option.poll_id = poll.id WHERE poll.topic_id = %s GROUP BY poll.id', [topic.id])[0]
            except:
                raise Http404
            topic.poll.options = PollOption.objects.filter(poll=topic.poll).order_by('display_order')
        if topic.has_attachment:
            topic.attachments = Attachment.objects.filter(tp_id=topic.id)

        all = [topic] + list(posts_list)
        only_see = ''
        if 'author' in request.GET:
            # 只看该作者
            only_see = request.GET['author']
            all = [tp for tp in all if tp.u_name == only_see]

        # 分页
        all,page_int = paginator_action(all,config.replies_per_page,page)

        post_form = PostFormSimple()

        # 显示成功，帖子点击率加1
    else:
        post_form = PostFormSimple(request.POST)
        if post_form.is_valid():
            data = post_form.cleaned_data
            content = data['content']
            ip = get_remote_ip(request)
            now = datetime.datetime.now()
            post = Post(author=request.user, topic_id=topic_id, ip=ip, post_time=now, last_edit_time=now,
                        content=content)
            post.save()

            update_after_topic_post(request.user, forum, now, topic, False)

            return HttpResponseRedirect(reverse('topic', args=(bbs_name, topic_id)))
        error = {'message': post_form.errors}
        return render_to_response('common/custom_error.html', {'config': config, 'error': error})
    return render_to_response(bbs_name + '/forum/topic.html',
                              {'bbs': bbs, 'forum': forum, 'config': config, 'page': page_int,'only_see':only_see,
                               'is_manager': is_manager, 'topic': topic, 'all': all, 'post_form': post_form},
                              context_instance=RequestContext(request))


def post(request, bbs_name, post_id):
    """
    点击回复贴链接，跳转到指定回复贴处
    """
    topic = Post.objects.get(id=post_id).topic
    if not topic.is_visible:
        error = {'message': u'帖子被删除或隐藏'}
        return render_to_response('common/custom_error.html', {'config': config, 'error': error})
    posts = topic.post_set.filter(is_visible=True).order_by('-post_time')
    i = 2  # 从沙发 ，2楼开始找
    found = False
    for p in posts:
        if p.id == post_id:
            found = True
            break
        i += 1
    if not found:
        return HttpResponseRedirect(reverse('topic', args=(bbs_name, topic.id)))
    # pages = (num - 1) / config.replies_per_page + 1  # 总页数
    page = (i - 1) / config.replies_per_page + 1  # 寻找的回复贴所在页数
    url = reverse('topic_with_page', args=(bbs_name, topic.id, page)) + '#%s' % (post_id,)
    return HttpResponseRedirect(url)


def poll_action(request):
    if request.method == 'GET':
        raise Http404
    result = {'success': False, 'message': ''}
    if not request.user.is_authenticated():
        result['message'] = u'您还未登录'
    else:
        poll_result = json.loads(request.POST['poll_result'])
        poll_id = request.POST['poll_id']
        poll = get_object_or_404(Poll, id=poll_id)
        has_voted = poll.has_voted(request.user.name)
        if has_voted:
            result['message'] = u'您已经投过票了'
        elif datetime.datetime.now() > datetime.datetime.strptime(poll.expiry, '%Y-%m-%d %H:%M'):
            result['message'] = u'投票已过期'
        else:
            if poll.add_vote(request.user.name, poll_result):
                result['success'] = True
            else:
                result['message'] = u'投票失败'
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')


def support_against_action(request):
    if request.method == 'GET':
        raise Http404
    result = {'success': False, 'message': '', 'new_num': 0}
    if not request.user.is_authenticated():
        result['message'] = u'您还未登录'
    else:
        is_topic = request.POST['is_topic']
        tp_id = request.POST['tp_id']
        type = request.POST['type']
        if is_topic:
            tp = Topic.objects.get(id=tp_id)
        else:
            tp = Post.objects.get(id=tp_id)
        has_voted = tp.has_vote(request.user.name)
        if has_voted:
            result['message'] = u'您已经投过了'
        elif tp.author == request.user:
            result['message'] = u'不能对本人的帖子发表意见'
        else:
            if type == 'support':
                new_num = tp.do_support_or_against(True, request.user.name)
            else:
                new_num = tp.do_support_or_against(False, request.user.name)
            if new_num:
                result['success'] = True
                result['new_num'] = new_num
            else:
                result['message'] = u'投票失败'
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')


def change_favorite(request):
    if request.method == 'GET':
        raise Http404
    result = {'success': False, 'message': '','has_fav': False}
    if not request.user.is_authenticated():
        result['message'] = u'您还未登录'
    else:
        topic_id = request.POST['topic_id']
        try:
            fav_relation = Favorite.objects.filter(topic_id=topic_id, user=request.user)
            if len(fav_relation) > 0:
                fav_relation.delete()
                result['has_fav'] = False
            else:
                Favorite.objects.create(topic_id=topic_id, user=request.user)
                result['has_fav'] = True
            result['success'] = True
        except:
            result['success'] = False
            result['message'] = u'更改收藏状态失败'
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')

def get_favorite_state(request):
    if request.method == 'GET':
        raise Http404
    result = {'success': False, 'has_fav': False, 'message': ''}
    if not request.user.is_authenticated():
        result['message'] = u'您还未登录'
    else:
        topic_id = request.POST['topic_id']
        try:
            fav_relations = Favorite.objects.filter(topic_id=topic_id, user=request.user)
            if len(fav_relations) > 0:
                result['has_fav'] = True
            result['success'] = True
        except:
            result['success'] = False
            result['message'] = u'获取收藏信息失败'
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')


def attach_download(request, attach_id):
    attach = get_object_or_404(Attachment, pk=attach_id)
    result = check_visit_level(request, attach.download_level)
    if result:
        return result
    # 附件下载数加1
    Attachment.objects.filter(id=attach_id).update(downloads=F('downloads') + 1)
    # 如果要给上传者加分，在这里处理
    return HttpResponseRedirect(os.path.join(settings.MEDIA_URL, attach.file.url))


@login_required
def new_reply(request, bbs_name, topic_id):
    bbs = config.test_bbs_name(bbs_name)
    if not bbs:
        raise Http404
    topic = Topic.objects.select_related('forum', 'author').get(id=topic_id)
    forum = topic.forum
    if get_read_level_from_request(request) < forum.post_level:
        error = {'message': u'所在用户组访问权限小于版块回帖权限'}
        return render_to_response('common/custom_error.html', {'config': config, 'error': error})
    if request.method == 'POST':
        post_form = PostFormFull(request.POST)
        if post_form.is_valid():
            data = post_form.cleaned_data
            content = data['content']
            ip = get_remote_ip(request)
            now = datetime.datetime.now()
            prefix = request.POST.get('prefix','')
            post = Post(author=request.user, topic_id=topic_id, ip=ip, post_time=now, last_edit_time=now,
                        content=content, prefix=prefix)
            post.save()
            update_after_topic_post(request.user, forum, now, topic, False)
            return HttpResponseRedirect(reverse('topic', args=(bbs_name, topic_id)))

    forum.path_lists = get_path_lists(forum.path_list, bbs['id'])
    attach_form = AttachmentForm()
    prefix = ''
    is_reply_topic = reply_to_id = reply_type = None
    if 'id' in request.GET and 'type' in request.GET and 'topic' in request.GET:
        is_reply_topic = request.GET['topic'] == 'True'
        reply_to_id = request.GET['id']
        reply_type = request.GET['type']

    reply_to = topic
    if is_reply_topic == False:  # 不能用 if not
        reply_to = Post.objects.select_related('author').get(id=reply_to_id)
    if reply_type == 'post':
        prefix = u'<b>回复 ' + reply_to.author.nick_name + u' 的帖子</b>'
    if reply_type == 'refer':
        prefix = u'<div class="quote"><div class="quote_block"><div>{0}</div><div class="quote_author">{1} 发表于 {2}</div></div></div>' \
            .format(truncatechars_html(reply_to.content, 100), reply_to.author.nick_name, reply_to.post_time)
    if request.method == 'GET':
        post_form = PostFormFull()
    return render_to_response(bbs_name + '/forum/new_reply.html',
                              {'bbs': bbs, 'forum': forum, 'config': config, 'is_reply_topic': is_reply_topic,
                               'reply_to_id': reply_to_id, 'reply_type': reply_type, 'reply_to': reply_to,
                               'topic': topic, 'post_form': post_form, 'attach_form': attach_form, 'prefix': prefix},
                              context_instance=RequestContext(request))


def get_post_attachment(request):
    if request.method == 'GET':
        raise Http404
    post_id = request.POST['post_id']
    attachs = list(Attachment.objects.values().filter(tp_id=post_id))
    return HttpResponse(json.dumps(attachs, ensure_ascii=False), content_type='application/json')


def manage(request, action):
    if request.method == 'GET':
        raise Http404
    result = {'success': False, 'message': ''}
    forum_id = request.POST['forum_id']
    is_manager = check_manager(request, forum_id)
    if not is_manager:
        result['message'] = u'您没有管理权限'
    else:
        topic_id_list = json.loads(request.POST['id_list'])
        if action == 'all_top':
            if request.user.is_admin:
                Topic.objects.filter(id__in=topic_id_list).update(is_top_all=True)
                result['success'] = True
            else:
                result['message'] = u'必须是管理员才有全论坛置顶权限'
        elif action == 'undo_all_top':
            if request.user.is_admin:
                Topic.objects.filter(id__in=topic_id_list).update(is_top_all=False)
                result['success'] = True
            else:
                result['message'] = u'必须是管理员才有全论坛置顶权限'
        elif action == 'top':
            Topic.objects.filter(id__in=topic_id_list).update(is_top=True)
            result['success'] = True
        elif action == 'undo_top':
            Topic.objects.filter(id__in=topic_id_list).update(is_top=False)
            result['success'] = True
        elif action == 'bottom':
            Topic.objects.filter(id__in=topic_id_list).update(is_bottom=True)
            result['success'] = True
        elif action == 'undo_bottom':
            Topic.objects.filter(id__in=topic_id_list).update(is_bottom=False)
            result['success'] = True
        elif action == 'digest':
            Topic.objects.filter(id__in=topic_id_list).update(is_digest=True)
            result['success'] = True
        elif action == 'undo_digest':
            Topic.objects.filter(id__in=topic_id_list).update(is_digest=False)
            result['success'] = True
        elif action == 'del':
            Topic.objects.filter(id__in=topic_id_list).update(is_visible=False)
            result['success'] = True
        else:
            result['message'] = u'未知管理选项'
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')


def search(request, bbs_name):
    bbs = config.test_bbs_name(bbs_name)
    if not bbs:
        raise Http404
    if 'type' in request.GET and 'kw' in request.GET:
        type = request.GET['type']
        kw = request.GET['kw']
        if type == 'title':
            kws = kw.split(' ')
            results = Topic.objects.select_related('forum', 'subject', 'author').annotate(replies=Count('post'))
            for word in kws:
                results = results.filter(title__icontains=word)
            print len(results)
        elif type == 'user':
            results = MyUser.objects.select_related('user_group').filter(
                Q(name__icontains=kw) | Q(nick_name__icontains=kw))
        else:
            raise Http404
    else:
        type = None
        results = None
        kw = None
    return render_to_response(bbs_name + '/search.html',
                              {'bbs': bbs, 'config': config, 'results': results, 'type': type, 'kw': kw},
                              context_instance=RequestContext(request))


# @login_required
# def send_message(request, to_name):
# from_user_id = request.user.id
#     to_user_id = MyUser.objects.values('id').get(name=to_name)

def page_not_found(request):
    return render_to_response('common/404.html', {'config': config}, context_instance=RequestContext(request))


def server_error(request):
    return render_to_response('common/500.html', {'config': config}, context_instance=RequestContext(request))


def http_forbidden(request):
    return render_to_response('common/403.html', {'config': config}, context_instance=RequestContext(request))


def bad_request(request):
    return render_to_response('common/400.html', {'config': config}, context_instance=RequestContext(request))




