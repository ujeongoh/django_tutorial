from django.test import TestCase
from polls_api.serializers import QuestionSerializer, VoteSerializer
from django.contrib.auth.models import User
from polls.models import Question, Choice, Vote


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
