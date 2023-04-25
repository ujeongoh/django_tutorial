from django.contrib import admin
from .models import *

#Register your models here
#admin.site.register(Question)
admin.site.register(Choice)

# CRUD : Create Read Update Delete

# 커스터마이징
#class ChoiceInline(admin.StackedInline): # 수직정렬
class ChoiceInline(admin.TabularInline): # 수평정렬
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('질문 섹션', {'fields': ['question_text']}),
        ('생성일', {'fields': ['pub_date'], 'classes': ['hidden']}),
    ]
    readonly_fields = ['pub_date'] # 읽기 전용 처리
    inlines = [ChoiceInline] # Choice를 생성할 때 같이 만들 수 있도록 함

admin.site.register(Question, QuestionAdmin)
