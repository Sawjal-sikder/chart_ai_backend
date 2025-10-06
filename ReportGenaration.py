import os
import json
import base64
from Config import model

import re





def trade_analysis(image_path, extracted_data, trading_style="swing", trading_strategy="technical"):
    # === Encode local image to base64 ===
    image_path = image_path
    with open(image_path, "rb") as f:
        image_base64 = base64.b64encode(f.read()).decode("utf-8")
    image_data_url = f"data:image/png;base64,{image_base64}"

    # === Build prompt ===
    # Define JSON structure separately to avoid f-string formatting issues
    json_structure = '''
{
  "pattern_identification": {
    "pattern": "string",
    "bias": "string"
  },
  "trend_analysis": {
    "trend": "string", 
    "sentiment": "string",
    "momentum": "string"
  },
  "key_levels": {
    "support_level": "number",
    "resistance_level": "number", 
    "breakout_confirmation": "number"
  },
  "indicator_analysis": {
    "market_sentiment": "string",
    "trend": "string",
    "volatility": "string",
    "volume": "string",
    "candlestick_behavior": "string"
  },
  "trading_recommendation": {
    "strategy": "string",
    "entry_point": "string",
    "stop_loss": "string",
    "target": "string",
    "alternative_plan": "string", 
    "outlook": "string"
  },
  "risk_assessment": {
    "key_risks": ["string"],
    "position_sizing": "string",
    "stop_loss_management": "string"
  },
  "game_plan": "string",
  "confidence_score": "string"
}
'''

    prompt = f"""You are an expert financial analyst with 20 years of experience in technical analysis. And you are skilled at identifying chart patterns, trends, and key levels from trade charts.



Analyze the following stock market data or trade using the user preferences {trading_style} and {trading_strategy} and provide a structured trading analysis.
Use the extracted data below:

{extracted_data}

CRITICAL INSTRUCTIONS:
- Your response must ONLY be valid JSON format
- No markdown formatting, no code blocks, no explanatory text
- No exceptions, no additional commentary
- Start directly with {{ and end with }}
- Follow this EXACT structure:

{json_structure}

MANDATORY RESPONSE FORMAT:
Return ONLY the JSON object following this exact structure. Any deviation will be rejected.

"""
    
#     Return the result ONLY in valid JSON format with the following structure:
# {json_structure}
    # === Send request ===
    response = model.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system", 
                "content": "You are a financial analyst that ONLY responds with valid JSON format. Never use markdown, code blocks, or any text outside of JSON structure. Your entire response must be parseable JSON starting with { and ending with }."
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": image_data_url}},
                ],
            }
        ],
        max_tokens=1500,
        response_format={"type": "json_object"}
    )

    # === Process response ===
    response_data = response.choices[0].message.content
    
    # Clean and validate JSON response
    try:
        # Remove any markdown formatting if present
        if response_data.strip().startswith("```json"):
            match = re.search(r"```json(.*?)```", response_data, re.DOTALL)
            if match:
                response_data = match.group(1).strip()
        elif response_data.strip().startswith("```"):
            match = re.search(r"```(.*?)```", response_data, re.DOTALL)
            if match:
                response_data = match.group(1).strip()
        
        # Remove any leading/trailing whitespace
        response_data = response_data.strip()
        
        # Ensure it starts with { and ends with }
        if not response_data.startswith('{'):
            # Try to find the first { and extract from there
            start_idx = response_data.find('{')
            if start_idx != -1:
                response_data = response_data[start_idx:]
        
        if not response_data.endswith('}'):
            # Try to find the last } and extract up to there
            end_idx = response_data.rfind('}')
            if end_idx != -1:
                response_data = response_data[:end_idx + 1]
        
        # Parse JSON
        parsed_response = json.loads(response_data)
        
        # Validate required fields are present
        required_fields = [
            "pattern_identification", "trend_analysis", "key_levels", 
            "indicator_analysis", "trading_recommendation", "risk_assessment", 
            "game_plan", "confidence_score"
        ]
        
        for field in required_fields:
            if field not in parsed_response:
                raise ValueError(f"Missing required field: {field}")
        
        return parsed_response
        
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        print(f"Raw response: {response_data}")
        # Return a default structure if parsing fails
        return {
            "pattern_identification": {"pattern": "Error", "bias": "Neutral"},
            "trend_analysis": {"trend": "Unknown", "sentiment": "Neutral", "momentum": "Unknown"},
            "key_levels": {"support_level": 0, "resistance_level": 0, "breakout_confirmation": 0},
            "indicator_analysis": {"market_sentiment": "Neutral", "trend": "Unknown", "volatility": "Medium", "volume": "Medium", "candlestick_behavior": "Error parsing response"},
            "trading_recommendation": {"strategy": "Hold", "entry_point": "N/A", "stop_loss": "N/A", "target": "N/A", "alternative_plan": "Wait for clearer signals", "outlook": "Unknown"},
            "risk_assessment": {"key_risks": ["Response parsing error"], "position_sizing": "Minimal", "stop_loss_management": "Conservative"},
            "game_plan": "Error in analysis - manual review required",
            "confidence_score": "0%"
        }
    except Exception as e:
        print(f"Unexpected error: {e}")
        print(f"Raw response: {response_data}")
        return {
            "pattern_identification": {"pattern": "Error", "bias": "Neutral"},
            "trend_analysis": {"trend": "Unknown", "sentiment": "Neutral", "momentum": "Unknown"},
            "key_levels": {"support_level": 0, "resistance_level": 0, "breakout_confirmation": 0},
            "indicator_analysis": {"market_sentiment": "Neutral", "trend": "Unknown", "volatility": "Medium", "volume": "Medium", "candlestick_behavior": "Error processing response"},
            "trading_recommendation": {"strategy": "Hold", "entry_point": "N/A", "stop_loss": "N/A", "target": "N/A", "alternative_plan": "Wait for clearer signals", "outlook": "Unknown"},
            "risk_assessment": {"key_risks": ["Processing error"], "position_sizing": "Minimal", "stop_loss_management": "Conservative"},
            "game_plan": "Error in analysis - manual review required",
            "confidence_score": "0%"
        }
 