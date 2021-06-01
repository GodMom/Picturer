# -*- coding: utf-8 -*-
from django.forms import *
from django import forms
from .models import Member
import re


class RegisterForm(forms.Form):
    username = forms.CharField(label=u'用户名', max_length=12, label_suffix=None)
    password1 = forms.CharField(label=u'密码', label_suffix=None, widget=widgets.PasswordInput
    (attrs={'class': 'register', 'autocomplete': 'new-password'}))
    password2 = forms.CharField(label=u'确认密码', label_suffix=None, widget=widgets.PasswordInput
    (attrs={'class': 'register', 'autocomplete': 'new-password'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if not 4 <= len(username) <= 13:
            raise forms.ValidationError(u'*用户名由4-13个字符或数字组成，请重新输入!')
        elif not re.match(u"^[a-zA-Z0-9\u4e00-\u9fa5]", username):
            raise forms.ValidationError(u'*用户名只能由汉字,英文字母或数字组成!')
        else:
            user_result = Member.objects.filter(username__exact=username)
            if len(user_result) != 0:
                raise forms.ValidationError(u'*用户名已存在,换个其他的吧')

        return username

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if not 6 <= len(password1) <= 15:
            raise forms.ValidationError(u'*密码为6-13位,再想想吧')
        elif not re.match(r'([0-9]+(\w+|\_+|[A-Za-z]+))+|([A-Za-z]+(\w+|\_+|\d+))+|((\w+|\_+)+(\d+|\w+))+', password1):
            raise forms.ValidationError(u'*密码至少由英文字母,数字,以及_其中两种及以上组成')

        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 is None:
            return password2
        if password1 != password2:
            raise forms.ValidationError(u'*两次密码不一致,请重新检查')

        return password2


class LoginForms(forms.Form):
    username = forms.CharField(label=u'用户名', max_length=12)
    password = forms.CharField(label=u'密码', widget=forms.PasswordInput(attrs={'class': 'register'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user_result = Member.objects.filter(username__exact=username)
        if not user_result.exists():
            raise forms.ValidationError(u'*用户名或密码错误,请再检查一下吧')
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        return password
