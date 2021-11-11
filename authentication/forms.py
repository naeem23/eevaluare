from django import forms
from django.contrib.auth.forms import (
	UserCreationForm, UserChangeForm, AdminPasswordChangeForm, PasswordResetForm, SetPasswordForm
	)
from django.contrib.auth import get_user_model
User = get_user_model()
import re


# ============================================================================
# =============================== Sing In Form ===============================
# ============================================================================
class SigninForm(forms.Form):
	username = forms.CharField(
		widget = forms.TextInput(
			attrs = {
				'placeholder': 'Username',
				'class': 'form-control',
			}
		)) 

	password = forms.CharField(
		widget = forms.PasswordInput(
			attrs = {
				'placeholder': 'Password',
				'class': 'form-control',
			}
		))


# ============================================================================
# =============================== Sing Up Form ===============================
# ============================================================================
class SignupForm(UserCreationForm):
	username = forms.CharField(widget = forms.TextInput(attrs = {'placeholder': 'Username','class': 'form-control',}))

	email = forms.EmailField(widget = forms.EmailInput(attrs = {'placeholder': 'Email','class': 'form-control',}))

	password1 = forms.CharField(widget = forms.PasswordInput(attrs = {'placeholder': 'Password','class': 'form-control',}))

	password2 = forms.CharField(widget = forms.PasswordInput(attrs = {'placeholder': 'Confirm Password','class': 'form-control',}))

	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2',)


# ============================================================================
# ======================= Admin User creation Form ===========================
# ============================================================================
class AgentCreationForm(UserCreationForm):
	username = forms.CharField(widget = forms.TextInput(attrs = {'placeholder': 'Username','class': 'form-control',}))

	first_name = forms.CharField(required=False, widget = forms.TextInput(attrs = {'placeholder': 'First Name','class': 'form-control',}))

	last_name = forms.CharField(required=False, widget = forms.TextInput(attrs = {'placeholder': 'Last Name','class': 'form-control',}))

	email = forms.EmailField(widget = forms.EmailInput(attrs = {'placeholder': 'Email','class': 'form-control',}))

	password1 = forms.CharField(widget = forms.PasswordInput(attrs = {'placeholder': 'Password','class': 'form-control',}))

	password2 = forms.CharField(widget = forms.PasswordInput(attrs = {'placeholder': 'Confirm Password','class': 'form-control',}))

	class Meta:
		model = User
		fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2',)


# ============================================================================
# =============================== User update form============================
# ============================================================================
class AgentUpdateForm(UserChangeForm):
	username = forms.CharField(widget = forms.TextInput(attrs = {'placeholder': 'Username','class': 'form-control',}))

	first_name = forms.CharField(required=False, widget = forms.TextInput(attrs = {'placeholder': 'First Name','class': 'form-control',}))

	last_name = forms.CharField(required=False, widget = forms.TextInput(attrs = {'placeholder': 'Last Name','class': 'form-control',}))

	email = forms.EmailField(widget = forms.EmailInput(attrs = {'placeholder': 'Email','class': 'form-control',}))

	class Meta:
		model = User 
		fields = ('username', 'email', 'first_name', 'last_name')



# ============================================================================
# ========================== Password change Form ============================
# ============================================================================
class AgentPasswordChangeForm(AdminPasswordChangeForm):
	password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',}))

	password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

	class Meta:
		model = User
		fields = ('password1', 'password2')



# ============================================================================
# =========================== Password reset Form ============================
# ============================================================================
class ForgetPassword(forms.Form):
	email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': "Email", 'class': 'form-control'}))

	def clean_email(self):
		email = self.cleaned_data.get('email')

		email_correction = re.match('^[_a-zA-Z0-9-]+(\.[_a-zA-Z0-9-]+)*@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*(\.[a-zA-Z]{2,4})$', email)
		if not email_correction:
			raise forms.ValidationError('Enter a valid email!')
		else:
			email_exists = User.objects.filter(email__iexact=email).exists()
			if not email_exists:
				raise forms.ValidationError('Email is not registered!')

		return email



# ============================================================================
# ====================== Otp for email verification ==========================
# ============================================================================
class OTPForm(forms.Form):
	otp = forms.CharField(max_length=6, min_length=6, widget=forms.TextInput(attrs={'placeholder': '******', 'class': 'form-control text-center otp'}))



# ============================================================================
# ============================= new password set ============================
# ============================================================================
class ResetNewPass(SetPasswordForm):
	new_password1 = forms.CharField(widget = forms.PasswordInput(attrs = {'placeholder': 'New Password', 'class': 'form-control',}))
	new_password2 = forms.CharField(widget = forms.PasswordInput(attrs = {'placeholder': 'Confirm New Password', 'class': 'form-control',}))



# ============================================================================
# ====================== Admin Inspector creation Form =======================
# ============================================================================
class AddInspectorForm(UserCreationForm):
	username = forms.CharField(widget = forms.TextInput(attrs = {'placeholder': 'Username','class': 'form-control',}))
	first_name = forms.CharField(required=False, widget = forms.TextInput(attrs = {'placeholder': 'First Name','class': 'form-control',}))
	last_name = forms.CharField(required=False, widget = forms.TextInput(attrs = {'placeholder': 'Last Name','class': 'form-control',}))
	email = forms.EmailField(widget = forms.EmailInput(attrs = {'placeholder': 'Email','class': 'form-control',}))
	password1 = forms.CharField(widget = forms.PasswordInput(attrs = {'placeholder': 'Password','class': 'form-control',}))
	password2 = forms.CharField(widget = forms.PasswordInput(attrs = {'placeholder': 'Confirm Password','class': 'form-control',}))
	telephone = forms.CharField(required=False, widget = forms.TextInput(attrs = {'class': 'form-control'}))
	profile_picture = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
	certification_number = forms.CharField(widget = forms.TextInput(attrs={'placeholder': 'Certification Number','class': 'form-control'}))
	certification_text = forms.CharField(widget = forms.Textarea(attrs={'class': 'form-control', 'rows': '5'}))
	stamp = forms.FileField(required=False, widget = forms.FileInput(attrs={'class': 'form-control'}))

	class Meta:
		model = User
		fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'profile_picture', 'telephone', 'certification_number', 'certification_text', 'stamp')



# ============================================================================
# =========================== Inspector update Form ==========================
# ============================================================================
class InspectorUpdateForm(UserChangeForm):
	username = forms.CharField(widget = forms.TextInput(attrs = {'placeholder': 'Username','class': 'form-control',}))
	first_name = forms.CharField(required=False, widget = forms.TextInput(attrs = {'placeholder': 'First Name','class': 'form-control',}))
	last_name = forms.CharField(required=False, widget = forms.TextInput(attrs = {'placeholder': 'Last Name','class': 'form-control',}))
	email = forms.EmailField(widget = forms.EmailInput(attrs = {'placeholder': 'Email','class': 'form-control',}))
	telephone = forms.CharField(required=False, widget = forms.TextInput(attrs = {'class': 'form-control'}))
	certification_number = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control'}))
	certification_text = forms.CharField(widget = forms.Textarea(attrs = {'class': 'form-control', 'rows': '8'}))
	stamp = forms.FileField(widget = forms.FileInput(attrs={'class': 'form-control'}))

	class Meta:
		model = User 
		fields = ('username', 'email', 'first_name', 'last_name', 'telephone', 'certification_number', 'certification_text', 'stamp')
