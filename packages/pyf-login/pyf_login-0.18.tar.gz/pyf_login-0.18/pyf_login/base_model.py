from django.db import models


class BaseModel(models.Model):
    id = models.AutoField(primary_key=True, help_text="主键，自增的整数")  # 主键ID
    created_at = models.DateTimeField(null=True, blank=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name="更新时间")

    class Meta:
        abstract = True
