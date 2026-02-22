from django.contrib.auth.forms import UserCreationForm
from .models import Customer_Profile, Vendor_Profile, CustomUser
from django.forms import ModelForm
from django import forms

#User creation form for the customer
class CustomerCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'phone_number', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomerCreationForm,self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class':'form-control',
            'placeholder':'Username'
        })
    def __init__(self, *args, **kwargs):
        super(CustomerCreationForm,self).__init__(*args, **kwargs)
        
        self.fields['phone_number'].widget.attrs.update({
            'class':'form-control',
            'placeholder':'Phone Number'
        })
    def __init__(self, *args, **kwargs):
        super(CustomerCreationForm,self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class':'form-control',
            'placeholder':'Enter Email'
        })
    def __init__(self, *args, **kwargs):
        super(CustomerCreationForm,self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class':'form-control',
            'placeholder':'Enter Password'
        })
    def __init__(self, *args, **kwargs):
        super(CustomerCreationForm,self).__init__(*args, **kwargs)
        self.fields['password2'].widget.attrs.update({
            'class':'form-control',
            'placeholder':'Confirm Password'
        })


class CustomerProfileForm(forms.ModelForm):
    # Add the username field manually since it is part of the User model
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )

    class Meta:
        model = Customer_Profile
        fields = ['name', 'username', 'email', 'phone_number',]  # Fields from Customer_Profile model

    def __init__(self, *args, **kwargs):
        super(CustomerProfileForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Full Name'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Email'
        })
        self.fields['phone_number'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Phone Number'
        })

        # Set initial username value from the associated User instance
        if self.instance and self.instance.user:
            self.fields['username'].initial = self.instance.user.username

    def save(self, commit=True):
        profile = super(CustomerProfileForm, self).save(commit=False)
        # Save the username to the associated User instance
        if self.instance.user:
            self.instance.user.username = self.cleaned_data['username']
            if commit:
                self.instance.user.save()
                profile.save()
        return profile
   

#User creation form for the vendor
class VendorCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username','phone_number', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(VendorCreationForm,self).__init__(*args, **kwargs)


    



class VendorProfileForm(ModelForm):
    class Meta:
        model = Vendor_Profile
        fields = ['profile_picture', 'business_name', 'name', 'city', 'username', 'email', 'phone_number', 'business_description']


    def __init__(self, *args, **kwargs):
        super(VendorProfileForm, self).__init__(*args, **kwargs)

        self.fields['profile_picture'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Profile Picture',
        })
        self.fields['business_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter Name of Business'
        })
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Owners name'
        })
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'username'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Email'
        })
        self.fields['city'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter City or Country'
        })
        self.fields['business_description'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Describe your business'
        })


class AccountReviewForm(forms.Form):
    review_text = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Leave a review...', 'rows': 4}), required=False)
  
   




