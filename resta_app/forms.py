from django import forms 

from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from.models import Menu,customer_details
from django.core.exceptions import ValidationError

class Menuform(forms.Form):
    name=forms.CharField(max_length=100)
    price=forms.FloatField()
    food_category=forms.CharField(max_length=100)


class registrationform(UserCreationForm):
    class Meta:
        model=User
        fields=['username','first_name','last_name','email','password1','password2']
        
        labels={
            'username':'Enter Username',
            'first_name':'Enter first name',
            'last_name':'Enter Last name',
            'email':'Enter Email',
            'password1':'Enter password',
            'password2':'Enter confirm password',
        }
        
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'password1':forms.PasswordInput(attrs={'class':'form-control'}),
            'password2':forms.PasswordInput(attrs={'class':'form-control'}),
        }

def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email
def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():   
            raise ValidationError('First name should only contain alphabetic characters ')
        return first_name

def clean_last_name(self):
        last_name = self.cleaned_data.get('first_name')
        if not last_name.isalpha():   
            raise ValidationError('First name should only contain alphabetic characters ')
        return last_name
    
class loginform(UserCreationForm):
    class Meta:
        model=User
        fields=['username','password']
        
        labels={
            'username':'Enter Username',
            'password':'Enter password',
        }
        
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'password':forms.PasswordInput(attrs={'class':'form-control'}),
        }
        
class menu_detailsform(forms.ModelForm):
    class Meta:
        model=Menu
        fields=['item_name','food_category','description','price','image']
        
        labels={
            'item_name':'Enter item_name',
            'food_category':'Enter food_category',
            'description':'Enter description',
            'price':'Enter price',
            'image':'add image',
        }
        
        widgets={
            'item_name':forms.TextInput(attrs={'class':'form-control'}),
            'food_category':forms.Select(attrs={'class':'form-control'}),
            'description':forms.TextInput(attrs={'class':'form-control'}),
            'price':forms.NumberInput(attrs={'class':'form-control'}),
            'image':forms.FileInput(attrs={'class':'form-control'}),
        }
        
class userauthenticationForm (AuthenticationForm):
    username=forms.CharField(label="Enter username",widget=forms.TextInput(attrs={'class':'form-control'})),
    password=forms.CharField(label="Enter password",widget=forms.PasswordInput(attrs={'class':'form-control'})),   
    
    class Meta:
        model=User
        fields=['username']

class Customerform(forms.ModelForm):
    class Meta:
        model=customer_details
        fields=['Name','address','city','pincode']
        
        labels={
            'Name':'Enter name',
            'address':'Enter address',
            'city':'Enter city',
            'pincode':'Enter pincode',
        }
        widgets={
            'Name':forms.TextInput(attrs={'class':'form-control'}),
            'address':forms.TextInput(attrs={'class':'form-control'}),
            'city':forms.TextInput(attrs={'class':'form-control'}),
            'pincode':forms.NumberInput(attrs={'class':'form-control'}),
        }
        
