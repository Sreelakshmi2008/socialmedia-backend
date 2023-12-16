from django.db import models
from authentication.models import CustomUser
import uuid

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    caption = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    hashtags = models.ManyToManyField('HashTag',related_name='hash')

    def __str__(self):
        return f"{self.user.username} ---- {self.caption} ---- {self.created_at}"


    


class PostMedia(models.Model):
    post = models.ForeignKey(Post, related_name='post_media', on_delete=models.CASCADE)
    media_file = models.FileField(upload_to='post_media/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.post.user.username}-{self.post.caption}-{self.media_file} - {self.uploaded_at}"



class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)

    
class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content =  models.TextField()
    commented_at = models.DateTimeField(auto_now_add=True)



class HashTag(models.Model):
    hashtag = models.CharField(null=True,max_length=50)
    def __str__(self):
        return self.hashtag





class Follow(models.Model):
    follower = models.ForeignKey(
        CustomUser, related_name="following", on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        CustomUser, related_name="followers", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"

    def followers_count(self):
        return self.followers.count()

    def following_count(self):
        return self.following.count()
