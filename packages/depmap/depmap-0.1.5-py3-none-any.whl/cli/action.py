# action.py

import os
import json
import requests
from .auth import get_headers
from .utils import handle_response, API_ENDPOINT

def get_all_actions(names_only=False, active_only=False):
    try:
        endpoint = f"{API_ENDPOINT}/action"
        params = {}
        if names_only:
            params['name'] = ''
        if active_only:
            params['active'] = ''
        
        headers = get_headers()
        response = requests.get(endpoint, params=params, headers=headers)
        response.raise_for_status()
        actions = handle_response(response)
        
        if active_only and isinstance(actions, dict):
            return {name: action.get('active', False) for name, action in actions.items()}
        return actions
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
        return {"error": str(e)}
    except Exception as e:
        print(f"Error getting all actions: {e}")
        return {"error": str(e)}

def get_specific_action(action, query=None):
    try:
        endpoint = f"{API_ENDPOINT}/action/{action}"
        if query:
            endpoint += f"?{query}"
        headers = get_headers()
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
        return handle_response(response)
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
        return {"error": str(e)}
    except Exception as e:
        print(f"Error getting specific action: {e}")
        return {"error": str(e)}

def store_action(action, prompt, include, schema, active=False):
    try:
        payload = {
            "action": action,
            "prompt": prompt,
            "include": include,
            "schema": schema,
            "active": active
        }
        headers = get_headers()
        response = requests.post(f"{API_ENDPOINT}/action", json=payload, headers=headers)
        response.raise_for_status()
        return handle_response(response)
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
        return {"error": str(e)}
    except Exception as e:
        print(f"Error storing action: {e}")
        return {"error": str(e)}

def update_action(action=None, prompt=None, include=None, schema=None, active=None):
    try:
        if action is None:
            return update_all_actions(active)
        
        payload = {"action": action}
        if prompt is not None:
            payload["prompt"] = prompt
        if include is not None:
            payload["include"] = include
        if schema is not None:
            payload["schema"] = schema
        if active is not None:
            payload["active"] = active
        headers = get_headers()
        response = requests.put(f"{API_ENDPOINT}/action", json=payload, headers=headers)
        response.raise_for_status()
        return handle_response(response)
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
        return {"error": str(e)}
    except Exception as e:
        print(f"Error updating action: {e}")
        return {"error": str(e)}

def delete_action(action):
    try:
        payload = {"action": action}
        headers = get_headers()
        response = requests.delete(f"{API_ENDPOINT}/action", json=payload, headers=headers)
        response.raise_for_status()
        return handle_response(response)
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
        return {"error": str(e)}
    except Exception as e:
        print(f"Error deleting action: {e}")
        return {"error": str(e)}

def store_action_from_file(filename):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        action = data.get("action")
        prompt = data.get("prompt")
        include = data.get("include")
        schema = data.get("schema")
        active = data.get("active", False)  # Default to False
        return store_action(action, prompt, include, schema, active)
    except Exception as e:
        print(f"Error storing action from file: {e}")
        return {"error": str(e)}

def add_all_actions_from_dir(directory):
    try:
        results = []
        for filename in os.listdir(directory):
            if filename.endswith(".json"):
                filepath = os.path.join(directory, filename)
                result = store_action_from_file(filepath)
                results.append(result)
        return results
    except Exception as e:
        print(f"Error adding all actions from directory: {e}")
        return {"error": str(e)}

def delete_all_actions():
    try:
        actions = get_all_actions(names_only=True)
        if isinstance(actions, list):
            for action in actions:
                delete_action(action)
        return {"status": "All actions deleted"}
    except Exception as e:
        print(f"Error deleting all actions: {e}")
        return {"error": str(e)}

def update_all_actions(active):
    try:
        actions = get_all_actions(names_only=True)
        results = []
        if isinstance(actions, list):
            for action in actions:
                result = update_action(action, active=active)
                results.append(result)
        return results
    except Exception as e:
        print(f"Error updating all actions: {e}")
        return {"error": str(e)}

def handle_action_command(args):
    if args.action_command == "list":
        if args.status:
            result = get_all_actions(active_only=True)
        else:
            result = get_all_actions(args.names_only)
        if 'error' not in result:
            print(json.dumps(result, indent=2))
        else:
            print(f"Error listing actions: {result['error']}")
    elif args.action_command == "get":
        result = get_specific_action(args.action, args.query)
        if 'error' not in result:
            print(json.dumps(result, indent=2))
        else:
            print(f"Error getting action: {result['error']}")
    elif args.action_command == "store":
        if args.file:
            result = store_action_from_file(args.file)
        else:
            result = store_action(args.action, args.prompt, args.include, args.schema, args.active)
        if 'error' not in result:
            print(json.dumps(result, indent=2))
        else:
            print(f"Error storing action: {result['error']}")
    elif args.action_command == "update":
        result = update_action(args.action, args.prompt, args.include, args.schema, args.active)
        if 'error' not in result:
            if isinstance(result, list):
                print("Updated all actions:")
                for r in result:
                    print(json.dumps(r, indent=2))
            else:
                print(json.dumps(result, indent=2))
        else:
            print(f"Error updating action: {result['error']}")
    elif args.action_command == "delete":
        result = delete_action(args.action)
        if 'error' not in result:
            print(json.dumps(result, indent=2))
        else:
            print(f"Error deleting action: {result['error']}")
    elif args.action_command == "delete_all":
        result = delete_all_actions()
        if 'error' not in result:
            print(json.dumps(result, indent=2))
        else:
            print(f"Error deleting all actions: {result['error']}")
    elif args.action_command == "add_all":
        result = add_all_actions_from_dir(args.directory)
        if 'error' not in result:
            print("Actions added from directory:")
            print(json.dumps(result, indent=2))
        else:
            print(f"Error adding actions from directory: {result['error']}")