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




class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'categories'


class Menu_item(models.Model):
    product_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(
    Category,
    models.DO_NOTHING,
    db_column="category_id",
    related_name="products",
)
    product_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    ingredients = models.TextField(blank=True, null=True)
    original_price = models.DecimalField(max_digits=8, decimal_places=2)
    discount_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    stock_quantity = models.IntegerField()
    is_available = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'products'

class Review(models.Model):
    review_id = models.AutoField(primary_key=True)

    user = models.ForeignKey(
        User,
        db_column="user_id",
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    product = models.ForeignKey(
        Menu_item,
        db_column="product_id",
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    rating = models.IntegerField()

    review_text = models.TextField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(blank=True, null=True)

    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "reviews"
        app_label = "store"

    def __str__(self):
        return f"{self.user.full_name} - {self.product.product_name}"


class Favorite(models.Model):
    favorite_id = models.AutoField(primary_key=True)

    user = models.ForeignKey(
        User,
        db_column="user_id",
        on_delete=models.CASCADE,
        related_name="favorites",
    )

    product = models.ForeignKey(
        Menu_item,
        db_column="product_id",
        on_delete=models.CASCADE,
        related_name="favorites",
    )

    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "favorites"
        app_label = "store"

