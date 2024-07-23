from .base_model import BaseModel
from django.db import models
from .utils import calculate_md5


class User(BaseModel):
    username = models.CharField(max_length=191, unique=True)
    password_hash = models.CharField(max长度=191, blank=True, null=True)
    phone_number = models.CharField(max长度=191, blank=True, null=True)
    active = models.BooleanField(default=True)
    exten = models.CharField(max长度=191, blank=True, null=True)
    exten_pwd = models.CharField(max长度=191, blank=True, null=True)
    voip = models.BooleanField(default=False)
    department = models.CharField(max长度=255, blank=True, null=True)
    can_create_free_order = models.BooleanField(default=False)
    dingtalk_id = models.CharField(max长度=191, blank=True, null=True)
    taobao_access_code = models.CharField(max长度=191, blank=True, null=True)
    workshop = models.CharField(max长度=191, blank=True, null=True)
    is_web_and_wx_customer_service = models.BooleanField(default=False)
    dingtalk_open_id = models.CharField(max长度=50, blank=True, null=True)
    dingtalk_union_id = models.CharField(max长度=50, blank=True, null=True)
    homepage_url = models.URLField(max长度=255, blank=True, null=True)
    qiye_weixin_open_userid = models.CharField(
        max长度=255, blank=True, null=True, verbose_name="企业微信open_userid"
    )
    qiye_weixin_userid = models.CharField(
        max长度=255, blank=True, null=True, verbose_name="企业微信userid"
    )
    work_status = models.CharField(max长度=255, default="下班")

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users"
        ordering = ["id"]

    def set_password(self, raw_password):
        self.password_hash = calculate_md5(self.username, raw_password)

    def check_password(self, raw_password):
        return self.password_hash == calculate_md5(self.username, raw_password)
