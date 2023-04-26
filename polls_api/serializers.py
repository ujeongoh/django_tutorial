from rest_framwork import serializers
from polls.models import Question # serialize 할 모델 가져오기


class QuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    question_text = serializers.CharField(max_length=200)
    pub_date = serializers.DateTimeField(read_only=True)

    # 유효성 검사를 통과한 데이터를 기반으로 저장
    def create(self, validated_data):
        return Question.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        # validated_data는 ordered dict 형태로 .get() 메소드를 사용할 수 있다
        instance.question_text = validated_data.get('question_text', instance.question_text)
        instance.save()
        return instance
