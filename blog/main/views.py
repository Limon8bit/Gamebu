from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, TemplateView, FormView, UpdateView
import logging
from django.views.generic.detail import SingleObjectMixin
from .form import LoginUserForm, PostForm, RegisterUserForm, CommentForm, ProfileForm
from .models import Post, User, Comment, Profile
from .utils import UserDataMixin


class Index(UserDataMixin, ListView):
    model = Post
    template_name = 'main/index.html'
    context_object_name = 'posts'
    logger = logging.getLogger('main_base')
    linecache = False

    def get_queryset(self):
        self.logger.info('Get posts from db', extra=super().get_user_data())
        return Post.objects.all().order_by('-publish_date')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Главная'
        context['comments'] = {}
        for post in self.get_queryset():
            context['comments'][post.pk] = context['comments_count'] = len(list(Comment.objects.filter(post=post)))
        return context


class About(TemplateView):
    template_name = 'main/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'О проекте'
        return context


class CreatePost(UserDataMixin, LoginRequiredMixin, CreateView):
    form_class = PostForm
    login_url = reverse_lazy('main:login')
    template_name = 'main/create_post.html'
    logger = logging.getLogger('main_create_post')

    def get_success_url(self):
        return reverse('main:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Создать пост'
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        self.logger.info('Create new post', extra=super().get_user_data())
        return super().post(request, *args, **kwargs)


class ShowPost(DetailView):
    model = Post
    template_name = 'main/show_post.html'
    slug_url_kwarg = 'post_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        post_id = Post.objects.get(slug=self.request.path.rsplit("/", 1)[1]).id
        context['comments'] = Comment.objects.filter(post=post_id)
        context['title'] = f'Пост {Post.objects.get(slug=self.request.path.rsplit("/", 1)[1]).title}'
        context['form'] = CommentForm()
        return context


class PostComment(SingleObjectMixin, FormView):
    model = Post
    form_class = CommentForm
    template_name = 'main/show_post.html'

    def get_form_kwargs(self):
        kwargs = super(PostComment, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        comment = form.save(commit=False)
        post = Post.objects.get(slug=self.request.path.rsplit("/", 1)[1])
        comment.__setattr__('post', post)
        comment.__setattr__('author', self.request.user)
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('main:show_post', kwargs={
            'post_slug': self.request.path.rsplit('/', 1)[1]
        })


class PostDetailView(View):
    def get(self, request, *args, **kwargs):
        view = ShowPost.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostComment.as_view()
        return view(request, *args, **kwargs)


class LoginUser(UserDataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'main/login.html'
    logger = logging.getLogger('main_user_activity')

    def get_context_data(self, **kwargs):
        context = super(LoginUser, self).get_context_data(**kwargs)
        context['title'] = 'Вход'
        return context

    def get_success_url(self):
        return reverse('main:index')

    def post(self, request, *args, **kwargs):
        self.logger.info('Login', extra=super().get_user_data())
        return super().post(request, *args, **kwargs)


class LogoutUser(LoginRequiredMixin, UserDataMixin, LogoutView):
    next_page = reverse_lazy('main:index')


class RegisterUser(UserDataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'main/register.html'
    success_url = reverse_lazy('main:login')
    logger = logging.getLogger('main_users_creating')

    def get_context_data(self, **kwargs):
        context = super(RegisterUser, self).get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context

    def post(self, request, *args, **kwargs):
        self.logger.info('', extra=super().get_user_data())
        return super().post(request, *args, **kwargs)


class Search(ListView):
    model = Post
    template_name = 'main/search.html'
    context_object_name = 'posts'

    def get_queryset(self):
        query = self.request.GET.get("q")
        post_list = Post.objects.filter(
            Q(title__icontains=query) | Q(text__icontains=query) |
            Q(title__icontains=query.capitalize()) | Q(text__icontains=query.capitalize())
        )
        return post_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['comments'] = {}
        for post in self.get_queryset():
            context['comments'][post.pk] = context['comments_count'] = len(list(Comment.objects.filter(post=post)))
        return context


class UserPage(ListView):
    model = User
    template_name = 'main/user.html'
    slug_url_kwarg = 'user_slug'
    context_object_name = 'posts'

    def select_template(self):
        if User.objects.get(slug=self.request.path.rsplit('/', 1)[1]) == self.request.user:
            self.template_name = 'main/my_profile.html'
        else:
            self.template_name = 'main/user.html'
        return self.template_name


    def get_queryset(self):
        post_list = Post.objects.filter(
            author=User.objects.get(slug=self.request.path.rsplit('/', 1)[1]).id
        ).order_by('-publish_date')
        return post_list

    def get_context_data(self, **kwargs):
        context = super(UserPage, self).get_context_data()
        context['author'] = User.objects.get(slug=self.request.path.rsplit('/', 1)[1])
        context['title'] = f"Страница пользователя: {context['author']}"
        context['owner'] = User.objects.get(slug=self.request.path.rsplit('/', 1)[1])
        context['comments'] = {}
        for post in self.get_queryset():
            context['comments'][post.pk] = context['comments_count'] = len(list(Comment.objects.filter(post=post)))
        return context




class MyProfile(LoginRequiredMixin, UserDataMixin, ListView):
    model = Post
    template_name = 'main/my_profile.html'
    context_object_name = 'posts'
    logger = logging.getLogger('main_base')

    def get_queryset(self):
        self.logger.info('Get posts from db', extra=super().get_user_data())
        return Post.objects.filter(author=self.request.user.id).order_by('-publish_date')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Моя страница'
        context['comments'] = {}
        for post in self.get_queryset():
            context['comments'][post.pk] = context['comments_count'] = len(list(Comment.objects.filter(post=post)))
        return context


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'main/update.html'
    pk_url_kwarg = 'user_pk'

    def get_form_class(self):
        return ProfileForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Редактирование профиля'
        return context
