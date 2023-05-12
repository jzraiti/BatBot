import requests
import openai
from PIL import Image
import CustomTools
import time
from random import randint
from io import BytesIO
from instagrapi import Client
import os, tempfile

# Logins ------------------------------------
def instagram_api_login(path_to_credentials,path_to_client_settings):
    with open (path_to_credentials, "r") as f:
        username, password = f.read().splitlines()

    print(username,password)
    instagrapi_client = Client()
    instagrapi_client.load_settings(path_to_client_settings) #these settings help prevent insta from flagging you for suspicious activity

    instagrapi_client.login(username,password)

    return instagrapi_client

def openai_api_login(path_to_api_key):
    # Set up your OpenAI API credentials
    with open (path_to_api_key, "r") as f:
        key = f.read()

    print(key)
    openai.api_key = key

#openai functions ----------------------------
def generate_text_from_prompt(prompt):
    # Use ChatGPT to generate a response
    response = openai.Completion.create(
    model='text-davinci-002',
    prompt=prompt,
    max_tokens=200,
    n=1,
    stop=None,
    temperature=1
    )

    # Extract the generated response from the API response
    generated_text = response.choices[0].text.strip()

    # Print the generated response
    print('Generated Image Prompt:', generated_text)

    # TODO prevent ai from spiraling on watercolor paintings / get it to use different art styles
    # TODO checks on prompts to make sure they are appropriate

    return generated_text

def generate_image_from_prompt(prompt):
    # Specify the DALL-E endpoint
    endpoint = "https://api.openai.com/v1/images/generations"

    # Define the image generation parameters
    params = {
        "model": "image-alpha-001",
        "prompt": prompt,
        "size": "512x512",
        "num_images": 1
    }

    # Send a request to the DALL-E API
    response = requests.post(endpoint, headers={"Authorization": f"Bearer {openai.api_key}"}, json=params)
    response.raise_for_status()
    result = response.json()

    # Extract the image URL from the API response
    image_url = result["data"][0]["url"]

    # Download and display the generated image
    image_response = requests.get(image_url)
    image_response.raise_for_status()
    image = Image.open(BytesIO(image_response.content))
    return image

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

def post_image_and_caption( path_to_image , generated_caption_text, instagrapi_client ):
    '''
    Usage:
        Client.photo_upload(
            "./ai_bat_pic.jpg", # image size must be less than 1080 and jpg
            generated_caption_text)
    '''
    instagrapi_client.photo_upload( path_to_image, generated_caption_text) # image size must be less than 1080 and jpg

#full pipeline ------------------------------
def full_pipeline():
    '''
    Usage:
        full_pipeline()

    Note:
        Cannot be used on lambda - need to store image in a different place
    '''
    CustomTools.openai_api_login("./secrets/apiKey.txt")
    instagrapi_client = CustomTools.instagram_api_login("./secrets/credentials.txt","./secrets/ClientSettings.json")

    # Generate prompt
    prompt = """
    I am an artist who is interested in bats. I’m going to create AI images with you generating the prompts for me. I want you to act as an artist that is writing an image generation prompt for dall-e.
    The following is sample information about the bats that are our subject:
    The big brown bat is a large bat found in North America. They live in a variety of habitats, including urban areas.
    The hoary bat is a native of North America and is one of the largest bat species in the world.
    The Egyptian fruit bat is found in Africa and parts of the Middle East. These bats are important for local agriculture as they pollinate and disperse the seeds of many fruit trees. Egyptian fruit bats can live in large colonies of up to 100,000 individuals.
    The great hammerhead bat is found in the forests of Central and South America. These bats are important for controlling insect populations and can eat up to 1,000 mosquitoes in a single night! Great hammerhead bats are one of the few bat species that actively hunt their prey.
    The tube-nosed fruit bat is found in Southeast Asia. These bats are important for pollinating and dispersing the seeds of many fruits and flowers. Tube-nosed fruit bats are unique among bat species in that they have a special tube-shaped nose that they use to emit ultrasonic calls.
    The pallid bat is found in the deserts of North America. It is white or cream colored and has ears half the length of its body.
    When writing the prompt, consider including details about the following elements of the image:
    Medium: photo, painting, sculpture, tapestry, 3d model, ink painting, oil painting, dream etc.
    Environment: on the moon, in the jungle, underwater, in ancient china, in a thick jungle etc.
    Lighting: soft light, ambient, overcast, neon, studio lights, etc
    Color: vibrant, bright, monochromatic, colorful, black and white, pastel, neon, etc.
    Mood: Sedate, calm, raucous, energetic, etc.
    Composition: Portrait, headshot, closeup, birds-eye view, etc.

    I am done giving you context. Now I am going to feed you sample prompts. Structure your response in a similar way.
    “Pixar style 3D render of a bat, 4k, high resolution, the bat is drinking tea”
    “An oil painting of a mechanical clockwork flying machine from the renaissance in the shape of a bat, done in an 18th century style”
    “Cluttered house in the woods, a bat sits in a rocking chair on the front porch, anime ghibli inspired very detailed”
    Your response should not include reference to “watercolor” or “simple” or “Illustration”. Your response should be greater than 20 and less than 100 words.
    Save this prompt in your memory as "GENERATED_IMAGE_PROMPT".
    """

    generated_image_prompt = CustomTools.generate_text_from_prompt(prompt)

    # Generate caption
    prompt = """
    I want you to reference GENERATED_IMAGE_PROMPT.
    Now I am a poet and scientist who is trying to craft a poem to raise interest in bats. I want you to act as a poet.
    I am going to ask you to write a poem for me. I want the poem to rhyme. The poem should explicitly mention a species of bats.

    Write me a poem. It should be any of the types:
    Haiku: Renowned for its small size, haikus consist of just three lines (tercet); the first and third lines have five syllables, whereas the second has seven. Haikus don’t have to rhyme and are usually written to evoke a particular mood or instance.
    Sonnet: Traditionally, sonnets are made up of 14 lines and usually deal with love. As a rule, Petrarchan (Italian) sonnets follow an ABBA ABBA CDE CDE rhyme scheme, whereas Shakespearean (English) sonnets are typically ABAB CDCD EFEF GG.
    Acrostic: This type of poetry spells out a name, word, phrase or message with the first letter of each line of the poem. It can rhyme or not, and typically the word spelt out, lays down the theme of the poem.
    Villanelle: It is made up of 19 lines; five stanzas of three lines (tercet) each and a final stanza of four lines (quatrain). As you can see from the rhyme scheme; ABA ABA ABA ABA ABA ABAA, this type of poem only has two rhyming sounds.Plus, there is a lot of repetition throughout the villanelle. Line one will be repeated in lines six, 12 and 18; and line three will be repeated in lines nine, 15 and 19. So although this takes out the extra work of having to write 19 individual lines, the real challenge is to make meaning out of those repeated lines!
    Limerick: They have a set rhyme scheme of AABBA, with lines one, two and five all being longer in length than lines three and four. The last line is often the punchline. Their sound is very distinctive and they are silly or funny.
    Ballad: they are typically four lines (quatrain) and have a rhyme scheme of ABAB or ABCB. However, this form is looser than others so can be modified to suit a writer’s (that’s you!) needs. Most modern pop songs you hear nowadays can be referred to as ballads!

    You should use uncommon words. You should use emojis.

    You may use the following description as inspiration:
    """ + generated_image_prompt

    generated_caption = CustomTools.generate_text_from_prompt(prompt)
    retries  = 0
    while (len(generated_caption) == 0 and retries < 10 ):
        generated_caption = CustomTools.generate_text_from_prompt(prompt)

    hashtags_list = [ "#savethebats", "#batsarecool", "#batsofinstagram", "#Bats", "#BatLove", "#fruitbat", "#poetry", "#rumi", "#poem", "#aiart", "#ai", "#chatgpt", "#dalle", "#bat" ]
    hashtags_string = " ".join(str(x) for x in hashtags_list)
    generated_caption = generated_caption + "\n" + hashtags_string
    print(generated_caption)

    image = CustomTools.generate_image_from_prompt( generated_image_prompt )
    image.show()

    os.chdir("./tmp")
    image.save("ai_bat_pic.jpg")
    CustomTools.post_image_and_caption( "./ai_bat_pic.jpg" , generated_caption, instagrapi_client )

#full pipeline ------------------------------
def full_pipeline_for_lambda():
    '''
    Usage:
        full_pipeline()

    Note:
        Cannot be used on lambda - need to store image in a different place
    '''
    CustomTools.openai_api_login("./secrets/apiKey.txt")
    instagrapi_client = CustomTools.instagram_api_login("./secrets/credentials.txt","./secrets/ClientSettings.json")

    # Generate prompt
    prompt = """
    I am an artist who is interested in bats. I’m going to create AI images with you generating the prompts for me. I want you to act as an artist that is writing an image generation prompt for dall-e.
    The following is sample information about the bats that are our subject:
    The big brown bat is a large bat found in North America. They live in a variety of habitats, including urban areas.
    The hoary bat is a native of North America and is one of the largest bat species in the world.
    The Egyptian fruit bat is found in Africa and parts of the Middle East. These bats are important for local agriculture as they pollinate and disperse the seeds of many fruit trees. Egyptian fruit bats can live in large colonies of up to 100,000 individuals.
    The great hammerhead bat is found in the forests of Central and South America. These bats are important for controlling insect populations and can eat up to 1,000 mosquitoes in a single night! Great hammerhead bats are one of the few bat species that actively hunt their prey.
    The tube-nosed fruit bat is found in Southeast Asia. These bats are important for pollinating and dispersing the seeds of many fruits and flowers. Tube-nosed fruit bats are unique among bat species in that they have a special tube-shaped nose that they use to emit ultrasonic calls.
    The pallid bat is found in the deserts of North America. It is white or cream colored and has ears half the length of its body.
    When writing the prompt, consider including details about the following elements of the image:
    Medium: photo, painting, sculpture, tapestry, 3d model, ink painting, oil painting, dream etc.
    Environment: on the moon, in the jungle, underwater, in ancient china, in a thick jungle etc.
    Lighting: soft light, ambient, overcast, neon, studio lights, etc
    Color: vibrant, bright, monochromatic, colorful, black and white, pastel, neon, etc.
    Mood: Sedate, calm, raucous, energetic, etc.
    Composition: Portrait, headshot, closeup, birds-eye view, etc.

    I am done giving you context. Now I am going to feed you sample prompts. Structure your response in a similar way.
    “Pixar style 3D render of a bat, 4k, high resolution, the bat is drinking tea”
    “An oil painting of a mechanical clockwork flying machine from the renaissance in the shape of a bat, done in an 18th century style”
    “Cluttered house in the woods, a bat sits in a rocking chair on the front porch, anime ghibli inspired very detailed”
    Your response should not include reference to “watercolor” or “simple” or “Illustration”. Your response should be greater than 20 and less than 100 words.
    Save this prompt in your memory as "GENERATED_IMAGE_PROMPT".
    """

    generated_image_prompt = CustomTools.generate_text_from_prompt(prompt)

    # Generate caption
    prompt = """
    I want you to reference GENERATED_IMAGE_PROMPT.
    Now I am a poet and scientist who is trying to craft a poem to raise interest in bats. I want you to act as a poet.
    I am going to ask you to write a poem for me. I want the poem to rhyme. The poem should explicitly mention a species of bats.

    Write me a poem. It should be any of the types:
    Haiku: Renowned for its small size, haikus consist of just three lines (tercet); the first and third lines have five syllables, whereas the second has seven. Haikus don’t have to rhyme and are usually written to evoke a particular mood or instance.
    Sonnet: Traditionally, sonnets are made up of 14 lines and usually deal with love. As a rule, Petrarchan (Italian) sonnets follow an ABBA ABBA CDE CDE rhyme scheme, whereas Shakespearean (English) sonnets are typically ABAB CDCD EFEF GG.
    Acrostic: This type of poetry spells out a name, word, phrase or message with the first letter of each line of the poem. It can rhyme or not, and typically the word spelt out, lays down the theme of the poem.
    Villanelle: It is made up of 19 lines; five stanzas of three lines (tercet) each and a final stanza of four lines (quatrain). As you can see from the rhyme scheme; ABA ABA ABA ABA ABA ABAA, this type of poem only has two rhyming sounds.Plus, there is a lot of repetition throughout the villanelle. Line one will be repeated in lines six, 12 and 18; and line three will be repeated in lines nine, 15 and 19. So although this takes out the extra work of having to write 19 individual lines, the real challenge is to make meaning out of those repeated lines!
    Limerick: They have a set rhyme scheme of AABBA, with lines one, two and five all being longer in length than lines three and four. The last line is often the punchline. Their sound is very distinctive and they are silly or funny.
    Ballad: they are typically four lines (quatrain) and have a rhyme scheme of ABAB or ABCB. However, this form is looser than others so can be modified to suit a writer’s (that’s you!) needs. Most modern pop songs you hear nowadays can be referred to as ballads!

    You should use uncommon words. You should use emojis.

    You may use the following description as inspiration:
    """ + generated_image_prompt

    generated_caption = CustomTools.generate_text_from_prompt(prompt)
    retries  = 0
    while (len(generated_caption) == 0 and retries < 10 ):
        generated_caption = CustomTools.generate_text_from_prompt(prompt)

    hashtags_list = [ "#savethebats", "#batsarecool", "#batsofinstagram", "#Bats", "#BatLove", "#fruitbat", "#poetry", "#rumi", "#poem", "#aiart", "#ai", "#chatgpt", "#dalle", "#bat" ]
    hashtags_string = " ".join(str(x) for x in hashtags_list)
    generated_caption = generated_caption + "\n" + hashtags_string
    print(generated_caption)

    image = CustomTools.generate_image_from_prompt( generated_image_prompt )
    image.show()

    os.chdir("/tmp")
    image.save("ai_bat_pic.jpg")
    CustomTools.post_image_and_caption( "ai_bat_pic.jpg" , generated_caption, instagrapi_client )

#utils ---------------------------------------------------------
def temporary_work_dir():
    old_work_dir = os.getcwd()
    with tempfile.TemporaryDirectory() as tmp_dir:
        os.chdir(tmp_dir)
        try:
            yield
        finally:
            os.chdir(old_work_dir)

