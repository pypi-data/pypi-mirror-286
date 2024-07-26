import json
import requests
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter
from boto3.dynamodb.types import TypeDeserializer

API_ENDPOINT = "https://tykjwglg3bys3otpainslcu32y0qjbtx.lambda-url.us-east-1.on.aws"

def dynamodb_to_json(dynamodb_obj):
    try:
        deserializer = TypeDeserializer()
        return deserializer.deserialize({'M': dynamodb_obj})
    except Exception as e:
        print(f"Error converting DynamoDB object to JSON: {e}")
        return {}

def handle_response(response):
    try:
        response.raise_for_status()
        if response.text:
            data = response.json()
            if isinstance(data, dict) and 'Item' in data:
                return dynamodb_to_json(data['Item'])
            return parse_json_recursively(data)
        else:
            return {}
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
        return {"error": str(e)}
    except ValueError as e:
        print(f"Error parsing JSON: {e}")
        return {"error": "Invalid JSON response"}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"error": str(e)}

def parse_json_recursively(data):
    try:
        if isinstance(data, str):
            try:
                return parse_json_recursively(json.loads(data))
            except json.JSONDecodeError:
                return data
        elif isinstance(data, dict):
            return {k: parse_json_recursively(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [parse_json_recursively(i) for i in data]
        else:
            return data
    except Exception as e:
        print(f"Error parsing JSON recursively: {e}")
        return data

def format_json(data):
    try:
        parsed_data = parse_json_recursively(data)
        formatted_json = json.dumps(parsed_data, indent=2)
        return highlight(formatted_json, JsonLexer(), TerminalFormatter())
    except Exception as e:
        print(f"Error formatting JSON: {e}")
        return json.dumps(data, indent=2)

def format_analysis_result(result):
    output = []

    try:
        output.append(f"Label: {result['label']}")
            
        if 'dependencies' in result:
            # Flattened result
            output.append("Dependencies:")
            if isinstance(result['dependencies'], list):
                for dep in result['dependencies']:
                    output.append(f"  {dep['name']}: {dep['current']} (Latest: {dep.get('latest', 'unknown')})")
            else:
                output.append(format_json(result['dependencies']))    
        elif 'action' in result:
            # Single action result
            action_result = result['result']
            output.append(f"\nAction: {result['action']}")
            output.append(f"Status: {action_result['status']}")
            output.append(f"Processed: {action_result['processed']}")
            output.append(f"Unprocessed count: {action_result['unprocessed_count']}")

            if 'details' in action_result:
                output.append("\nDetails:")
                for detail in action_result['details']:
                    output.append(f"\n  File: {detail['file']}")
                    output.append(f"  Analysis:\n{format_json(detail['analysis'])}")
        else:
            # Multiple actions result
            for action, action_result in result['actions'].items():
                output.append(f"\nAction: {action}")
                output.append(f"Status: {action_result['status']}")
                output.append(f"Processed: {action_result['processed']}")
                output.append(f"Unprocessed count: {action_result['unprocessed_count']}")

                if 'details' in action_result:
                    output.append("\n  Details:")
                    for detail in action_result['details']:
                        output.append(f"\n    File: {detail['file']}")
                        output.append(f"    Analysis:\n{format_json(detail['analysis'])}")

    except Exception as e:
        output.append(f"Error formatting analysis result: {e}")

    return "\n".join(output)
