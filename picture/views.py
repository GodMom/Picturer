# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib import auth
from .forms import *
from .models import *
import json
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def homepage(request):
    auth.logout(request)
    tags = Tag.objects.all()
    form = LoginForms()
    works = Works.objects.all()
    return render(request, 'picture/homepage.html', {'form': form, 'tags': tags, 'works': works})


@login_required
def hello(request):
    tags = Tag.objects.all()
    works = Works.objects.all()
    return render(request, 'picture/homepage.html', {'tags': tags,  'works': works})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password2']

            member1 = Member.objects.create_user(username=username, password=password)
            member1.save()
            user = auth.authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password2'])
            auth.login(request, user)
            return HttpResponseRedirect('/picture/hello/')
    else:
        form = RegisterForm()

    return render(request, 'picture/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForms(request.POST)
        result = {'redirect': '', 'error': ''}
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                result['redirect'] = '/hello'
                auth.login(request, user)
                return JsonResponse(json.dumps(result, ensure_ascii=False), safe=False)
            else:
                result['error'] = u'*??????????????????,??????????????????'
                return JsonResponse(json.dumps(result, ensure_ascii=False), safe=False)
        result['error'] = form.errors[u'username'][0]
        return JsonResponse(json.dumps(result, ensure_ascii=False), safe=False)


def online(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
            return HttpResponse("yes")
        else:
            return HttpResponse("no")


@login_required
def publish(request):
    if request.method == 'POST':
        if int(request.POST.get('works')) == -1:
            choice = []
            for i in request.POST:
                if 'tag_' in i:
                    if int(request.POST[i]) == 1:
                        choice.append(i.replace('tag_', ''))
            title = request.POST.get('title')
            article = request.POST.get('description')
            user = Member.objects.get(username=request.user)
            work = Works(title=title, description=article, like_num=0, col_num=0, author_id=user)
            work.save()
            works = Works.objects.filter(author_id=request.user).order_by('-sub_time')[0]
            tags = Tag.objects.filter(tag_name__in=choice)
            for i in tags:
                works.tag_work.add(i)
            img = request.FILES.get('file')
            image = Image(works_id=works, img=img)
            image.save()
            works.image_set.add(image)
            works.save()
            return JsonResponse(json.dumps({'ID': str(works.ID)}, ensure_ascii=True), safe=False)
        else:
            work = Works.objects.get(ID=int(request.POST.get('works')))
            img = request.FILES.get('file')
            image = Image(works_id=work, img=img)
            image.save()
            work.image_set.add(image)
            work.save()
            return JsonResponse(json.dumps({'ID': str(work.ID)}, ensure_ascii=True), safe=False)
    else:
        tags = Tag.objects.all()
        return render(request, 'picture/publish.html', {'tags': tags})


def search(request):
    if request.method == 'GET':
        work_name = request.GET.get('name')
        tag_name = request.GET.get('tag')
        if tag_name is None:
            works = Works.objects.filter(title__contains=work_name)
            return render(request, 'picture/search.html', {'works': works})
        elif work_name is None:
            works = Works.objects.filter(tag_work__tag_name=tag_name)
            return render(request, 'picture/search.html', {'works': works})
        else:
            return HttpResponse('Fuck')
    else:
        return HttpResponse('fuck')


def show(request):
    if request.method == 'GET':
        work_id = request.GET.get('work')
        work = Works.objects.get(ID=int(work_id))
        img = Image.objects.filter(works_id=work)
        return render(request, 'picture/shower.html', {'work': work, 'img': img})


def tax_figure(request):
    if request.method == 'GET':
        return render(request, 'picture/tax.html')



def all_goods(request):
    if request.method == 'GET':
        data = [{'id': '1', 'title': u'??????', 'price': '1.00', 'detail': u'??????', 'stock': u'??????'},
                {'id': '2', 'title': u'??????', 'price': '5.00', 'detail': u'??????', 'stock': u'??????'},
                {'id': '3', 'title': u'??????', 'price': '2.00', 'detail': u'??????', 'stock': u'??????'},
                {'id': '4', 'title': u'??????', 'price': '1.50', 'detail': u'??????', 'stock': u'??????'},
                {'id': '5', 'title': u'????????????', 'price': '3.00', 'detail': u'??????', 'stock': u'??????'},
                {'id': '6', 'title': u'?????????', 'price': '1.00', 'detail': u'??????', 'stock': u'??????'},
                {'id': '7', 'title': u'????????????', 'price': '4.00', 'detail': u'??????', 'stock': u'??????'},
                {'id': '8', 'title': u'????????????', 'price': '2.00', 'detail': u'??????', 'stock': u'??????'},
                {'id': '9', 'title': u'????????????', 'price': '6.00', 'detail': u'??????', 'stock': u'??????'},
                {'id': '10', 'title': u'????????????', 'price': '4.5', 'detail': u'??????', 'stock': u'??????'},
                {'id': '11', 'title': u'?????????', 'price': '3.50', 'detail': u'??????', 'stock': u'??????'}]
        return HttpResponse(json.dumps(data, ensure_ascii=False), content_type='application/json')


def details(request):
    if request.method == 'GET':
        id = int(request.GET.get('id'))
        data = [{'id': '1', 'title': u'??????', 'price': '1.00', 'detail': u'??????', 'stock': u'??????'},
                {'id': '2', 'title': u'??????', 'price': '5.00', 'detail': u'??????', 'stock': u'??????'},
                {'id': '3', 'title': u'??????', 'price': '2.00', 'detail': u'??????', 'stock': u'??????'},
                {'id': '4', 'title': u'??????', 'price': '1.50', 'detail': u'??????', 'stock': u'??????'},
                {'id': '5', 'title': u'????????????', 'price': '3.00', 'detail': u'??????', 'stock': u'??????'},
                {'id': '6', 'title': u'?????????', 'price': '1.00', 'detail': u'??????', 'stock': u'??????'},
                {'id': '7', 'title': u'????????????', 'price': '4.00', 'detail': u'??????', 'stock': u'??????'},
                {'id': '8', 'title': u'????????????', 'price': '2.00', 'detail': u'??????', 'stock': u'??????'},
                {'id': '9', 'title': u'????????????', 'price': '6.00', 'detail': u'??????', 'stock': u'??????'},
                {'id': '10', 'title': u'????????????', 'price': '4.5', 'detail': u'??????', 'stock': u'??????'},
                {'id': '11', 'title': u'?????????', 'price': '3.50', 'detail': u'??????', 'stock': u'??????'}]
        return HttpResponse(json.dumps(data[id-1], ensure_ascii=False), content_type='application/json')


def addcart(request):
    if request.method == 'GET':
        return HttpResponse('yes')


def cutcart(request):
    if request.method == 'GET':
        return HttpResponse('yes')



def loadcart(request):
    if request.method == 'GET':
        a = [
         {'id': 1, 'title': '???????????? ??????', 'image': '/image/s5.png', 'num': 1, 'price': 2.00, 'selected': 'true'},
         {'id': 2, 'title': '?????? 500g', 'image': '/image/s6.png', 'num': 1, 'price': 1.00, 'selected': 'true'}
        ]
        return HttpResponse(json.dumps(a, ensure_ascii=False), content_type='application/json')


def get_address(request):
    if request.method == 'GET':
        my_address = {'name': u'?????????', 'phone': u'10086', 'detail': u'??????'}
        return HttpResponse(json.dumps(my_address, ensure_ascii=False), content_type='json')


@csrf_exempt
def set_address(request):
    if request.method == 'POST':
        data = request.POST
        print(data)
        return HttpResponse('yes')


def load_goods(request):
    if request.method == 'GET':
        data = [
  {
    "id": "guowei",
    "banner": "/image/c1.png",
    "cate": "??????",
    "detail": [
      {
        "id": 1,
        "thumb": "/image/goods1.jpg",
        "name": "??????"
      },
      {
        "id": 2,
        "thumb": "/image/goods2.jpg",
        "name": "??????"
      },
    ]
  },
  {
    "id": "chaohuo",
    "banner": "/image/c1.png",
    "cate": "??????",
    "detail": [
      {
        "id": 3,
        "thumb": "/image/goods3.jpg",
        "name": "??????"
      },
      {
        "id": 4,
        "thumb": "/image/goods4.jpg",
        "name": "??????"
      },
    ]
  },
  {
    "id": "latiao",
    "banner": "/image/c1.png",
    "cate": "??????",
    "detail": [
      {
        "id": 5,
        "thumb": "/image/goods5.jpg",
        "name": "????????????"
      },
      {
        "id": 6,
        "thumb": "/image/goods6.jpg",
        "name": "?????????"
      },
    ]
  },
  {
    "id": "binggao",
    "banner": "/image/c1.png",
    "cate": "??????",
    "detail": [
      {
        "id": 7,
        "thumb": "/image/goods7.jpg",
        "name": "????????????"
      },
      {
        "id": 8,
        "thumb": "/image/goods8.jpg",
        "name": "????????????"
      },
      {
        "id": 9,
        "thumb": "/image/goods9.jpg",
        "name": "????????????"
      },
    ]
  },
  {
    "id": "drink",
    "banner": "/image/c1.png",
    "cate": "??????",
    "detail": [
      {
        "id": 10,
        "thumb": "/image/goods9.jpg",
        "name": "????????????"
      },
      {
        "id": 11,
        "thumb": "/image/goods10.jpg",
        "name": "?????????"
      },
    ]
  }]
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type='json')


def special_goods(request):
    if request.method == 'GET':
        kind = request.GET.get('kind')
        if kind == 'guowei':
            goods = [{'id': '1', 'title': u'??????', 'price': '1.00', 'detail': u'??????', 'stock': u'??????'},
                 {'id': '2', 'title': u'??????', 'price': '5.00', 'detail': u'??????', 'stock': u'??????'}]
        elif kind == 'latiao':
            goods = [{'id': '5', 'title': u'????????????', 'price': '3.00', 'detail': u'??????', 'stock': u'??????'},
                 {'id': '6', 'title': u'?????????', 'price': '1.00', 'detail': u'??????', 'stock': u'??????'}]
        elif kind == 'feizhai':
            goods = [{'id': '5', 'title': u'????????????', 'price': '3.00', 'detail': u'??????', 'stock': u'??????'},
                     {'id': '9', 'title': u'????????????', 'price': '6.00', 'detail': u'??????', 'stock': u'??????'},
                     {'id': '10', 'title': u'????????????', 'price': '4.5', 'detail': u'??????', 'stock': u'??????'}]
        else:
            return HttpResponse('What do you fucking want??')
        return HttpResponse(json.dumps(goods, ensure_ascii=False), content_type='json')


def get_json(request):
    if request.method == 'GET':
        data = open('d:/data/result.txt', 'r')
        lines = data.readlines()
        result = []
        for line in lines:
            data_r = {}
            line = line.strip('\n')
            data_r.update(ip=line.split('\t', 2)[0])
            data_r.update(num=line.split('\t', 2)[1])
            result.append(data_r)
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='json')

