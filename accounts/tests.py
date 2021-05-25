from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile
from rest_framework.test import APIClient
from blog.models import Post, Comment, PostLike, CommentLike


class TestProfileModel(TestCase):
    def setUp(self):
        self.user_data = {
            "username": "JohnDoe",
            "password": "JoanaDoe",
            "email": "johndoe@mail.com",
        }

        self.profile_data = {
            "username": "JohnDoe",
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@mail.com",
        }

        self.post_data = {
            "title": "Best book ever!",
            "content": "This book is really awesome!",
        }

    def _test_user_must_have_a_profile(self):
        user = User.objects.create_user(**self.user_data)
        profile = Profile.objects.create(**self.profile_data, user=user)

        user = User.objects.get(pk=1)

        self.assertEqual(profile.user, user)
        self.assertEqual(user.profile, profile)

    def _test_profile_can_create_posts(self):
        user = User.objects.create_user(**self.user_data)
        profile = Profile.objects.create(**self.profile_data, user=user)

        post = Post.objects.create(**self.post_data, profile=profile)

        profile.posts.add(post)
        profile = Profile.objects.get(pk=1)

        self.assertEqual(profile.posts.all().count(), 1)
        self.assertEqual(profile.posts.first(), post)

    def _test_profile_can_create_comments_on_posts(self):
        user = User.objects.create_user(**self.user_data)
        profile = Profile.objects.create(**self.profile_data, user=user)

        post = Post.objects.create(**self.post_data, profile=profile)

        comment = Comment.objects.create(
            **self.comment_data, profile=profile, post=post
        )

        post.comments.add(comment)
        profile.posts.add(post)

        profile = Profile.objects.get(pk=1)

        self.assertEqual(profile.posts.first().comments.all().count(), 1)
        self.assertEqual(profile.posts.first().comments.first(), comment)

    def _test_profile_can_create_like_in_comments(self):
        user = User.objects.create_user(**self.user_data)
        profile = Profile.objects.create(**self.profile_data, user=user)

        post = Post.objects.create(**self.post_data, profile=profile)

        comment = Comment.objects.create(
            **self.comment_data, profile=profile, post=post
        )
        post.comments.add(comment)
        profile.posts.add(post)

        like = CommentLike.objects.create(profile=profile, comment=comment)

        profile.posts.first().comments.first().likes.add(like)
        profile = Profile.objects.get(pk=1)

        self.assertEquals(profile.posts.first().comments.first().likes.first(), like)
        self.assertEquals(profile.posts.first().comments.first().likes.all().count(), 1)

    def _test_profile_cant_like_comments_twice(self):
        user = User.objects.create_user(**self.user_data)
        profile = Profile.objects.create(**self.profile_data, user=user)

        post = Post.objects.create(**self.post_data, profile=profile)

        comment = Comment.objects.create(
            **self.comment_data, profile=profile, post=post
        )
        post.comments.add(comment)
        profile.posts.add(post)

        like = CommentLike.objects.create(profile=profile, comment=comment)

        profile.posts.first().comments.first().likes.add(like)
        like = CommentLike.objects.create(profile=profile, comment=comment)

        profile.posts.first().comments.first().likes.add(like)
        profile = Profile.objects.get(pk=1)

        self.assertEquals(profile.posts.first().comments.first().likes.first(), like)
        self.assertEquals(profile.posts.first().comments.first().likes.all().count(), 1)

    def _test_profile_can_create_like_in_posts(self):
        user = User.objects.create_user(**self.user_data)
        profile = Profile.objects.create(**self.profile_data, user=user)

        post = Post.objects.create(**self.post_data, profile=profile)

        profile.posts.add(post)

        like = PostLike.objects.create(profile=profile, post=post)

        profile.posts.first().add(like)
        profile = Profile.objects.get(pk=1)

        self.assertEquals(profile.posts.first().likes.first(), like)
        self.assertEquals(profile.posts.first().likes.all().count(), 1)

    def _test_profile_can_follow_profiles(self):
        user = User.objects.create_user(**self.user_data)
        user_1 = User.objects.create_user(**self.user_data_1)

        profile_0 = Profile.objects.create(**self.profile_data, user=user)
        profile_1 = Profile.objects.create(**self.profile_data_1, user=user_1)

        profile_0.following.add(profile_1)
        self.assertEquals(profile_0.following.first(), profile_1)
        self.assertEquals(len(profile_0.followers.all()), 0)
        self.assertEquals(len(profile_1.followers.all()), 1)

        profile_1.following.add(profile_0)
        self.assertEquals(profile_1.following.first(), profile_0)
        self.assertEquals(len(profile_0.followers.all()), 1)

    def _test_profile_cant_like_post_more_than_once(self):
        user = User.objects.create_user(**self.user_data)
        profile = Profile.objects.create(**self.profile_data, user=user)

        post = Post.objects.create(**self.post_data, profile=profile)

        profile.posts.add(post)

        like_0 = PostLike.objects.create(profile=profile, post=post)
        profile.posts.first().add(like_0)

        like = PostLike.objects.create(profile=profile, post=post)
        profile.posts.first().add(like)

        like = PostLike.objects.create(profile=profile, post=post)
        profile.posts.first().add(like)

        profile = Profile.objects.get(pk=1)

        self.assertEquals(profile.posts.first().likes.first(), like_0)
        self.assertEquals(profile.posts.first().likes.all().count(), 1)

    def _test_profile_cant_like_comments_more_than_once(self):
        user = User.objects.create_user(**self.user_data)
        profile = Profile.objects.create(**self.profile_data, user=user)

        post = Post.objects.create(**self.post_data, profile=profile)
        comment = Comment.objects.create(**self.comment_data, post=post)
        post.comments.add(comment)
        profile.posts.add(post)

        like_0 = CommentLike.objects.create(profile=profile, comment=comment)
        profile.posts.first().comments.first().add(like_0)

        like = CommentLike.objects.create(profile=profile, comment=comment)
        profile.posts.first().comments.first().add(like)

        like = CommentLike.objects.create(profile=profile, comment=comment)
        profile.posts.first().comments.first().add(like)

        profile = Profile.objects.get(pk=1)

        self.assertEquals(profile.posts.first().comments.first().likes.first(), like_0)
        self.assertEquals(profile.posts.first().comments.first().likes.all().count(), 1)


class TestAccountsView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.account_info = {
            "username": "JohnDoea",
            "password": "JoanaDoe",
            "email": "john@email.com",
        }

    def test_user_can_login(self):
        User.objects.create_user(**self.account_info)
        response = self.client.post("/accounts/login/", self.account_info)
        self.assertTrue(response.json()["token"] is not None)

    def test_user_can_create_account(self):
        response = self.client.post("/accounts/", self.account_info)

        self.assertEquals(response.status_code, 201)
        self.assertDictContainsSubset(response.json(), self.account_info)
