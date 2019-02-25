# -*- coding: utf-8 -*-
import datetime
import pickle
from django import template
from django.core.urlresolvers import reverse
from account.models import MyUser
from forum.models import Post
from ggxxBBS import config

register = template.Library()


@register.filter
def addattrs(field, css):
    """
    在模板的form的field中，特别是input中添加各种attr
    """
    attrs = {}
    definition = css.split(',')
    for d in definition:
        if '=' not in d:
            attrs['class'] = d
        else:
            t, v = d.split('=')
            attrs[t] = v
    return field.as_widget(attrs=attrs)


@register.filter
def is_new(time):
    """
    24小时内发表的topic为新帖
    """
    now = datetime.datetime.now()
    delta = now - time
    return delta.days == 0


@register.filter
def has_replied(user, topic):
    """
    根据传入的主题帖，判断用户是否已经回复过这个帖子，用于回复可见帖子
    """
    if user.is_authenticated():
        if topic.author_id == user.id:
            return True
        posts = Post.objects.values('id').filter(topic_id=topic.id, author_id=user.id)
        return bool(posts)
    return False


@register.filter
def has_voted(poll, user):
    if user.is_authenticated():
        return poll.has_voted(user.name)
    return False


@register.filter
def get_vote_width(vote_num, sum_num):
    if sum_num == 0:
        return 0
    width = round(vote_num * config.poll_option_max_length / sum_num, 1)
    return width


@register.filter
def get_topic_pages(replies_num):
    num = replies_num + 1
    num_pages = (num - 1) / config.replies_per_page + 1
    return range(1,num_pages + 1)

@register.filter
def remove_color_prefix(value):
    return value.replace('#','')

@register.filter
def get_floor_string(num,page):
    floor = (page - 1) * config.replies_per_page + num
    if floor == 1:
        return u'楼主'
    elif floor == 2:
        return u'沙发'
    elif floor == 3:
        return u'板凳'
    else:
        return unicode(floor) + u'楼'

@register.filter
def friendly_time(value):
    now = datetime.datetime.now()
    time_str = value.strftime('%H:%M')
    date_str = value.strftime('%Y-%m-%d')
    day_delta = now.date() - value.date()
    days = day_delta.days
    if days > 10:
        return date_str
    elif days > 2:
        return unicode(days) + u'天前'
    elif days == 2:
        return u'前天 ' + time_str
    elif days == 1:
        return u'昨天 ' + time_str
    else:
        delta_seconds = (now - value).seconds
        if delta_seconds >= 3600:
            return unicode(delta_seconds / 3600) + u'小时前'
        elif delta_seconds >= 60:
            return unicode(delta_seconds / 60) + u'分钟前'
        else:
            return unicode(delta_seconds) + u'秒前'

@register.filter
def get_sex_img_html(sex):
    if sex == 1:
        return '<img title="男" height="15" src="/static/images/male.gif">'
    elif sex == 0:
        return '<img title="女" height="15" src="/static/images/female.gif">'
    else:
        return '<img title="外星人" height="15" src="/static/images/alien3.gif">'

@register.filter
def str_datetime(value):
    return value.strftime("%Y-%m-%d %H:%M")

@register.filter
def mark(value,kw):
    kws = kw.split(' ')
    for word in kws:
        value = value.replace(word,'<em>' + word + '</em>')
    return value

# @register.filter
# def pickle_load(value):
#     s = pickle.loads(value)
#     return s