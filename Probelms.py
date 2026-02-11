import os
import requests

USERNAME = "chuzhumin98"
REPO_NAME = "PythonForMillions"
TARGET_FOLDER = "PythonForMillions_Flat"
LIMIT = 150  # Number of files to pull

# Changed from 'master' to 'main' to match the repository's branch configuration
url = f"https://api.github.com/repos/{USERNAME}/{REPO_NAME}/git/trees/main?recursive=1"

print(f"Fetching repository structure from {USERNAME}/{REPO_NAME}...")
response = requests.get(url).json()

if isinstance(response, dict) and "message" in response:
    print("❌ GitHub API Error:", response["message"])
    print("If you hit rate limits, try again later or add an auth token.")
    exit()

if "tree" not in response:
    print("❌ Unexpected response format from GitHub Tree API.")
    exit()

# Filter for python files in the tree layout
all_items = response["tree"]
python_files = [item for item in all_items if item["type"] == "blob" and item["path"].endswith(".py")]

print(f"Found a total of {len(python_files)} Python files across all subfolders.")
print(f"Downloading up to {LIMIT} files into a single flat folder...\n")

os.makedirs(TARGET_FOLDER, exist_ok=True)

downloaded = 0
for file_info in python_files:
    if downloaded >= LIMIT:
        break

    original_path = file_info["path"]
    file_name = os.path.basename(original_path)
    
    # Point the raw content path to 'main' as well
    download_url = f"https://raw.githubusercontent.com/{USERNAME}/{REPO_NAME}/main/{original_path}"
    
    # Check for duplicate names across different subdirectories and add suffixes
    local_file_path = os.path.join(TARGET_FOLDER, file_name)
    if os.path.exists(local_file_path):
        name_part, ext_part = os.path.splitext(file_name)
        counter = 1
        while os.path.exists(local_file_path):
            local_file_path = os.path.join(TARGET_FOLDER, f"{name_part}_{counter}{ext_part}")
            counter += 1

    try:
        file_data = requests.get(download_url).content
        with open(local_file_path, 'wb') as f:
            f.write(file_data)
        
        downloaded += 1
        print(f"[{downloaded}/{LIMIT}] Saved: {os.path.basename(local_file_path)}")
    except Exception as e:
        print(f"❌ Failed to download {file_name}: {e}")

print(f"\n✅ Done! All {downloaded} files have been successfully dumped into '{TARGET_FOLDER}'.")