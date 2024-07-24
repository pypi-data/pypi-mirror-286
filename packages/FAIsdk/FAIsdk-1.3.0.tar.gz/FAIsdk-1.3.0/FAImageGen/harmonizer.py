# FAIsdk/FAImageGen/harmonizer.py
import base64
from io import BytesIO
from PIL import Image
from .api_client import APIClient

class Harmonizer:
    def __init__(self, client: APIClient):
        self.client = client

    def image_to_base64(self, image_path):
        with Image.open(image_path) as img:
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            return base64.b64encode(buffered.getvalue()).decode('utf-8')

    def harmonize_image(self, image_path, prompt):
        image_base64 = self.image_to_base64(image_path)
        data = {
            "image": image_base64,
            "prompt": prompt,
            "mode": "harmonize"
        }
        response = self.client.post('Image-gen', json_data=data)
        if response.status_code == 200:
            response_data = response.json()
            if 'image' in response_data:
                image_data = response_data['image']
                image_bytes = base64.b64decode(image_data)
                image = Image.open(BytesIO(image_bytes))
                image.save("harmonized_output_image.png")
                print("Harmonized image retrieved and saved as harmonized_output_image.png.")
                return image
            else:
                print("Response does not contain 'image'")
        else:
            print(f"Failed to harmonize image. Status code: {response.status_code}")
            print(response.text)
