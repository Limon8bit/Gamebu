from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import TextInput, CharField, PasswordInput, ModelForm, Textarea, FileInput, EmailInput, \
    DateInput, Select
from .models import Post, User, Comment


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
                'placeholder': 'Текст поста'
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
    email = CharField(
        label='Почта',
        widget=EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Почта',
            'id': 'floatingInput'
        })
    )
    b_date = CharField(
        label='Дата рождения',
        widget=DateInput(attrs={
            'class': 'form-control',
            'placeholder': 'Дата рождения',
            'type': 'date',
            'required': False
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
        fields = ['username', 'email', 'b_date', 'user_from', 'user_sex', 'password1', 'password2']
        widgets = {
            'user_sex': Select(attrs={
                'id': 'floatingSelect',
                'class': 'form-select',
            }),
        }


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
