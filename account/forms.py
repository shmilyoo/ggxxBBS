# -*- coding: utf-8 -*-
from django import forms
from django.core.validators import RegexValidator
from django.forms.extras.widgets import SelectDateWidget
from account import models as accountModel

from django.utils.safestring import mark_safe
from account.models import MyUser, UserGroup
from ckeditor.widgets import CKEditorWidget
from ggxxBBS import config, settings
import os

BIRTH_YEAR_CHOICES = ('1980', '1981', '1982')
alphanumeric = RegexValidator(r'^[a-zA-Z]\w{3,15}$')

# # test
# class MyForm(forms.Form):
#     name = forms.CharField(min_length=1, max_length=8, label=u'姓名')
#     nick_name = forms.CharField(required=False)
#     birth_year1 = forms.DateField()
#     birth_year = forms.DateField(widget=SelectDateWidget(years=BIRTH_YEAR_CHOICES))


class RegForm(forms.ModelForm):
    password2 = forms.CharField(label=u'密码(再一次)', widget=forms.PasswordInput, required=True,
                                error_messages={'required': u'密码2不能为空。'})

    class Meta:
        model = accountModel.MyUser
        fields = ['name', 'gender', 'password']
        localized_fields = ('__all__',)

    def clean(self):
        data = super(RegForm, self).clean()
        p1 = data.get('password')
        p2 = data.get('password2')
        name = data.get('name')
        if p1 != p2 or p1 == '':
            self.add_error('password', u'两个密码必须相同。')
        try:
            alphanumeric(name)
        except:
            self.add_error('name', u'用户名需字母开头,由字母数字和_组成,4-16字符。')
        if MyUser.objects.filter(name=name).exists():
            self.add_error('name', u'用户名已存在。')


class UserGroupForm(forms.ModelForm):
    class Meta:
        model = accountModel.UserGroup
        fields = ['name', 'need_credits', 'icon', 'read_level']
        localized_fields = ('__all__',)

    def clean_icon(self):
        icon = self.cleaned_data.get('icon')
        if not icon:
            self.add_error('icon', u'必须定义代表用户级别的图标')
        if not os.path.exists(os.path.join(settings.STATICFILES_DIRS[0],icon)):
            self.add_error('icon',u'指定路径文件不存在')
        return icon


class UserInfoForm(forms.ModelForm):

    class Meta:
        model = accountModel.MyUser
        fields = ['nick_name','email','gender','bio','signature']
        localized_fields = ('__all__',)
        widgets = {
            'signature': CKEditorWidget(config_name='basic')
        }

class AvatarForm(forms.ModelForm):

    class Meta:
        model = accountModel.MyUser
        fields = ['avatar']

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar and avatar.size > config.max_avatar_size:
            self.add_error('avatar', u'上传图标不能超过' + str(config.max_avatar_size) + u'字节')
        return avatar