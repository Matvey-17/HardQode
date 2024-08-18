from django.contrib.auth import get_user_model
from rest_framework import permissions, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response

from api.v1.serializers.user_serializer import CustomUserSerializer, BalanceSerializer, BalanceAdminSerializer
from users.models import Balance

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    http_method_names = ["get", "head", "options"]
    permission_classes = (permissions.IsAdminUser,)


class BalanceViewSet(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request):
        serializer = BalanceAdminSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        balance = Balance.objects.all().select_related('user')
        serializer = BalanceSerializer(balance, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if pk is None:
            return Response({'error': 'Метод PUT не разрешен'})

        try:
            instance = Balance.objects.get(pk=pk)
        except:
            return Response({'error': 'Данного баланса не существует'})

        serializer = BalanceAdminSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class BalanceUserView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        balance = Balance.objects.filter(user=request.user).select_related('user')
        serializer = BalanceSerializer(balance, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
