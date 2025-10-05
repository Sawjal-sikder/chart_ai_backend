from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import *
import requests
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def ImageAnalysisView(request):
    if request.method == "POST":
        file = request.FILES.get('file')
        trading_style = request.POST.get('trading_style')
        trading_strategy = request.POST.get('trading_strategy')
        
        # Save to DB
        trading_request = TradingRequest.objects.create(
            file=file,
            trading_style=trading_style,
            trading_strategy=trading_strategy
        )
        
        
        # Reset file pointer to beginning
        file.seek(0)
        file_content = file.read()
        file.seek(0)  # Reset again for potential reuse
        
        # Prepare file for requests with proper content
        files = {
            'file': (file.name, file_content, file.content_type or 'application/octet-stream')
        }
        data = {
            'trading_style': trading_style,
            'trading_strategy': trading_strategy
        }

        # Call external analysis API
        api_url = "http://10.10.7.75:8000/api/v1/trade-analysis" 
        try:
            logger.info(f"Making API request to {api_url} with data: {data}")
            response = requests.post(api_url, files=files, data=data, timeout=60)
            
            # Log response details for debugging
            logger.info(f"API response status: {response.status_code}")
            logger.info(f"API response headers: {dict(response.headers)}")
            
            if response.status_code != 200:
                # Get detailed error information
                try:
                    error_details = response.json()
                    logger.error(f"API error response: {error_details}")
                except:
                    error_details = {"error": response.text or "Unknown error"}
                    logger.error(f"API error text: {response.text}")
                
                api_response_data = {
                    "error": f"API request failed with status {response.status_code}",
                    "details": error_details,
                    "status_code": response.status_code
                }
            else:
                response.raise_for_status()
                api_response_data = response.json()
                
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


        TradingResponse_data = TradingResponse.objects.create(
            request=trading_request,
            response_data=api_response_data
        )
        
        request_id = trading_request.id
        request_all_data = TradingRequest.objects.get(id=request_id)
        request_data = {
                    "id": request_all_data.id,
                    "file": request_all_data.file.url if request_all_data.file else None,
                    "trading_style": request_all_data.trading_style,
                    "trading_strategy": request_all_data.trading_strategy,
                }

        data = {
            "id": TradingResponse_data.id,
            "request_data": request_data,
            "response_data": TradingResponse_data.response_data,
        }

        return JsonResponse({"data": data})
    return JsonResponse({"error": "Invalid request method"}, status=400)
