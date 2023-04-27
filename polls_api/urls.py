from django.urls import path
from .views import *

# @api_view 데코레이터 사용
# urlpatterns = [
#     path('question/', question_list, name='question-list'),
#     path('question/<int:id>/', question_detail, name='question-detail')
# ]

# API_View 클래스 상속한 클래스 사용
urlpatterns = [
    path('question/', QuestionList.as_view(), name='question-list'),
    path('question/<int:id>/', QuestionDetail.as_view(), name='question-detail'),
]
