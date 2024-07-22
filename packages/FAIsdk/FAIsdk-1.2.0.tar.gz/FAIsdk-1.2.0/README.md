# InstantLight-sdk

## Installation

Install the SDK using pip:

```bash
pip install FAIsdk
```

## Usage of InstantLight

Here’s an example of how to use the InstantLight SDK to make an API call and handle the response:

```bash
from FAIsdk.InstantLight import InstantLightSDK
from PIL import Image
import base64
from io import BytesIO

# Initialize the SDK
sdk = YourSDK(
    base_url='https://api.fotographer.ai/instantLight',
    api_key='your_api_key',
    email='your_email@example.com'
)

# Convert images to base64
def image_to_base64(image_path):
    with Image.open(image_path) as img:
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')

# Prepare the image data
foreground_image64 = image_to_base64('path_to_foreground_image.png')
background_image64 = image_to_base64('path_to_background_image.png')

# Define the image data
image_data = {
    "foreground_image64": foreground_image64,
    "background_image64": background_image64,
    "prompt": "example prompt",
    "mode": 2,
    "prompt_strength": 0.8,
    "inf_factor": 1.00,
    "mask_strength": 0.5,
    "image_width": 1400,
    "image_height": 1400,
    "additional_prompt": "",
    "negative_prompt": "",
    "lights": []
}

# Make the API call
response = sdk.image_generation.get_image_gen(image_data)

# Print the response keys for debugging
print("Response Keys:", response.keys())

# Print the keys at all levels of the response for debugging
for key, value in response.items():
    if isinstance(value, dict):
        print(f"Response[{key}] Keys: {value.keys()}")

# Save the image and mask image if they exist in the response
if 'image' in response:
    image_data = response['image']
    image_bytes = base64.b64decode(image_data)
    image = Image.open(BytesIO(image_bytes))
    image.save("output_image.png")
    print("Image retrieved and saved as output_image.png.")
    
    if 'mask_image' in response:
        mask_data = response['mask_image']
        mask_bytes = base64.b64decode(mask_data)
        mask_image = Image.open(BytesIO(mask_bytes))
        mask_image.save("output_mask_image.png")
        print("Mask retrieved and saved as output_mask_image.png.")
else:
    print("Response does not contain 'image'")
```

Make sure to update `your_api_key` and `your_email@example.com` with the actual values in the example usage section.

## Usage of ImageGen

```bash
from FAIsdk.FAImageGen import ImageGen as FAImageGenSDK
from PIL import Image
import base64
from io import BytesIO

# Initialize the SDK
sdk = FAImageGenSDK(
    base_url='https://api.fotographer.ai/Image-gen',
    api_key='your_api_key',
    email='your_email@example.com'
)

# Convert images to base64
def image_to_base64(image_path):
    with Image.open(image_path) as img:
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')

# Prepare the image data
foreground_image64 = image_to_base64('path_to_foreground_image.png')
background_image64 = image_to_base64('path_to_background_image.png')

# Define the image data
image_data = {
    "foreground_image64": foreground_image64,
    "background_image64": background_image64,
    "prompt": "example prompt",
    "mode": 2,
    "prompt_strength": 0.8,
    "inf_factor": 1.00,
    "mask_strength": 0.5,
    "image_width": 1400,
    "image_height": 1400,
    "additional_prompt": "",
    "negative_prompt": "",
    "lights": []
}

# Make the API call
response = sdk.image_generation.get_image_gen(image_data)

# Print the response keys for debugging
print("Response Keys:", response.keys())

# Save the image and mask image if they exist in the response
if 'image' in response:
    image_data = response['image']
    image_bytes = base64.b64decode(image_data)
    image = Image.open(BytesIO(image_bytes))
    image.save("output_image.png")
    print("Image retrieved and saved as output_image.png.")
    
    if 'mask_image' in response:
        mask_data = response['mask_image']
        mask_bytes = base64.b64decode(mask_data)
        mask_image = Image.open(BytesIO(mask_bytes))
        mask_image.save("output_mask_image.png")
        print("Mask retrieved and saved as output_mask_image.png.")
else:
    print("Response does not contain 'image'")
```