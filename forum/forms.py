# -*- coding: utf-8 -*-
import datetime

from django import forms
from django.core.exceptions import NON_FIELD_ERRORS
from django.core.validators import RegexValidator
from django.utils.html import strip_tags, remove_tags
from django.utils.safestring import mark_safe
from forum import models as forumModels
from forum.helper import check_empty
from ggxxBBS import config
from ckeditor.widgets import CKEditorWidget


form_tag_regex = RegexValidator(r'^[a-zA-Z][a-zA-Z0-9]+$')


class ForumForm(forms.ModelForm):
    class Meta:
        model = forumModels.Forum
        fields = ['belong', 'parent_id', 'name', 'tag', 'descr', 'content', 'allow_topic', 'icon', 'topic_credit',
                  'post_credit', 'visit_level', 'topic_level', 'post_level']
        widgets = {
            # 'parent_id':forms.Select(),
            'content': CKEditorWidget(config_name='basic'),
        }
        # initial = {
        # 'parent_id':[('0' * 32, u'首页')]
        # }
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': u"所属论坛与版块名，所属论坛与标签，必须唯一",
            }
        }

    def clean(self):
        data = super(ForumForm, self).clean()
        visit_level = data.get('visit_level')
        topic_level = data.get('topic_level')
        post_level = data.get('post_level')
        if not topic_level >= post_level >= visit_level:
            self.add_error('visit_level', u'允许发帖需要权限≥回帖≥访问')

    def clean_icon(self):
        icon = self.cleaned_data.get('icon')
        if icon and icon.size > config.max_avatar_size:
            self.add_error('icon', u'上传图标不能超过' + str(config.max_avatar_size) + u'字节')
        return icon

    def clean_belong(self):
        belong = self.cleaned_data.get('belong')
        if belong == '0':
            self.add_error('belong', u'请选择论坛')
        return belong

    def clean_tag(self):
        tag = self.cleaned_data.get('tag')
        try:
            form_tag_regex(tag)
        except:
            self.add_error('tag', u'标签由1个及以上的字母或数字组成,由字母开头')
        return tag



class TopicForm(forms.ModelForm):
    class Meta:
        model = forumModels.Topic
        fields = ['read_level', 'title', 'content', 'title_bold', 'is_hide', 'is_poll']
        widgets = {
            'content': CKEditorWidget(config_name='default'),
            'subject': forms.Select(),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')

        return title

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if check_empty(content):
            self.add_error('content', u'帖子内容不能为空')
        return content

class PostFormSimple(forms.ModelForm):
    class Meta:
        model = forumModels.Post
        fields = ['content']
        widgets = {
            'content': CKEditorWidget(config_name='basic')
        }

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if check_empty(content):
            self.add_error('content', u'帖子内容不能为空')
        return content

class PostFormFull(forms.ModelForm):
    class Meta:
        model = forumModels.Post
        fields = ['content']
        widgets = {
            'content': CKEditorWidget(config_name='default')
        }

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if check_empty(content):
            self.add_error('content', u'帖子内容不能为空')
        return content

class AttachmentForm(forms.ModelForm):
    class Meta:
        model = forumModels.Attachment
        fields = ['file', 'file_name', 'download_level']


class PollForm(forms.ModelForm):
    class Meta:
        model = forumModels.Poll
        fields = ['descr', 'is_multi', 'is_visible', 'max_choices', 'expiry']

    def clean_expiry(self):
        expiry = self.cleaned_data.get('expiry')
        try:
            poll_expire_time = datetime.datetime.strptime(expiry, '%Y-%m-%d %H:%M')
        except Exception as e:
            poll_expire_time = datetime.datetime.now() + datetime.timedelta(days=7)
        return unicode(poll_expire_time.strftime('%Y-%m-%d %H:%M'))



