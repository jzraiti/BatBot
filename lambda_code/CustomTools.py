from openai import OpenAI
import time
from random import randint
from instagrapi import Client

#Logins ------------------------------------
def instagram_api_login(path_to_credentials,path_to_client_settings):
    with open (path_to_credentials, "r") as f:
        username, password = f.read().splitlines()

    print(username,password)
    instagrapi_client = Client()
    instagrapi_client.load_settings(path_to_client_settings) #these settings help prevent insta from flagging you for suspicious activity

    instagrapi_client.login(username,password)

    return instagrapi_client

def openai_api_login(path_to_api_key):
    with open ("./secrets/apiKey.txt", "r") as f:
        key = f.read()

    print(key)
    openai_client = OpenAI(api_key=key)
    return openai_client

#openai functions ----------------------------

#instagram functions -------------------------
def like_hashtag_medias( instagrapi_client , hashtag,number_of_media ):
    '''
    Usage:
        Hashtags = ["savethebats","batsarecool","batsofinstagram","Bats","BatLove","fruitbat"]

        for hashtag in Hashtags:
        CustomTools.like_hashtag_medias(Client,hashtag,2)
    '''
    print(f"Starting...")
    medias = instagrapi_client.hashtag_medias_recent(hashtag,number_of_media)
    print(f"number of media found in {hashtag} : {len(medias)}")
    for i, media in enumerate(medias):
        instagrapi_client.media_like(media.id)
        time.sleep(randint(1,3))
        print(f"Liked post number {i+1} of hashtag {hashtag}")

def like_list_of_hashtag_medias(instagrapi_client, hashtags_list, max_number_of_likes):
    """REQUIRES RANDOM
    likes a random number of media up to the max number of likes

    Args:
        instagrapi_client (Client): client from login
        hashtags_list (list of strings): List of hashtags in the format ["#savethebats", "#batsarecool"]
    """
    for hashtag in hashtags_list:
        hashtag = hashtag.replace("#","")

        random_number = randint(1, max_number_of_likes)
        like_hashtag_medias( instagrapi_client , hashtag , random_number )

def post_image_and_caption( path_to_image , generated_caption_text, instagrapi_client ):
    '''
    Usage:
        Client.photo_upload(
            "./ai_bat_pic.jpg", # image size must be less than 1080 and jpg
            generated_caption_text)
    '''
    instagrapi_client.photo_upload( path_to_image, generated_caption_text) # image size must be less than 1080 and jpg

#full pipeline ------------------------------