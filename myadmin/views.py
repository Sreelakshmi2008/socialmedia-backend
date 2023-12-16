from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from authentication.api.serializers import UserRegisterSerializer,UserLoginSerializer,GetUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework import permissions
from rest_framework.authentication import authenticate
# from django.contrib.auth import authenticate
from authentication.models import CustomUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from posts.models import *
from posts.serializer import *

# Create your views here.


# get all registeres users 
class RegisteredUsers(APIView):
 
    def get(self,request):
        users = CustomUser.objects.filter(is_superuser=False)
        serializer = GetUserSerializer(instance=users, many=True)
        return Response(serializer.data,status=200)

# get details of user with a  email
class UserDetail(APIView):
 
    def get(self,request,userEmail):
        print(" requested for details of user")
        detail = CustomUser.objects.get(email=userEmail)
        print(detail)
        serializer = GetUserSerializer(instance=detail)
        print(serializer.data)
        return Response(serializer.data,status=200)



# delete user with id
class DeleteUser(APIView):
   
    def patch(self, request, id):
        try:
            user = CustomUser.objects.get(id=id)
            user.is_deleted = True
            user.save()
            return Response({"message": "success"}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            print("user not found")
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)


# block user with id
class BlockUser(APIView):
    def patch(self, request, id):
        try:
            user = CustomUser.objects.get(id=id)
            print(user.is_active,"in block fun checking user")
            b = user.is_active
            user.is_active = not b
            print(user.is_active,"after change")
            user.save()
            return Response({"message": "success"}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return Response({"message": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class DeletePost(APIView):
    def delete(self,request,id):
        try:
            p = Post.objects.get(id=id)
            p.delete()
            return Response({"message": "success"}, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            print("post not found")
            return Response({"message": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
       


class DeleteComment(APIView):
    permission_classes=[IsAdminUser]
    def delete(self,request,id):
        try:
            p = Comment.objects.get(id=id)
            p.delete()
            return Response({"message": "success"}, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            print("post not found")
            return Response({"message": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
       

class AdminUserPosts(APIView):
    permission_classes=[IsAdminUser]
    def get(self,request,userEmail):
        print(" requested for details of user")
        detail = CustomUser.objects.get(email=userEmail)
        print(detail)
        p = Post.objects.filter(user=detail)
        serializer = GetPostSerializer(instance=p,many=True)
        print(serializer.data)
        return Response(serializer.data,status=200)


class AdminUserPostsDetails(APIView):
    permission_classes=[IsAdminUser]
    def get(self,request,id):
        p = Post.objects.filter(id=id)
        serializer = GetPostSerializer(instance=p,many=True)
        print(serializer.data)
        return Response(serializer.data,status=200)

