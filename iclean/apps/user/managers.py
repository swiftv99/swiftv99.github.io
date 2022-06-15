from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    """
    Custom manager that helps to create user and super user and it is
    assigned to Custom User class!
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have a email!")
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user