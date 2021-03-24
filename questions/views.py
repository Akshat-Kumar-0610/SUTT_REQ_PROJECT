from .models import Question,Answer,QuestionRating,Report
from django.views.generic import ListView ,DetailView,CreateView,UpdateView,DeleteView
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.models import User
from .forms import QuestionForm,AnswerForm
from django.urls import reverse_lazy ,reverse,resolve
from django.http import HttpResponseRedirect,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.db.models import Count

class MySocialAccount(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        u = sociallogin.user
        if not u.email.split('@')[1] == "pilani.bits-pilani.ac.in":
            raise ImmediateHttpResponse(render(request,'questions/error.html'))


class Home(ListView):
    model=Question
    context_object_name='question'
    template_name='questions/home.html'
    order=['-Date']

def about(request):
    return render(request,'questions/about.html',{'title':'about'})  

class QuestionDetailView(LoginRequiredMixin,DetailView):        
    model=Question
    order=['']
    def get_context_data(self, **kwargs):
        ans=Answer.objects.filter(question_id=self.kwargs['pk']).annotate(lcount=Count('like')).order_by('-lcount')
        context = super().get_context_data(**kwargs)
        context['answer']=ans
        return context
    
class QuestionCreateView(LoginRequiredMixin,CreateView):      
    model=Question
    fields=['title','content','subject','image_post']
    template_name='questions/question_form.html'
    def form_valid(self, form ):
        form.instance.author=self.request.user       
        return super().form_valid(form)

class QuestionUpdateView(UserPassesTestMixin,LoginRequiredMixin,UpdateView):  
    model=Question
    fields=['title','content','subject']
    def form_valid(self, form ):
        form.instance.author=self.request.user     
        return super().form_valid(form)
    def test_func(self):
        question=self.get_object()
        if self.request.user==question.author:          
            return True
        return False

class QuestionDeleteView(UserPassesTestMixin,LoginRequiredMixin,DeleteView):   
    model= Question
    def test_func(self):
        question=self.get_object()
        if self.request.user==question.author:           
            return True
        return False
    success_url='/'

class AnswerCreateView(LoginRequiredMixin,CreateView):       
    model=Answer
    fields=['body','image_post']
    template_name='questions/answer.html'
    def form_valid(self, form ,*args,**kwargs):
        form.instance.question_id=self.kwargs['pk']               
        form.instance.user=self.request.user                 
        return super().form_valid(form)
    def get_success_url(self,**kwargs):
        return reverse('question', args=[str(self.kwargs['pk'])])
        
class QuestionRate(LoginRequiredMixin,CreateView):
    model=QuestionRating
    fields=['rate']
    template_name='questions/questionrate.html'
    def form_valid(self, form ,*args,**kwargs):
        rating= QuestionRating.objects.filter(question_id=self.kwargs['pk'])
        rating_user=[]
        for ques in rating:
            rating_user.append(ques.user.username)
        if self.request.user.username not in rating_user:
            form.instance.question_id=self.kwargs['pk']
            form.instance.user=self.request.user 
            ques=Question.objects.get(id=self.kwargs['pk'])
            r_s=form.instance.rate
            nu=len(rating_user)+1
            for ques in rating:
                r_s+=ques.rate
            if nu==0:
                ratingf=0
            else:
                ratingf=float(r_s/nu)
            Question.objects.filter(id=self.kwargs['pk']).update(rating=ratingf)
            return super().form_valid(form)
        else:
            messages.error(self.request, f'You have already rated and can not rate once again')
            return HttpResponseRedirect(reverse('question', args=[str(self.kwargs['pk'])]))
    def get_success_url(self,**kwargs):
        return reverse('question', args=[str(self.kwargs['pk'])])

@login_required           
def like_view(request,pk):
    question2=get_object_or_404(Answer, pk=pk)                                     
    url_name = resolve(request.path).url_name
    ques=question2.question.pk
    if request.user in question2.dislike.all():
        print(pk)
        question2.like.add(request.user)
        question2.dislike.remove(request.user)
        return HttpResponseRedirect(reverse('question', args=[str(question2.question.pk)]))       
    else:
        
        question2.like.add(request.user)
        return HttpResponseRedirect(reverse('question', args=[str(question2.question.pk)]))       

@login_required             
def unlike_view(request,pk):
    question2=get_object_or_404(Answer, pk=pk)                                  
    question2.like.remove(request.user)
    return HttpResponseRedirect(reverse('question', args=[str(question2.question.pk)]))    

@login_required             
def dislike_view(request,pk):
    question2=get_object_or_404(Answer, pk=pk)                                 
    if request.user in question2.like.all():
        question2.dislike.add(request.user)
        question2.like.remove(request.user)
        return HttpResponseRedirect(reverse('question', args=[str(question2.question.pk)]))       
    else:
        question2.dislike.add(request.user)
        return HttpResponseRedirect(reverse('question', args=[str(question2.question.pk)]))
@login_required           
def undislike_view(request,pk):
    question2=get_object_or_404(Answer, pk=pk)
    question2.dislike.remove(request.user)
    return HttpResponseRedirect(reverse('question', args=[str(question2.question.pk)]))

@login_required          
def report(request,pk):
    question=get_object_or_404(Question, pk=pk)
    reports=[report for report in Report.objects.all()]
    if not reports:
            Report.objects.create(question=question,count=1)
            return HttpResponseRedirect(reverse('question', args=[str(question.pk)]))  
    else:
        for report in reports:
            if report.question.title==question.title:
                report.count+=1
                report.save()
                return HttpResponseRedirect(reverse('question', args=[str(question.pk)]))      
        else:
            Report.objects.create(question=question,count=1)
            return HttpResponseRedirect(reverse('question', args=[str(question.pk)]))    
     