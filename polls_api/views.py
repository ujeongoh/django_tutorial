from polls.models import Question
from polls_api.serializers import *
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from .permissions import IsOwnerOrReadOnly


class QuestionList(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    # permission_classes 지정 시 login하지 않았을 경우 질문을 생성할 수 없다
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # perform_create를 오버라이드하여 데이터를 생성 시 owner가 현재 접속하고 있는 user로 설정되도록 한다.
    def perform_create(self, serializer):
        # owner 필드가 읽기 전용인데도 값을 지정하여 적용할 수 있는 이유는 save함수가 주어진 값을 그대로 저장하기 때문이다.
        serializer.save(owner=self.request.user)
    # def post() 가 ListCreateAPIView에 구현되어 있고, 이를 상속받았으므로 여기서도 사용가능하다

class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    # 상세화면에서도 login 하지 않았으면 질문 생성 못함. 또한 login했을 경우에도 본인이 작성한 것이 아니라면 수정하지 못하도록 해야함 --> 제공되는 permission class가 아니라 따로 permissions.py를 만들어주어야 한다.
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RegisterUser(generics.CreateAPIView):
    serializer_class = RegisterSerializer