from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import path, include
from questions.views import Home,about
from django.contrib.auth.views import LogoutView
from questions.views import (
    QuestionCreateView,
    QuestionUpdateView,
    QuestionDeleteView,
    AnswerCreateView,
    QuestionDetailView,
    QuestionRate,
    like_view,
    dislike_view,
    unlike_view,
    undislike_view,
    report
)
from Profile.views import (
    ProfileDetailView,
    profile_edit
)
urlpatterns = [
    path('admin/', admin.site.urls),                                                                                                                                                        
    path('', Home.as_view() ,name='home'),
    path('about/', about ,name='about'),
    path('accounts/', include('allauth.urls')),
    path('logout', LogoutView.as_view(),name='logout'),
    path('profileedit/', profile_edit, name='profile_edit'),                                                                                                                                  
    path('question/<pk>/', QuestionDetailView.as_view(), name='question'),                                                                                                                             
    path('create/', QuestionCreateView.as_view(), name='question_create'),                                                                                                                             
    path('question/<pk>/update/', QuestionUpdateView.as_view(), name='question_update'),                                                                                                               
    path('question/<pk>/delete/', QuestionDeleteView.as_view(), name='question_delete'),                                                                                                               
                                                                                                                        
    path('question/<int:pk>/answer/',AnswerCreateView.as_view(), name='answer_create'),
    path('userprofile/<pk>/', ProfileDetailView.as_view(), name='profile-detail'),  
    path('question/<pk>/rate/', QuestionRate.as_view(), name='question_rate'),         
    path('question/<pk>/answer/', AnswerCreateView.as_view(), name='answer'), 
    path('report/<pk>',report ,name='report'),    
    path('like/<pk>', like_view, name='like_post'),                                                                                                                           
    path('dislike/<pk>', dislike_view, name='dislike_post'),                                                                                                                   
    path('unlike/<pk>', unlike_view, name='unlike_post'),                                                                                                                       
    path('undislike/<pk>', undislike_view, name='undislike_post'),                                          

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


