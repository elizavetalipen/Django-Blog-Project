from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserInfo, Post, Comment, Cathegory, Tag, Post_Tag, Post_Cathegory
from .forms import NewUserForm, LoginForm, PostForm, UserEditForm
from django.middleware import csrf
from django.utils import timezone


class TestLoginLogout(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.user = User.objects.create_user(username='testuser', email='testuser@test.com', 
                                             password='testpassword123')
        self.profile = UserInfo.objects.create(user=self.user,
                                avatar_image='https://res.cloudinary.com/dnkuhic7l/image/upload/v1683463431/blank_img_pgvahm.png', 
                                cover_image='https://res.cloudinary.com/dnkuhic7l/image/upload/v1683461446/cld-sample-2.jpg',
                                bio='Tell us about yourself')

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
        self.assertEqual(profile.bio, 'Tell us about yourself')

    def tearDown(self):
        User.objects.filter(username=self.user_data['username']).delete()
        self.existing_user.delete()


class TestUserProfile(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
            email='testuser@gmail.com',password='testpass123')
        
        self.profile = UserInfo.objects.create(user=self.user, 
                                avatar_image='https://res.cloudinary.com/dnkuhic7l/image/upload/v1683463431/blank_img_pgvahm.png', 
                                cover_image='https://res.cloudinary.com/dnkuhic7l/image/upload/v1683461446/cld-sample-2.jpg',
                                bio='Tell us about yourself')    

    def test_profile_view(self):
        response = self.client.get(reverse('profile', args=[self.user.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile/user_profile.html')
        self.assertContains(response, self.profile.bio)

    def test_password_change(self):
        self.client.login(username='testuser', password='testpass123')
        valid_data = {
            'old_password': 'testpass123',
            'new_password1': 'newtestpass123',
            'new_password2': 'newtestpass123'
        }
        invalid_data = {
            'old_password': 'wrongpass123',
            'new_password1': 'newtestpass',
            'new_password2': 'newtestpass'
        }
        # успешная смена пароля
        success_response = self.client.post(reverse('change_password'),valid_data)
        self.assertEqual(success_response.status_code, 302)
        self.assertRedirects(success_response, reverse('profile', kwargs={'pk': self.user.pk}))
        self.assertTrue(User.objects.get(username='testuser').check_password('newtestpass123'))
        # неуспешная смена пароля
        fail_response = self.client.post(reverse('change_password'),invalid_data)
        self.assertEqual(fail_response.status_code, 200)
        self.assertContains(fail_response, 'Your old password was entered incorrectly')
        self.assertFalse(User.objects.get(username='testuser').check_password('newtestpass'))
    
    def test_edit_profile(self):
        self.client.login(username='testuser', password='testpass123')
        profile_data = {
        'username': 'newusername',
        'email': 'newemail@gmail.com',
        'bio': 'Updated bio',}
        response = self.client.post(reverse('edit_profile'),profile_data)
        self.assertRedirects(response, reverse('profile', args=[self.user.pk]))
        self.user.refresh_from_db()
        # проверяем, что введенные данные сохранены
        self.assertEqual(self.user.username, 'newusername')
        self.assertEqual(self.user.email, 'newemail@gmail.com')
        self.assertEqual(self.user.userinfo.bio, 'Updated bio')

    def test_delete_profile(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('delete_profile'), {'password': 'testpass123'})
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(username='testuser').exists())
        self.assertFalse(UserInfo.objects.filter(user=self.user).exists())

    def tearDown(self):
        self.profile.delete()
        self.user.delete()

#посты
class TestPosts(TestCase):
    def setUp(self):
        self.client = Client()

        category = Cathegory.objects.create(title='Test')
        tag1 = Tag.objects.create(title='tag1')
        tag2 = Tag.objects.create(title='tag2')
        tags = [tag1, tag2]
        self.post_data =  {
            'title': 'Good post',
            'content': 'This is a new post',
            'tags': 'tag1,tag2',
            'category': category.id,}
        
        self.user = User.objects.create_user(
            username='testuser', password='testpass123')
        self.post = Post.objects.create(
            user=self.user, title='Test post', content='This is a test post')
        self.post.published = timezone.now()

        post_cat = Post_Cathegory.objects.create(post=self.post, cathegory_id=category.id)
        for tag in tags:
            post_tag = Post_Tag(post=self.post, tag=tag)


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


    def test_post_create(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('newpost'),self.post_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(title='Good post').exists())


    def test_post_edit(self):
        self.client.login(username='testuser', password='testpass123')
        category2 = Cathegory.objects.create(title='Another Test')
        tag3 = Tag.objects.create(title='tag3')
        edited_post_data = { 
            'title': 'Edited post',
            'content': 'This is an edited post',
            'tags': 'tag1,tag3',
            'category': category2.id,}
        response = self.client.post(reverse('edit_post', args=[self.post.pk]), edited_post_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(title='Edited post').exists())

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


        
  





