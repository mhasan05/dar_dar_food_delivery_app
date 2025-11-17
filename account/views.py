from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from utils.common_function import user_token
from utils.db import DB
from django.db import transaction
import logging
from django.core.exceptions import ValidationError
from .models import *
from django.contrib.auth.password_validation import validate_password
from rest_framework import status,permissions
from utils.common_function import send_otp
from django.utils import timezone
from .serializers import *
logger = logging.getLogger(__name__)

#User Auth Views Start
32446
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"status":"error","message": "Email and password are required."}, status=400)

        user = authenticate(email=email.lower(), password=password)
        if not user:
            return Response({"status":"error","message": "Invalid email or password."}, status=400)
        if not user.is_active:
            return Response({"status":"error","message": "Account not verified. Please verify OTP."}, status=403)
        
        if str(user.role).upper() != "USER":
            if not user.is_approved:
                return Response({"status":"error","message": "Account not approved. Please wait for approval."}, status=403)

        tokens = user_token(user)
        
        if str(user.role).upper() == "USER":
            user = UserProfile.objects.filter(email=user.email).first()
            serializers = UserProfileSerializer(user)
        elif str(user.role).upper() == "RIDER":
            user = RiderProfile.objects.filter(email=user.email).first()
            serializers = RiderProfileSerializer(user)
        elif str(user.role).upper() == "VENDOR":
            user = VendorProfile.objects.filter(email=user.email).first()
            serializers = VendorProfileSerializer(user)
        elif str(user.role).upper() == "ADMIN":
            user = UserAuth.objects.filter(email=user.email).first()
            serializers = AdminProfileSerializer(user)
        return Response({
            "status":"success",
            "message": "Login successful.",
            "access_token": tokens,
            "data": serializers.data
        }, status=200)

class SignupView(APIView):
    def post(self, request):
        full_name = request.data.get('full_name')
        email = request.data.get('email')
        phone_number = request.data.get('phone_number')
        role = request.data.get('role')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')

        if password != confirm_password:
            return Response({"status": "error", "message": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

        if not email or not password:
            return Response({"status": "error", "message": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_password(password)
        except ValidationError as e:
            return Response({"status": "error", "message": f"Password error: {', '.join(e.messages)}"}, status=status.HTTP_400_BAD_REQUEST)

        if UserAuth.objects.filter(email=email.lower()).exists():
            return Response({"status": "error", "message": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        if UserAuth.objects.filter(phone_number=phone_number).exists():
            return Response({"status": "error", "message": "Phone number already exists."}, status=status.HTTP_400_BAD_REQUEST)
        if role.upper() not in ["USER", "RIDER", "VENDOR", "ADMIN"]:
                    return Response({"status": "error", "message": "Invalid role."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                if role.upper() == "USER":
                    user = UserProfile.objects.create_user(full_name=full_name, email=email.lower(),role=role.upper(), phone_number=phone_number, password=password,is_approved=True)
                    user.save()
                elif role.upper() == "RIDER":
                    user = RiderProfile.objects.create_user(full_name=full_name, email=email.lower(),role=role.upper(), phone_number=phone_number, password=password)
                    user.save()
                elif role.upper() == "VENDOR":
                    user = VendorProfile.objects.create_user(full_name=full_name, email=email.lower(),role=role.upper(), phone_number=phone_number, password=password)
                    user.save()
            sent_email = send_otp(user)

            if not sent_email:
                return Response({"status": "error", "message": "Something went wrong, please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({"status": "success", "message": "Account created successfully. Please verify your email."}, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            return Response({"status": "error", "message": "Something went wrong, please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VerifyOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        try:
            user = UserAuth.objects.get(email=email)
        except UserAuth.DoesNotExist:
            return Response({"status":"error","message": "User not found."}, status=404)
        if user.otp != otp:
            return Response({"status":"error","message": "Invalid OTP."}, status=400)
        if timezone.now() > user.otp_expired:
            return Response({"status":"error","message": "OTP expired. Please request a new one."}, status=400)
        

        user.is_active = True
        user.otp = None
        user.otp_expired = None
        user.save()
        tokens = user_token(user)
        return Response({"status":"success","message": "Account verified successfully.","access_token":tokens}, status=200)

class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = UserAuth.objects.get(email=email)
        except UserAuth.DoesNotExist:
            return Response({"status":"error","message": "User not found."}, status=404)

        sent_email = send_otp(user)
        if not sent_email:
            return Response({"status":"error","message": "Something went wrong, please try again later."}, status=500)
        return Response({"status":"success","message": "OTP sent to your email for password reset."}, status=200)

class ResetPasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        # --- Validation layer ---
        if not new_password or not confirm_password:
            return Response({"status":"error","message": "Both new and confirm passwords are required."}, status=400)
        if len(new_password) < 8:
            return Response({"status":"error","message": "New password must be at least 8 characters long."}, status=400)
        if confirm_password != new_password:
            return Response({"status":"error","message": "Password doesn't match."}, status=400)

        user = request.user
        
        user.set_password(new_password)
        user.save()
        return Response({"status":"success","message": "Password reset successfully."}, status=200)

class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        # --- Validation layer ---
        if not old_password or not new_password:
            return Response({"status":"error","message": "Both old and new passwords are required."}, status=400)
        if len(new_password) < 8:
            return Response({"status":"error","message": "New password must be at least 8 characters long."}, status=400)
        if old_password == new_password:
            return Response({"status":"error","message": "New password cannot be same as old password."}, status=400)

        user = request.user
        if not user.check_password(old_password):
            return Response({"status":"error","message": "Old password is incorrect."}, status=400)

        user.set_password(new_password)
        user.save()
        return Response({"status":"success","message": "Password changed successfully."}, status=200)

class ResendOTPView(APIView):
    """
    Allows users to request a new OTP if the previous one expired or they didn’t receive it.
    """
    def post(self, request):
        email = request.data.get('email')
        try:
            user = UserAuth.objects.get(email=email)
        except UserAuth.DoesNotExist:
            return Response({"status":"error","message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        sent_email = send_otp(user)
        if not sent_email:
            return Response({"status":"error","message": "Something went wrong, please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(
            {"status":"success","message": "A new OTP has been sent to your email."},
            status=status.HTTP_200_OK
        )

class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request,pk=None):
        if pk:
            user = UserAuth.objects.filter(pk=pk).first()
        else:
            user = request.user
        if user:
            if str(user.role).upper() == 'ADMIN':
                user = UserAuth.objects.filter(email=user.email).first()
                serializer = AdminProfileSerializer(user)
            elif str(user.role).upper() == 'USER':
                user = UserProfile.objects.filter(email=user.email).first()
                serializer = UserProfileSerializer(user)
            elif str(user.role).upper() == 'RIDER':
                user = RiderProfile.objects.filter(email=user.email).first()
                serializer = RiderProfileSerializer(user)
            elif str(user.role).upper() == 'VENDOR':
                user = VendorProfile.objects.filter(email=user.email).first()
                serializer = VendorProfileSerializer(user)
            return Response({"status":"success","data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status":"error","message": "User not found."}, status=status.HTTP_404_NOT_FOUND)

class UpdateUserProfile(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request,pk=None):
        if pk:
            user = UserAuth.objects.filter(pk=pk).first()
            if not user:
                return Response({"status":"error","message": "User not found."}, status=404)
        else:
            user = request.user
        data = request.data
        update_fields=[]

        if str(user.role).upper() == 'ADMIN':
            if 'full_name' in data:
                user.full_name = data.get('full_name')
                update_fields.append('full_name')
            if 'phone_number' in data:
                user.phone_number = data.get('phone_number')
                update_fields.append('phone_number')
            user.save(update_fields=update_fields)
            serializers = AdminProfileSerializer(user)
        
        elif str(user.role).upper() == 'USER':
            user = UserProfile.objects.filter(email=user.email).first()
            if 'full_name' in data:
                user.full_name = data.get('full_name')
                update_fields.append('full_name')
            if 'phone_number' in data:
                user.phone_number = data.get('phone_number')
                update_fields.append('phone_number')
            if 'image' in request.FILES:
                user.image = request.FILES['image']
                update_fields.append('image')
            if 'address' in data:
                user.address = data.get('address')
                update_fields.append('address')
            user.save(update_fields=update_fields)
            serializers = UserProfileSerializer(user)

        elif str(user.role).upper() == 'VENDOR':
            user = VendorProfile.objects.filter(email=user.email).first()
            if 'full_name' in data:
                user.full_name = data.get('full_name')
                update_fields.append('full_name')
            if 'phone_number' in data:
                user.phone_number = data.get('phone_number')
                update_fields.append('phone_number')
            if 'image' in request.FILES:
                user.image = request.FILES['image']
                update_fields.append('image')
            if 'shop_name' in data:
                user.shop_name = data.get('shop_name')
                update_fields.append('shop_name')
            if 'shop_image' in request.FILES:
                user.shop_image = request.FILES['shop_image']
                update_fields.append('shop_image')
            if 'shop_license' in data:
                user.shop_license = data.get('shop_license')
                update_fields.append('shop_license')
            if 'shop_type' in data:
                user.shop_type = data.get('shop_type')
                update_fields.append('shop_type')
            if 'shop_address' in data:
                user.shop_address = data.get('shop_address')
                update_fields.append('shop_address')
            if 'bank_name' in data:
                user.bank_name = data.get('bank_name')
                update_fields.append('bank_name')
            if 'account_name' in data:
                user.account_name = data.get('account_name')
                update_fields.append('account_name')
            if 'account_number' in data:
                user.account_number = data.get('account_number')
                update_fields.append('account_number')
            if 'branch' in data:
                user.branch = data.get('branch')
                update_fields.append('branch')
            user.save(update_fields=update_fields)
            serializers = VendorProfileSerializer(user)

        elif str(user.role).upper() == 'RIDER':
            user = RiderProfile.objects.filter(email=user.email).first()
            if 'full_name' in data:
                user.full_name = data.get('full_name')
                update_fields.append('full_name')
            if 'phone_number' in data:
                user.phone_number = data.get('phone_number')
                update_fields.append('phone_number')
            if 'image' in request.FILES:
                user.image = request.FILES['image']
                update_fields.append('image')
            if 'vehicle_type' in data:
                user.vehicle_type = data.get('vehicle_type')
                update_fields.append('vehicle_type')

            if 'license_number' in data:
                user.license_number = data.get('license_number')
                update_fields.append('license_number')

            if 'vehicle_plate' in data:
                user.vehicle_plate = data.get('vehicle_plate')
                update_fields.append('vehicle_plate')

            if 'availability_status' in data:
                user.availability_status = data.get('availability_status')
                update_fields.append('availability_status')
            user.save(update_fields=update_fields)
            serializers = RiderProfileSerializer(user)

        

        return Response(
            {"status": "success", "message": "Profile updated successfully.", "data": serializers.data},
            status=status.HTTP_200_OK
        )

class DeleteUserView(APIView):
    def delete(self, request,pk=None):
        user = UserAuth.objects.filter(pk=pk).first()
        if not user:
            return Response({"status":"error","message": "User not found."}, status=404)
        user.delete()
        return Response({"status":"success","message": "User deleted successfully."}, status=200)


class AllUserListView(APIView):
    def get(self, request):
        users = UserAuth.objects.all()
        combined_data = []
        for user in users:
            if str(user.role).upper() == 'VENDOR':
                combined_data.append(VendorProfile.objects.get(email=user.email))
            elif str(user.role).upper() == 'USER':
                combined_data.append(UserProfile.objects.get(email=user.email))
            elif str(user.role).upper() == 'RIDER':
                combined_data.append(RiderProfile.objects.get(email=user.email))
            else:
                pass
        
        serializer = CombinedUserSerializer(combined_data, many=True)
        return Response({
            "status": "success",
            "message": "All users fetched successfully.",
            "data": serializer.data
        }, status=200)