import time
import schedule
import pytz
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import requests
import random
import os

# Google Drive API setup
DRIVE_FOLDER_ID = os.getenv(
    "DRIVE_FOLDER_ID"
)  # Replace with your Google Drive folder ID
API_KEY = os.getenv("API_KEY")  # Replace with your Google API key

# Pinterest API setup
PROD_PINTEREST_ACCESS_TOKEN = os.getenv("PROD_PINTEREST_ACCESS_TOKEN")
PINTEREST_ACCESS_TOKEN = os.getenv(
    "PROD_PINTEREST_ACCESS_TOKEN"
)  # Replace with your Pinterest access token
PINTEREST_BOARD_ID = os.getenv(
    "PINTEREST_BOARD_ID"
)  # Replace with your Pinterest board ID
INSTAGRAM_HANDLE = os.getenv("INSTAGRAM_HANDLE")  # Replace with your Instagram handle

# Timezone and posting schedule
AEST = pytz.timezone("Australia/Sydney")
POSTING_START_HOUR = 8  # 8 AM AEST
POSTING_END_HOUR = 21  # 9 PM AEST

# Captions for wedding photography posts
CAPTIONS = [
    "Capturing love in every moment. See more on Instagram @{handle} 📸 #WeddingPhotography",
    "Forever starts here. Check out my work on Instagram @{handle} 💍 #LoveInFocus",
    "Every love story deserves a beautiful frame. Follow @{handle} on Instagram! ✨ #WeddingMoments",
    "From vows to victory dances, I capture it all. Visit @{handle} on Instagram! 💕 #WeddingVibes",
    "Timeless memories, one click at a time. More on Instagram @{handle} 🌟 #ForeverMoments",
]


def authenticate_google_drive():
    """Return Google Drive service with API key."""
    return build("drive", "v3", developerKey=API_KEY)


def get_image_links():
    """Fetch image links from public Google Drive folder."""
    try:
        service = authenticate_google_drive()
        query = f"'{DRIVE_FOLDER_ID}' in parents and mimeType contains 'image/'"
        results = (
            service.files()
            .list(q=query, fields="files(id, name, webContentLink)")
            .execute()
        )
        files = results.get("files", [])
        # Use webContentLink for direct image download
        image_links = [file["webContentLink"] for file in files]
        return image_links
    except HttpError as error:
        print(f"An error occurred with Google Drive API: {error}")
        return []


def create_pinterest_post(image_url, caption):
    """Create a Pinterest post."""
    url = "https://api.pinterest.com/v5/pins"
    headers = {
        "Authorization": f"Bearer {PINTEREST_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    data = {
        "board_id": PINTEREST_BOARD_ID,
        "title": "Wedding Photography by Kyra",
        "description": caption.format(handle=INSTAGRAM_HANDLE),
        "link": f"https://www.instagram.com/{INSTAGRAM_HANDLE}/",
        "media_source": {"source_type": "image_url", "url": image_url},
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        print(f"Posted to Pinterest: {caption}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to post to Pinterest: {e}")


def schedule_posts():
    """Schedule posts evenly between 8 AM and 9 PM AEST."""
    image_links = get_image_links()
    if not image_links:
        print("No images found in the folder.")
        return

    today = datetime.now(AEST).replace(hour=0, minute=0, second=0, microsecond=0)
    start_time = today.replace(hour=POSTING_START_HOUR, tzinfo=AEST)
    end_time = today.replace(hour=POSTING_END_HOUR, tzinfo=AEST)
    total_seconds = (end_time - start_time).total_seconds()
    interval_seconds = total_seconds / len(image_links) if image_links else 1

    for i, image_url in enumerate(image_links):
        post_time = start_time + timedelta(seconds=i * interval_seconds)
        caption = random.choice(CAPTIONS)
        schedule.every().day.at(post_time.strftime("%H:%M")).do(
            create_pinterest_post, image_url=image_url, caption=caption
        )
        print(
            f"Scheduled post at {post_time.strftime('%H:%M')} with image: {image_url}"
        )


def main():
    """Main function to run the scheduler."""
    schedule.every().day.at("02:00").do(schedule_posts)  # Run daily at 2 AM AEST
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute


if __name__ == "__main__":
    main()
