from rest_framework import serializers
from authentication.models import CustomUser
from django.contrib.auth.hashers import make_password



# user register serializer
class UserRegisterSerializer(serializers.ModelSerializer): 
    print("serializer for registering user")
    profile_pic = serializers.ImageField(required=False)  # Update the field definition

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'name', 'phone','profile_pic')

    # create user
    def create(self, data):
        print("Create method in UserRegisterSerializer is called")

        profile_pic = data.pop('profile_pic', None)
        user = CustomUser.objects.create_user(**data,profile_pic=profile_pic)
        
        print(user)
        return user



class UserLoginSerializer(serializers.Serializer):
    email_or_username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)
    
   
    def validate(self, data):
        email_or_username = data.get('email_or_username')
        password = data.get('password')
        print(data,"serializer data")
    
        return data
class GetUserSerializer(serializers.ModelSerializer):
     class Meta:
        model = CustomUser
        fields = '__all__'

