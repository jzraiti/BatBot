import requests
import openai
from PIL import Image

import CustomTools
import time
from random import randint
from io import BytesIO
from instagrapi import Client

def login_to_instagram(path_to_credentials,path_to_client_settings):
    with open (path_to_credentials, "r") as f:
        username, password = f.read().splitlines()

    print(username,password)
    client = Client()
    client.load_settings(path_to_client_settings) #these settings help prevent insta from flagging you for suspicious activity

    client.login(username,password)

    return client

def like_hashtag_medias(client,hashtag,number_of_media):
    print(f"Starting...")
    medias = client.hashtag_medias_recent(hashtag,number_of_media)
    print(f"number of media found in {hashtag} : {len(medias)}")
    for i, media in enumerate(medias):
        client.media_like(media.id)
        time.sleep(randint(1,3))
        print(f"Liked post number {i+1} of hashtag {hashtag}")

def post_image_and_caption():
    return 0

def openai_api_login(path_to_api_key):
    # Set up your OpenAI API credentials
    with open ("./tmp/apiKey.txt", "r") as f:
        key = f.read()

    print(key)
    openai.api_key = key

#def generate_