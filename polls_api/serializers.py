from rest_framework import serializers
from polls.models import Question # serialize 할 모델 가져오기
from django.contrib.auth.models import User


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question # Meta 클래스 내부의 model 속성을 통해 Serialize할 대상 모델을 지정할 수 있습니다.
        fields = ['id', 'question_text', 'pub_date'] # Meta 클래스 내부의 fields 속성을 통해 Serialize할 대상 필드들을 리스트 형태로 나열하여 지정할 수 있습니다.

class UserSerializer(serializers.ModelSerializer):
    # User 의 id를 통해서 불러들일 수 있는 question들을 명시한다.
    questions = serializers.PrimaryKeyRelatedField(many=True, queryset=Question.objects.all())
    class Meta:
        model = User
        fields = ['id', 'username', 'questions']