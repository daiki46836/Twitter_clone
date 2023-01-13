from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import AccountForm, AddAccountForm

# ログイン・ログアウト処理に利用
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# 新規登録
class AccountRegistration(TemplateView):
    def __init__(self):
        self.params = {
        "AccountCreate":False,
        "account_form": AccountForm(),
        "add_account_form":AddAccountForm(),
        }

    def get(self,request):
        self.params["account_form"] = AccountForm()
        self.params["add_account_form"] = AddAccountForm()
        self.params["AccountCreate"] = False
        return render(request,"accounts/register.html",context=self.params)

    def post(self,request):
        self.params["account_form"] = AccountForm(data=request.POST)
        self.params["add_account_form"] = AddAccountForm(data=request.POST)

        if self.params["account_form"].is_valid() and self.params["add_account_form"].is_valid():
            account = self.params["account_form"].save()
            # パスワードをハッシュ化
            account.set_password(account.password)
            account.save()

            add_account = self.params["add_account_form"].save(commit=False)
            # AccountForm & AddAccountForm 1vs1 紐付け
            add_account.user = account
            # 画像アップロード有無検証
            if 'account_image' in request.FILES:
                add_account.account_image = request.FILES['account_image']
            add_account.save()

             # アカウント作成情報更新
            self.params["AccountCreate"] = True

        else:
            # フォームが有効でない場合
            print(self.params["account_form"].errors)
            return render(request,"accounts/register.html",context=self.params)

        return render(request,"accounts/login.html")

# ログイン
def Login(request):
    # POST
    if request.method == 'POST':
        ID = request.POST.get('userid')
        Pass = request.POST.get('password')

        user = authenticate(username=ID, password=Pass)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse('ログインIDまたはパスワードが間違っています。')
        else:
            return HttpResponse('ログインIDまたはパスワードが間違っています。')
    # GET
    else:
        return render(request, 'accounts/login.html')

# ログアウト
@login_required
def Logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('Login'))

# ホーム
@login_required
def home(request):
    params = {"UserID":request.user,}
    return render(request, "accounts/home.html",context=params)
