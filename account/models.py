from django.db import models
from userauths.models import User
# Create your models here.
import uuid
from userauths.models import User


from shortuuid.django_fields import ShortUUIDField
from django.db.models.signals import post_save

ACCOUNT_STATUS = (
    ("active", "Active"),
    ("in-active", "In-active"),
    ("pending", "Pending")
)

MARITAL_STATUS = (
    ("married", "Married"),
    ("single", "Single"),
    ("other", "Other")
)

GENDER = (
    ("male", "Male"),
    ("female", "Female"),
    ("other", "Other")
)

# NATIONALITY = (
#     ("india", "India"),
#     ("nigeria", "Nigeria"),
#     ("united_kingdom", "United_kingdom")
# )

IDENTITY_TYPE = (
    ("national_id_card", "National_ID_Card"),
    ("drivers_licence", "Driver_Licence"),
    ("international_passport", "International Passport")
)


def user_directory_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s_%s" %(instance.id, ext)
    return "user_{0}/{1}".format(instance.user.id, filename)

class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # account_balance = models.DecimalField(max_digits=10, decimal_places=2)
    account_balance = models.DecimalField(max_digits=25, decimal_places=2, default=0.00)
    account_number = ShortUUIDField(unique=True, length=10, max_length=25, prefix="217", alphabet="1234567890")
    account_id = ShortUUIDField(unique=True, length=7, max_length=25, prefix="DEX", alphabet="1234567890")
    pin_number = ShortUUIDField(unique=True, length=4, max_length=7, alphabet="1234567890")
    red_code = ShortUUIDField(unique=True, length=7, max_length=7, alphabet="abcdefgh1234567890")
    account_status = models.CharField(max_length=100, choices=ACCOUNT_STATUS, default="In-active")
    date = models.DateTimeField(auto_now_add=True)
    kyc_confirmed = models.BooleanField(default=False)
    recommended_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, related_name="recommended_by")

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username}'s Account"

class KYC(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    account = models.OneToOneField(Account, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to ="kyc", default="default.jpg")


    marital_status = models.CharField(choices=MARITAL_STATUS, max_length=40)
    gender = models.CharField(choices=GENDER, max_length=1000)
    identity_type = models.CharField(choices=IDENTITY_TYPE, max_length=140)
    identity_image = models.ImageField(upload_to="kyc", null=True, blank=True)

    date_of_birth = models.DateTimeField(auto_now_add=False)
    signature = models.ImageField(upload_to="kyc")

    # Address

    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    # Contact
    mobile = models.CharField(max_length=1000)
    fax = models.CharField(max_length=1000)

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}"




# To Create Account Immediately After a User Register on our Banking App

def create_account(sender, instance, created, **kwargs):
    # Check if a new instance of the sender (User model) was just created.
    if created:
    # If so, create a new Account object associated with the user instance.
        Account.objects.create(user=instance)

# Define a function named save_account that takes several parameters.
def save_account(sender, instance, **kwargs):
# Save the associated account object when the user instance is saved.
    instance.account.save()

# Connect the create_account function to the post_save signal of the User model.
post_save.connect(create_account, sender=User)
# Connect the save_account function to the post_save signal of the User model.
post_save.connect(save_account, sender=User)

# class Pin_Number(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     pin_number =  models.CharField(unique=True, max_length=7)
#     date_created = models.DateTimeField(auto_now_add=True)
#     date_modified = models.DateTimeField(auto_now_add=True)