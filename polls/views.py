from django.shortcuts import render
from django.http import HttpResponse
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
    question = Question.objects.get(pk=question_id)
    context = {
        'question': question
    }
    #return HttpResponse(f'입력받은 질문id입니다 : {question_id}')
    return render(request, 'polls/detail.html', context)