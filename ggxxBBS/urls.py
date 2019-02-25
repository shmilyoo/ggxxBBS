# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from forum import views
import ggxxBBS.config




urlpatterns = patterns('',
                       url(r'^admin/', include('forum.urls_admin')),
                       url(r'^ckeditor/', include('ckeditor.urls')),
                       url(r'^user/', include('account.urls')),
                       url(r'^user_center/', include('account.uc_urls')),
                       url(r'^$', 'forum.views.redirect', name='choose_bbs'),
                       url(r'^upload_attachment/$', 'forum.views.upload_attachment', name='upload_attachment'),
                       url(r'^get_post_attachment/$', 'forum.views.get_post_attachment', name='get_post_attachment'),
                       url(r'^poll_action/$','forum.views.poll_action',name='poll_action'),
                       url(r'^support_or_against/$','forum.views.support_against_action',name='support_against'),
                       url(r'^attach_download/(?P<attach_id>\w+)/$','forum.views.attach_download',name='attach_download'),
                       url(r'^change_favorite/$','forum.views.change_favorite',name='change_favorite'),
                       url(r'^get_favorite_state/$','forum.views.get_favorite_state',name='get_favorite_state'),
                       # url(r'^send_message/(?P<user_name>([a-zA-Z]\w{3,15}))/$','forum.views.send_message',name='send_message'),
                       url(r'^manage/(?P<action>(all_top|undo_all_top|top|undo_top|bottom|undo_bottom|digest|undo_digest|del))/$', 'forum.views.manage', name='manage'),

                       url(r'^(?P<bbs_name>\w+)/search/$', 'forum.views.search', name='search'),

                       url(r'^(?P<bbs_name>\w+)/new_topic/(?P<forum_tag>\w+)/$', 'forum.views.forum_new_topic', name='forum_new_topic'),
                       url(r'^(?P<bbs_name>\w+)/edit_tp/(?P<tp_id>([a-f0-9]{32}))/(?P<t_or_p>(t|p))/$', 'forum.views.forum_edit_tp', name='forum_edit_tp'),
                       url(r'^(?P<bbs_name>\w+)/new_reply/(?P<topic_id>\w+)/$', 'forum.views.new_reply', name='forum_new_reply'),
                       url(r'^(?P<bbs_name>\w+)/topic/(?P<topic_id>([a-f0-9]{32}))/$', 'forum.views.topic', name='topic'),
                       url(r'^(?P<bbs_name>\w+)/topic/(?P<topic_id>([a-f0-9]{32}))/(?P<page>([0-9]*))/$', 'forum.views.topic', name='topic_with_page'),
                       url(r'^(?P<bbs_name>\w+)/post/(?P<post_id>([a-f0-9]{32}))/$', 'forum.views.post', name='post'),
                       url(r'^(?P<bbs_name>\w+)/(?P<forum_tag>\w+)/$', 'forum.views.forum_index', name='forum_index'),
                       url(r'^(?P<bbs_name>\w+)/$', 'forum.views.index', name='index'),
)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'forum.views.page_not_found'
handler500 = 'forum.views.server_error'
handler403 = 'forum.views.http_forbidden'
handler400 = 'forum.views.bad_request'
