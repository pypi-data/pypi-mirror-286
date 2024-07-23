from django.db import models
from .utils import calculate_md5
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set")
        user = self.model(username=username, **extra_fields)
        if password:
            user.set_password(password)  # 使用set_password方法
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser):
    username = models.CharField(max_length=191, unique=True)
    password_hash = models.CharField(max_length=191, blank=True, null=True)
    phone_number = models.CharField(max_length=191, blank=True, null=True)
    active = models.BooleanField(default=True)
    exten = models.CharField(max_length=191, blank=True, null=True)
    exten_pwd = models.CharField(max_length=191, blank=True, null=True)
    voip = models.BooleanField(default=False)
    department = models.CharField(max_length=255, blank=True, null=True)
    can_create_free_order = models.BooleanField(default=False)
    dingtalk_id = models.CharField(max_length=191, blank=True, null=True)
    taobao_access_code = models.CharField(max_length=191, blank=True, null=True)
    workshop = models.CharField(max_length=191, blank=True, null=True)
    is_web_and_wx_customer_service = models.BooleanField(default=False)
    dingtalk_open_id = models.CharField(max_length=50, blank=True, null=True)
    dingtalk_union_id = models.CharField(max_length=50, blank=True, null=True)
    homepage_url = models.URLField(max_length=255, blank=True, null=True)
    qiye_weixin_open_userid = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="企业微信open_userid"
    )
    qiye_weixin_userid = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="企业微信userid"
    )
    work_status = models.CharField(max_length=255, default="下班")

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = "users"
        ordering = ["id"]

    def set_password(self, raw_password):
        self.password_hash = calculate_md5(self.username, raw_password)

    def check_password(self, raw_password):
        return self.password_hash == calculate_md5(self.username, raw_password)
