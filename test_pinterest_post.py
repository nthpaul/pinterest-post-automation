from scheduler import create_pinterest_post

if __name__ == "__main__":
    test_image_url = "https://drive.google.com/uc?id=1mm2t6QHA6DmJ8AcCwsMcMMnheMzkvBYN&export=download"
    test_caption = "Test post"
    create_pinterest_post(test_image_url, test_caption)
