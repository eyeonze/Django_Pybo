from django.contrib.auth import logout, login, authenticate
from django.shortcuts import redirect, render
from common.forms import UserForm



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