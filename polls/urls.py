from django.urls import path
from . import views
from views import *
# 앱 이름 설정 - html파일에서 name으로 url을 접근할 때 이제 앞에 'polls:'도 붙여줘야 함
app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>', views.detail, name='detail'),
    path('<int:question_id>/result', views.result, name='result'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('signup', SignupView.as_view()),
]
