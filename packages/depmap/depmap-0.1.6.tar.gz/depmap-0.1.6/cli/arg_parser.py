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

    # Clone commands
    clone_parser = subparsers.add_parser("clone", help="Clone repositories and upload to S3")
    clone_parser.add_argument("-u", "--url", help="Single repository URL to clone")
    clone_parser.add_argument("-f", "--file", help="File containing repository URLs to clone")
    clone_parser.add_argument("-l", "--label", required=True, help="Label for the upload (used as root folder in S3)")

    return parser
