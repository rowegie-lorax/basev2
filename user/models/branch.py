from django.db import models
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE

from .account import Account


class Branch(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    name = models.CharField(max_length=100)
    account = models.ForeignKey(Account, null=True)
    branch_alias = models.CharField(max_length=100, blank=True, null=True)
    location = models.TextField()
    phone = models.CharField(max_length=20, blank=True,
                             null=True, default=None)
    create_at = models.DateTimeField(auto_now_add=True, null=True)
    update_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-create_at',)
        unique_together = (('name', 'account'),)
