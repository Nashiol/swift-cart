from .models import CustomUser, Customer_Profile, Vendor_Profile
from django .dispatch import receiver
from django.db import transaction
from django.db.models.signals import post_save, post_delete
from django.contrib.auth import get_user_model
from .models import AccountReview

#Creating profiles for each user type
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 'CUSTOMER':
            print('CREATING....CUSTOMER PROFILE') 
            Customer_Profile.objects.create(
            user=instance,
            email=instance.email,
            phone_number=instance.phone_number,
            )
        elif instance.user_type == 'VENDOR':
            print('CREATING....VENDOR PROFILE')   
            Vendor_Profile.objects.create(
            user=instance,
            email=instance.email,
            phone_number=instance.phone_number,
            username=instance.username
            )


#Saving Proifles after user is created
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 'CUSTOMER' and hasattr(instance, 'customer_profile'):
        print('Worked')
        transaction.on_commit(lambda: instance.Customer_Profile.save(
            update_fields=['email', 'phone_number']
        ))
    elif instance.user_type == 'VENDOR' and hasattr(instance, 'vendor_profile'):
        print('Worked')
        transaction.on_commit(lambda: instance.Vendor_Profile.save(
            update_fields=['email', 'phone_number', 'username']
        ))




@receiver(post_save, sender=Customer_Profile)
def save_user_from_customer(sender, instance, **kwargs):
    print('updating customer profile')
    user = instance.user
    user.save(update_fields=['email', 'phone_number'])

@receiver(post_save, sender=Vendor_Profile)
def save_user_from_vendor(sender, instance, **kwargs):
    print('updating vendor profile')
    user = instance.user
    user.save(update_fields=['username', 'email', 'phone_number'])


# When a profile is deleted a User has to be deleted
@receiver(post_delete, sender=Customer_Profile)
def delete_customer_user(sender, instance,  **kwargs):
    print('DELETING CUSTOMER...')
    user = instance.user
    user.delete()

@receiver(post_delete, sender=Vendor_Profile)
def delete_provider_user(sender, instance,  **kwargs):
    print('DELETING VENDOR...')
    user = instance.user
    user.delete()
    

@receiver(post_delete, sender=get_user_model())
def create_review_after_account_deletion(sender, instance, **kwargs):
    # Create the review after the user is deleted
    if instance.user_type in ['CUSTOMER', 'VENDOR']:  # Check if it's a valid user type
        review_text = "User account deleted. No further reviews will be accepted."
        AccountReview.objects.create(
            user=instance,
            review_text=review_text
        )

