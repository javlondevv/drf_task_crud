from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer

from .models import Task, CustomUser
from .serializers import TaskSerializer
from .serializers import UserRegistrationSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .serializers import UserLoginSerializer


class UserLoginAPIView(APIView):
    @swagger_auto_schema(
        request_body=UserLoginSerializer,
        operation_description="User Login",
        responses={status.HTTP_200_OK: 'Login successful', status.HTTP_400_BAD_REQUEST: 'Invalid credentials'}
    )
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']

            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserMe(APIView):
    serializer_class = UserRegistrationSerializer

    def get(self, request, format=None):
        if request.user.is_authenticated:
            user = CustomUser.objects.get(id=request.user.id)
            serializer = self.serializer_class(user)
            return Response(serializer.data)
        else:
            return Response({'message': 'User is not authenticated'}, status=401)


class UserRegistrationAPIView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    parser_classes = (FormParser, MultiPartParser)
    permission_classes = (AllowAny,)
    renderer_classes = [JSONRenderer]


class TaskListCreateView(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    parser_classes = MultiPartParser, FormParser


class TaskDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    parser_classes = MultiPartParser, FormParser
