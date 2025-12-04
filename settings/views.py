from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *

class PrivacyPolicyListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return PrivacyPolicy.objects.all().first()
        except PrivacyPolicy.DoesNotExist:
            return None

    def get(self, request):
        policies = PrivacyPolicy.objects.all().order_by('-created_on')
        serializer = PrivacyPolicySerializer(policies, many=True)
        return Response({'status': 'success', 'data': serializer.data})

    def post(self, request):
        get_privacy_policy = PrivacyPolicy.objects.all()
        if get_privacy_policy:
            return Response({'status':'error','message':'data already exist.'})
        serializer = PrivacyPolicySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'status': 'error', 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        policy = self.get_object()
        if not policy:
            return Response({'status': 'error', 'message': 'Privacy policy not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PrivacyPolicySerializer(policy, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'data': serializer.data})
        return Response({'status': 'error', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        policy = self.get_object()
        if not policy:
            return Response({'status': 'error', 'message': 'Privacy policy not found'}, status=status.HTTP_404_NOT_FOUND)
        policy.delete()
        return Response({'status': 'success', 'message': 'Privacy policy deleted'}, status=status.HTTP_204_NO_CONTENT)

class TermsAndConditionsListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return TermsAndCondition.objects.all().first()
        except TermsAndCondition.DoesNotExist:
            return None

    def get(self, request):
        terms = TermsAndCondition.objects.all().order_by('-created_on')
        serializer = TermsAndConditionSerializer(terms, many=True)
        return Response({'status': 'success', 'data': serializer.data})

    def post(self, request):
        get_terms = TermsAndCondition.objects.all()
        if get_terms:
            return Response({'status':'error','message':'data already exist.'})
        serializer = TermsAndConditionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'status': 'error', 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        terms = self.get_object()
        if not terms:
            return Response({'status': 'error', 'message': 'Terms and conditions not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TermsAndConditionSerializer(terms, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'data': serializer.data})
        return Response({'status': 'error', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        terms = self.get_object()
        if not terms:
            return Response({'status': 'error', 'message': 'Terms and conditions not found'}, status=status.HTTP_404_NOT_FOUND)
        terms.delete()
        return Response({'status': 'success', 'message': 'Terms and conditions deleted'}, status=status.HTTP_204_NO_CONTENT)
    
class AboutUsListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return AboutUs.objects.all().first()
        except AboutUs.DoesNotExist:
            return None

    def get(self, request):
        about_us = AboutUs.objects.all().order_by('-created_on')
        serializer = AboutUsSerializer(about_us, many=True)
        return Response({'status': 'success', 'data': serializer.data})

    def post(self, request):
        get_about_us = AboutUs.objects.all()
        if get_about_us:
            return Response({'status':'error','message':'data already exist.'})
        serializer = AboutUsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'status': 'error', 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        about_us = self.get_object()
        if not about_us:
            return Response({'status': 'error', 'message': 'About us not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = AboutUsSerializer(about_us, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'data': serializer.data})
        return Response({'status': 'error', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        about_us = self.get_object()
        if not about_us:
            return Response({'status': 'error', 'message': 'About us not found'}, status=status.HTTP_404_NOT_FOUND)
        about_us.delete()
        return Response({'status': 'success', 'message': 'About us deleted'}, status=status.HTTP_204_NO_CONTENT)
    


class FAQCreateView(APIView):

    def get(self, request):
        faqs = FAQ.objects.all()
        serializer = FAQSerializer(faqs, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request):
        question = request.data.get('question')
        answer = request.data.get('answer')

        if not question or not answer:
            return Response({"status": "error", "message": "Question and Answer are required."}, status=status.HTTP_400_BAD_REQUEST)

        faq = FAQ.objects.create(question=question, answer=answer)
        faq.save()

        return Response({"status": "success", "message": "FAQ created successfully.", "data": FAQSerializer(faq).data}, status=status.HTTP_201_CREATED)
    
    def patch(self, request, faq_id):
        try:
            faq = FAQ.objects.get(id=faq_id)
        except FAQ.DoesNotExist:
            return Response({"status": "error", "message": "FAQ not found."}, status=status.HTTP_404_NOT_FOUND)

        faq.question = request.data.get('question', faq.question)
        faq.answer = request.data.get('answer', faq.answer)
        faq.save()

        return Response({"status": "success", "message": "FAQ updated successfully.", "data": FAQSerializer(faq).data}, status=status.HTTP_200_OK)
    
    def delete(self, request, faq_id):
        try:
            faq = FAQ.objects.get(id=faq_id)
        except FAQ.DoesNotExist:
            return Response({"status": "error", "message": "FAQ not found."}, status=status.HTTP_404_NOT_FOUND)

        faq.delete()
        return Response({"status": "success", "message": "FAQ deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
class FAQDetailView(APIView):
    def get(self, request, faq_id):
        try:
            faq = FAQ.objects.get(id=faq_id)
        except FAQ.DoesNotExist:
            return Response({"status": "error", "message": "FAQ not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = FAQSerializer(faq)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    


class FeedbackCreateView(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request):
        feedbacks = Feedback.objects.all()
        serializer = FeedbackSerializer(feedbacks, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        name = request.data.get('name')
        comments = request.data.get('comments')

        if not name or not comments:
            return Response({"status": "error", "message": "Name and Comments are required."}, status=status.HTTP_400_BAD_REQUEST)

        feedback = Feedback.objects.create(name=name, comments=comments)
        feedback.save()

        return Response({"status": "success", "message": "Feedback submitted successfully.", "data": FeedbackSerializer(feedback).data}, status=status.HTTP_201_CREATED)
    
    def patch(self, request, feedback_id):
        try:
            feedback = Feedback.objects.get(id=feedback_id)
        except Feedback.DoesNotExist:
            return Response({"status": "error", "message": "Feedback not found."}, status=status.HTTP_404_NOT_FOUND)

        feedback.name = request.data.get('name', feedback.name)
        feedback.comments = request.data.get('comments', feedback.comments)
        feedback.save()

        return Response({"status": "success", "message": "Feedback updated successfully.", "data": FeedbackSerializer(feedback).data}, status=status.HTTP_200_OK)
    
    def delete(self, request, feedback_id):
        try:
            feedback = Feedback.objects.get(id=feedback_id)
        except Feedback.DoesNotExist:
            return Response({"status": "error", "message": "Feedback not found."}, status=status.HTTP_404_NOT_FOUND)

        feedback.delete()
        return Response({"status": "success", "message": "Feedback deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    

class FeedbackDetailView(APIView):
    def get(self, request, feedback_id):
        try:
            feedback = Feedback.objects.get(id=feedback_id)
        except Feedback.DoesNotExist:
            return Response({"status": "error", "message": "Feedback not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = FeedbackSerializer(feedback)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

