from django.urls import path
from .views import *

urlpatterns = [
    path('privacy_policies/', PrivacyPolicyListCreateAPIView.as_view(), name='privacy_policies'),
    path('terms_conditions/', TermsAndConditionsListCreateAPIView.as_view(), name='terms_conditions'),
    path('about_us/', AboutUsListCreateAPIView.as_view(), name='about_us'),

    path('faq/', FAQCreateView.as_view(), name='faq'),
    path('faq/<str:faq_id>/', FAQCreateView.as_view(), name='single_faq'),
    path('single_faq/<str:faq_id>/', FAQDetailView.as_view(), name='single_faq'),

    path('feedback/', FeedbackCreateView.as_view(), name='feedback'),
    path('feedback/<str:feedback_id>/', FeedbackCreateView.as_view(), name='single_feedback'),
    path('single_feedback/<str:feedback_id>/', FeedbackDetailView.as_view(), name='single_feedback'),
]