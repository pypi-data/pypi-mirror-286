import requests
from bs4 import BeautifulSoup
import os

def download_pin(pinterest_url, filename=None):
    """
    Downloads an image from the specified Pinterest URL.

    Args:
        pinterest_url (str): The URL of the Pinterest pin containing the image.
        filename (str, optional): The desired filename for the downloaded image.
            If not provided, a filename will be generated based on the URL.

    Returns:
        str: The path to the downloaded image file. None if an error occurs.

    Raises:
        requests.exceptions.RequestException: If there's an issue fetching the content.
        Exception: For any unexpected errors.
    """

    try:
        response = requests.get(pinterest_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Prioritize images with explicit classes
        image_tags = soup.find_all('img', class_=['h-image-fit', 'h-unsplash-img'])

        # Fallback to images with specific source URLs
        if not image_tags:
            image_tags = soup.find_all('img', attrs={'src': lambda src: src and src.startswith('https://i.pinimg.com/')})

        if not image_tags:
            print(f"Image URL not found on Pinterest: {pinterest_url}")
            return None

        image_url = image_tags[0]['src']

        if not filename:
            filename = image_url.split('/')[-1]

        # Create a safe directory to avoid overwriting existing files
        safe_filename = os.path.splitext(filename)[0] + "_" + os.path.splitext(filename)[1]
        safe_filepath = os.path.join(os.getcwd(), safe_filename)
        counter = 1
        while os.path.exists(safe_filepath):
            counter += 1
            safe_filename = os.path.splitext(filename)[0] + "_" + str(counter) + os.path.splitext(filename)[1]
            safe_filepath = os.path.join(os.getcwd(), safe_filename)

        response = requests.get(image_url, stream=True)
        response.raise_for_status()

        with open(safe_filepath, 'wb') as f:
            for chunk in response.iter_content(52000):
                f.write(chunk)

        print(f"Image downloaded successfully: {safe_filepath}")
        return safe_filepath

    except requests.exceptions.RequestException as e:
        print(f"Error fetching content from URL: {e}")
    except Exception as e:
        print(f"Unexpected 1  error: {e}")
    return None
