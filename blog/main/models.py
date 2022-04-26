from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db.models import PROTECT, TextField, ForeignKey, CASCADE, DateTimeField
from django.db.models.signals import post_save
from django.urls import reverse
from django.dispatch import receiver
from unidecode import unidecode
from django.db import models
from django.utils.text import slugify


class UserManager(BaseUserManager):
    def _create_user(self, username, slug, password, **extra_fields):
        if not username:
            raise ValueError('Неверный логин')
        user = self.model(username=username, slug=slug, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, slug, password, **extra_fields):
        extra_fields['is_staff'] = False
        extra_fields['is_superuser'] = False
        return self._create_user(username, slug, password, **extra_fields)

    def create_superuser(self, username, slug, password,**extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        return self._create_user(username, slug, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        'Username',
        max_length=20,
        db_index=True,
        unique=True
    )
    slug = models.SlugField(
        'Slug',
        max_length=25,
        blank=True,
        null=True
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['slug']

    objects = UserManager()

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('main:user', kwargs={'user_slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(str(self.username)))
        return super().save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    email = models.EmailField(
        'Email',
        max_length=50,
        unique=True,
        blank=True,
        null=True
    )
    b_date = models.DateField(
        'Birthday',
        blank=True,
        null=True,
    )
    user_from = models.CharField(
        'User from',
        max_length=50,
        blank=True,
        null=True,
    )
    user_sex = models.ForeignKey(
        'Sex',
        on_delete=PROTECT,
        blank=True,
        null=True,
    )

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def get_absolute_url(self):
        return reverse('main:my_profile')


class Post(models.Model):
    title = models.CharField('Title', max_length=30)
    slug = models.SlugField('Slug', max_length=35)
    text = models.TextField('Text', max_length=10000, null=True, blank=True)
    image = models.ImageField('Image', upload_to='main', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=CASCADE)
    publish_date = models.DateTimeField('Publish time', auto_now=True)

    def get_absolute_url(self):
        return reverse('main:show_post', kwargs={'post_slug': self.slug})

    def save(self, *args, **kwargs):
        last_obj = Post.objects.all().order_by('id').last()
        if last_obj:
            last_pk = last_obj.pk + 1
        else:
            last_pk = 1
        unidecode_title = unidecode(str(self.title))
        string = f'{unidecode_title}_{str(last_pk)}'
        self.slug = slugify(string)
        return super().save(*args, **kwargs)


class Sex(models.Model):
    name = models.CharField('Sex', max_length=10, db_index=True, blank=True, null=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    text = TextField('Text', max_length=250)
    author = ForeignKey(User, on_delete=CASCADE)
    post = ForeignKey(Post, on_delete=CASCADE)
    post_time = DateTimeField(auto_now=True)