from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User 
from django.urls import reverse

SUBJECT_CHOICES= (
    ("M1", "M1"),
    ("M2", "M2"),
    ("M3", "M3"),
    ("MEOW", "MEOW"),
    ("Gen Chem", "Gen Chem"),
    ("EG", "EG"),
    ("ES", "ES"),
    ("PnS", "PnS"),
    ('General','General')
)
RATING_CHOICES= (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5)
)
class Question(models.Model):
    title=models.CharField(max_length=200)
    image_post =models.ImageField(null= True, blank = True,upload_to='images/')
    content=models.TextField()
    Date=models.DateTimeField(default=timezone.now)
    author=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='author')
    subject=models.CharField(max_length = 20,choices = SUBJECT_CHOICES,default='General')
    rating=models.DecimalField(default=0,decimal_places=2,max_digits=3)
    class Meta:
        ordering = ['-rating']


    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('question',kwargs={'pk':self.pk})

class QuestionRating(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.IntegerField(choices= RATING_CHOICES,default=1)

    def __str__(self):
        return self.question.title or ' '

class Answer(models.Model):
    question=models.ForeignKey(Question,related_name='answer', on_delete=models.CASCADE,verbose_name='post')
    user=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='answered_by')
    body=models.TextField()
    image_post =models.ImageField(null= True, blank = True,upload_to='images/')
    like =models.ManyToManyField(User,related_name='like',blank=True,verbose_name='liked_by')
    dislike =models.ManyToManyField(User,related_name='dislike',blank=True,verbose_name='disliked_by')
    date_added=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return '%s - %s' % (self.question.title, self.question.pk)

    class Meta:
        ordering = ['-date_added']

class Report(models.Model):
    question=models.OneToOneField(Question,on_delete=models.CASCADE, related_name='question')
    count=models.IntegerField(default=0)
    def __str__(self):
        return '%s - %s' % (self.question.title, self.question.pk   )