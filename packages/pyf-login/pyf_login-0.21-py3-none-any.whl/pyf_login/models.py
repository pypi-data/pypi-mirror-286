from django.db import models
from .utils import calculate_md5


class User(models.Model):
    username = models.CharField(max_length=191, blank=True, null=True, unique=True)
    password_hash = models.CharField(max_length=191, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    phone_number = models.CharField(max_length=191, blank=True, null=True)
    active = models.BooleanField(default=None, null=True, blank=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    exten = models.CharField(max_length=191, blank=True, null=True)
    exten_pwd = models.CharField(max_length=191, blank=True, null=True)
    voip = models.BooleanField(default=False)
    department = models.CharField(max_length=255, blank=True, null=True)
    can_create_free_order = models.BooleanField(default=False)
    dingtalk_id = models.CharField(max_length=191, blank=True, null=True)
    taobao_access_code = models.CharField(max_length=191, blank=True, null=True)
    name = models.CharField(max_length=191, blank=True, null=True)
    workshop = models.CharField(max_length=191, blank=True, null=True)
    is_web_and_wx_customer_service = models.BooleanField(
        default=None, null=True, blank=True
    )
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

    class Meta:
        db_table = "users"
        ordering = ["id"]

    def set_password(self, raw_password):
        self.password_hash = calculate_md5(self.username, raw_password)

    def check_password(self, raw_password):
        return self.password_hash == calculate_md5(self.username, raw_password)

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True
