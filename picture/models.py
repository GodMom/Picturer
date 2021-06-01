# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from django.db.models import permalink
from django.urls import reverse
import uuid


def user_directory_path(instance, filename):
    suffix = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], suffix)
    return os.path.join('img', str(instance.works_id.author_id.username), 'work', filename)


class Member(AbstractUser):
    username = models.CharField(primary_key=True, max_length=13, blank=False)
    head = models.ImageField(upload_to='head', default='cute.jpg', blank=True)
    password = models.CharField(max_length=15, blank=False)

    def __unicode__(self):
        return self.username

    class Meta:
        swappable = 'AUTH_USER_MODEL'

    @permalink
    def get_absolute_url(self):
        return reverse('mem', None, {'name': self.username})


class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    tag_name = models.CharField(max_length=6)

    def __unicode__(self):
        return self.tag_name


class Works(models.Model):
    ID = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20, blank=False)
    author_id = models.ForeignKey(Member, on_delete=models.CASCADE)
    tag_work = models.ManyToManyField(Tag, related_name='work_tag')
    description = models.TextField(max_length=200, blank=True)
    sub_time = models.DateTimeField(auto_now_add=True)
    like_num = models.PositiveIntegerField(default=0)
    col_num = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return self.title


class Image(models.Model):
    ID = models.AutoField(primary_key=True)
    works_id = models.ForeignKey(Works, on_delete=models.CASCADE)
    img = models.ImageField(upload_to=user_directory_path)

    def __unicode__(self):
        return str(self.img)


class Fans(models.Model):
    att_id = models.ForeignKey(Member, related_name='att_mem2', on_delete=models.CASCADE, db_index=True)
    fans_id = models.ForeignKey(Member, related_name='fans_mem', on_delete=models.CASCADE, db_index=True)


class Attention(models.Model):
    self_id = models.ForeignKey(Member, related_name='self_mem', on_delete=models.CASCADE, db_index=True)
    att_id = models.ForeignKey(Member, related_name='att_mem1', on_delete=models.CASCADE, db_index=True)


