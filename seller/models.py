from django.db import models
from account.models import User

# Model Manager


class SellerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.SELLER)


# The more fields to the user
class SellerDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Seller Details'
        verbose_name_plural = 'Seller Details'


# The proxy model for the user
class Seller(User):
    objects = SellerManager()

    @property
    def more(self):
        return self.SellerDetails

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = User.SELLER
        return super.save(*args, **kwargs)
