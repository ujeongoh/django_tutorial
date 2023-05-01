from django.test import TestCase
from polls_api.serializers import QuestionSerializer, VoteSerializer
from django.contrib.auth.models import User
from polls.models import Question, Choice, Vote
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.utils import timezone


class QuestionListTest(APITestCase):
    def setUp(self):
        self.question_data = {'question_text': 'some question'}
        # url을 만들어준다. reverse_lazy 와 같은 동작을 한다.
        self.url = reverse('question-list')

    # 질문 생성기능 확인
    def test_create_question(self):
        # 먼저 User를 생성한다.
        user = User.objects.create(username='testuser', password='testpass')
        # APITestCase 를 상속받았기 때문에 강제로 로그인시키는 force_authenticate기능을 사용할 수 있다.
        self.client.force_authenticate(user=user)
        # 질문이 잘 생성되었는지 확인
        response = self.client.post(self.url, self.question_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 1)

        # 내용이 잘 저장되었는지 확인
        question = Question.objects.first()
        self.assertEqual(question.question_text,
                         self.question_data['question_text'])
        self.assertLess(
            (timezone.now() - question.pub_date).total_seconds(), 1)

    # 사용자가 로그인 되어있지 않을 때 질문생성되지 않는 것을 확인
    def test_create_question_without_authentication(self):
        response = self.client.post(self.url, self.question_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # 질문리스트 조회 확인
    def test_list_question(self):
        question = Question.objects.create(question_text='Question 1')
        choice = Choice.objects.create(
            question=question, choice_text='Question 1 - Choice 1')
        Question.objects.create(question_text='Question 2')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['choices']
                         [0]['choice_text'], choice.choice_text)


class VoteSerializerTest(TestCase):
    # 테스트 실행을 위한 데이터 생성한다. 테스트가 실행되기 전에 실행되는 메소드이다.
    # 각각 테스트는 독립적이고 테스트가 끝날 때마다 setUp을 다시 해준다.
    # 테스트마다 독립적으로 실행되면서 임시 DB에 데이터를 저장했다가 테스트를 마치면 테스트 데이터를 삭제한다.
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.question = Question.objects.create(
            question_text='abc',
            owner=self.user,
        )
        self.choice = Choice.objects.create(
            question=self.question,
            choice_text='1'
        )

    # 투표 기능 테스트
    def test_vote_serializer(self):
        data = {
            'question': self.question.id,
            'choice': self.choice.id,
            'voter': self.user.id
        }
        serializer = VoteSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        vote = serializer.save()

        self.assertEqual(vote.question, self.question)
        self.assertEqual(vote.choice, self.choice)
        self.assertEqual(vote.voter, self.user)

    # 이미 질문에 투표한 사용자가 또 투표했을 때 에러발생하는지 확인
    def test_vote_serializer_with_duplicate_vote(self):
        choice1 = Choice.objects.create(
            question=self.question,
            choice_text='2'
        )
        Vote.objects.create(question=self.question,
                            choice=self.choice, voter=self.user)

        data = {
            'question': self.question.id,
            'choice': self.choice.id,
            'voter': self.user.id
        }
        serializer = VoteSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    # 질문에 해당하지 않는 선택지를 골랐을 때 에러 발생하는지 확인
    def test_vote_serilaizer_with_unmatched_question_and_choice(self):
        question2 = Question.objects.create(
            question_text='abc',
            owner=self.user,
        )

        choice2 = Choice.objects.create(
            question=question2,
            choice_text='1'
        )
        data = {
            'question': self.question.id,
            'choice': choice2.id,
            'voter': self.user.id
        }
        serializer = VoteSerializer(data=data)
        self.assertFalse(serializer.is_valid())


class QuestionSerializerTestCase(TestCase):
    def test_with_valid_data(self):
        serializer = QuestionSerializer(data={'question_text': 'abc'})
        self.assertEqual(serializer.is_valid(), True)
        new_question = serializer.save()
        self.assertIsNotNone(new_question.id)

    def test_with_invalid_data(self):
        serializer = QuestionSerializer(data={'question_text': ''})
        self.assertEqual(serializer.is_valid(), False)
