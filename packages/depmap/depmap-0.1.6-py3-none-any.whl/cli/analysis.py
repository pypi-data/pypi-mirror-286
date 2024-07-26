# analysis.py

import json
import time
import requests
from tqdm import tqdm
from .auth import get_headers
from .utils import handle_response, API_ENDPOINT, format_analysis_result

def start_analysis(label, model):
    payload = {"model": model}

    try:
        headers = get_headers()
        response = requests.post(f"{API_ENDPOINT}/analysis/{label}", json=payload, headers=headers)
        response.raise_for_status()
        return handle_response(response)
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
        print(f"Response content: {e.response.content}")
        return {"error": str(e)}
    except Exception as e:
        print(f"Unexpected error starting analysis: {e}")
        return {"error": str(e)}

def get_analysis_status(label):
    try:
        headers = get_headers()
        endpoint = f"{API_ENDPOINT}/analysis/{label}/status"
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
        return handle_response(response)
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
        return {"error": str(e)}
    except Exception as e:
        print(f"Error getting analysis status: {e}")
        return {"error": str(e)}

def get_analysis_results(label, file=None, details=False, action=None, flatten=False):
    try:
        headers = get_headers()
        endpoint = f"{API_ENDPOINT}/analysis/{label}"
        params = {}
        if file:
            params['file'] = file
        if details:
            params['details'] = 'true'
        if action:
            params['action'] = action
        if flatten:
            params['flatten'] = 'true'
        response = requests.get(endpoint, params=params, headers=headers)
        response.raise_for_status()
        return handle_response(response)
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
        return {"error": str(e)}
    except Exception as e:
        print(f"Error getting analysis results: {e}")
        return {"error": str(e)}

def delete_analysis_results(label, action=None):
    try:
        headers = get_headers()
        endpoint = f"{API_ENDPOINT}/analysis/{label}"
        if action:
            endpoint += f"/{action}"
        response = requests.delete(endpoint, headers=headers)
        response.raise_for_status()
        return handle_response(response)
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
        return {"error": str(e)}
    except Exception as e:
        print(f"Error deleting analysis results: {e}")
        return {"error": str(e)}

def start_and_poll_analysis(label, model):
    try:
        # Start the analysis
        start_result = start_analysis(label, model)
        if 'error' in start_result:
            print(f"Failed to start analysis: {start_result['error']}")
            return start_result

        print(f"Analysis started: {json.dumps(start_result, indent=2)}")

        # Initialize a single progress bar
        pbar = tqdm(total=100, desc="Analyzing", unit="%")

        poll_count = 0
        max_polls = 12  # Maximum number of polls (1 minute with 5-second intervals)

        while poll_count < max_polls:
            time.sleep(5)  # Wait for 5 seconds between polls
            result = get_analysis_status(label)
            poll_count += 1

            if 'error' in result:
                print(f"Error polling analysis: {result['error']}")
                break

            actions = result.get('actions', {})
            if not actions:
                print("No actions were processed. The analysis may have failed or no matching files were found.")
                break

            all_completed = True
            total_progress = 0
            action_count = 0

            for action, status in actions.items():
                processed, total = map(int, status['processed'].split('/'))
                if total == 0:
                    print(f"No files to process for action: {action}")
                    continue

                progress = (processed / total) * 100
                total_progress += progress
                action_count += 1

                if status['status'] not in ['COMPLETED', 'FAILED']:
                    all_completed = False

            if action_count > 0:
                average_progress = total_progress / action_count
                pbar.n = average_progress
                pbar.refresh()

            if all_completed:
                pbar.close()
                final_result = get_analysis_results(label)
                if 'error' not in final_result:
                    print(f"\nAnalysis completed: {json.dumps(final_result, indent=2)}")
                break

        else:
            print("Analysis is taking longer than expected. Please check the status manually.")

        pbar.close()
        return result
    except Exception as e:
        print(f"Unexpected error in start_and_poll_analysis: {e}")
        return {"error": str(e)}

def handle_analysis_command(args):
    if args.analysis_command == "start":
        if args.poll:
            result = start_and_poll_analysis(args.label, args.model)
            if result and 'error' not in result:
                print("Analysis complete or timed out. Check status for details.")
            elif 'error' in result:
                print(f"Error during analysis: {result['error']}")
        else:
            result = start_analysis(args.label, args.model)
            if 'error' not in result:
                print("Analysis started:")
                print(json.dumps(result, indent=2))
            else:
                print(f"Error starting analysis: {result['error']}")
    elif args.analysis_command == "status":
        result = get_analysis_status(args.label)
        if 'error' not in result:
            print("Analysis status:")
            print(json.dumps(result, indent=2))
        else:
            print(f"Error getting analysis status: {result['error']}")
    elif args.analysis_command == "get":
        result = get_analysis_results(
            args.label,
            file=args.file,
            details=args.details,
            action=args.action,
            flatten=args.combine
        )
        if 'error' not in result:
            print("Analysis results:")
            print(format_analysis_result(result))
        else:
            print(f"Error getting analysis results: {result['error']}")
    elif args.analysis_command == "delete":
        result = delete_analysis_results(args.label, args.action)
        if 'error' not in result:
            print("Analysis deletion result:")
            print(json.dumps(result, indent=2))
        else:
            print(f"Error deleting analysis results: {result['error']}")