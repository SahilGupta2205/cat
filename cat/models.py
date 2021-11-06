from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.core.validators import FileExtensionValidator, MinValueValidator, RegexValidator
from django.utils import timezone
from django.urls import reverse


# Create your models here.
class MyProfile(models.Model):
    name = models.CharField(max_length = 100)
    user = models.OneToOneField(to=User, on_delete=CASCADE)
    age = models.IntegerField(default="18", validators=[MinValueValidator(18)])
    address = models.CharField(max_length=200,null=True, blank=True)
    status = models.CharField(max_length=20, default="None", choices=(("single","single"), ("married","married"), ("None","None")))
    gender = models.CharField(max_length=20, default="None", choices=(("male","male"), ("female","female"),("other","other"),("None","None")))
    phone_no = models.CharField(validators=[RegexValidator("^0?[5-9]{1}\d{9}$")], max_length=15, null=True, blank=True)
    description = models.CharField(max_length=200,null=True, blank=True)
    pic=models.ImageField(upload_to = "images\\", null=True)
    def __str__(self):
        return "%s" % self.user

class MyPost(models.Model):
    pic=models.ImageField(upload_to = "images\\", null=True)
    # pic=models.VideoFeild()
    # pic = models.FileField(upload_to='videos_uploaded\\',null=True,validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])
    subject = models.CharField(max_length = 200)
    msg = models.TextField(null=True, blank=True)
    cr_date = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(to=MyProfile, on_delete=CASCADE, null=True, blank=True)
    def __str__(self):
        return "%s" % self.subject








class PostLike(models.Model):
    post = models.ForeignKey(to=MyPost, on_delete=CASCADE)
    liked_by = models.ForeignKey(to=MyProfile, on_delete=CASCADE)
    cr_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "%s" % self.liked_by

class PostComment(models.Model):
    post = models.ForeignKey(MyPost,related_name="comments", on_delete=CASCADE)
    msg = models.TextField()
    commented_by = models.ForeignKey(to=User, on_delete=CASCADE)
    cr_date = models.DateTimeField(auto_now_add=True)
    # flag = models.CharField(max_length=20, null=True, blank=True, choices=(("racist","racist"), ("abbusing","abbusing")))
    def __str__(self):
        return "%s - %s" % (self.post.subject, self.commented_by)
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.post.pk})


class FollowUser(models.Model):
    profile = models.ForeignKey(to=MyProfile, on_delete=CASCADE, related_name="profile")
    followed_by = models.ForeignKey(to=MyProfile, on_delete=CASCADE, related_name="followed_by")
    def __str__(self):
        return "%s is followed by %s" % (self.profile, self.followed_by)




