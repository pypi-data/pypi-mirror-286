# clone.py

import os
import shutil
import zipfile
import requests
import subprocess
from .auth import get_headers
from .utils import API_ENDPOINT, handle_response
from concurrent.futures import ThreadPoolExecutor, as_completed

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clone_repo(url, temp_dir):
    try:
        repo_name = url.split('/')[-1]
        repo_path = os.path.join(temp_dir, repo_name)
        
        if os.path.exists(repo_path):
            print(f"Repository {repo_name} already cloned, skipping...")
            return repo_path
        
        subprocess.run(['git', 'clone', '--depth', '1', url, repo_path], check=True)
        return repo_path
    except subprocess.CalledProcessError as e:
        print(f"Error cloning {url}: {e}")
        return None

def get_presigned_url(label):
    try:
        headers = get_headers()
        response = requests.post(f"{API_ENDPOINT}/clone", json={"label": label}, headers=headers)
        response.raise_for_status()
        return response.json()['presigned_url']
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
        return None
    except Exception as e:
        print(f"Error getting presigned URL: {e}")
        return None

def zip_label_dir(label_dir):
    zip_path = label_dir + '.zip'
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(label_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        if os.path.exists(file_path) and os.path.isfile(file_path):
                            arcname = os.path.relpath(file_path, label_dir)
                            zipf.write(file_path, arcname)
                        else:
                            logger.warning(f"Skipping non-existent or non-file path: {file_path}")
                    except PermissionError:
                        logger.warning(f"Permission denied: Skipping file {file_path}")
                    except Exception as e:
                        logger.error(f"Error adding file {file_path} to zip: {e}")
        logger.info(f"Created zip file: {zip_path}")
        return zip_path
    except Exception as e:
        logger.error(f"Error creating zip file: {e}")
        return None

def upload_to_s3(zip_path, presigned_url):
    try:
        with open(zip_path, 'rb') as f:
            response = requests.put(presigned_url, data=f)
            response.raise_for_status()
        print(f"Successfully uploaded {zip_path}")
        return True
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error uploading {zip_path}: {e}")
        return False
    except Exception as e:
        print(f"Error uploading {zip_path}: {e}")
        return False

def trigger_unzip(label):
    print(f"Unzipping {label} at target....")

    try:
        headers = get_headers()
        response = requests.put(f"{API_ENDPOINT}/clone", json={"label": label}, headers=headers)
        response.raise_for_status()
        print(f"Successfully unzipped {label} at target")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error unzipping {label} at target: {e}")
    except Exception as e:
        print(f"Error unzipping {label} at target: {e}")

def clone_and_upload(label, urls):
    temp_dir = os.path.join('temp_clones', label)
    os.makedirs(temp_dir, exist_ok=True)
    zip_path = None

    try:
        # Clone repositories
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_url = {executor.submit(clone_repo, url, temp_dir): url for url in urls}
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    future.result()
                except Exception as e:
                    print(f"Error processing {url}: {e}")

        # Zip the label directory
        zip_path = zip_label_dir(temp_dir)

        # Get presigned URL and upload
        presigned_url = get_presigned_url(label)
        if presigned_url:
            upload_success = upload_to_s3(zip_path, presigned_url)
            if upload_success:
                print(f"Successfully uploaded {label}")
            else:
                print(f"Failed to upload {label}")
        else:
            print(f"Failed to get presigned URL for {label}")
    
    except Exception as e:
        print(f"Error during clone and upload process: {e}")
    
    finally:
        # Clean up
        if zip_path and os.path.exists(zip_path):
            os.remove(zip_path)
            print(f"Removed temporary zip file: {zip_path}")
        
        if os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
                print(f"Removed temporary clone directory: {temp_dir}")
            except Exception as e:
                print(f"Error removing temporary directory {temp_dir}: {e}")

def handle_clone_command(args):
    urls = []
    if args.url:
        urls.append(args.url)
    elif args.file:
        try:
            with open(args.file, 'r') as f:
                urls = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"Error reading file {args.file}: {e}")
            return
    else:
        print("Error: Please provide either a URL (-u) or a file (-f) containing URLs.")
        return

    if not urls:
        print("Error: No valid URLs provided.")
        return

    try:
        clone_and_upload(args.label, urls)
    except Exception as e:
        print(f"Error in clone and upload process: {e}")                