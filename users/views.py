from django.shortcuts import render, redirect, get_object_or_404
from.forms import CustomerCreationForm, VendorCreationForm, CustomerProfileForm, VendorProfileForm
from django.contrib.auth import login, logout, authenticate
from django .contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Vendor_Profile, Customer_Profile, CustomUser, AccountReview
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db import IntegrityError
from django.contrib.auth.backends import ModelBackend
from checkouts.models import OrderItem
from django.db.models import F
from services.models import Review
from.forms import AccountReviewForm


def signup(request):
    return render(request, 'users/signup.html')






# Create your views here.
def customer_signup(request):
    form = CustomerCreationForm()
    if request.method == 'POST':
        form = CustomerCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'CUSTOMER'
            print('Creating customer......')
            user.save()

            # Create a Customer_Profile after saving the user
            Customer_Profile.objects.create(user=user)  # Create the profile

            # Specify the backend as a string, not a class reference
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            return redirect('customer-dashboard-update')  # Redirect to the update page
        else:
            print('Passwords do not match')

    else:
        form = CustomerCreationForm()

    context = {
        'form': form, 
    }
    return render(request, 'users/customer-signup.html', context)



def customerProfile(request):
    if request.method == 'POST':
        try:
            # Try to get the existing profile for the logged-in user
            profile = Customer_Profile.objects.get(user=request.user)
            form = CustomerProfileForm(request.POST, instance=profile)  # Update the profile
        except Customer_Profile.DoesNotExist:
            # If no profile exists, create a new one
            form = CustomerProfileForm(request.POST)

        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Profile saved successfully!')
            return redirect('customer-dashboard')  # Redirect to the dashboard or another page

    else:
        # Display an empty form if the request is not POST
        try:
            profile = Customer_Profile.objects.get(user=request.user)
            form = CustomerProfileForm(instance=profile)  # Prefill form if profile exists
        except Customer_Profile.DoesNotExist:
            form = CustomerProfileForm()  # Empty form if no profile

    return render(request, 'users/customer-dashboard-update.html', {'form': form})








def vendor_signup(request):
    form = VendorCreationForm()
    if request.method == 'POST':
        form = VendorCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'VENDOR'
            user.save()

            # Create Vendor_Profile for the user
            Vendor_Profile.objects.create(user=user)

            # Explicitly set the backend and log in the user
            user.backend = 'django.contrib.auth.backends.ModelBackend'  # Adjust based on your default backend
            login(request, user)

            messages.success(request, 'Vendor account created successfully.')
            return redirect('vendor-profile-form')
        else:
            messages.error(request, 'Please check the form fields.')

    context = {'form': form}
    return render(request, 'users/vendor-signup.html', context)





def vendorProfile(request):
    user = request.user
    form = VendorProfileForm()
    try:
        profile = Vendor_Profile.objects.get(user=user)
        print('profile has user')
    except:
        profile = None 
        print('no user')  
    if request.method == 'POST':
        form = VendorProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user
            profile.save()    
            messages.success(request, 'Profile saved') 
            return redirect('vendor-profile')
        else:
            messages.error(request, 'Check fields')
    else:
        form = VendorProfileForm()        
    context = {
        'form':form,
    }    
    return render(request, 'users/vendor-profile-form.html', context)








#Login function
def loginUser(request):
    if request.user.is_authenticated:
        return redirect('services:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Attempt to find the user by email
        try:
            user = CustomUser.objects.get(email=username)
        except CustomUser.DoesNotExist:
            messages.error(request, 'Username does not exist, please enter your email!')
            return render(request, 'users/login.html')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print(f'logged in user type: {user.user_type}')
            login(request, user)
            messages.success(request, f'Welcome back {request.user.username}.') 
            
            # Redirect based on user type
            if user.user_type == 'CUSTOMER':
                return redirect('services:home')
            elif user.user_type == 'VENDOR':
                return redirect('services:home')  # Replace with the correct URL for vendor profile 
        else:
            messages.error(request, "Username or password is incorrect.")
    return render(request, 'users/login.html')

#Logout function
def logoutUser(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')


#Dashboards for the users
from django.db.models import Avg
from checkouts.models import OrderItem, Order
#The dashboard for the vendor

@login_required(login_url='login')
def vendor_profile(request):
    user = request.user
    profile = get_object_or_404(Vendor_Profile, user=user)

    # Fetch the orders associated with the vendor's products, excluding "Shipped" and "Delivered" statuses
    order_items = (
        OrderItem.objects.filter(product__vendor=profile, order__status__in=[Order.Status.PENDING, Order.Status.CANCELED])
        .annotate(total_price=F('product__price') * F('quantity'))  # Annotate total price
    )

    # Calculate the average rating for the vendor
    reviews = Review.objects.filter(vendor=profile)  # Assuming 'vendor' is a ForeignKey to Vendor_Profile
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']  # Calculate average rating

    # If there are no reviews, set the average rating to 0
    if average_rating is None:
        average_rating = 0

    # Handle profile updates
    if request.method == 'POST':
        form = VendorProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('vendor-profile')  # Redirect after saving
    else:
        form = VendorProfileForm(instance=profile)

    context = {
        'profile': profile,
        'form': form,
        'order_items': order_items,  # Pass annotated orders to the template
        'average_rating': average_rating,  # Pass the average rating to the template
        'star_range': range(1, 6),  # Pass the range of numbers for stars
    }
    return render(request, 'users/vendor-profile.html', context)




#The customer dashboard/profile 
@login_required(login_url='login')
def customer_dashboard(request):
    user = request.user
    profile = Customer_Profile.objects.get(user=request.user)  # Assuming the profile is already created
    return render(request, 'users/customer-dashboard.html', {'profile': profile})


#For updating the customer profile
@login_required(login_url='login')
def customer_dashboard_update(request):
    user = request.user
    profile = Customer_Profile.objects.get(user=user)
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('customer-dashboard')  # Redirect to profile page after successful update
    else:
        form = CustomerProfileForm(instance=profile)

    return render(request, 'users/customer-dashboard-update.html', {'form': form})





@login_required
def vendor_profile_update(request):
    try:
        # Try to get the Vendor_Profile for the logged-in user
        profile = Vendor_Profile.objects.get(user=request.user)
    except Vendor_Profile.DoesNotExist:
        # If no profile exists, create a new one
        profile = Vendor_Profile.objects.create(user=request.user)

    user = request.user  # Get the User instance

    if request.method == 'POST':
        form = VendorProfileForm(request.POST, request.FILES, instance=profile)

        # Check if the 'remove_picture' checkbox is checked and remove the profile picture
        if 'remove_picture' in request.POST and request.POST['remove_picture'] == 'on':
            profile.profile_picture = None  # Remove the profile picture

        if form.is_valid():
            # Update username if it has been changed
            new_username = form.cleaned_data.get('username')
            if new_username and new_username != user.username:
                user.username = new_username
                try:
                    user.save()  # Save the updated User instance
                except IntegrityError as e:
                    form.add_error('username', 'Username is already taken.')
                    return render(request, 'users/vendor-profile-form.html', {'form': form})

            form.save()  # Save the profile instance
            return redirect('vendor-profile')  # Redirect to the profile page after saving
    else:
        form = VendorProfileForm(instance=profile)  # Pre-populate form with existing profile data
        form.fields['username'].initial = user.username  # Set initial value for the username field

    return render(request, 'users/vendor-profile-form.html', {'form': form})



from django.db import transaction

@login_required
def delete_customer_account(request):
    if request.user.user_type != 'CUSTOMER':
        messages.error(request, "Only customers can delete their accounts.")
        return redirect('home')

    if request.method == 'POST':
        form = AccountReviewForm(request.POST)
        if form.is_valid():
            # Create the review before account deletion
            review_text = form.cleaned_data.get('review_text')
            if review_text:
                # Save the review with user email, not directly tied to the User instance
                AccountReview.objects.create(
                    user_email=request.user.email,  # Save email as identifier
                    review_text=review_text.strip()
                )

            try:
                with transaction.atomic():
                    # Get and delete the customer profile
                    profile = Customer_Profile.objects.get(user=request.user)
                    profile.delete()

                    # Delete the user account
                    user = request.user
                    user.delete()

                # Log the user out after deletion
                logout(request)
                messages.success(request, "Your customer account has been successfully deleted.")
                return redirect('services:home')

            except Customer_Profile.DoesNotExist:
                messages.error(request, "Customer profile not found.")
                return redirect('customer-dashboard')

    else:
        form = AccountReviewForm()

    return render(request, 'users/delete-customer-account.html', {'form': form})


@login_required
def delete_vendor_account(request):
    if request.user.user_type != 'VENDOR':
        messages.error(request, "Only vendors can delete their accounts.")
        return redirect('home')

    if request.method == 'POST':
        form = AccountReviewForm(request.POST)
        if form.is_valid():
            # Create the review before account deletion
            review_text = form.cleaned_data.get('review_text')
            if review_text:
                # Save the review with user email, not directly tied to the User instance
                AccountReview.objects.create(
                    user_email=request.user.email,  # Save email as identifier
                    review_text=review_text.strip()
                )

            try:
                with transaction.atomic():
                    # Get and delete the vendor profile
                    profile = Vendor_Profile.objects.get(user=request.user)
                    profile.delete()

                    # Delete the user account
                    user = request.user
                    user.delete()

                # Log the user out after deletion
                logout(request)
                messages.success(request, "Your vendor account has been successfully deleted.")
                return redirect('services:home')

            except Vendor_Profile.DoesNotExist:
                messages.error(request, "Vendor profile not found.")
                return redirect('vendor-profile')

    else:
        form = AccountReviewForm()

    return render(request, 'users/delete-vendor-account.html', {'form': form})