import dropbox
import os
import shutil
from dotenv import load_dotenv
from dropbox.oauth import DropboxOAuth2FlowNoRedirect


def zip_the_folder():
    path = os.path.dirname(__file__)
    path = path.split("functions")[0]
    pack_dir = os.path.join(path, "server_pack")
    shutil.make_archive("server_pack", "zip", pack_dir)

def upload_dropbox():
    zip_the_folder()
    load_dotenv()
    TOKEN = os.getenv("ACCESS_TOKEN")

    dbx = dropbox.Dropbox(TOKEN)
    with open("server_pack.zip", "rb") as f:
        file_content = f.read()
    dbx.files_upload(file_content, '/server_pack.zip', mode=dropbox.files.WriteMode.overwrite)
    os.remove("server_pack.zip")

if __name__ == "__main__":
    upload_dropbox()
