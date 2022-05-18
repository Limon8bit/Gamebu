from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import TextInput, CharField, PasswordInput, ModelForm, Textarea, FileInput, EmailInput, \
    DateInput, Select, DateField
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
                'class': 'form-control',
                'placeholder': 'Название поста'
            }),
            'text': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Текст поста',
                'style': 'resize: none'
            }),
            'image': FileInput(attrs={
                'class': 'form-control'
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
            'class': 'form-control',
            'placeholder': 'Логин',
            'id': 'floatingInput'
        })
    )
    password = CharField(
        label='Пароль',
        widget=PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль',
            'id': 'floatingPassword'
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
            'class': 'form-control',
            'placeholder': 'Имя пользователя',
            'id': 'floatingInput'
        })
    )
    password1 = CharField(
        label='Пароль',
        widget=PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль',
            'id': 'floatingPassword',
        })
    )
    password2 = CharField(
        label='Повторите пароль',
        widget=PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторите пароль',
            'id': 'floatingPassword',
            'aria-label': "Floating label select example"
        })
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class ProfileForm(ModelForm):
    email = CharField(
        label='Почта',
        widget=EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Почта',
            'id': 'floatingInput'
        })
    )
    user_from = CharField(
        label='Ваш город',
        widget=TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ваш город',
            'id': 'floatingInput',
            'required': 'False'
        })
    )
    class Meta:
        model=Profile
        fields= ('email', 'b_date', 'user_from', 'user_sex', 'bio')
        widgets = {
            'user_sex': Select(attrs={
                'id': 'floatingSelect',
                'class': 'form-select',
            }),
            'b_date': DateInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'required': False,
                'onfocus': "(this.type='date')",
            }),
            'bio': Textarea(attrs={
                'class': 'form-control',
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
        def check(str):
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            if (re.fullmatch(regex, str)):
                return(True)
            else:
                print(False)
        if b_date > date.today():
            self._errors['b_date'] = self.error_class([
                'Путешествия во времени вредны для вашего здоровья!'
            ])
        if not check(email):
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
                'class': 'form-control',
                'placeholder': 'Текст комментария'
            }),
        }
