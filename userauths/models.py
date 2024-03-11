from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
from django.db.models.signals import post_save
from shortuuid.django_fields import ShortUUIDField
from django.utils.text import slugify
import shortuuid

GENDER = (
    ("male", "male"),
    ("female", "female")
)

STATUS = (
    ("active", "Active"),
    ("closed", "Closed"),
    ("blacklisted", "Blacklisted"),
    ("disabled", "Disabled"),
)


# Create your models here.


def user_directory_path(instance, filename):
    extension = filename.split(".")[-1]
    filename = "%s.%s" % (instance.user.id, extension),
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class User(AbstractUser):
    full_name = models.CharField(max_length=200, null=True, blank=True)
    username = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    gender = models.CharField(max_length=100, choices=GENDER, default='male', null=True, blank=True)
    otp = models.CharField(max_length=10, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return str(self.username)


class Profile(models.Model):
    pid = ShortUUIDField(length=8, max_length=25, alphabet="abcdefjhigklmnopqrstuvwxyz123")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cover_image = models.ImageField(upload_to=user_directory_path, default="cover.jpg", blank=True, null=True)
    image = models.ImageField(upload_to=user_directory_path, default="default.jpg", blank=True, null=True)
    full_name = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    gender = models.CharField(max_length=100, choices=GENDER, default='male', null=True, blank=True)
    status = models.CharField(max_length=100, choices=STATUS, default='active')
    bio = models.TextField(max_length=500, null=True, blank=True)
    about_me = models.TextField(max_length=500, null=True, blank=True)

    country = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)

    working_at = models.CharField(max_length=200, blank=True, null=True)

    instagram = models.CharField(max_length=200, null=True, blank=True)
    facebook = models.CharField(max_length=200, null=True, blank=True)

    verified = models.BooleanField(default=False, blank=True, null=True)

    date = models.DateTimeField(auto_now_add=True)

    slug = models.SlugField(unique=True, null=True, blank=True)

    def __str__(self):
        if self.full_name:
            return str(self.full_name)
        else:
            return str(self.user.username)

    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug is None:
            uuid_key = shortuuid.uuid()
            uniqueid = uuid_key[:2]
            self.slug = slugify(self.full_name) + "-" + str(uniqueid.lower())

        super(Profile, self).save(*args, **kwargs)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)

# class Profile(models.Model):
#     pid = ShortUUIDField(length=8, max_length=30, alphabet="abcdefjhigklmnopqrstuvwxyz0123456789")
#     user = models.OneToOneField(User, on_delete=models.CASCADE, )
#     background_image = models.ImageField(upload_to='user_directory_path', default="cover.jpg")
#     profile_image = models.ImageField(upload_to='user_directory_path', default="default.jpg")
#     full_name = models.CharField(max_length=200, null=True, blank=True)
#     bio = models.TextField(blank=True, null=True, max_length=500)
#     phone_number = models.CharField(max_length=50, null=True, blank=True)
#     gender = models.CharField(max_length=100, choices=GENDER, default="male")
#     about_me = models.TextField(blank=True, null=True, max_length=500)
#     status = models.CharField(max_length=100, choices=STATUS, default="active")
#
#     country = models.CharField(max_length=200, null=True, blank=True)
#     state = models.CharField(max_length=200, null=True, blank=True)
#     city = models.CharField(max_length=200, null=True, blank=True)
#     address = models.CharField(max_length=200, null=True, blank=True)
#
#     # studies_at = models.CharField(max_length=200)
#
#     instagram = models.CharField(max_length=200, null=True, blank=True)
#     facebook = models.CharField(max_length=200, null=True, blank=True)
#     linkedin = models.CharField(max_length=200, null=True, blank=True)
#     twitter = models.CharField(max_length=200, null=True, blank=True)
#
#     verified = models.BooleanField(default=False)
#     date = models.DateTimeField(auto_now_add=True)
#
#     # followers = models.ManyToManyField(User, blank=True, related_name='followers')
#     # following = models.ManyToManyField(User, blank=True, related_name='following')
#     # friends = models.ManyToManyField(User, blank=True, related_name="blocked")
#
#
#
#
#     def __str__(self):
#         return self.user.username
