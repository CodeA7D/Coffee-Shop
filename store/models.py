from django.contrib.auth.hashers import check_password, make_password
from django.db import models


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=20, default='Customer')
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'Users'
        app_label = 'store'

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        return self

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def is_active(self):
        return True

    @property
    def is_staff(self):
        return str(self.role).lower() == 'admin'

    @property
    def is_superuser(self):
        return str(self.role).lower() == 'admin'

    def get_full_name(self):
        return self.full_name or self.email

    def get_email(self):
        return self.email

    def get_username(self):
        return self.email

    def get_session_auth_hash(self):
        return self.password or ''

    def __str__(self):
        return self.email
