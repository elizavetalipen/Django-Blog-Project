from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm
from .models import Post, Comment, UserInfo, Cathegory, Tag
from django.contrib.auth.models import User 
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Field, Row, Column


class PostForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Cathegory.objects.all())
    tags = forms.CharField(max_length=100)

    class Meta:
        model = Post
        fields = ('title', 'content', 'post_image', 'category','tags')
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'style': 'height: 300px'}),
        }

# форма для регистрации
class NewUserForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(NewUserForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Register'))

        self.helper.layout = Layout(
            Div(
                Field('username', css_class='form-control col-md-6'),
                Field('email', css_class='form-control col-md-6'),
                css_class='form-group'
            ),
            Div(
                Field('password1', css_class='form-control col-md-6'),
                Field('password2', css_class='form-control col-md-6'),
                css_class='form-group'
            )
        )


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Login'))

        self.helper.layout = Layout(
            Div(
                Field('username', css_class='form-control col-md-6'),
                css_class='form-group'
            ),
            Div(
                Field('password', css_class='form-control col-md-6'),
                css_class='form-group'
            )
        )


# форма для редактирования информации в профиле
class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['avatar_image', 'cover_image', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 10}),}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))
        self.helper.layout = Layout(
            Field('avatar_image', css_class='form-control-file'),
            Field('cover_image', css_class='form-control-file'),
            Field('bio', css_class='form-control'),
        )


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username']
    
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))
        self.helper.layout = Layout(
            Div(
            Field('username', css_class='form-control col-md-6'),
            Field('email', css_class='form-control col-md-6'),
            css_class='form-group')
        )


class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget = forms.PasswordInput()
        self.fields['new_password1'].widget = forms.PasswordInput()
        self.fields['new_password2'].widget = forms.PasswordInput()

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Change Password'))
        self.helper.layout = Layout(
            Div(
                Field('old_password', css_class='form-control'),
                Field('new_password1', css_class='form-control'),
                Field('new_password2', css_class='form-control'),
                css_class='form-group'
            )
        )



class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Comment',
                'rows': '4'
            }),
        }

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Post Comment'))