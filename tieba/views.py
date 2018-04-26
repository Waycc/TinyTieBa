from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from tieba import models, forms
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.utils.decorators import method_decorator
import json
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from tieba.utils import is_login, query_set
# Create your views here.


class Registration(View):
    """用户注册视图"""

    @method_decorator(is_login)
    def get(self,request):

        return render(request, 'registration.html')

    def post(self,request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        name = request.POST.get('name')
        errors = {'field_errors':None, 'all_errors':''}
        next_url = request.GET.get('next','/tieba/index/')
        registration_form_obj = forms.UserRegistrationForm(request.POST)
        if registration_form_obj.is_valid():
                user = models.UserProfile(email=email,name=name)
                user.set_password(password)
                user.save()
                login(request, user)
                return redirect(next_url)
        else:
            errors['field_errors'] = registration_form_obj.errors.get_json_data()
            print(errors)
        return render(request, 'registration.html', {'errors':errors})


class LoginView(View):
    """用户登录处理视图"""

    @method_decorator(is_login)
    def get(self, request):
        is_get = True
        return render(request, 'login.html',{'user': 'root@126.com', 'pwd': 'asd456789','is_get':is_get})

    def post(self, request):
        login_form_obj = forms.UserLoginForm(request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')
        errors = {'field_errors':None, 'all_errors':''}
        if login_form_obj.is_valid():
            user = authenticate(username=email, password=password)
            if user:
                login(request, user)
                next_url = request.GET.get('next','/tieba/index')
                return redirect(next_url)
            else:
                errors['all_errors'] = '邮箱或密码错误'
        else:
            errors['field_errors'] = login_form_obj.errors.get_json_data()  # { 'email': [{'message': '邮箱不能为空', 'code': 'required'}] }
        return render(request,'login.html',{'errors': errors})


class IndexView(View):
    """用户登录后默认跳转的视图"""

    def dispatch(self, request, *args, **kwargs):
        return super(IndexView,self).dispatch(request, *args, **kwargs)

    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'index.html')

    def post(self, request):
        pass


class FView(View):
    """具体贴吧的视图"""

    def dispatch(self, request, *args, **kwargs):
        return super(FView,self).dispatch(request, *args, **kwargs)

    def get(self, request):
        tieba_name = request.GET.get('tieba_name', '')
        if tieba_name:
            return redirect('/tieba/f?kw=%s'%(tieba_name))

        kw = request.GET.get('kw','')
        page = request.GET.get('p')
        tieba_obj = models.TieBa.objects.filter(name=kw).first()
        if kw == '0':
            return render(request, 'new_tieba.html')
        try:
            article_obj_list = tieba_obj.article_set.all()
        except AttributeError:
            return HttpResponse(mark_safe('没有找到该贴吧，<a href="/tieba/f?kw=0">现在创建新的贴吧</a>'))

        article_obj_list = query_set(article_obj_list,page,1)
        page_range = iter(range(1,article_obj_list.paginator.num_pages+1))
        return render(request, 'f.html', {'tieba_obj':tieba_obj,
                                          'article_obj_list':article_obj_list,
                                          'page_range':page_range
                                          })

    @method_decorator(login_required)
    def post(self, request):
        """创建新的贴吧"""
        tieba_name = request.POST.get('tieba_name')
        background_img = request.FILES.get('background_img')
        head_img = request.FILES.get('head_img')
        new_tieba_forms = forms.NewTieBaForm(request.POST)
        error_msg = ''
        if new_tieba_forms.is_valid():
            if head_img and background_img:
                new_tieba_obj = models.TieBa(name=tieba_name,
                                             background_img=background_img,
                                             head_img=head_img)
            elif background_img:
                new_tieba_obj = models.TieBa(name=tieba_name,
                                             background_img=background_img)
            elif head_img:
                new_tieba_obj = models.TieBa(name=tieba_name,
                                             head_img=head_img)
            else:
                new_tieba_obj = models.TieBa(name=tieba_name)
            new_tieba_obj.save()
            return redirect('/tieba/f?kw=%s'%tieba_name)

        else:
            error_msg = new_tieba_forms.errors.get_json_data()
            print('no')
        return render(request,'new_tieba.html',{'error_msg':error_msg})

class ArticleView(View):
    """具体贴子的视图"""
    def dispatch(self, request, *args, **kwargs):
        return super(ArticleView,self).dispatch(request, *args, **kwargs)

    def get(self, request, article_id):
        comment_obj_list = models.Comment.objects.filter(article=article_id, to_comment=None)

        article_obj = models.Article.objects.filter(id=article_id).first()
        try:
            tieba_obj = article_obj.tieba
        except AttributeError as e:
            return HttpResponse('没有找到该帖子')
        return render(request, 'article.html', {'article_obj':article_obj,
                                                'tieba_obj':tieba_obj,
                                                'comment_obj_list':comment_obj_list})

    def post(self, request, article_id):
        errors = {'field_errors':{}, 'all_errors':'', 'status':True}
        #创建帖子
        if article_id == '0':
            article_form_obj = forms.ArticleForm(request.POST)
            title = request.POST.get('title','')
            content = request.POST.get('content','')
            tieba_id = request.POST.get('tieba_id','')
            if article_form_obj.is_valid():
                tieba_obj = models.TieBa.objects.filter(id=tieba_id).first()
                article = models.Article(author=request.user,title=title,content=content,tieba=tieba_obj)
                article.save()
            else:
                errors['status'] = False
                for error_name, error in article_form_obj.errors.get_json_data().items():
                    errors['field_errors'][error_name] = error[0]['message']
                print(errors)
        return HttpResponse(json.dumps(errors))


class HomeMainView(View):
    """个人资料页面"""
    @method_decorator(login_required)
    def get(self,request):
        is_login_user = False
        uid = request.GET.get('uid', '')
        if uid:
            user_obj = models.UserProfile.objects.filter(id=uid).first()
            if user_obj == request.user:
                is_login_user = True
        else:
            return HttpResponse('没有找到该用户')
        return render(request, 'home.html',{'user_obj': user_obj, 'is_login_user': is_login_user})

    @method_decorator(login_required)
    def  post(self, request):
        pass


class FollowView(View):
    """处理贴吧关注"""
    def get(self, request):
        pass

    @method_decorator(login_required)
    def post(self, request):
        msg = {'status':False}
        tieba_id = request.POST.get('tieba_id')
        follow = request.POST.get('follow')
        followed_tieba_query = request.user.followed_tieba
        if follow == '0' and tieba_id:
            followed_tieba_query.remove(tieba_id)
            msg['status'] = True
        elif follow == '1'and tieba_id:
            followed_tieba_query.add(tieba_id)
            msg['status'] = True
        return HttpResponse(json.dumps(msg))


class EditProfile(View):

    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'edit_profile.html')

    def post(self, request):
        pass


class Portrait(View):
    """修改用户头像"""

    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'portrait.html')

    def post(self, request):
        img = request.FILES.get('img')
        if img:
            user_obj = models.UserProfile.objects.filter(id=request.user.id).first()
            user_obj.head_img = img
            user_obj.save()
        return redirect('/tieba/profile/')


class Comment(View):
    """评论"""
    def get(self, request):
        pass

    def post(self, request):
        msg = {'status':False}
        to_whom = request.POST.get('to_whom','')
        article_id = request.POST.get('article_id','')
        comment_id = request.POST.get('comment_id','')
        comment = request.POST.get('comment','')
        article_obj = models.Article.objects.filter(id=article_id).first()
        print(article_id)
        if comment.startswith('回复'):
            comment = comment.split(':',1)[1]
        if comment_id:
            # 处理子评论
            to_comment_obj = models.Comment.objects.filter(id=comment_id).first()
            comment_obj = models.Comment(
                    author=request.user,
                    article=article_obj,
                    content=comment,
                    to_whom=to_whom,
                    to_comment=to_comment_obj,
            )
            comment_obj.save()
            msg['status'] = True
        else:
            # 处理非子评论
            comment_obj_form = forms.CommentForm(request.POST)
            msg = {'field_errors':{},'status':False}
            if comment_obj_form.is_valid():
                comment_obj = models.Comment(
                    author = request.user,
                    article = article_obj,
                    content = comment,
                )
                comment_obj.save()
                msg['status'] = True
            else:
                error_msg = comment_obj_form.errors.get_json_data()
                msg['field_errors']['content'] = error_msg['comment'][0]['message']

        return HttpResponse(json.dumps(msg))


class SearchArticle(View):
    """处理文章搜索"""
    def get(self,request):
        sk = request.GET.get('sk')
        if sk:
           article_obj_list = models.Article.objects.filter(content__contains=sk)
        else:
            return HttpResponse('请输入搜索关键词')
        print(article_obj_list)
        return render(request,'search_article.html',{'article_obj_list':article_obj_list, 'sk':sk})


    def post(self,request):
        sk = request.POST.get('sk')
        if not sk:
            return HttpResponse('请输入搜索关键词')
        url = ''.join([request.path,'?sk=',sk])
        result = {'url':url}
        return HttpResponse(json.dumps(result))




def acc_logout(request):
    """注销"""
    logout(request)
    next = request.GET.get('next', '/tieba/login')
    return redirect(next)

def all_tieba(request):
    """返回现有的贴吧列表"""
    all_tieba_obj = models.TieBa.objects.all()
    return render(request,'all_tieba.html',{'all_tieba_obj':all_tieba_obj})
