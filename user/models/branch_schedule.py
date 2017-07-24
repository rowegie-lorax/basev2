from django.db import models
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE

from .branch import Branch


class BranchSchedule(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    day = models.CharField(max_length=10)
    status = models.CharField(max_length=10)
    start = models.TimeField()
    end = models.TimeField()
    date = models.DateTimeField(null=True, blank=True)
    branch = models.ForeignKey(Branch, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s %s %s to %s %s' % (
                str(self.date), self.day,
                str(self.start), str(self.end), self.status)
