# coding=utf-8
from forum.models import Message, Notification
from models import UserGroup, MyUser
from django.contrib.auth import login


def my_login(request,user):
    login(request,user)
    user.is_logout = False
    user.save(update_fields=['is_logout'])
    # 待办 同步
    user.refresh_ug()


def get_read_level_from_request(request):
    if not hasattr(request,'user'):
        return 0
    if request.user.is_authenticated():
        a = UserGroup.objects.values('read_level').get(pk=request.user.user_group_id)
        return a['read_level']
    else:
        return 0

def get_unread_message_num(user):
    return Message.objects.filter(to_user=user,has_read=False).count()

def get_unread_notification_num(user):
    return Notification.objects.filter(to_user=user,has_read=False).count()
