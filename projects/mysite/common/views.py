from django.contrib.auth import logout, login, authenticate
from django.shortcuts import redirect, render
from common.forms import UserForm
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth.models import User
import random




def logout_view(request):
    logout(request)
    return redirect('index')
 
def signup(request):
    if request.method == "POST":
        # 회원가입 정보 다 입력하고 회원가입 진행할 때
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('index')
    else:
        # index에서 회원가입 버튼눌렀을 때 (POST x)
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})

def password_find(request): 
    if request.method == "POST" :
        #user id가 올바른지 체크필요
        user_id = request.POST['username']
        print(user_id)
        user = User.objects.get(username = user_id)
        num = random.randrange(100000, 999999)
        print(num)
        
        email = EmailMessage(
            'Pybo 비밀번호 변경 인증번호입니다.', #이메일 제목
            str(num), #내용
            to=[user.email], #받는 이메일
        )
        email.send()
        context = {'random':num, 'user':user}
        return render(request, 'common/password_change.html', context)
        
    return render(request, 'common/password_find.html')

def password_change(request, user_id):
    user = User.objects.get(username = user_id)
    if request.method == "POST":
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            user.set_password(password1)
            user.save()
        else :
            messages.error(request, 'Password not same')
    return render(request, 'common/login.html')
        
        
            