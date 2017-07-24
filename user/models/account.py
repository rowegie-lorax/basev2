from django.db import models
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE
from .user import User


class Account(models.Model):
    _safedelete_policy = SOFT_DELETE_CASCADE

    name = models.CharField(max_length=100)
    user = models.OneToOneField(User)
    # metadata = JSONField(load_kwargs={'object_pairs_hook': collections.OrderedDict})
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + ' - ' + self.create_at.strftime('%Y-%m-%d %H:%M:%S')
