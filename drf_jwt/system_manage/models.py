from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.query_utils import Q
# Create your models here.

class AccessPermissionManager(models.Manager):
    def get_queryset(self):
        return super(AccessPermissionManager, self).\
            get_queryset().filter(
                Q(content_type=AccessPermission.PERMISSION_TYPE.READ) |
                Q(content_type=AccessPermission.PERMISSION_TYPE.WRITE)
            )


class AccessPermission(Permission):
    """Proxy model for permission"""

    class Meta:
        proxy = True

    class __PERMISSION_TYPE:
        def get_all_permissions(self):
                    """Get list of all permissions."""
                    return [
                        self.READ,
                        self.WRITE
                    ]

        @property
        def WRITE(self):
            return ContentType.objects.get_or_create(
                app_label='write',
                model="write_permission",
            )[0]

        @property
        def READ(self):
            return ContentType.objects.get_or_create(
            app_label='read',
            model='read_permission',
            )[0]

    PERMISSION_TYPE = __PERMISSION_TYPE()
    objects = AccessPermissionManager()
    
    def save(self, *args, **kwargs):
        # Check Permission Type.
        if self.content_type not in self.PERMISSION_TYPE.get_all_permissions():
            raise ValueError('Not permitted Permission Type.')
        
        # ct, created = ContentType.objects.get_or_create(
        #     model=self._meta.verbose_name, app_label=self._meta.app_label,
        # )

        #self.content_type = ct
        super(AccessPermission, self).save(*args)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
  
    class Meta:
        db_table='auth_profile'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
