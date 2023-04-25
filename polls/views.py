from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import *

# Create your views here.
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    #output = ', '.join([q.question_text for q in latest_question_list])
    #return HttpResponse(output)
    context = {
        # template에서 'first_question'으로 해당 값에 접근할 수 있다.
        'questions': latest_question_list,
        'first_question': latest_question_list[0]
    }
    
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    # 주어진 question_id를 가진 Question이 없을 경우 예외처리

    # 1. try~except 로 예외처리
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist!")

    # 2. get_object_or_404 메소드로 예외처리
    question = get_object_or_404(Question, pk=question_id)
    context = {
        'question': question
    }
    
    return render(request, 'polls/detail.html', context)