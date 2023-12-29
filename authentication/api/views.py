
from rest_framework.response import Response
from rest_framework import status,generics
from rest_framework.views import APIView
from authentication.api.serializers import UserRegisterSerializer,UserLoginSerializer,GetUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import permissions
from rest_framework.authentication import authenticate
# from django.contrib.auth import authenticate
from authentication.models import CustomUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import api_view, permission_classes
import requests
from authentication import helper
from .serializers import *
from django.db.models import Count,Q
from django.db.models.functions import ExtractMonth, ExtractYear
from django.utils import timezone
from posts.serializer import *
# user regiatration  view
class RegisterView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser]

    def post(self, request):
        data = request.data
        print(data)

        #fetched data sending to serializer
        serializer = UserRegisterSerializer(data=data)
        if serializer.is_valid():

            # if valid user is created using serializer
            user = serializer.save()
            print(serializer.data,"serializer data")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        data = request.data
        print(data)
       
        # fetched data sending to serializer
        serializer = UserLoginSerializer(data=data)
        print(serializer)
        
        if serializer.is_valid(raise_exception=True):
            # If valid data fetched
            email_or_username = serializer.validated_data['email_or_username']
            password = serializer.validated_data['password']
            
            try:
                # authenticate with email or username
                user = authenticate(request, username=email_or_username, password=password)
                print(user)
                
                # if user instance is returned and create token and considered as user logged in
                if user:
                    if user.is_deleted:
                        return Response({"details": "This account has been deleted."}, status=401)

                    print("success login")
                    refresh = RefreshToken.for_user(user)
                    refresh['email'] = user.email
                    refresh['is_superuser'] = user.is_superuser
                    access_token = str(refresh.access_token)
                    refresh_token = str(refresh)

                    return Response(
                        {
                            "email_or_username": email_or_username,
                            "password": password,
                            "access": access_token,
                            "refresh": refresh_token,
                        },
                        status=201,
                    )
                else:
                    # If user is None, wrong email or password
                    return Response({"details": "Invalid email or password"}, status=401)

            except CustomUser.DoesNotExist:
                # If user doesn't exist, wrong email or password
                return Response({"details": "no user email or password"}, status=401)

# get details of logged in user
class GetUserView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
 
    def get(self,request):
    
        user_email = request.user
        print(request.user)
        user_details = CustomUser.objects.get(email=user_email)
        serializer = AccountSerializer(instance=user_details,context={'request':request})
        print(serializer.data)
        return Response(serializer.data,status=200)


from google.auth.transport.requests import Request as AuthRequest
from google.oauth2 import id_token
class GoogleLoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        token = request.data['google_token']
        try:
            auth_request = AuthRequest()

            # Validate the Google OAuth token
            id_info = id_token.verify_oauth2_token(token, auth_request)

            user_email = id_info['email']

            print(user_email)
            
            try:
                print("try")
                user_exist = CustomUser.objects.get(email=user_email)
                if user_exist.is_deleted:
                        return Response({"details": "This account has been deleted."}, status=401)

                print("success login")
                refresh = RefreshToken.for_user(user_exist)
                refresh['email'] = user_exist.email
                refresh['is_superuser'] = user_exist.is_superuser
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)

                return Response(
                    {
                        "email_or_username": user_email,
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                    status=201,
                )
            except CustomUser.DoesNotExist:
                print("except")
                return Response({"details": "User does not exist."}, status=status.HTTP_401_UNAUTHORIZED)

        except ValueError as e:
            return Response({'error': f'Invalid token: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
         
      
from django.conf import settings

class ChangeProfilePicView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    parser_classes = [MultiPartParser]
    def patch(self,request):
        print(request.data)
        u = request.user
        print(request.data.get('profile_pic'))
        u.profile_pic = request.data.get('profile_pic')
        u.save()
        print(u.profile_pic)
        full_path = f"{settings.CUSTOM_DOMAIN}{settings.MEDIA_URL}{u.profile_pic}"
        print(full_path)
        return Response({'message':"success",'updatedProfilePic':full_path},status=200)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def CheckAuth(request):
    # If the view reaches here, the user is authenticated
    return Response({'message': 'Authenticated'})



class EditProfileView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    
    def patch(self,request):
        print(request.data)
        u = request.user
        u.username = request.data.get('username')
        u.name = request.data.get('name')
        u.email = request.data.get('email')
        u.phone = request.data.get('phone')
        u.save()
        return Response({'message':"success"},status=200)
    

class OtpSent(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        print(request.user)
        user = request.user
        mobile = user.phone
        if user:  #if user exists
            helper.send('+91' + str(mobile))
            return Response({'message':"success"},status=200)
        else:
            return Response({'message':"User Not Found"},status=401)
            

class OtpVerify(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request):
        # Extract 'otp' from the query parameters
     
        otp = request.data.get('otp')
        user = request.user
        mobile = user.phone
        print(mobile,otp)
        if helper.check('+91' + str(mobile), otp):
                print(user,"this is user")
                return Response({'message':"succes"},status=200)
        else:
                return Response({'message':"Invalid Otp"},status=400)


class ChangePassword(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    
    def patch(self,request):
        print(request.data)
        u = request.user
        if u:
            password = request.data['password']
            print(u.password," before changing")
            u.password = make_password(password)
            u.save()
            print(u.password," after changing")
            
            return Response({'message':"success"},status=200)
        else:
            return Response({'message':"fail"},status=status.HTTP_400_BAD_REQUEST)

    

from django.db.models import F


   
class JoiningMonthCountView(APIView):
    
    def get(self, request):
        
        user_counts = (
            CustomUser.objects.annotate(
                joining_month=F('date_joined__month'),
                joining_year=F('date_joined__year')
            )
            .values('joining_month', 'joining_year')
            .annotate(user_count=Count('id'))
            .order_by('joining_year', 'joining_month')
        )
        print(user_counts)
        serializer = JoiningMonthCountSerializer(user_counts, many=True)

        return Response(serializer.data)
    



class CustomUserSearchAPIView(APIView):
    def get(self, request, *args, **kwargs):
        query = request.query_params.get('query', None)

        if not query:
            return Response({'error': 'Query parameter "query" is required'}, status=status.HTTP_400_BAD_REQUEST)

        queryset = CustomUser.objects.filter(Q(username__icontains=query)|Q(name__icontains=query)).exclude(pk=request.user.id)
        print(queryset)
        


        serializer = GetUserSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetOtherUserView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = AccountSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance,context={'request':request})
       
        post_serializer = GetPostSerializer( Post.objects.filter(user=instance)
        , many=True,context={'request':request})

        return Response({'posts': post_serializer.data,'user_data': serializer.data})