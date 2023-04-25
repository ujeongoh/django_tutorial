from django.contrib import admin
from .models import *

#Register your models here
#admin.site.register(Question)
#admin.site.register(Choice)

# CRUD : Create Read Update Delete

# 커스터마이징
#class ChoiceInline(admin.StackedInline): # 수직정렬
class ChoiceInline(admin.TabularInline): # 수평정렬
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('질문 섹션', {'fields': ['question_text']}),
        #('생성일', {'fields': ['pub_date']}),
        ('생성일', {'fields': ['pub_date'], 'classes': ['hidden']}), # 'classes' 를 지정하면 hidden, collapsed 옵션으로 숨김처리 할 수 있음
    ]
    # 표시하고 싶은 필드를 나열한다
    list_display = ['question_text', 'pub_date', 'was_published_recently']
    readonly_fields = ['pub_date'] # 읽기 전용 처리
    inlines = [ChoiceInline] # Choice를 생성할 때 같이 만들 수 있도록 함
    list_filter = ['pub_date'] # 필드의 타입을 보고 자동으로 그에 맞는 필터를 제공함
    search_fields = ['question_text', 'choice__choice_text'] # 필드값을 검색하는 검색창을 생성 - choice 객체의 필드에 접근을 위해서는 'choice__choice_text' 와 같이 접근한다

admin.site.register(Question, QuestionAdmin)
