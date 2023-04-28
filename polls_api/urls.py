from django.urls import path, include
from .views import *

# @api_view 데코레이터 사용
# urlpatterns = [
#     path('question/', question_list, name='question-list'),
#     path('question/<int:id>/', question_detail, name='question-detail')
# ]

# API_View 클래스 상속한 클래스 사용
urlpatterns = [
    path('question/', QuestionList.as_view(), name='question-list'),
    path('question/<int:pk>/', QuestionDetail.as_view(), name='question-detail'),
    path('users/', UserList.as_view(), name='user-list'),
    path('users/<int:pk>', UserDetail.as_view(), name='user-detail'),
    path('register/', RegisterUser.as_view()),
    # rest_framework가 제공하는 로그인 기능을 사용하기 위함
    path('api-auth/', include('rest_framework.urls')),
]
