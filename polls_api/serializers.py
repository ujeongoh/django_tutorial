from rest_framework import serializers
from polls.models import Question, Choice, Vote  # serialize 할 모델 가져오기
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class VoteSerializer(serializers.ModelSerializer):
    voter = serializers.ReadOnlyField(source='voter.username')

    class Meta:
        model = Vote
        fields = ['id', 'question', 'choice', 'voter']


class ChoiceSerializer(serializers.ModelSerializer):
    votes_count = serializers.SerializerMethodField()

    class Meta:
        model = Choice
        fields = ['choice_text', 'votes_count']

    def get_votes_count(self, obj):
        return obj.vote_set.count()


class QuestionSerializer(serializers.ModelSerializer):
    # 새로운 질문이 생성될 때 owner 필드에 현재 요청을 보낸 사용자를 자동으로 할당
    owner = serializers.ReadOnlyField(source='owner.username')
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        # Meta 클래스 내부의 model 속성을 통해 Serialize할 대상 모델을 지정할 수 있다.
        model = Question
        # Meta 클래스 내부의 fields 속성을 통해 Serialize할 대상 필드들을 리스트 형태로 나열하여 지정할 수 있다.
        fields = ['id', 'question_text', 'pub_date', 'owner', 'choices']


class UserSerializer(serializers.ModelSerializer):
    # User 의 id를 통해서 불러들일 수 있는 question들을 명시한다.
    # questions = serializers.StringRelatedField(many=True, read_only=True)
    # questions = serializers.PrimaryKeyRelatedField(many=True, queryset=Question.objects.all())
    # questions = serializers.SlugRelatedField(many=True, read_only=True, slug_field='pub_date')
    questions = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name='question-detail')

    class Meta:
        model = User
        fields = ['id', 'username', 'questions']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    # custom validate
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {'password': '두 패스워드가 일치하지 않습니다.'})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ['username', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}
