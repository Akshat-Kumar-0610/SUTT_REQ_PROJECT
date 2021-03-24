from django.shortcuts import render
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import ProfileUpdateForm,UserUpdateForm
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .models import Profile
from questions.models import Question, Answer
from django.views.generic import ListView, DetailView,UpdateView


class MySocialAccount(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        u = sociallogin.account.user
        if  u.email.split('@')[1] != "pilani.bits-pilani.ac.in":
            raise ImmediateHttpResponse(render('error.html'))

'''class ProfileDetailView(ListView):          
    model=Profile
    template_name='Profile/details.html'
    context_object_name = 'question'
    paginate_by =  5
    
    def get_queryset(self):
        user=get_object_or_404(User, id=self.kwargs.get('pk'))
        self.questions=Question.objects.filter(author=user).order_by('-Date')
        return Question.objects.filter(author=user).order_by('-Date')

    def get_context_data(self, **kwargs):
        
        view_profile=Profile.objects.get(user__id=self.kwargs.get('pk'))       
        context={'question':self.questions,'profile_v':view_profile}
        return context'''
class ProfileDetailView(DetailView):
    model=Profile
    template_name = 'Profile/details.html'
    paginate_by = 5
    def get_context_data(self, **kwargs):
        question = Question.objects.filter(author__id=self.kwargs.get('pk'))
        context = super().get_context_data(**kwargs)
        context['question']=question
        return context
        
@login_required
def profile_edit(request):
    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user) 
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        #print('POST',request.POST,'FILE',request.FILES,'USER',request.user,request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')   
            return redirect('home')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'Profile/profile_update.html',context)
