import dropbox
import os
import shutil
from dotenv import load_dotenv
from dropbox.oauth import DropboxOAuth2FlowNoRedirect

def create_dropbox_client():
    load_dotenv()
    APP_KEY = os.getenv("APP_KEY")
    APP_SECRET = os.getenv("APP_SECRET")
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")

    # Create a Dropbox client instance with the access token and refresh token
    dbx = dropbox.Dropbox(
        oauth2_access_token=ACCESS_TOKEN,
        oauth2_refresh_token=REFRESH_TOKEN,
        app_key=APP_KEY,
        app_secret=APP_SECRET,
    )

    # The Dropbox SDK will now handle refreshing the token automatically when needed
    return dbx

# def get_dropbox_access_token():
    load_dotenv()
    APP_KEY = os.getenv("APP_KEY")
    APP_SECRET = os.getenv("APP_SECRET")
    # Create the OAuth2 flow instance
    auth_flow = dropbox.oauth.DropboxOAuth2FlowNoRedirect(
        consumer_key=APP_KEY,
        consumer_secret=APP_SECRET,
        token_access_type='offline',  # Use 'offline' to get a refreshable token
        scope=['files.content.read', 'files.content.write'],  # Specify scopes if necessary
        include_granted_scopes='user'  # Include previously granted scopes for this user
    )

    # Start the OAuth flow and get the authorization URL
    authorize_url = auth_flow.start()
    print("1. Go to: " + authorize_url)
    print("2. Click 'Allow' (you might have to log in first).")
    print("3. Copy the authorization code.")

    # Prompt the user to enter the authorization code
    auth_code = input("Enter the authorization code here: ").strip()

    # Exchange the authorization code for an access token
    try:
        oauth_result = auth_flow.finish(auth_code)
        access_token = oauth_result.access_token
        refresh_token = oauth_result.refresh_token if hasattr(oauth_result, 'refresh_token') else None
        print("Access token: " + access_token)
        if refresh_token:
            print("Refresh token: " + refresh_token)
        return access_token, refresh_token
    except Exception as e:
        print("Error: " + str(e))
        return None, None

# get_dropbox_access_token()


def zip_the_folder():
    path = os.path.dirname(__file__)
    path = path.split("functions")[0]
    pack_dir = os.path.join(path, "server_pack")
    shutil.make_archive("server_pack", "zip", pack_dir)

def upload_dropbox():
    zip_the_folder()
    load_dotenv()
    dbx = create_dropbox_client()
    with open("server_pack.zip", "rb") as f:
        file_content = f.read()
    dbx.files_upload(file_content, '/server_pack.zip', mode=dropbox.files.WriteMode.overwrite)
    os.remove("server_pack.zip")

if __name__ == "__main__":
    upload_dropbox()
