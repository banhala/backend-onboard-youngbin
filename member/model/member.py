from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class MemberManager(BaseUserManager):

    def create_user(
        self, email: str, username: str, password: str = None, **extra_fields
    ):
        if not email:
            raise ValueError("이메일은 필수입니다")
        if not username:
            raise ValueError("사용자명은 필수입니다")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class Member(AbstractBaseUser):

    id = models.BigAutoField(primary_key=True)
    email: str = models.EmailField(unique=True, verbose_name="이메일", max_length=254)
    username: str = models.CharField(verbose_name="사용자명", max_length=150)
    password: str = models.CharField(verbose_name="비밀번호", max_length=128)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = MemberManager()

    class Meta:
        db_table = "members"
        verbose_name = "회원"
        verbose_name_plural = "회원"

    def __str__(self) -> str:
        return self.email

    @property
    def is_anonymous(self) -> bool:
        return False

    @property
    def is_authenticated(self) -> bool:
        return True
