from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Post)
admin.site.register(PostMedia)
admin.site.register(Follow)
admin.site.register(Comment)
admin.site.register(HashTag)
admin.site.register(SavedPost)
admin.site.register(Like)
admin.site.register(Notification)