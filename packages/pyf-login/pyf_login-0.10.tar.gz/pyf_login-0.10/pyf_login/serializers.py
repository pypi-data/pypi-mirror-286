from rest_framework import serializers
from .models import User
from rest_framework.serializers import ModelSerializer
from extensions.BaseSerializer import BaseModelSerializer


class UserViewsetSerializer(BaseModelSerializer, ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password_hash",  # 确保使用password_hash
            "created_at",
            "updated_at",
            "phone_number",
            "active",
            "email",
            "exten",
            "exten_pwd",
            "voip",
            "department",
            "can_create_free_order",
            "dingtalk_id",
            "taobao_access_code",
            "name",
            "workshop",
            "is_web_and_wx_customer_service",
            "dingtalk_open_id",
            "dingtalk_union_id",
            "homepage_url",
            "qiye_weixin_open_userid",
            "qiye_weixin_userid",
            "work_status",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class AdminLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=64, label="账号")
    password = serializers.CharField(required=True, max_length=64, label="密码")
