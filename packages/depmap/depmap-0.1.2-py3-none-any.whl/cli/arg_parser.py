import argparse

def create_parser():
    parser = argparse.ArgumentParser(description="Repository Analysis CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Analysis commands
    analysis_parser = subparsers.add_parser("analysis", help="Analysis-related commands")
    analysis_subparsers = analysis_parser.add_subparsers(dest="analysis_command")

    start_parser = analysis_subparsers.add_parser("start", help="Start a new analysis")
    start_parser.add_argument("-l", "--label", required=True, help="Label of the uploaded repository")
    start_parser.add_argument("-m", "--model", default="haiku", choices=["haiku", "sonnet", "opus"], help="Model to use for analysis (default: haiku)")
    start_parser.add_argument("-p", "--poll", action="store_true", help="Poll until analysis is complete")

    status_parser = analysis_subparsers.add_parser("status", help="Get analysis status")
    status_parser.add_argument("-l", "--label", required=True, help="Label of the analyzed repository")

    get_parser = analysis_subparsers.add_parser("get", help="Get analysis results")
    get_parser.add_argument("-l", "--label", required=True, help="Label of the analyzed repository")
    get_parser.add_argument("-f", "--file", help="Specific file to retrieve results for")
    get_parser.add_argument("-a", "--action", help="Specific action to retrieve results for")
    get_parser.add_argument("-d", "--details", action="store_true", help="Include detailed file results")
    get_parser.add_argument("-c", "--combine", action="store_true", help="Combine all dependencies into a single list")

    delete_parser = analysis_subparsers.add_parser("delete", help="Delete analysis results")
    delete_parser.add_argument("-l", "--label", required=True, help="Label of the analyzed repository")
    delete_parser.add_argument("-a", "--action", help="Specific action to delete results for")

    # Action commands
    action_parser = subparsers.add_parser("action", help="Action-related commands")
    action_subparsers = action_parser.add_subparsers(dest="action_command")

    list_actions_parser = action_subparsers.add_parser("list", help="List all actions")
    list_actions_parser.add_argument("-n", "--names-only", action="store_true", help="Get only action names")
    list_actions_parser.add_argument("-s", "--status", action="store_true", help="Include action statuses")

    get_action_parser = action_subparsers.add_parser("get", help="Get a specific action")
    get_action_parser.add_argument("action", help="Action name")
    get_action_parser.add_argument("-q", "--query", choices=["prompt", "include", "schema", "active"], help="Get specific part of the action")

    store_action_parser = action_subparsers.add_parser("store", help="Store a new action")
    store_action_parser.add_argument("action", nargs='?', help="Action name")
    store_action_parser.add_argument("prompt", nargs='?', help="Action prompt")
    store_action_parser.add_argument("include", nargs='?', help="Action include list")
    store_action_parser.add_argument("schema", nargs='?', help="Action schema")
    store_action_parser.add_argument("-a", "--active", action="store_true", help="Set action as active")
    store_action_parser.add_argument("-f", "--file", help="JSON file to load action details from")

    update_action_parser = action_subparsers.add_parser("update", help="Update an existing action or all actions")
    update_action_parser.add_argument("action", nargs='?', help="Action name (optional)")
    update_action_parser.add_argument("-p", "--prompt", help="New action prompt")
    update_action_parser.add_argument("-i", "--include", help="New action include list")
    update_action_parser.add_argument("-s", "--schema", help="New action schema")
    update_action_parser.add_argument("-a", "--active", type=lambda x: (str(x).lower() == 'true'), help="Set action(s) as active/inactive")

    delete_action_parser = action_subparsers.add_parser("delete", help="Delete an action")
    delete_action_parser.add_argument("action", help="Action name")

    delete_all_parser = action_subparsers.add_parser("delete_all", help="Delete all actions")

    add_all_parser = action_subparsers.add_parser("add_all", help="Add all actions from 'actions' directory")
    add_all_parser.add_argument("-d", "--directory", default="actions", help="Directory to load action JSON files from")

    # Clone commands
    clone_parser = subparsers.add_parser("clone", help="Clone repositories and upload to S3")
    clone_parser.add_argument("-u", "--url", help="Single repository URL to clone")
    clone_parser.add_argument("-f", "--file", help="File containing repository URLs to clone")
    clone_parser.add_argument("-l", "--label", required=True, help="Label for the upload (used as root folder in S3)")

    return parser
