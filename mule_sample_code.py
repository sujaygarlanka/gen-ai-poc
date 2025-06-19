import requests

# Step 1: Authenticate
def get_access_token(client_id, client_secret):
    url = "https://anypoint.mulesoft.com/accounts/api/v2/oauth2/token"
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()["access_token"]

# Step 2: Search for the API in Exchange
def search_api(api_name, access_token):
    url = f"https://anypoint.mulesoft.com/exchange/api/v2/assets?q={api_name}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    assets = response.json()
    return assets["results"][0] if assets["results"] else None

# Step 3: Get asset version info
def get_asset_metadata(group_id, asset_id, version, access_token):
    url = f"https://anypoint.mulesoft.com/exchange/api/v2/assets/{group_id}/{asset_id}/{version}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

# Step 4: Download spec file
def download_spec_file(group_id, asset_id, version, filename, access_token):
    url = f"https://anypoint.mulesoft.com/exchange/api/v2/assets/{group_id}/{asset_id}/{version}/files/{filename}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

# Main logic
if __name__ == "__main__":
    CLIENT_ID = "<YOUR_CLIENT_ID>"
    CLIENT_SECRET = "<YOUR_CLIENT_SECRET>"
    API_NAME = "your-api-name"

    token = get_access_token(CLIENT_ID, CLIENT_SECRET)
    asset = search_api(API_NAME, token)

    if not asset:
        print("API not found.")
        exit()

    group_id = asset["groupId"]
    asset_id = asset["assetId"]
    version = asset["latestVersion"]

    metadata = get_asset_metadata(group_id, asset_id, version, token)
    file_list = metadata.get("files", [])

    # Try to find a RAML or OAS file
    for f in file_list:
        if f.endswith((".raml", ".yaml", ".json")):
            spec = download_spec_file(group_id, asset_id, version, f, token)
            print(f"\n--- {f} ---\n{spec}")
            break
    else:
        print("No API spec file found.")