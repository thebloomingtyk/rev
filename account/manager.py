from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, title, email, first_name, last_name, role, password):
        if not title:
            raise ValueError('user Must have a title')
        if not email:
            raise ValueError('user Must have an email')
        if not first_name:
            raise ValueError('User must have first name')
        if not last_name:
            raise ValueError('User Must have last name')
        if not role:
            raise ValueError('User Must have a role')

        user = self.model(
            title=title,
            email=self.normalize_email(email=email),
            first_name=first_name,
            last_name=last_name,
            role=role
        )
        user.is_active = False
        user.set_password(raw_password=password)
        user.save()
        return user

    def create_superuser(self, email, first_name, last_name, password, title, role):
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            role=role,
            title=title
        )
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
