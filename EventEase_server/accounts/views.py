from django.contrib.auth import get_user_model
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.compat import coreapi, coreschema
from rest_framework.schemas import coreapi as coreapi_schema
from rest_framework.schemas import ManualSchema
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.decorators import permission_classes,api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.authtoken.models import Token

from wallet.models import UserWallet

from services.models import FoodService
from .serializers import(TokenSerializer,RegisterSerializer,OTPSerializer,AdminUserSerializer,
ChangePasswordRequestedSerialzer, ChangePasswordRequestsSerializer, UpdatePasswordSerializer,
EmailVerifiedSerializer)
from .models import OTP,User,PasswordChangeRequested,EmailVerified
from .permissions import IsOwner,IsAdminUser,IsPhoneVerified
from . import utils

# throttle here for brute force
class Login(ObtainAuthToken):
    permission_classes = [AllowAny]
    serializer_class = TokenSerializer
    if coreapi_schema.is_enabled():
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    name="email",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="email",
                        description="Valid email for authentication",
                    ),
                ),
                coreapi.Field(
                    name="password",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Password",
                        description="Valid password for authentication",
                    ),
                ),
            ],
            encoding="application/json",
        )


@api_view(['POST', ])
def log_out(request):
    user = request.user
    # models.Model.delete(Token.objects.get(user = user)) we can also use this to delete the token
    user.auth_token.delete()    # auth_token here is some how auto generated by the framework
    return Response(status=status.HTTP_204_NO_CONTENT)

class Register(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token ,created= Token.objects.get_or_create(user=user)
            wallet = UserWallet.objects.create(user=user)
            wallet.save()
            return Response({'Token': token.key},status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
 # i think throttle here is important 
class GenerateOTP(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
            verification_code = utils.random_code()
            # utils.send_message(method = 'pywhatkit',number=self.validated,message=f"your verfication code for EventEase is {verification_code}")
            # use something diffrent than pywhatkit in production
            print(verification_code)
            otp ,created= OTP.objects.get_or_create(user = request.user)
            print(otp)
            if otp.is_verified == True:
                return Response({'message' : 'you are already verified'},status=status.HTTP_400_BAD_REQUEST)
            otp.code = verification_code
            otp.save()
            return Response({'code' : f'{otp}'},status=status.HTTP_201_CREATED)

# throttle here for brute force
class VerifyOTP(APIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = OTPSerializer
    def post(self,request):
        print('0')
        serializer = OTPSerializer(data = request.data)
        if serializer.is_valid():
            verify_code = OTP.objects.get(user = request.user)
            print('1')
            if verify_code.is_expired():
                return Response({'message' : 'code has expired'},status=status.HTTP_400_BAD_REQUEST)
            if serializer.validated_data['code'] != verify_code.code:
                return Response({'message' : 'code is wrong'}, status=status.HTTP_400_BAD_REQUEST)
            if verify_code.is_verified == True :
                return Response({'message' : 'already verified'},status=status.HTTP_400_BAD_REQUEST)
            verify_code.is_verified = True
            verify_code.save()
            print('2')
            return Response({'message' : 'Verification Completed'},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ListOTP(ListAPIView):
    permission_classes = [IsAdminUser,]
    serializer_class = OTPSerializer
    queryset = OTP.objects.all()

class DestroyOTP(APIView):
    permission_classes = [IsAdminUser]
    def delete(self,request,id):
        otp = OTP.objects.get(id = id)
        otp.delete()
        return Response({'message' : 'deleted successfully'}, status= status.HTTP_204_NO_CONTENT)
    
# throttle here
class ChangePasswordRequested(APIView):
    serializer_class = ChangePasswordRequestedSerialzer
    permission_classes = [AllowAny]
    def post(self,request):
        serializer = ChangePasswordRequestedSerialzer(data = request.data)
        if serializer.is_valid():
            user = get_user_model().objects.filter(email=serializer.validated_data['email']).first()
            change_password_request,created = PasswordChangeRequested.objects.get_or_create(user = user)
            change_password_request.is_requested = True
            change_password_request.save()
            # make the user number not verified for securtiy
            otp = OTP.objects.get(user = user)
            otp.is_verified = False
            otp.save()
            return Response({'message' : 'email found'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class UpdatePassword(APIView):
    serializer_class = UpdatePasswordSerializer
    permission_classes = [AllowAny]
    def post(self,request):
        serializer = UpdatePasswordSerializer(data = request.data)
        if serializer.is_valid():
            user = get_user_model().objects.filter(email=serializer.validated_data['_email']).first()
            print(user) # the output of case no user found is : <QuerySet []>
            if not user:
                return Response({'message':'there is no user with the provided email'},status=status.HTTP_404_NOT_FOUND)
            try:
                change_password_requested = PasswordChangeRequested.objects.get(user = user)
            except PasswordChangeRequested.DoesNotExist:
                return Response({'message':'there is not request to change password'},status=status.HTTP_403_FORBIDDEN)
        
            if not change_password_requested.is_requested :
                return Response({'message':'there is not request to change password'},status = status.HTTP_403_FORBIDDEN)
            try:
                otp = OTP.objects.get(user = user)
            except OTP.DoesNotExist:
                return Response({'message':'you should verify your number'},status = 452)
            if not otp.is_verified:
                return Response({'message':'you should verify your number'},status = 452)
            # Update the user's password
            serializer.update(user, serializer.validated_data)
            # return request status to False
            change_password_requested.is_requested = False
            change_password_requested.save()
            return Response({'message':'changed successfully'},status=status.HTTP_200_OK)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class ChangePassowrdRequests(ListAPIView):
    queryset = PasswordChangeRequested.objects.all()
    serializer_class = ChangePasswordRequestsSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser|IsOwner]
        elif self.action in['list','create']:
            self.permission_classes = [IsAdminUser]
        else:
            pass
        return super().get_permissions()


# verifying email via link
 # i think throttle here is important 
class GenerateVerificationLink(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
            verification_token = utils.generate_verification_token()
            email_verified ,created= EmailVerified.objects.get_or_create(user = request.user)
            print(verification_token)
            if email_verified.is_verified == True:
                return Response({'message' : 'your email is already verified'},status=status.HTTP_400_BAD_REQUEST)
            # utils.send_verifcation_link('reciever@gmail.com',verification_token)
            email_verified.verfication_token = verification_token
            email_verified.save()
            return Response({'Token' : verification_token},status=status.HTTP_201_CREATED)

# throttle here for brute force
class VerifyEmail(APIView):
    permission_classes = [IsAuthenticated,]
    def post(self,request):
        verification_token = request.query_params.get('Token')
        try :
            email_verified = EmailVerified.objects.get(user = request.user)
        except EmailVerified.DoesNotExist:
            return Response({'message' : 'you need to generate email verfication token first'},status=status.HTTP_400_BAD_REQUEST)
        if email_verified.is_expired():
            return Response({'message' : 'verfication link has expired'},status=status.HTTP_400_BAD_REQUEST)
        if verification_token != email_verified.verfication_token:
            return Response({'message' : 'verfication token is wrong'}, status=status.HTTP_400_BAD_REQUEST)
        if email_verified.is_verified == True :
            return Response({'message' : 'already verified'},status=status.HTTP_400_BAD_REQUEST)
        email_verified.is_verified = True
        email_verified.save()
        return Response({'message' : 'Verification Completed'},status=status.HTTP_200_OK)


class ListEmailVerified(ListAPIView):
    permission_classes = [IsAdminUser,]
    serializer_class = EmailVerifiedSerializer
    queryset = EmailVerified.objects.all()
