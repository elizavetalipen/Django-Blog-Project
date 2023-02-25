from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment
from django.contrib.auth.models import User 


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'post_image')


class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()
		return user