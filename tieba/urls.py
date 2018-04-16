from django.urls import path
from django.conf.urls import url
from tieba import views
from django.conf import  settings
from django.conf.urls.static import static

urlpatterns = [
    path('index/',views.IndexView.as_view(),name='index'),
    path('f',views.FView.as_view(),name='tieba'),
    url(r'p/(?P<article_id>\d+)+', views.ArticleView.as_view(),name='article'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('registration/', views.Registration.as_view(), name='registration'),
    path('logout/', views.acc_logout, name='logout'),
    path('follow/', views.FollowView.as_view(), name='follow'),
    url(r'home/main/', views.HomeMainView.as_view(), name='home_main'),
    path('profile/', views.EditProfile.as_view(), name='edit_profile'),
    path('profile/portrait/', views.Portrait.as_view(), name='portrait'),
    path('comment/', views.Comment.as_view(), name='comment')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)