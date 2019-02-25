# -*- coding: utf-8 -*-
import json
from django.core.files.storage import FileSystemStorage

from django.db import models

from django.db.models import F
from account.models import MyUser
from ggxxBBS import config, settings
from django.db import connections
import datetime
# Create your models here.
from uuidfield import UUIDField
import datetime

CHOICE_BBS = [('0', u'请选择论坛')] + [(num, value['cnName']) for num, value in config.bbs_names.items()]
# CHOICE_FORUM = [('0' * 32,u'首页')]


class Forum(models.Model):
    id = UUIDField(primary_key=True, auto=True)
    parent_id = UUIDField(verbose_name=u'父版块', default='0' * 32)  # 顶级版块为 '0'*32
    belong = models.CharField(max_length=1, choices=CHOICE_BBS, default=0, verbose_name=u'所属论坛')  # 属于config定义里面的哪个论坛
    name = models.CharField(max_length=64, verbose_name=u'版块名称', default='')
    tag = models.CharField(max_length=64, verbose_name=u'标签', default='')  # 只能是字母，url访问用，同一个论坛不得重名，添加时验证
    descr = models.CharField(max_length=255, verbose_name=u'版块简要介绍(显示在版块列表中)', default='')  # 显示在主页及父版块的列表里
    content = models.TextField(blank=True, verbose_name=u'版块详细介绍(显示在此版块页面中)', default='')  # 编码为html后存入，显示在版块主页面
    path_list = models.CharField(max_length=255, verbose_name=u'版块所处路径',
                                 default='')  # 添加或修改版块时加入，从最上级到本级的tag字符串列表，','分割,一级版块为''，二级为'1,'，三级为'1,2,'
    # visible = models.BooleanField(default=True, verbose_name=u'是否显示')
    display_order = models.PositiveSmallIntegerField(default=9999, verbose_name=u'显示顺序')
    allow_topic = models.BooleanField(verbose_name=u'是否允许发帖', default=True)
    icon = models.ImageField(verbose_name=u'图标', upload_to='forumIcon', blank=True)
    topic_credit = models.PositiveSmallIntegerField(verbose_name=u'主题帖积分', default='5')
    post_credit = models.PositiveSmallIntegerField(verbose_name=u'回复帖积分', default='1')
    visit_level = models.PositiveSmallIntegerField(default=0, verbose_name=u'允许访问的阅读权限')  # 0为游客也允许访问，大于0则有访问限制
    topic_level = models.PositiveSmallIntegerField(default=1, verbose_name=u'允许发帖的阅读权限')  # 默认注册用户可以发帖
    post_level = models.PositiveSmallIntegerField(default=1, verbose_name=u'允许回帖的阅读权限')  # 默认注册用户可以回帖
    today_posts = models.PositiveSmallIntegerField(verbose_name=u'今日发帖', default='0')  # 包括发帖和回帖
    update_time = models.DateTimeField(verbose_name=u'今日发帖统计时间', default='2000-01-01 00:00:00')
    last_topic_id = models.CharField(max_length=32, verbose_name=u'最后主题帖ID', default='')
    last_topic_title = models.CharField(max_length=128, default='', verbose_name=u'最后主题标题')
    last_username = models.CharField(max_length=16, default='', verbose_name=u'最后发帖/回帖用户名')
    last_nickname = models.CharField(max_length=16, default='', verbose_name=u'最后发帖/回帖用户昵称')

    class Meta:
        db_table = 'forum'
        ordering = ['display_order']
        unique_together = [
            ['belong', 'name'], ['belong', 'tag']
        ]

    def __unicode__(self):
        return self.name

    def set_moderators(self, names):
        ModeratorRelation.objects.filter(forum__pk=self.id).delete()
        for n in names:
            user = MyUser.objects.get(name=n)
            ModeratorRelation.objects.create(forum=self, moderator=user)

    def get_moderators(self):
        moderators = MyUser.objects.filter(moderatorrelation__forum__pk=self.id)
        return moderators

    def get_subjects(self):
        subjects = Subject.objects.filter(forum=self).order_by('name')
        return subjects

    def get_subjects_json(self):
        subjects = Subject.objects.values().filter(forum=self).order_by('name')
        result = json.dumps(list(subjects), ensure_ascii=False)
        return result

    def update_statistics(self, time, t_id, t_title, user_name, nick_name):
        """
        每次发帖或者回帖后，用发帖回帖当时时间，判断更新今日贴子数目，并更新最新回复等文本信息
        返回1为成功
        """
        sql = 'update forum set last_topic_id=%s,last_topic_title=%s,last_username=%s,last_nickname=%s,' + \
              'today_posts=if(date(%s)>date(%s),1,today_posts+1),update_time=%s where id=%s'
        cursor = connections['default'].cursor()
        result = cursor.execute(sql, [t_id, t_title, user_name, nick_name, time, self.update_time, time, self.id])
        return result

    def new_topic_credits(self,user):
        """
        发表新帖，更新用户积分信息
        """
        topic_credit = self.topic_credit
        user.add_credits(topic_credit)

    def new_post_credits(self,user):
        """
        发表新帖，更新用户积分信息
        """
        post_credit = self.post_credit
        user.add_credits(post_credit)

    def get_icon(self):
        """
        如果icon为空，返回默认的版块图标
        """
        if self.icon:
            return self.icon
        else:
            return config.default_forum_icon_path

    moderators = property(get_moderators, set_moderators)


class Subject(models.Model):
    """
    有些版块拥有主题，比如建言献策就有 咨询、处理中、已办结等
    每个版块都有一个默认的主题，name为空，颜色默认，当添加主题时，如果没有选择下拉中的主题，则判断name为空的是否存在，不存在的话创建一个
    删除主题时，将链接到此主题的topic，链接到name为空的主题上，如果没有则创建一个
    """
    id = UUIDField(auto=True, primary_key=True)
    forum = models.ForeignKey(Forum, db_constraint=False, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=32, default='', verbose_name=u'主题标签')
    color = models.CharField(max_length=16, verbose_name=u'标签颜色',
                             default=u'#000000')  # 默认标题颜色为黑色

    class Meta:
        db_table = 'subject'
        unique_together = [
            ['forum', 'name']
        ]


class ModeratorRelation(models.Model):
    id = UUIDField(auto=True, primary_key=True)
    forum = models.ForeignKey(Forum, db_constraint=False, on_delete=models.DO_NOTHING)
    moderator = models.ForeignKey(settings.AUTH_USER_MODEL, db_constraint=False, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'moderator_relation'
        unique_together = [
            ['forum', 'moderator']
        ]


class Notification(models.Model):
    """
    用户接收的通知，如帖子被修改删除置顶加精等处理通知，有人回帖的通知
    """
    id = UUIDField(auto=True, primary_key=True)
    to_user = models.ForeignKey(MyUser, db_constraint=False, on_delete=models.DO_NOTHING, verbose_name=u'目的用户')
    time = models.DateTimeField(auto_now_add=True, verbose_name=u'发送时间')
    content = models.CharField(max_length=255, verbose_name=u'通知内容', default='')
    has_read = models.BooleanField(default=False,verbose_name=u'是否已读')
    is_show = models.BooleanField(default=True,verbose_name=u'是否显示')

    class Meta:
        db_table = 'notification'


class Message(models.Model):
    """
    用户间私信
    """
    id = UUIDField(auto=True, primary_key=True)
    from_user = models.ForeignKey(MyUser, related_name='from_user', db_constraint=False, on_delete=models.DO_NOTHING,
                                  verbose_name=u'源用户')
    to_user = models.ForeignKey(MyUser, related_name='to_user', db_constraint=False, on_delete=models.DO_NOTHING,
                                verbose_name=u'目的用户')
    time = models.DateTimeField(auto_now_add=True, verbose_name=u'发送时间')
    content = models.CharField(max_length=255, verbose_name=u'消息内容', default='')
    has_read = models.BooleanField(default=False,verbose_name=u'是否已读')
    show_at_from = models.BooleanField(default=True,verbose_name=u'是否显示在发件人的已发邮件中')
    show_at_to = models.BooleanField(default=True,verbose_name=u'是否显示在收件人的收到邮件中')


    class Meta:
        db_table = 'message'



# 1  	tid	主题tid	int	4	0
# 2  	fid	版块id	smallint	2	0
# 3  	iconid	主题图标id	tinyint	1	0	(0)
# 4  	readperm	阅读权限	int	4	0	(0)
# 5  	poster	作者	nchar	20	0	('')
# 6  	posterid	作者uid	int	4	0	(0)
# 7  	title	标题	nchar	60	0
# 8  	postdatetime	发布时间	datetime	8	3	(getdate())
# 9  	lastpost	最后回复时间	datetime	8	3	(getdate())
# 10  	lastpostid	最后回复帖子ID	int	4	0	(0)
# 11  	lastposter	最后回复用户名	nchar	20	0	('')
# 12  	lastposterid	最后回复用户名ID	int	4	0	(0)
# 13  	views	查看数	int	4	0	(0)
# 14  	replies	回复数	int	4	0	(0)
# 15  	displayorder	>0为置顶,<0不显示,==0正常 -1为回收站 -2待审核	int	4	0	(0)
# 16  	highlight	主题高亮识别号	varchar	500	0	('')
# 17  	digest	精华级别,1~3	tinyint	1	0	(0)
# 18  	hide	是否为回复可见帖	int	4	0	(0)
# 19  	attachment	是否含有附件	int	4	0	(0)
# 20  	closed	是否关闭,如果数值>1,值代表转向目标主题的tid	int	4	0	(0)
class Topic(models.Model):
    id = UUIDField(primary_key=True, auto=True)
    forum = models.ForeignKey(Forum, verbose_name=u'所属版块', db_constraint=False, on_delete=models.DO_NOTHING)
    subject = models.ForeignKey(Subject, default='0' * 32, verbose_name=u'帖子主题',
                                db_constraint=False, on_delete=models.DO_NOTHING)
    read_level = models.PositiveSmallIntegerField(verbose_name=u'阅读权限', default=0)
    author = models.ForeignKey(MyUser, verbose_name=u'发帖人', db_constraint=False, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=128, verbose_name=u'标题', default='')
    content = models.TextField(blank=False, verbose_name=u'正文')
    title_color = models.CharField(max_length=16, verbose_name=u'标题颜色',
                                   default=u'#000000')  # 默认标题颜色为黑色，拥有一定级别的用户、版主、管理员才可以更改标题颜色
    title_bold = models.BooleanField(default=False, verbose_name=u'标题是否加粗')
    post_time = models.DateTimeField(auto_now_add=True, verbose_name=u'发帖时间')
    last_edit_time = models.DateTimeField(auto_now=True, verbose_name=u'最后编辑时间')
    # replies = models.PositiveSmallIntegerField(default=0, verbose_name=u'被回复次数')
    is_hide = models.BooleanField(default=False, verbose_name=u'是否回复可见')
    is_visible = models.BooleanField(default=True, verbose_name=u'是否隐藏')  # 因为防止同步bug，帖子只隐藏，不从数据库删除
    is_locked = models.BooleanField(default=False, verbose_name=u'是否锁定')  # 锁定贴无法回复
    is_top = models.BooleanField(default=False, verbose_name=u'是否置顶')  # 修改置顶时同时修改最后编辑时间，置顶贴排序按照最后编辑时间算
    is_top_all = models.BooleanField(default=False, verbose_name=u'是否全站置顶')
    is_bottom = models.BooleanField(default=False, verbose_name=u'是否下沉')  # 下沉贴排序按照最后回复时间排序即可
    is_digest = models.BooleanField(default=False, verbose_name=u'是否精华帖')
    has_img = models.BooleanField(default=False, verbose_name=u'是否图片帖')
    is_poll = models.BooleanField(default=False, verbose_name=u'是否投票贴')
    has_attachment = models.BooleanField(default=False, verbose_name=u'是否有附件')
    day_hits = models.PositiveIntegerField(default=0, verbose_name=u'日点击')
    week_hits = models.PositiveIntegerField(default=0, verbose_name=u'周点击')
    month_hits = models.PositiveIntegerField(default=0, verbose_name=u'月点击')
    year_hits = models.PositiveIntegerField(default=0, verbose_name=u'年点击')
    all_hits = models.PositiveIntegerField(default=0, verbose_name=u'总点击')
    last_view = models.DateTimeField(auto_now=True, default=datetime.datetime.min, verbose_name=u'最后访问时间')
    ip = models.GenericIPAddressField(protocol='IPv4', verbose_name=u'发帖IP', default='0.0.0.0')
    support = models.PositiveIntegerField(default=0, verbose_name=u'支持')
    against = models.PositiveIntegerField(default=0, verbose_name=u'反对')
    vote_names = models.TextField(default='', verbose_name=u'支持和反对用户名')  # ;分隔
    remark = models.CharField(max_length=64, verbose_name=u'备注编辑管理操作', default='')
    # attachment

    class Meta:
        db_table = 'topic'

    # def is_new(self):
    # now = datetime.datetime.now()
    # aa = (now - self.post_time).hour
    #     if aa <= 24:
    #         return True
    #     else:
    #         return False

    def is_topic(self):
        return True

    def hit(self, hit_time):
        """
        主题帖被点击一次
        """
        sql = 'select last_view into @lastview_date from topic where id = %s;\
        set @hit_date = %s;\
        set @lastview_year=year(@lastview_date),@lastview_month=month(@lastview_date),@lastview_week=week(@lastview_date),\
        @hit_year=year(@hit_date),@hit_month=month(@hit_date),@hit_week=week(@hit_date);\
        update topic \
        set \
        all_hits = all_hits+1, \
        day_hits = if(date(@hit_date)=date(@lastview_date),day_hits+1,1),\
        week_hits = if(@lastview_year=@hit_year and @lastview_week=@hit_week,week_hits+1,1),\
        month_hits = if(@lastview_year=@hit_year and @lastview_month=@hit_month,month_hits+1,1),\
        year_hits = if(@lastview_year=@hit_year,year_hits+1,1),\
        last_view = @hit_date\
        where id=%s;'

        cursor = connections['default'].cursor()
        cursor.execute(sql, [self.id, hit_time, self.id])

    def has_vote(self, user_name):
        return user_name in self.vote_names.split(';')

    def do_support_or_against(self,is_support, user_name):
        if self.vote_names:
            vote_list = self.vote_names.split(';')
        else:
            vote_list = []
        vote_list.append(user_name)
        try:
            if is_support:
                Topic.objects.filter(pk=self.pk).update(vote_names=';'.join(vote_list), support=F('support') + 1)
                return self.support + 1
            else:
                Topic.objects.filter(pk=self.pk).update(vote_names=';'.join(vote_list), against=F('against') + 1)
                return self.against + 1
        except:
            return 0

class Post(models.Model):
    id = UUIDField(primary_key=True, auto=True)
    topic = models.ForeignKey(Topic, verbose_name=u'主题帖', db_constraint=False, on_delete=models.DO_NOTHING)
    author = models.ForeignKey(MyUser, verbose_name=u'发帖人', db_constraint=False, on_delete=models.DO_NOTHING)
    # title = models.CharField(max_length=128, verbose_name=u'标题', default='')
    prefix = models.TextField(verbose_name=u'回复前缀',default='')    # 回复 xxx x楼的帖子
    content = models.TextField(blank=False, verbose_name=u'正文')
    has_attachment = models.BooleanField(default=False, verbose_name=u'是否有附件')
    post_time = models.DateTimeField(auto_now_add=True, verbose_name=u'回帖时间', default='2000-01-01 00:00:00')
    last_edit_time = models.DateTimeField(auto_now=True, verbose_name=u'最后编辑时间', default='2000-01-01 00:00:00')
    is_visible = models.BooleanField(default=True, verbose_name=u'是否隐藏')
    ip = models.GenericIPAddressField(protocol='IPv4', verbose_name=u'回复IP', default='0.0.0.0')  # 最初的ip，修改后不变
    support = models.PositiveIntegerField(default=0, verbose_name=u'支持')
    against = models.PositiveIntegerField(default=0, verbose_name=u'反对')
    vote_names = models.TextField(default='', verbose_name=u'支持和反对用户名')  # ;分隔
    remark = models.CharField(max_length=64, verbose_name=u'备注编辑管理操作', default='')

    class Meta:
        db_table = 'post'

    def is_topic(self):
        return False

    def has_vote(self, user_name):
        return user_name in self.vote_names.split(';')

    def do_support_or_against(self,is_support, user_name):
        if self.vote_names:
            vote_list = self.vote_names.split(';')
        else:
            vote_list = []
        vote_list.append(user_name)
        try:
            if is_support:
                Post.objects.filter(pk=self.pk).update(vote_names=';'.join(vote_list), support=F('support') + 1)
                return self.support + 1
            else:
                Post.objects.filter(pk=self.pk).update(vote_names=';'.join(vote_list), against=F('against') + 1)
                return self.against + 1
        except:
            return 0


class Attachment(models.Model):
    id = UUIDField(primary_key=True, auto=True)
    user = models.ForeignKey(MyUser, db_constraint=False, on_delete=models.DO_NOTHING)  # 附件所属的用户，方便通知以及加分等
    # # 附件所属的主题帖
    # 修改为tp_id, 再加一字段为 belongto_topic true false
    # topic = models.ForeignKey(Topic, db_constraint=False, on_delete=models.DO_NOTHING)
    tp_id = models.CharField(max_length=32,verbose_name=u'post或topic的id')
    file = models.FileField(verbose_name=u'附件文件', upload_to='attachment')
    file_name = models.CharField(max_length=64, verbose_name=u'附件名称', default='')
    file_type = models.CharField(max_length=16, verbose_name=u'文件类型', default='')
    file_size = models.PositiveIntegerField(default=0, verbose_name=u'文件大小(字节)')
    downloads = models.PositiveIntegerField(default=0, verbose_name=u'下载次数')
    download_level = models.PositiveSmallIntegerField(verbose_name=u'阅读权限', default=0)

    class Meta:
        db_table = 'attachment'


class Poll(models.Model):
    id = UUIDField(primary_key=True, auto=True)
    topic = models.ForeignKey(Topic, db_constraint=False, on_delete=models.DO_NOTHING)
    descr = models.CharField(max_length=128, verbose_name=u'投票描述', default='', blank=True)
    is_multi = models.BooleanField(default=False, verbose_name=u'是否多选')
    is_visible = models.BooleanField(default=False, verbose_name=u'是否回复可见')  # 投票后可见结果
    max_choices = models.PositiveSmallIntegerField(default=1, verbose_name=u'最大可选数')
    expiry = models.CharField(verbose_name=u'过期时间', default='', max_length=32, blank=True)
    voters = models.TextField(verbose_name=u'投票用户列表', default='')  # 以name;name;...的格式存储

    class Meta:
        db_table = 'poll'

    def has_voted(self, user_name):
        voter_list = self.voters.split(';')
        if user_name in voter_list:
            return True
        return False

    def get_voters_num(self):
        """
        返回投票的总人数
        """
        if self.voters:
            return self.voters.count(';') + 1
        else:
            return 0

    def add_vote(self, user_name, option_id_list):
        if self.voters:
            voter_list = self.voters.split(';')
        else:
            voter_list = []
        voter_list.append(user_name)
        # 事务
        try:
            Poll.objects.filter(pk=self.pk).update(voters=';'.join(voter_list))
            PollOption.objects.filter(id__in=option_id_list).update(votes=F('votes') + 1)
            return True
        except Exception as e:
            return False

    def is_expired(self):
        expiry = datetime.datetime.strptime(self.expiry, '%Y-%m-%d %H:%M')
        return datetime.datetime.now() >= expiry


class PollOption(models.Model):
    id = UUIDField(primary_key=True, auto=True)
    poll = models.ForeignKey(Poll, db_constraint=False, on_delete=models.DO_NOTHING)
    option = models.CharField(max_length=32, verbose_name=u'选项')
    votes = models.PositiveSmallIntegerField(default=0, verbose_name=u'票数')
    display_order = models.PositiveSmallIntegerField(default=0, verbose_name=u'排序')
    # voters = models.TextField(verbose_name=u'投票用户列表',default='')  # 以name;name;...的格式存储,取消，使用不计名投票

    class Meta:
        db_table = 'poll_option'


class Favorite(models.Model):
    id = UUIDField(primary_key=True, auto=True)
    user = models.ForeignKey(MyUser, db_constraint=False, on_delete=models.DO_NOTHING)
    topic = models.ForeignKey(Topic, db_constraint=False, on_delete=models.DO_NOTHING)
    add_time = models.DateTimeField(verbose_name=u'收藏时间',auto_now_add=True)

    class Meta:
        db_table = 'favorite'
        unique_together = [
            ['user', 'topic']
        ]



























        #
        # class A(models.Model):
        # id = models.AutoField(primary_key=True)
        # name = models.CharField(max_length=16,default='')
        #
        # def __unicode__(self):
        #         return self.name
        #
        #
        # class B(models.Model):
        #     id = models.AutoField(primary_key=True)
        #     a = models.ForeignKey(A,db_constraint=False, on_delete=models.DO_NOTHING)
        #     time = models.DateTimeField(auto_now_add=True)
        #     name = models.CharField(max_length=16,default='')
        #
        #     def __unicode__(self):
        #         return self.name
        #
        # class C(models.Model):
        #     id = models.AutoField(primary_key=True)
        #     name = models.CharField(max_length=16,default='')
        #     time = models.DateTimeField(auto_now=True)
        #
        #     def __unicode__(self):
        #         return self.name