from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os

DRIVE_FOLDER_ID = os.getenv("DRIVE_FOLDER_ID", "")
API_KEY = os.getenv("API_KEY", "")


def authenticate_google_drive():
    return build("drive", "v3", developerKey=API_KEY)


def get_image_links():
    try:
        service = authenticate_google_drive()
        query = f"'{DRIVE_FOLDER_ID}' in parents and mimeType contains 'image/'"
        results = (
            service.files()
            .list(q=query, fields="files(id, name, webContentLink)")
            .execute()
        )
        files = results.get("files", [])
        image_links = [file["webContentLink"] for file in files]
        return image_links
    except HttpError as error:
        print(f"An error occurred: {error}")
        return []


if __name__ == "__main__":
    links = get_image_links()
    print("Found images:", links)
