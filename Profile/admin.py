from django.contrib import admin
from questions.models import Answer ,Question , QuestionRating,Report
from .models import Profile
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse

def Delete_post_and_ban_user(modeladmin,request,queryset):
    if not request.user.is_staff:
        raise PermissionDenied
    for obj in queryset:
        objques=Question.objects.get(id=obj.question.id)
        if objques.author.profile.ban==False:
           objques.author.profile.ban=True
           objques.author.profile.save()
        objques.delete()

    
@admin.register(Answer)
class Admin(admin.ModelAdmin):
    pass
@admin.register(Question)
class Admin(admin.ModelAdmin):
    pass

@admin.register(Profile)
class Admin(admin.ModelAdmin):
    pass

@admin.register(QuestionRating)
class Admin(admin.ModelAdmin):
    pass


@admin.register(Report)
class Admin(admin.ModelAdmin):
    actions = [Delete_post_and_ban_user]

