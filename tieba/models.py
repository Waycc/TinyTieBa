from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.


class MyUserManager(BaseUserManager):
    def create_user(self,email ,name, password=None):
        """CreCreates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email = self.normalize_email(email),
            name = name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password = password,
            name = name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class UserProfile(AbstractBaseUser):
    """用户表"""
    email = models.EmailField(max_length=32,unique=True)
    name = models.CharField(max_length=11,null=False, unique=True)
    create_date = models.DateTimeField(auto_now_add=True)
    role = models.ManyToManyField('Role',blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    followed_tieba = models.ManyToManyField('TieBa',blank=True)
    followed_user = models.ManyToManyField('self',blank=True)
    head_img = models.ImageField(upload_to='user/head/', default='default/head.jpg',null=True)
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['name']

    objects = MyUserManager()

    class Meta:
        verbose_name_plural = '用户表'

    def __str__(self):
        return '邮箱：%s,名字：%s'%(self.email, self.name)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Role(models.Model):
    """角色表"""
    role = models.CharField(max_length=16)
    permission = models.ManyToManyField('Permission')

    class Meta:
        verbose_name_plural = '角色表'

    def __str__(self):
        return self.role



class Permission(models.Model):
    '''权限表'''
    permission = models.CharField(max_length=128)

    class Meta:
        verbose_name_plural = '权限表'

    def __str__(self):
        return self.permission


class TieBa(models.Model):
    """贴吧表"""
    name = models.CharField(max_length=16, unique=True)
    background_img = models.ImageField(upload_to='tieba/background',default='default/background.jpg', null=True)
    head_img = models.ImageField(upload_to='tieba/head/', default='default/tieba_head.jpg', null=True)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = '贴吧表'

    def __str__(self):
        return self.name

class Article(models.Model):
    """贴子表"""
    author = models.ForeignKey('UserProfile',on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    tieba = models.ForeignKey('TieBa',on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '贴子表'

    def __str__(self):
        return self.title


class Comment(models.Model):
    """评论表"""

    author = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    article = models.ForeignKey('Article',on_delete=models.CASCADE)
    to_whom = models.CharField(max_length=16,null=True, blank=True)
    to_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name_plural = '评论表'


class ArticleImage(models.Model):
    name = models.CharField(max_length=16)
    img = models.ImageField(upload_to='article/', null=True)
    article = models.ForeignKey('Article',on_delete=models.CASCADE,null=True)



