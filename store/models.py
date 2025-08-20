from django.db import models

# Create your models here.


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()
    # products


class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        "Product", on_delete=models.SET_NULL, null=True, related_name="+"
    )


class Product(models.Model):
    # sku = models.CharField(max_length=10, primary_key=True)

    slug = models.SlugField()

    title = models.CharField(max_length=255)  # varchar(255)
    description = models.TextField()

    # 9999.99
    # price = models.DecimalField(max_digits=6, decimal_places=2)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion)


class Customer(models.Model):
    MEMBERSHIP_BRONZE = "B"
    MEMBERSHIP_SILVER = "S"
    MEMBERSHIP_GOLD = "G"

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, "Bronze"),
        (MEMBERSHIP_SILVER, "Silver"),
        (MEMBERSHIP_GOLD, "Gold"),
    ]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.CharField(null=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE
    )

    class Meta:
        db_table = "store_customers"
        indexes = [models.Index(fields=["last_name", "first_name"])]


class Order(models.Model):
    PAYMENT_PENING = "P"
    PAYMENT_COMPLETE = "C"
    PAYMENT_FAILED = "F"

    PAYMENT_STATUS = [
        (PAYMENT_PENING, "Pending"),
        (PAYMENT_COMPLETE, "Complete"),
        (PAYMENT_FAILED, "Failed"),
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS, default=PAYMENT_PENING
    )
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


# one to one relationship
class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)

    # if customer's field deleted, related address should be deleted
    # print we should add parent entity ==> which is means, parent entity should be created first!
    # models.CASCADE ==> delete it
    # models.SET_NULL ==> make it null
    # models.SET_DEFAULT ==> make it default
    # models.PROCTECT ==> make it prevent from deletion
    # we don't have to create reverse relationship on the customer class
    customer = models.OneToOneField(
        Customer, on_delete=models.CASCADE, primary_key=True
    )


# to to manu relationship
class MultipleAddress(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)

    # if customer's field deleted, related address should be deleted
    # print we should add parent entity ==> which is means, parent entity should be created first!
    # models.CASCADE ==> delete it
    # models.SET_NULL ==> make it null
    # models.SET_DEFAULT ==> make it default
    # models.PROCTECT ==> make it prevent from deletion
    # we don't have to create reverse relationship on the customer class
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


class Card(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class CardItem(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
