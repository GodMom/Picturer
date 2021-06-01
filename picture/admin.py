# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import *

# Register your models here.


admin.site.register(Member)
admin.site.register(Works)
admin.site.register(Tag)
admin.site.register(Fans)
admin.site.register(Attention)
admin.site.register(Image)