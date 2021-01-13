from django.contrib.auth import login, logout
from rest_framework import views, generics, permissions, status
from user.serializers import LoginSerializer, UserSerializer, \
                             UserUpdateSerializer, PasswordChangeSerializer
from rest_framework.response import Response


class LoginView(views.APIView):
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(UserSerializer(user).data)


class LogoutView(views.APIView):
    def post(self, request):
        logout(request)
        data = {'success': '성공적으로 로그아웃 되었습니다.'}
        return Response(data=data, status=status.HTTP_200_OK)


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)


class UserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserUpdateSerializer

    def get_object(self):
        return self.request.user


class PasswordChangeView(generics.UpdateAPIView):
    serializer_class = PasswordChangeSerializer

    def get_object(self):
        return self.request.user

    def update(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.change_password(
            self.get_object(),
            request.data['current_password'],
            request.data['new_password']
        )
        data = {'success': '비밀번호가 성공적으로 변경되었습니다.'}
        return Response(data=data, status=status.HTTP_200_OK)
