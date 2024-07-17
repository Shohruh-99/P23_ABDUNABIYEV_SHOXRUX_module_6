from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db.models import Model, DateTimeField, SlugField, CharField, ImageField, FloatField, TextField, ForeignKey, \
    CASCADE, TextChoices, IntegerField
from django.utils.text import slugify


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password = None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

class User(AbstractUser):
    class Role(TextChoices):
        ADMIN = "admin", "Admin"
        OPERATOR = "operator", "Operator"
        MANAGER = "manager", "Manager"
        DRIVER = "driver", "Driver"
        USER = "user", "User"

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    username = CharField(max_length=255, null=True)
    email = CharField(max_length=255, unique=True)
    phone_number = CharField(max_length=13, null=True)
    mobile_number = CharField(max_length=13, null=True)
    age = IntegerField(null=True)
    role = CharField(max_length=50, choices=Role.choices, default=Role.USER)

class BaseModel(Model):
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseSlugModel(Model):
    slug = SlugField(unique=True)

    class Meta:
        abstract = True

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.name)
        while self.__class__.objects.filter(slug=self.slug).exists():
            self.slug += '-1'
        super().save(force_insert, force_update, using, update_fields)


class Category(BaseModel, BaseSlugModel):
    class Meta:
        verbose_name_plural = 'Categories'

    name = CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(BaseModel, BaseSlugModel):
    name = CharField(max_length=100)
    image = ImageField(upload_to='products/')
    price = FloatField()
    quantity = IntegerField(default=1)
    description = TextField()
    category = ForeignKey('apps.Category', CASCADE, related_name='products', to_field='slug')

    def __str__(self):
        return self.name






