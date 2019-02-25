from django.conf.urls import patterns, include, url
from forum import views


urlpatterns = patterns('account.views',
                       # Examples:
                       # url(r'^$', 'ggxxBBS.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^inform/(?P<inform_type>(message|notice|send_message|sent_message|send_notice))/',
                           'uc_inform', name='uc_inform'),
                       url(r'^get_unread_json/', 'get_unread_json', name='get_unread_json'),
                       url(r'^set_message_read/', 'set_message_read', name='set_message_read'),
                       url(r'^set_message_bulk_read/', 'set_message_bulk_read', name='set_message_bulk_read'),
                       url(r'^set_notice_read/', 'set_notice_read', name='set_notice_read'),
                       url(r'^set_notice_bulk_read/', 'set_notice_bulk_read', name='set_notice_bulk_read'),
                       url(r'^bulk_del_receive_message/', 'bulk_del_receive_message', name='bulk_del_receive_message'),
                       url(r'^bulk_del_sent_message/', 'bulk_del_sent_message', name='bulk_del_sent_message'),
                       url(r'^bulk_del_notice/', 'bulk_del_notice', name='bulk_del_notice'),
                       url(r'^info/(?P<info_type>(summary|topic|post|fav))', 'uc_info', name='uc_info'),
                       url(r'^data/', 'uc_data', name='uc_data'),
                       url(r'^avatar/', 'uc_avatar', name='uc_avatar'),
                       url(r'^avatar_select_pic/', 'avatar_select_pic', name='avatar_select_pic'),
                       url(r'^avatar_save_avatar/', 'avatar_save_avatar', name='avatar_save_avatar'),
                       url(r'^password/', 'uc_password', name='uc_password'),


                       # url(r'^/', 'uc_avatar', name='uc_avatar'),

)
