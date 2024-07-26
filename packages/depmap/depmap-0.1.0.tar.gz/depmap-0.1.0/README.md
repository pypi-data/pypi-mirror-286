# Dependency Mapper CLI

DepMap CLI is a command-line interface tool for managing and analyzing software dependencies across repositories. It provides functionality for cloning repositories, managing actions, and running analyses.

## Table of Contents

1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Initial Setup](#initial-setup)
4. [Usage](#usage)
   - [Authentication](#authentication)
   - [Clone Commands](#clone-commands)
   - [Action Commands](#action-commands)
   - [Analysis Commands](#analysis-commands)
6. [Error Handling](#error-handling)
7. [Security Considerations](#security-considerations)
8. [Troubleshooting](#troubleshooting)

## Installation

1. Ensure you have Python 3.9+ installed on your system.
2. Download the CLI zip file from:
   ```
   https://github.com/trilogy-group/central-product-tpm/edit/master/POC/cc/repo/depmap/cli/depmap.zip
   ```
3. Extract the contents of the zip file to a directory of your choice.
4. Navigate to the extracted directory:
   ```
   cd path/to/extracted/directory
   ```
5. Create a virtual environment:
   ```
   python -m venv venv
   ```
6. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```
7. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Configuration

Add your API authentication token to the `.env` file:
   ```
   AUTH_TOKEN=your_auth_token_here
   ```

## Initial Setup

Before using the CLI for analysis, you must set up the necessary actions:

1. Store the dependency action:
   ```
   python cli.py action store dep -f actions/dep.json
   ```
   This command loads the action details from the `dep.json` file in the `actions` folder.

2. Activate the dependency action:
   ```
   python cli.py action update dep -a True
   ```
   This sets the 'active' attribute of the 'dep' action to True.

## Usage

The general syntax for using the DepMap CLI is:

```
python cli.py <command> <subcommand> [options]
```

### Authentication

The CLI uses an authentication token stored in the `.env` file. Ensure this file is present and contains a valid `AUTH_TOKEN` before running any commands.

### Clone Commands

Before running an analysis, you must first clone the target repository:

- Clone and upload a single repository:
  ```
  python cli.py clone -l <label> -u <url>
  ```

- Clone and upload multiple repositories under a single label:
  ```
  python cli.py clone -l <label> -f <file>
  ```
  
  The file should contain one repository URL per line, for example:
  ```
  https://github.com/trilogy-group/influitive-advocatehub-Influitive-Advocate
  https://github.com/trilogy-group/influitive-advocatehub-influitive
  ...
  ```

  The CLI will clone all repositories listed in the file and upload them together.

Examples:
1. Clone a single repo:
```
   python cli.py clone -l worksmart -u https://github.com/trilogy-group/worksmart-ts
   ```
2. Clone multiple repos at once:
   ```
   python cli.py clone -l influitive -f influitive.txt
   ```
   This will clone both repositories and group them under the 'influitive' label.

After cloning, you can analyze all the repositories under this label together using the analysis commands.

### Action Commands

Next, you must make sure that you have at least one action defined. Actions are prompts + scaffolding that are run against the files. For the time being - only one action is defined. You will find it in the 'actions' sub folder.

- List all actions:
  ```
  python cli.py action list [-n] [-s]
  ```

- Get a specific action:
  ```
  python cli.py action get <action> [-q <query>]
  ```

- Store a new action:
  ```
  python cli.py action store <action> <prompt> <include> <schema> [-a] [-f <file>]
  ```

- Update an action:
  ```
  python cli.py action update <action> [-p <prompt>] [-i <include>] [-s <schema>] [-a <active>]
  ```

- Delete an action:
  ```
  python cli.py action delete <action>
  ```

- Delete all actions:
  ```
  python cli.py action delete_all
  ```

- Add actions from a directory:
  ```
  python cli.py action add_all [-d <directory>]
  ```
### Analysis Commands

#### start
Starts a new analysis for the specified label using the given model.
- `-l, --label`: Required. Label for the analysis.
- `-m, --model`: Model to use for analysis (default: "haiku").
- `-p, --poll`: Optional. Poll until the analysis is complete.

#### status
Retrieves the status of an ongoing or completed analysis.
- `-l, --label`: Required. Label of the analysis to check.

#### get
Retrieves the results of a completed analysis.
- `-l, --label`: Required. Label of the analysis.
- `-d, --details`: Optional. Include detailed results.
- `-c, --combine`: Optional. Combine all dependencies into a single list.
- `-f, --file`: Optional. Specific file to retrieve results for.
- `-a, --action`: Optional. Specific action to retrieve results for.

#### delete
Deletes the results of an analysis.
- `-l, --label`: Required. Label of the analysis to delete.
- `-a, --action`: Optional. Specific action to delete results for.

## Error Handling

The CLI provides detailed error messages for various scenarios:
- HTTP errors (e.g., 401 Unauthorized)
- Network connectivity issues
- Invalid input parameters
- File I/O errors

If you encounter an error, the CLI will display a message describing the issue.

## Security Considerations

- The authentication token is stored in a `.env` file, which should be kept secure and not shared or committed to version control.
- All API requests are made over HTTPS, ensuring that data (including headers) is encrypted in transit.
- Avoid logging or displaying the authentication token in any output.

## Troubleshooting

1. **Authentication Issues**: Ensure your `AUTH_TOKEN` in the `.env` file is correct and up to date.
2. **Network Problems**: Check your internet connection and verify that you can reach the API endpoint.
3. **Invalid Commands**: Double-check the command syntax and required parameters.
4. **File Permissions**: Ensure you have the necessary permissions to read/write files in the working directory.

