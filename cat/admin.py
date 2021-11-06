
from django.contrib import admin
from cat.models import FollowUser, MyPost, MyProfile, PostLike
from django.contrib.admin.options import ModelAdmin
from .models import PostComment

class FollowUserAdmin(ModelAdmin):
    list_display = ["profile", "followed_by"]
    search_fields = ["profile", "followed_by"]
    list_filter = ["profile", "followed_by"]
admin.site.register(FollowUser, FollowUserAdmin)

class MyPostAdmin(ModelAdmin):
    list_display = ["subject", "cr_date","pic", "uploaded_by"]
    search_fields = ["subject", "msg", "uploaded_by"]
    list_filter = ["cr_date", "uploaded_by"]
admin.site.register(MyPost, MyPostAdmin)


class MyProfileAdmin(ModelAdmin):
    list_display = ["name","user", "phone_no", "pic"]
    search_fields = ["name", "status", "phone_no"]
    list_filter = ["status", "gender"]
admin.site.register(MyProfile, MyProfileAdmin)



class PostLikeAdmin(ModelAdmin):
    list_display = ["post", "liked_by"]
    search_fields = ["post", "liked_by"]
    list_filter = ["cr_date"]
admin.site.register(PostLike, PostLikeAdmin)



class PostCommentAdmin(admin.ModelAdmin):
    list_display = ["post","commented_by", "msg", "cr_date"]
    list_filter = ["commented_by","post"]
    # search_fields = ["msg", "MyPost__pic", "MyProfile__commented_by"]
admin.site.register(PostComment,PostCommentAdmin)