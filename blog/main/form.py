from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import TextInput, CharField, PasswordInput, ModelForm, Textarea, FileInput, EmailInput, \
    DateInput, Select
from .models import Post, User, Comment, Profile
from datetime import date
import re


class PostForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = 'Название поста'
        self.fields['text'].label = 'Содержание поста'
        self.fields['image'].label = 'Картинка'
        self.label_suffix = ''

    class Meta:
        model = Post
        fields = ['title', 'text', 'image']
        widgets = {
            'title': TextInput(attrs={
                'class': 'container-box-form_wrap-form_field-wrap__field',
                'placeholder': 'Название поста'
            }),
            'text': Textarea(attrs={
                'class': 'container-box-form_wrap-form_field-wrap__field',
                'placeholder': 'Текст поста',
                'style': 'resize: none'
            }),
            'image': FileInput(attrs={
                'class': 'right-navigation__button fileInput'
            })
        }

    def clean(self):
        super(PostForm, self).clean()
        text = self.cleaned_data.get('text')
        image = self.cleaned_data.get('image')
        if text == "" and image == None:
            self._errors['text'] = self.error_class([
                'Пост должен содержать текст или картинку!'
            ])
        return self.cleaned_data


class LoginUserForm(AuthenticationForm):
    username = CharField(
        label='Логин',
        widget=TextInput(attrs={
            'class': 'container-box-form_wrap-form_field-wrap__field',
            'placeholder': 'Логин',
            'id': 'Input'
        })
    )
    password = CharField(
        label='Пароль',
        widget=PasswordInput(attrs={
            'class': 'container-box-form_wrap-form_field-wrap__field',
            'placeholder': 'Пароль',
            'id': 'Password'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegisterUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    username = CharField(
        label='Имя пользователя',
        widget=TextInput(attrs={
            'class': 'container-box-form_wrap-form_field-wrap__field',
            'placeholder': 'Имя пользователя',
            'id': 'floatingInput'
        })
    )
    password1 = CharField(
        label='Пароль',
        widget=PasswordInput(attrs={
            'class': 'container-box-form_wrap-form_field-wrap__field',
            'placeholder': 'Пароль',
            'id': 'floatingPassword',
        })
    )
    password2 = CharField(
        label='Повторите пароль',
        widget=PasswordInput(attrs={
            'class': 'container-box-form_wrap-form_field-wrap__field',
            'placeholder': 'Повторите пароль',
            'id': 'floatingPassword',
            'aria-label': "Floating label select example"
        })
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class ProfileForm(ModelForm):
    user_from = CharField(
        label='Ваш город',
        widget=TextInput(attrs={
            'class': 'container-box-form_wrap-form_field-wrap__field',
            'placeholder': 'Ваш город',
            'id': 'floatingInput',
            'required': 'False'
        })
    )
    class Meta:
        model=Profile
        fields= ('email', 'b_date', 'user_from', 'user_sex', 'bio')
        widgets = {
            'email': TextInput(attrs={
                'class': 'container-box-form_wrap-form_field-wrap__field',
                'placeholder': 'Почта',
                'id': 'floatingInput',
            }),
            'user_sex': Select(attrs={
                'id': 'floatingSelect',
                'class': 'container-box-form_wrap-form_field-wrap__field',
            }),
            'b_date': DateInput(attrs={
                'class': 'container-box-form_wrap-form_field-wrap__field',
                'type': 'text',
                'required': False,
                'onfocus': "(this.type='date')",
            }),
            'bio': Textarea(attrs={
                'class': 'container-box-form_wrap-form_field-wrap__field',
                'placeholder': 'О себе',
                'id': 'floatingInput',
                'type': 'text',
                'style': 'height: 200px; resize: none',
            }),
        }

    def clean(self):
        super(ProfileForm, self).clean()
        b_date = self.cleaned_data.get('b_date')
        email = self.cleaned_data.get('email')
        print(email)
        if b_date > date.today():
            self._errors['b_date'] = self.error_class([
                'Путешествия во времени вредны для вашего здоровья!'
            ])
        if email is None:
            self._errors['email'] = self.error_class([
                'Неверный формат электронной почты'
            ])
        return self.cleaned_data

class CommentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['text'].label = ''
        self.label_suffix = ''

    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': Textarea(attrs={
                'class': 'right-navigation-comment_field__comment_form',
                'placeholder': 'Текст комментария (250 символов)'
            }),
        }
