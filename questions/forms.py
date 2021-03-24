from django import forms
from django.contrib.auth.models import User
from .models import Question,Answer,QuestionRating

class QuestionForm(forms.ModelForm):
    email=forms.EmailField()
    first_name=forms.CharField(label='First Name')
    last_name=forms.CharField(label='last Name',required=False)
    subject=forms.CharField(label='Subject')
    image_post=forms.ImageField(label='image',required=False)
    class Meta:
        model=Question
        fields =['title','author','content','subject','Date','image_post']

class AnswerForm(forms.ModelForm):
    image_post=forms.ImageField(label='image',required=False)

    class Meta:
        model=Answer
        fields =['body','image_post']

RATING_CHOICES= (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
)
class RateForm(forms.ModelForm):
    rate=forms.ChoiceField(choices=RATING_CHOICES)

    class Meta:
        model=QuestionRating
        fields =['rate']