from django.contrib import admin
from .models import Post, User, Profile, Sex, Comment


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('title',),
    }

class UserAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('username',),
    }


admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(Sex)