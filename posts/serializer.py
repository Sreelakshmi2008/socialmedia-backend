from rest_framework import serializers
from posts.models import *
from authentication.api.serializers import GetUserSerializer


class PostMediaSerializer(serializers.ModelSerializer):
    media_file = serializers.FileField(max_length=None, use_url=True)

    class Meta:
        model = PostMedia
        fields = ['id', 'media_file', 'uploaded_at']

    
    
class HashTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = HashTag
        fields = '__all__'
    


class GetPostSerializer(serializers.ModelSerializer):
    post_media = PostMediaSerializer(many=True, read_only=True)
    hashtags = HashTagSerializer(many=True,read_only=True)
    user=GetUserSerializer(read_only=True)
    is_following_author = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'user', 'caption', 'created_at', 'updated_at', 'post_media','hashtags','is_following_author']
    

    def get_user(self,obj):
        instance = obj.user
        user_ser = GetUserSerializer(instance)
        return user_ser.data

    
    
    def get_is_following_author(self, obj):
        request_user = self.context['request'].user
        user = obj.user
        if request_user.is_authenticated:
            try:
                follow_instance = Follow.objects.get(follower=request_user, following=user)
                return True
            except Follow.DoesNotExist:
                return False
        return False







class PostCreationSerializer(serializers.ModelSerializer):
    hashtags = HashTagSerializer(many=True,read_only=True)
    class Meta:
        model = Post
        fields = ['caption', 'user','hashtags']
        read_only_fields = ['user']  # Make the user field read-only

    def validate(self, data):
        # Set the user field to the current user during validation
        data['user'] = self.context['request'].user
        return data

    

class CommentSerializer(serializers.ModelSerializer):
   
    user=GetUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('content', 'commented_at', 'user','post')
        

    def create(self, validated_data):
        user = self.context['request'].user


        # Create the comment with the extracted user instance
        comment = Comment.objects.create(user=user, **validated_data)
        return comment
    def get_user(self,obj):
        print("object")
        instance = obj.user
        print(instance,"instance")
        user_ser = GetUserSerializer(instance)
        return user_ser.data




# ----------------------------------------------------------------

class AccountSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    followings_count = serializers.SerializerMethodField()

 
    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_followings_count(self, obj):
        return obj.following.count()  

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "name",
            "username",
            "email",
            "profile_pic",
            "last_login",
            "is_staff",
            "is_active",
            "is_superuser",
            "followers_count",
            "followings_count",
        ]




class FollowSerializer(serializers.ModelSerializer):
    following = serializers.SlugRelatedField(
        slug_field="email", queryset=CustomUser.objects.all()
    )
    follower = serializers.SlugRelatedField(
        slug_field="email", queryset=CustomUser.objects.all()
    )

    class Meta:
        model = Follow
        fields = ["follower", "following", "created_at"]


# serializers.py

class FollowerSerializer(serializers.ModelSerializer):
    follower = AccountSerializer(read_only=True)
    is_following_follower = serializers.SerializerMethodField()

    def get_is_following_follower(self, obj):
        user = self.context['request'].user
        follower = obj.follower
        if user.is_authenticated:
            try:
                follow_instance = Follow.objects.get(follower=user, following=follower)
                return True
            except Follow.DoesNotExist:
                return False
        return False

    class Meta:
        model = Follow
        fields = ["follower", "created_at", "is_following_follower"]


class FollowingSerializer(serializers.ModelSerializer):
    following = AccountSerializer( read_only=True)

    class Meta:
        model = Follow
        fields = ["following", "created_at"]







