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
        "content": "You are a Dall E prompt generator. You will be trying to create prompts to create art that features different species of fungi. The images you generate should be inspired by diverse art styles and works of art from around the world and throughout history. "
        },
        {
        "role": "user",
        "content": "I am an artist trying to promote the research and conservation of fungi via interesting and novel art forms. Please generate Dall-E prompts that utilize art styles from different periods of history and around the world and add fungi to them."
        },
        {
        "role": "assistant",
        "content": "A traditional Japanese Ukiyo-e styled print depicting a serene landscape with giant mushrooms dropping spores instead of cherry blossom trees dropping leaves.\n An Aztec codex inspired illustration incorporating corn smut fungus, honoring their reverence for this delicacy, also known as huitlacoche \n.A Greek amphora illustration depicting the myth of Dionysus discovering wine through yeast fungi.\n An intricate, 17th-century Dutch Golden Age still life, including a variety of mushrooms and lichens among the typical fruits and flowers.\n An Art Nouveau masterpiece in the style of Gustav Klimt but with mycelium and hyphae connecting the figures instead of symbolic shapes."
        },
        {
        "role": "user",
        "content": "Thank you. Please provide one more."
        }
    ],
        temperature=1.1,
        max_tokens=50,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=1
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
        "content": "Write an original short poem about fungi. Use evocative language. The poem should promote environmentalism OR be humorous OR be from the fungus. Make it no longer than 15 words."
        },
        {
        "role": "user",
        "content": ("For context, the following is a description of an image that will accompany your poem: " + image_prompt )
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
    hashtags_list = [ "#mushroom", "#fungi", "#mushroomart", "#mycologysociety", "#mycology", "#psychedelic", "#psychedelicart", "#ai", "#chatgpt", "#dalle", "mushroomartworks", "#fungilove" ]
    hashtags_string = " ".join(str(x) for x in hashtags_list)

    #Make compound caption:
    caption = """{one}

    Support the research and conservation of fungi:
    https://www.centraltexasmycology.org/

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