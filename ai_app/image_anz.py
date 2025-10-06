from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import requests
import logging
import os
from payment.paymentPermission import HasActiveSubscription

from .models import TradingRequest, TradingResponse

logger = logging.getLogger(__name__)


class ImageAnalysisView(APIView):
    permission_classes = [HasActiveSubscription]


    def post(self, request):
        logger.info(f"Incoming POST request: FILES={request.FILES.keys()}, DATA={request.data}")

        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        trading_style = request.data.get('trading_style')
        trading_strategy = request.data.get('trading_strategy')

        # Save request in DB
        trading_request = TradingRequest.objects.create(
            user=request.user,
            file=file,
            trading_style=trading_style,
            trading_strategy=trading_strategy
        )

        # Safely read file content
        try:
            file.seek(0)
            file_content = file.read()
            file.seek(0)
        except Exception as e:
            logger.error(f"Error reading uploaded file: {str(e)}")
            return Response({"error": f"Invalid file: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        # Prepare file for external API
        files = {
            'file': (file.name, file_content, getattr(file, 'content_type', 'application/octet-stream'))
        }
        data = {
            'trading_style': trading_style,
            'trading_strategy': trading_strategy
        }

        api_url = os.getenv("ai_url", "http://127.0.0.1:8000/api/v1/trade-analysis")
        try:
            logger.info(f"Making API request to {api_url} with data: {data}")
            response = requests.post(api_url, files=files, data=data, timeout=60)

            logger.info(f"API response status: {response.status_code}")

            if response.status_code != 200:
                try:
                    error_details = response.json()
                except Exception:
                    error_details = {"error": response.text or "Unknown error"}

                api_response_data = {
                    "error": f"API request failed with status {response.status_code}",
                    "details": error_details,
                    "status_code": response.status_code
                }
            else:
                response.raise_for_status()
                api_response_data = response.json()
                
                # Save response in DB
                trading_response = TradingResponse.objects.create(
                    user=request.user,
                    request=trading_request,
                    response_data=api_response_data
                )

        except requests.exceptions.RequestException as e:
            logger.error(f"Request exception: {str(e)}")
            api_response_data = {
                "error": f"Failed to connect to analysis API: {str(e)}",
                "api_url": api_url
            }
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            api_response_data = {
                "error": f"Unexpected error during API call: {str(e)}"
            }        

        # Build clean request_data dict
        request_data = {
            "id": trading_request.id,
            "user": request.user.full_name if request.user.is_authenticated else "Anonymous",
            "file": trading_request.file.url if trading_request.file else None,
            "trading_style": trading_request.trading_style,
            "trading_strategy": trading_request.trading_strategy,
        }

        data = {
            "id": trading_response.id,
            "request_data": request_data,
            "response_data": trading_response.response_data,
        }

        return Response({"data": data}, status=status.HTTP_200_OK)
