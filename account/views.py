from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from utils.common_function import user_token
from utils.db import DB
from django.db import transaction
import logging
from django.core.exceptions import ValidationError
from .models import UserAuth
from django.contrib.auth.password_validation import validate_password
from rest_framework import status
from utils.common_function import send_otp

logger = logging.getLogger(__name__)

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
        tokens = user_token(user)
        data = {}
        
        if str(user.role).upper() == "USER":
            data = {"email": user.email, "phone_number": user.phone_number, "role": user.role}
        elif str(user.role).upper() == "RIDER":
            data = {"email": user.email, "phone_number": user.phone_number, "role": user.role}
        elif str(user.role).upper() == "VENDOR":
            data = {"email": user.email, "phone_number": user.phone_number, "role": user.role}
        elif str(user.role).upper() == "ADMIN":
            data = {"email": user.email, "phone_number": user.phone_number, "role": user.role}
        return Response({
            "status":"success",
            "message": "Login successful.",
            "access_token": tokens,
            "data": data
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

        try:
            with transaction.atomic():
                user = UserAuth.objects.create_user(full_name=full_name, email=email.lower(),role=role.upper(), phone_number=phone_number, password=password)
                user.save()
            sent_email = send_otp(user)

            if not sent_email:
                return Response({"status": "error", "message": "Something went wrong, please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({"status": "success", "message": "Account created successfully. Please verify your email."}, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            return Response({"status": "error", "message": "Something went wrong, please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)