# Create your views here.
# from .serializers import MyTokenObtainPairSerializer
# from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.decorators import api_view, permission_classes
from . import models, serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, IsAdminUser


# class MyObtainTokenPairView(TokenObtainPairView):
#     permission_classes = (AllowAny,)
#     serializer_class = MyTokenObtainPairSerializer

# class RegisterView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     permission_classes = (AllowAny,)
#     serializer_class = UserSerializer


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """

    serializer_class = serializers.ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Password updated successfully",
                "data": [],
            }
            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated, IsAdminUser])
def userGETPOST(request):
    if request.method == "GET":
        vendeur = models.CustomUser.objects.all()
        if not request.user.is_superuser:
            vendeur = models.CustomUser.objects.filter(
                selling_point=request.user.vendeur.selling_point
            )
        serializer = serializers.UserSerializer(vendeur, many=True)
        return Response(serializer.data)
    if request.method == "POST":
        serializer = serializers.UserSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserGetPost(generics.ListCreateAPIView):
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAdminUser]


class UserPk(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]
    def destroy(self, request, *args, **kwargs):
        """
        Mock delete: do not actually remove the user.
        """
        instance = self.get_object()
        data = self.get_serializer(instance).data
        return Response(
            {
                "status": "mock_delete",
                "message": "Delete is disabled. User was not removed.",
                "user": data,
            },
            status=status.HTTP_200_OK,
        )


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated, IsAdminUser])
def userPk(request, pk):
    try:
        user = models.CustomUser.objects.get(id=pk)

    except models.CustomUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serializer = serializers.UserSerializer(user)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = serializers.UserSerializer(
            user, data=request.data, context={"request": request}, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
