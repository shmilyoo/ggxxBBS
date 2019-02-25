from django.conf.urls import patterns, url
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.cache import never_cache

from ckeditor import views

urlpatterns = patterns(
    '',
    # url(r'^upload/', staff_member_required(views.upload), name='ckeditor_upload'),
    # url(r'^browse/', never_cache(staff_member_required(views.browse)), name='ckeditor_browse'),
    url(r'^upload/', views.upload, name='ckeditor_upload'),
    url(r'^browse/', never_cache(views.browse), name='ckeditor_browse'),
    url(r'^upload/image/', views.upload, name='ckeditor_upload_image'),
    url(r'^upload/attachment', views.upload, name='ckeditor_upload_attachment'),
    url(r'^upload/flash', views.upload, name='ckeditor_upload_flash'),
)
