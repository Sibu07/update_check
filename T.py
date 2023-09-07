def upload_to_github(file_path: str, target_path: str):
    with open(file_path, "rb") as f:
        file_content = f.read()

    encoded_content = base64.b64encode(file_content).decode("utf-8")

    headers = {"Authorization": f"token {github_access_token}"}
    url = f"{github_repo_url}/contents/{target_path}"

    # Check if the file already exists in the repository
    response = requests.get(url)
    if response.ok:
        # If the file exists, include the 'sha' parameter in the data
        existing_sha = response.json().get("sha")
        data = {
            "message": f"Update {target_path}",
            "content": encoded_content,
            "sha": existing_sha  # Include the 'sha' parameter for updates
        }
    else:
        # If the file is new, create it without the 'sha' parameter
        data = {
            "message": f"Upload {target_path}",
            "content": encoded_content
        }

    response = requests.put(url, json=data, headers=headers)

    if response.ok:
        print(f"File '{target_path}' uploaded to GitHub successfully.")
    else:
        print(f"Error uploading file '{target_path}' to GitHub.")
        print(response.status_code, response.text)
        
