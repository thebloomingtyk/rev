from django.db import models
from account.models import User

# Model Manager


class BuyerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.BUYER)


# The more fields to the user
class BuyerDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Buyer Details'


# The proxy model for the user
class Buyer(User):
    objects = BuyerManager()

    @property
    def more(self):
        return self.BuyerDetails

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = User.BUYER
        return super.save(*args, **kwargs)
