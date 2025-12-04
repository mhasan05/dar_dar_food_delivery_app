from rest_framework import serializers
from .models import *


class PrivacyPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivacyPolicy
        fields = ['id', 'title', 'content', 'created_on', 'updated_on']
        read_only_fields = ['created_on', 'updated_on']


class TermsAndConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermsAndCondition
        fields = ['id', 'title', 'content', 'created_on', 'updated_on']
        read_only_fields = ['created_on', 'updated_on']


class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = ['id', 'title', 'content', 'created_on', 'updated_on']
        read_only_fields = ['created_on', 'updated_on']


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'created_at', 'updated_at']


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'name', 'comments', 'created_at']
