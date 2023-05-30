from typing import Any
from django import http
from django.shortcuts import render
from django.views.generic import ListView, View, TemplateView
from django.urls import reverse
from django.http import HttpResponse, HttpRequest,HttpResponseRedirect
from django.contrib.auth.hashers import make_password,check_password
from PersonLog.form import UserForm, PersonForm
from PersonLog.models import User, Person
from django.contrib import messages
from .util import *
# Create your views here.

# 首页
class Index(TemplateView):
    template_name = "index.html"
    # 这里为了使用才故意这样写，应该直接在html中写就好了
    def get_context_data(self, **kwargs):
        return {
            "tourist": "12" #reverse("PersonLog:PersonList")
        }

# 登陆
class Login(View):
    def post(self, request: HttpRequest , *args, **kwargs):
        # 验证数据
        if request.POST.get("invite_code") != "1234":
            messages.info(request, "邀请码错误")
            return back(request)
        form = UserForm(request.POST)
        # 验证格式
        if not form.is_valid():
            error_msg = get_error_message(form.errors)
            messages.info(request, error_msg)
            return HttpResponseRedirect(reverse("PersonLog:index"))
        # 验证是否存在
        query_set = User.objects.filter(username=form.cleaned_data["username"]).values('passwd')
        if (query_set.exists()):
            # 账号存在
            if not check_password(form.cleaned_data["passwd"],query_set.first()["passwd"]):
                # 密码错误
                messages.info(request, "密码错误")
                return HttpResponseRedirect(reverse("PersonLog:index"))
        else:
            # 账号不存在，注册
            hash_passwd = make_password(form.cleaned_data["passwd"], "cba")
            User.objects.create(username=form.cleaned_data["username"], passwd=hash_passwd)
        # 登陆
        request.session["username"] = form.cleaned_data["username"]
        return HttpResponseRedirect(reverse("PersonLog:PersonList"))
    
# 人员展示
class PersonList(View):
    template_name = "PersonList.html"
    def get(self, request: HttpRequest) -> HttpResponse:
        query_set = Person.objects.all()
        context = {"PersonList": query_set}
        if (request.session.get("username")):
            context["username"] = request.session.get("username")
        return render(request, self.template_name, context)
    
# 人员添加
class PersonAdd(View):
    template_name = "PersonAdd.html"
    def get(self, request: HttpRequest) -> HttpResponse:
        if (not request.session.get("username")):
            messages.info(request, "没登陆不允许操作这个")
            return back(request)
        return render(request, self.template_name)
    
    def post(self, request: HttpRequest) -> HttpResponse:
        form = PersonForm(request.POST, request.FILES)
        if not form.is_valid():
            messages.info(request ,get_error_message(form.errors))
            return back(request)
        print(form.cleaned_data)
        Person.objects.create(**form.cleaned_data)
        return HttpResponseRedirect(reverse("PersonLog:PersonList"))

# 人员删除
class PersonDel(View):
    def get(self, request: HttpRequest, id):
        if (not request.session.get("username")):
            messages.info(request, "没登陆不允许操作这个")
            return back(request)
        query_set = Person.objects.filter(id = id)
        if not query_set.exists():
            messages.info(request, "删除错误")
            return back(request)
        query_set.delete()
        return back(request)

# 人员修改
class PersonModify(View):
    template_name = "PersonModify.html"
    def get(self, request: HttpRequest, id):
        if (not request.session.get("username")):
            messages.info(request, "没登陆不允许操作这个")
            return back(request)
        return render(request, self.template_name, {"person_data": Person.objects.get(id=id)})
    
    def post(self, request: HttpRequest, id):
        # 验证数据
        form = PersonForm(request.POST,request.FILES)
        # 先取消form中所有require
        for key in form.fields:
            form.fields[key].required = False
            
        if not form.is_valid():
            messages.info(request ,get_error_message(form.errors))
            return back(request)
        # 进行修改
        target_person = Person.objects.get(id=id)
        for key, value in form.cleaned_data.items():
            if (key == "pic"):
                if key in request.FILES:
                    setattr(target_person, key, value)
            elif ((key in request.POST or key in request.FILES) and (not value is None)):
                setattr(target_person, key, value)
        target_person.save()
        return HttpResponseRedirect(reverse("PersonLog:PersonList"))
        
        
    
        
    
    
        
    
    
    
        
        
            
            
            
        
        
        
        
        
