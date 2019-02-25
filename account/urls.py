from django.conf.urls import patterns, include, url
from forum import views


urlpatterns = patterns('account.views',
                       # Examples:
                       # url(r'^$', 'ggxxBBS.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       # url(r'^admin/', include(admin.site.urls)),
                       url(r'^login/$', 'user_login', name='login'),
                       url(r'^logout/$', 'user_logout', name='logout'),
                       url(r'^reg/$', 'user_reg', name='reg'),
                       url(r'^panel/(?P<user_name>([a-zA-Z]\w{3,15}))$', 'user_panel_name', name='user_panel_name'),
                       url(r'^search/$', 'user_search', name='user_search'),
)
