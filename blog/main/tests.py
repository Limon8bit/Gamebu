from django.test import TestCase

from .models import Post, User, Comment


class PostModelTest(TestCase):
    def setUp(self):
        User.objects.create_user(
            username='admin',
            id=1,
            email='admn@admin.com',
            slug='admin',
            password='admin',
        )

        Post.objects.create(
            title='some_post',
            text='text_of_some_post',
            image=None,
            author=User.objects.get(id=1),
        )

    def test_model_data(self):
        post = Post.objects.get(title='some_post')
        self.assertEqual(post.author.username, 'admin')


class CommentAuthorModelTest(TestCase):
    def setUp(self):
        User.objects.create_user(
            username='admin',
            id=1,
            email='admn@admin.com',
            slug='admin',
            password='admin',
        )

        Post.objects.create(
            title='some_post',
            text='text_of_some_post',
            image=None,
            author=User.objects.get(id=1),
        )

        Comment.objects.create(
            text='comment_text',
            author=User.objects.get(id=1),
            post=Post.objects.get(title='some_post'),
        )

    def test_model_data(self):
        comment = Comment.objects.get(text='comment_text')
        self.assertEqual(comment.author.username, 'admin')


class FullCommentModelTest(TestCase):
    def setUp(self):
        User.objects.create_user(
            username='admin',
            id=1,
            email='admn@admin.com',
            slug='admin',
            password='admin',
        )

        Post.objects.create(
            title='some_post',
            text='text_of_some_post',
            image=None,
            author=User.objects.get(id=1),
        )

        Comment.objects.create(
            text='comment_text',
            author=User.objects.get(id=1),
            post=Post.objects.get(title='some_post'),
        )

    def test_model_data(self):
        comment = Comment.objects.get(text='comment_text')
        self.assertTrue(comment.author.username == 'admin' and
                        comment.post.title == 'some_post')
