from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse


def z_login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.POST.get('next', '/')   # 如果没有 next 参数，默认重定向到首页
            next_url = next_url if next_url else '/'
            return redirect(next_url)
        else:
            # 如果认证失败，可以返回一个错误消息
            messages.error(request, "用户名或密码错误")
    # 对于GET请求，显示登录表单
    return render(request, '14_global_setting/login_page.html')


def z_logout_view(request):
    logout(request)
    return HttpResponse('登出成功！')
