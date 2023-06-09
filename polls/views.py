from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.db.models import F
from .models import Question, Choice, Vote
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm

# Create your views here.


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # output = ', '.join([q.question_text for q in latest_question_list])
    # return HttpResponse(output)
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


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # choice 라는 name을 가진 tag의 value(choice_id)를 가져온다.
        selected_choice = question.choices.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {'question': question, 'error_message': f"선택이 없습니다. ID={request.POST['choice']}"})
    else:
        # 서버에서 연산을 하게 되면 사용자들이 동시에 투표했을 때 정확한 카운트를 하지 못할 수 있음
        # selected_choice.votes += 1

        # F 모듈을 활용하기 - F의 인자로 주어지는 컬럼 값에 대한 처리를 하게 해준다.
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        # 인자를 받아야하는 url경로이기 떄문에 arg파라미터로 인자를 넘겨줌
        return HttpResponseRedirect(reverse('polls:result', args=(question_id,)))


def result(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/result.html', {'question': question})


class SignupView(generic.CreateView):
    form_class = UserCreationForm
    # 사용자 생성 성공 후에는 user리스트 화면으로 이동시킨다
    # url.py에 정의했던 name을 기반으로 url을 만들어준다
    success_url = reverse_lazy('user-list')
    template_name = 'registration/signup.html'
