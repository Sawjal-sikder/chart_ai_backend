# views.py
from payment.paymentPermission import HasActiveSubscription
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import requests
import logging
import os
from .models import ChatbotInteraction
from .serializers import ChatbotInteractionSerializer

logger = logging.getLogger(__name__)

class ChatbotView(APIView):
    permission_classes = [HasActiveSubscription]
    def post(self, request):
        user_input = request.data.get("user_input")
        api_url = os.getenv("ai_chatbot_url", "http://127.0.0.1:8000/api/v1/chat")
        user = request.user if request.user.is_authenticated else None

        if not user_input:
            return Response({"error": "No input provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Call AI chatbot API
        try:
            response = requests.post(api_url, json={"user_input": user_input})
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Chatbot API request failed: {e}")
            return Response({"error": "Failed to connect to AI service"}, status=status.HTTP_502_BAD_GATEWAY)

        try:
            api_response_data = response.json()
        except ValueError:
            logger.error("Invalid JSON response from AI service")
            return Response({"error": "Invalid response format from AI service"}, status=status.HTTP_502_BAD_GATEWAY)

        # Save interaction
        interaction = ChatbotInteraction.objects.create(
            user=user,
            user_input=user_input,
            bot_response=api_response_data.get('response', '')
        )

        # Serialize instance
        serializer = ChatbotInteractionSerializer(interaction)
        return Response(serializer.data, status=status.HTTP_200_OK)
