from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserInfo, Post, Comment, Cathegory
from .forms import NewUserForm, LoginForm
from django.middleware import csrf
from django.utils import timezone


class TestLoginLogout(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.user = User.objects.create_user(username='testuser', email='testuser@test.com', 
                                             password='testpassword123')
        self.profile = UserInfo.objects.create(user=self.user, avatar_image='images/userimg/blank_img.png', 
                                                    cover_image='images/userimg/blank_cover.jpg',bio='...',)

    def test_login_success(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword123',
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_failure(self):
        data = {
            'username': 'testuser',
            'password': 'wrongpassword',
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_logout(self):
        self.client.force_login(self.user)
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def tearDown(self):
        self.user.delete()
        self.profile.delete()


class TestRegister(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        self.existing_user = User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='existingpass123'
        )

    def test_successful(self):
        response = self.client.post(reverse('register'), self.user_data, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_user_created(self):
        self.client.post( reverse('register'), data=self.user_data)
        user = User.objects.filter(username=self.user_data['username']).first()
        self.assertIsNotNone(user)

    def test_username_exists(self):
        self.user_data['username'] = self.existing_user.username
        response = self.client.post(reverse('register'), self.user_data)
        form = response.context['register_form']
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], ['A user with that username already exists.'])

    def test_email_exists(self):
        self.user_data['email'] = self.existing_user.email
        response = self.client.post(reverse('register'), self.user_data)
        form = response.context['register_form']
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['User with such email already exists!'])

    def test_default_profile_created(self):
        self.client.post(reverse('register'), data=self.user_data)
        user = User.objects.filter(username=self.user_data['username']).first()
        profile = UserInfo.objects.filter(user=user).first()
        self.assertIsNotNone(profile)
        self.assertEqual(profile.avatar_image.name, 'images/userimg/blank_img.png')
        self.assertEqual(profile.cover_image.name, 'images/userimg/blank_cover.jpg')
        self.assertEqual(profile.bio, '...')

    def tearDown(self):
        User.objects.filter(username=self.user_data['username']).delete()
        self.existing_user.delete()


class TestUserProfile(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
            email='testuser@example.com',password='testpass123')
        
        self.profile = UserInfo.objects.create(user=self.user, avatar_image='images/userimg/blank_img.png', 
                                                    cover_image='images/userimg/blank_cover.jpg',bio='...',)    

    def test_profile_view(self):
        response = self.client.get(reverse('profile', args=[self.user.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile/user_profile.html')
        self.assertContains(response, self.profile.bio)
    
    def test_edit_profile(self):
        pass

    def test_delete_profile(self):
        pass

    def tearDown(self):
        self.profile.delete()
        self.user.delete()

#посты
class TestPosts(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpass123')
        self.post = Post.objects.create(
            user=self.user,title='Test post',content='This is a test post',)

    def test_post_view(self):
        response = self.client.get(reverse('post', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.content)
        self.assertContains(response, self.post.user)

    def test_post_delete(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('delete_post', args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

    # add tags and cathegory
    # test post create
    # test post edit 

    def tearDown(self):
        self.post.delete()
        self.user.delete()


# комментарии
class TestComments(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        self.post = Post.objects.create(
            title='Test Post', user=self.user, content='Test Content'
        )
        self.comment = Comment.objects.create(
            post=self.post, user=self.user, content='Test Comment'
        )

    def test_comment_edit(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('edit_comment', kwargs={'pk': self.comment.pk})
        response = self.client.post(url, data={'content': 'Updated Comment'})
        self.assertEqual(response.status_code, 302)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, 'Updated Comment')
        self.assertIsNotNone(self.comment.edited)

    def test_comment_delete(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('delete_comment', kwargs={'pk': self.comment.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())

    def tearDown(self):
        self.comment.delete()
        self.post.delete()
        self.user.delete()

        
  





