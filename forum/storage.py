# -*-coding:utf-8 -*-
import os
import datetime
from django.core.files.storage import FileSystemStorage
from django.conf import settings


class FileStorage(FileSystemStorage):
    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):
        # 初始化
        super(FileStorage, self).__init__(location, base_url)

    # 重写 _save方法
    def _save(self, name, content):
        # ckeditor不使用缩略图，没必要，增加同步复杂度
        # is_thumb = os.path.splitext(name)[0].endswith('_thumb')
        # if not is_thumb:

        # 文件扩展名
        ext = os.path.splitext(name)[1]
        # 文件目录
        d = os.path.dirname(name)
        # 定义文件名，年月日时分秒微秒
        fn = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        # 重写合成文件名
        name = os.path.join(d, fn + ext)
        # 调用父类方法
        return super(FileStorage, self)._save(name, content)