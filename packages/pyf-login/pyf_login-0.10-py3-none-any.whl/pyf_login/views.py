from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from django.db import transaction
from .jwt_token import JwtToken
from .utils import MyJsonResponse, calculate_md5
from .models import User
from .serializers import AdminLoginSerializer
import logging


class AdminLoginView(GenericAPIView):
    """后台登录的视图类"""

    serializer_class = AdminLoginSerializer

    @transaction.atomic
    def post(self, request):
        """后台登录接口"""
        res = MyJsonResponse()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get("username")
        password = serializer.data.get("password")
        user = User.objects.filter(username=username).first()

        if not user:
            res.update(msg="User not found.", code=2)
            return Response(res.data, status=status.HTTP_404_NOT_FOUND)
        if not user.check_password(password):
            res.update(msg="Wrong password.", code=2)
            return Response(res.data, status=status.HTTP_400_BAD_REQUEST)
        payload = {"id": user.id, "username": username}
        logging.debug(payload)
        jwt_token = JwtToken().encode_user(payload)
        user.save()
        res.update(data={"token": jwt_token})
        return Response({"token": jwt_token}, status=status.HTTP_200_OK)
