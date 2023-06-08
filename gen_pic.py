import requests
from requests.structures import CaseInsensitiveDict
from PIL import Image
import secret
import os
import time
import openai

openai.api_key = secret.chatgpt_api

def generate_image(prompt):
    while True:
        try:
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size="256x256",
                response_format="url"
            )
            break  # if the request is successful, we break the loop
        except:
            time.sleep(3)  # wait for 3 seconds before trying again

    if response is None:
        raise ValueError("Failed to generate image")

    image_url = response['data'][0]['url']
    return image_url
