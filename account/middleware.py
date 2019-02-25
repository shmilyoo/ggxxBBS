# coding=utf-8
from django.utils.timezone import now
from account.models import MyUser
from forum.helper import get_remote_ip


class SetLastVisitMiddleware(object):
    def process_response(self, request, response):
        if hasattr(request,'user') and request.user.is_authenticated():
            # Update last visit time after request finished processing.
            last_visit_ip = get_remote_ip(request)
            MyUser.objects.filter(pk=request.user.pk).update(last_visit=now(),last_visit_ip=last_visit_ip)
            # 待办 同步
        return response