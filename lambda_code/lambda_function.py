import CustomTools
from openai import OpenAI
import os
import requests
from io import BytesIO
from PIL import Image


def lambda_handler(event, context):
    print('Loading function')
    #-----------------------------------
    #login to instagram
    instagrapi_client = CustomTools.instagram_api_login("./secrets/credentials.txt","./secrets/ClientSettings.json")

    #openai client
    with open ("./secrets/apiKey.txt", "r") as f:
        key = f.read()
    print(key)
    openai_client = OpenAI(api_key=key)

    #Generate image prompt
    response = openai_client.chat.completions.create(
    model="gpt-4",
    messages=[
        {
        "role": "system",
        "content": "You are a Dall E prompt generator. You will be trying to create prompts to create art that features different species of bats. The images you generate should be inspired by diverse art styles and works of art from around the world and throughout history. "
        },
        {
        "role": "user",
        "content": "I am an artist trying to promote the conservation of bat populations via interesting and novel art forms. Please generate Dall-E prompts that utilize art styles from different periods of history and from around the world and have as their subjects bats rather than humans."
        },
        {
        "role": "assistant",
        "content": " A Victorian-style portrait of a Vampire Bat with intricate lace detailing. \n An Egyptian Hieroglyphic mural depicting the life cycle of an Egyptian Fruit Bat.\n Impressionist painting in Monet's style showcasing Mexican Free-tailed Bats flying at dusk over water lilies pond.\n Japanese Ukiyo-e woodblock print featuring Japanese Pipistrelle bats against Mount Fuji backdrop. \nThe Starry Night inspired post-impressionistic artwork showing Big Brown Bats swirling around cypress trees under starlit sky \nGuernica-style cubism art by Picasso, portraying Townsend’s big-eared bat amidst chaos and peace symbols \nAmerican Gothic parody where instead of farmers there are two Pallid bats holding farming tools standing before their cave home \nArt Nouveau poster design promoting conservation efforts for Indiana Myotis (Myotis sodalis) using vibrant colors and organic forms\n Pop Art representation à la Andy Warhol: Four panels each displaying different species - Little Red Flying Fox, Greater Bulldog bat, Lesser Short-nosed fruit bat & Kitti's hog-nosed bat \nSurrealist Salvador Dali-inspired melting clocks scene but replacing clocks with Spotted-winged fruit bats hanging from tree branches "
        },
        {
        "role": "user",
        "content": "Please provide one more."
        }
    ],
    temperature=1.15,
    max_tokens=70,
    top_p=1,
    frequency_penalty=2,
    presence_penalty=2
    )
    image_prompt = response.choices[0].message.content
    print('Image Prompt:', image_prompt)


    #Generate image based on image prompt
    response = openai_client.images.generate(
        model="dall-e-3",
        prompt=image_prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url

    # Download and display the generated image
    image_response = requests.get(image_url)
    image_response.raise_for_status()
    image = Image.open(BytesIO(image_response.content))

    #Generate a caption
    response = openai_client.chat.completions.create(
    model="gpt-4",
    messages=[
        {
        "role": "system",
        "content": "You are an Instagram caption generator. Your goal is to promote bat conservation through poetry and humor. "
        },
        {
        "role": "user",
        "content": "Write an original short poem about bats. Use evocative language. The poem should promote environmentalism OR be humorous OR be from the perspective of a bat. Make it no longer than 15 words."
        },
        {
        "role": "user",
        "content": ("for context, the following is a description of an image which will accompany your poem: " + image_prompt )
        }
    ],
    temperature=1,
    max_tokens=100,
    top_p=1,
    frequency_penalty=2,
    presence_penalty=2
    )

    poem = response.choices[0].message.content
    print('Caption:', poem)

    #Declare Hashtags
    hashtags_list = [ "#savethebats", "#batsarecool", "#batsofinstagram", "#Bats", "#BatLove", "#fruitbat", "#aiart", "#ai", "#chatgpt", "#dalle", "#bat" ]
    hashtags_string = " ".join(str(x) for x in hashtags_list)

    #Make compound caption:
    caption = """{one}

    Support the research and conservation of bats:
    https://www.batcon.org/

    {three}
    """.format(one=poem, three= hashtags_string)

    max_number_of_likes = 3
    try:
        CustomTools.like_list_of_hashtag_medias(instagrapi_client, hashtags_list, max_number_of_likes)
    except Exception as e:
        print("Error occurred while executing CustomTools.like_list_of_hashtag_medias:", str(e))

    #Post image to instagram
    os.chdir("/tmp")
    image.save("ai_mush_pic.jpg")
    CustomTools.post_image_and_caption( "./ai_mush_pic.jpg" , caption, instagrapi_client )

    #-----------------------------------
    return "success"  # Echo back the first key value
    #raise Exception('Something went wrong')