from rest_framework import serializers
from polls.models import Question # serialize 할 모델 가져오기
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class QuestionSerializer(serializers.ModelSerializer):
    # 읽기전용으로 만들기 위해 따로 만들어준다.
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Question # Meta 클래스 내부의 model 속성을 통해 Serialize할 대상 모델을 지정할 수 있습니다.
        fields = ['id', 'question_text', 'pub_date', 'owner'] # Meta 클래스 내부의 fields 속성을 통해 Serialize할 대상 필드들을 리스트 형태로 나열하여 지정할 수 있습니다.

class UserSerializer(serializers.ModelSerializer):
    # User 의 id를 통해서 불러들일 수 있는 question들을 명시한다.
    questions = serializers.PrimaryKeyRelatedField(many=True, queryset=Question.objects.all())
    class Meta:
        model = User
        fields = ['id', 'username', 'questions']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    # custom validate
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': '두 패스워드가 일치하지 않습니다.'})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()  
        return user  
    class Meta:
        model = User
        fields = ['username', 'password', 'password2']
        extra_kwargs = {'password':{'write_only':True}} 