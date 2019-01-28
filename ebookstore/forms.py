from django import forms
from .models import UserProfile,Order, Comment,Complain,Saleontelestai
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm 











class RegistrationForm(UserCreationForm):
	email = forms.EmailField(required=True,widget=forms.TextInput(
	        	attrs={
	        			'class':'form-control',


	        	}))

	class Meta:
		model = User
		fields = (
			'username',
			'first_name',
			'last_name',
			'email',
			'password1',
			'password2'
			) 
	def save(self,commit = True):
		user = super(RegistrationForm,self).save(commit = False)
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.email = self.cleaned_data['email']

		if commit:
			user.save()
class EditProfileForm(forms.ModelForm):
	 email = forms.CharField(widget=forms.TextInput(
	        	attrs={
	        			'class':'form-control',


	        	}))
	   
	 first_name = forms.SlugField(widget=forms.TextInput(
	        	attrs={
	        			'class':'form-control',


	        	}))
	        
	 last_name =  forms.CharField(widget=forms.TextInput(
	        	attrs={
	        			'class':'form-control',


	        	}))
	 class Meta:
	 	model = User
	 	fields = [
					'email',
					'first_name',
					'last_name',
					
					]
class UserUpdateForm(forms.ModelForm):
	

	city =  forms.CharField(widget=forms.TextInput(
	        	attrs={
	        			'class':'form-control',


	        	}))
	age =  forms.CharField(widget=forms.TextInput(
	        	attrs={
	        			'class':'form-control',


	        	}))
	address =  forms.CharField(widget=forms.TextInput(
	        	attrs={
	        			'class':'form-control',


	        	}))
	phone_number = forms.CharField(widget=forms.TextInput(
	        	attrs={
	        			'class':'form-control',


	        	}))

	
	


	        	

	class Meta:
		model = UserProfile
		fields = [
			
			'gender',
			'age',
			'city',
			'address',
			'phone_number'
			
	]

class orderinformation(forms.ModelForm):
	class Meta:
		model = Order
		fields = [
			'delivery_location',

			]

class CommentForm(forms.ModelForm):
	
	text =  forms.CharField(widget=forms.Textarea(
	        	attrs={
	        			'class':'form-control',


	        	}))
	class Meta: 
 		model = Comment 
 		fields = ['text']


class ComplainForm(forms.ModelForm):
 	
 	name =  forms.CharField(widget=forms.TextInput(
	        	attrs={
	        			'class':'form-control',


	        	}))

 	text = forms.CharField(widget=forms.Textarea(
	        	attrs={
	        			'class':'form-control',


	        	}))
 	telephone_number = forms.CharField(widget=forms.TextInput(
	        	attrs={
	        			'class':'form-control',


	        	}))
 	email = forms.CharField(widget=forms.TextInput(
	        	attrs={
	        			'class':'form-control',


	        	}))

 	class Meta: 
 		model = Complain 
 		fields = ['name','telephone_number','email','text']	

class SaleontelestaiForm(forms.ModelForm):
 	
 	name =  forms.CharField(widget=forms.TextInput(
	        	attrs={
	        			'class':'form-control',


	        	}))

 	product_category= forms.CharField(widget=forms.TextInput(
	        	attrs={
	        			'class':'form-control',


	        	}))
 	telephone_number = forms.CharField(widget=forms.TextInput(
	        	attrs={
	        			'class':'form-control',


	        	}))
 	address = forms.CharField(widget=forms.TextInput(
	        	attrs={
	        			'class':'form-control',


	        	}))
 	store_name = forms.CharField(widget=forms.TextInput(
	        	attrs={
	        			'class':'form-control',


	        	}))
 	email = forms.CharField(widget=forms.TextInput(
	        	attrs={
	        			'class':'form-control',


	        	}))

 	class Meta: 
 		model = Saleontelestai 
 		fields = ['name','address','telephone_number','email','store_name','product_category']	

				