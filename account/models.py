# -*- coding: utf-8 -*-

# Create your models here.
import datetime
from django.core.context_processors import request
from django.utils import timezone
from ggxxBBS import settings, config
from uuidfield.fields import UUIDField
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

GENDER = ((True, u'男'), (False, u'女'), (None, u'保密'))


class UserGroupManager(BaseUserManager):
    def get_or_create_default_ug(self):
        try:
            ug = UserGroup.objects.get(need_credits=0)
        except:
            ug = UserGroup.objects.create(need_credits=0, name=u'初来乍到', read_level=1)
        return ug


class UserGroup(models.Model):
    id = UUIDField(auto=True, primary_key=True)
    name = models.CharField(max_length=16, blank=False, verbose_name=u'名称')
    need_credits = models.PositiveIntegerField(verbose_name=u'需要积分', default=0, unique=True)
    icon = models.CharField(max_length=200, verbose_name=u'图标', default='')
    read_level = models.PositiveSmallIntegerField(default=1, verbose_name=u'阅读权限')  # 1为初始注册用户权限
    can_ip = models.BooleanField(default=False, verbose_name=u'查看IP')

    objects = UserGroupManager()

    class Meta:
        db_table = 'user_group'


# class AdminGroup(models.Model):
# id = UUIDField(auto=True, primary_key=True)
# type = models.CharField(max_length=16,verbose_name=u'管理类型',unique=True,default='')
#
#     class Meta:
#         db_table = 'admin_group'
#
# def create_default_ag():
#     try:
#         ag = AdminGroup.objects.get(type=u'会员')
#     except:
#         ag = AdminGroup.objects.create(type=u'会员')
#     return ag


class MyUserManager(BaseUserManager):
    def create_user(self, name, password=None, nick_name=None, gender=None, reg_ip='', is_admin=False):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not name:
            raise ValueError(u'用户必须提供用户名称')

        user = self.model(name=name)
        if nick_name:
            user.nick_name = nick_name
        else:
            user.nick_name = name
        # user.admin_group = create_default_ag()
        user.user_group = UserGroup.objects.get_or_create_default_ug()
        user.is_admin = is_admin
        user.reg_ip = reg_ip
        user.gender = gender
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(name=name)
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    id = UUIDField(auto=True, primary_key=True)
    name = models.CharField(verbose_name=u'用户名', max_length=16, unique=True)  # 登录用户名
    nick_name = models.CharField(max_length=16, verbose_name=u'昵称', unique=True)  # 昵称，不设置则与name相同
    email = models.EmailField(verbose_name=u'电子邮件', max_length=255, blank=True)
    is_active = models.BooleanField(default=True, verbose_name=u'是否可用')  # 是否禁用
    is_admin = models.BooleanField(default=False, verbose_name=u'是否管理员')  # 是否管理员
    gender = models.NullBooleanField(choices=GENDER, default=None, verbose_name=u'性别')  # 性别，none为保密，false为女，true或其他为男
    avatar = models.ImageField(verbose_name=u'头像', upload_to='avatar', default='')
    avatarwidth = models.PositiveSmallIntegerField(verbose_name=u'头像宽度', default=60)
    avatarheight = models.PositiveSmallIntegerField(verbose_name=u'头像高度', default=60)
    bio = models.CharField(max_length=255, verbose_name=u'个人简介', blank=True)
    signature = models.CharField(max_length=500, verbose_name=u'个人签名', blank=True)
    is_logout = models.BooleanField(verbose_name=u'是否登出状态', default=True)
    # admin_group = models.ForeignKey(AdminGroup, default=0, verbose_name=u'管理员组',db_constraint=False)  # 0表示不是管理员
    user_group = models.ForeignKey(UserGroup, verbose_name=u'用户组', db_constraint=False,
                                   on_delete=models.DO_NOTHING)  # 用户组id，默认普通会员
    reg_ip = models.GenericIPAddressField(protocol='IPv4', verbose_name=u'注册IP')  # 注册IP地址
    reg_time = models.DateField(auto_now_add=True, verbose_name=u'注册日期')  # 注册日期
    last_visit = models.DateTimeField(auto_now_add=True, verbose_name=u'最后访问时间')  # 上次访问时间
    last_visit_ip = models.GenericIPAddressField(protocol='IPv4', verbose_name=u'最后访问IP', default='0.0.0.0')
    # topic_num = models.PositiveIntegerField(default=0, verbose_name=u'主题数')  #发表主题数
    # post_num = models.PositiveIntegerField(default=0, verbose_name=u'回复数')  #发表回复数
    # digest_number = models.PositiveIntegerField(default=0, verbose_name=u'精华帖数')
    credits = models.PositiveIntegerField(default=0, verbose_name=u'积分')

    objects = MyUserManager()

    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'user'

    def get_full_name(self):
        # The user is identified by their email address
        return self.name

    def get_short_name(self):
        # The user is identified by their email address
        return self.name

    def __unicode__(self):  # __unicode__ on Python 2
        return self.name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def refresh_ug(self):
        if self.user_group_id in ['10000000000000000000000000000002', '10000000000000000000000000000003',
                                  '10000000000000000000000000000004']:
            return
        ug = UserGroup.objects.filter(need_credits__lte=self.credits).order_by('-need_credits')[0]
        self.user_group = ug
        self.save(update_fields=['user_group'])

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    @property
    def is_superuser(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are superuser
        return self.is_admin

    @property
    def username(self):
        return self.name

    def get_avatar(self):
        if self.avatar:
            return self.avatar
        else:
            return config.default_avatar_path

    def add_credits(self, num):
        self.credits = self.credits + num
        self.save(update_fields=['credits'])

    def subtract_credits(self, num):
        c = self.credits - num
        if c < 0:
            c = 0
        self.credits = c
        self.save(update_fields=['credits'])

    # def add_topic_num(self,num):
    #     self.topic_num += num
    #     self.save(update_fields=['topic_num'])
    #
    # def add_post_num(self,num):
    #     self.post_num += num
    #     self.save(update_fields=['post_num'])
    #
    # def update_after_topic(self,bonus):
    #     """
    #     发帖后更新用户信息，发帖数+1,积分更新
    #     """
    #     self.topic_num += 1
    #     self.credits += bonus
    #     self.save(update_fields=['topic_num','credits'])
    #
    # def update_after_post(self,bonus):
    #     """
    #     回帖后更新用户信息，回帖数+1,积分更新
    #     """
    #     self.post_num += 1
    #     self.credits += bonus
    #     self.save(update_fields=['post_num','credits'])

# class Info(models.Model):
#     """
#     额外的用户信息
#     """
#     # uuid = UUIDField(auto=True,hyphenate=True,primary_key=True)
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, db_column='user_id')
#
#
#     # name1 = models.CharField(max_length=64,default='yy')
#     # ages = models.IntegerField(default=20)
#
#     class Meta:
#         db_table = 'user_info'



