import CustomTools
import openai
import instagrapi
import os
from PIL import Image, ImageOps


def lambda_handler(event, context):
    print('Loading function')
    #-----------------------------------

    #note first time you login you may need to change client settings
    instagrapi_client = CustomTools.login("./secrets/apiKey.txt","./secrets/credentials.txt","./secrets/ClientSettings.json")
    instagrapi_client.account_info()

    response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {
            "role": "system",
            "content": "You are a DallE prompt generator. Your goal is to create prompts that create images of tattoo designs. "
        },
        {
            "role": "user",
            "content": "I am a tattoo artist. I am trying to generate tattoo designs. I need you to create Dallee prompts that would create tattoo designs that I can print to a piece of paper. I want the tattoos to be black and white. I want the tattoos to be relatively small and simple."
        },
        {
            "role": "assistant",
            "content": "Minimalist black and white geometric tattoo design featuring triangles, circles and lines\n\nSmall intricate mandala-inspired pattern in black ink for a wrist or ankle tattoo\n\nBlack silhouette of an elegant feather with delicate details as small forearm tattoo.\n\nCrescent moon encompassing pine trees within itself drawn only using fine line work.\n\nTiny constellation star map drawing appropriate for finger tattoos in monochrome.\n\nSimplistic rendition of DNA helix strip tattoo styled minimalistically making it perfect choice behind ear position\n\nBeautifully simplified hummingbird captured mid-flight created just by strokes ideal stand-alone piece towards inner bicep area."
        },
        {
            "role": "user",
            "content": "One more"
        }
    ],
    temperature=0.9,
    max_tokens=100,
    top_p=1,
    frequency_penalty=2,
    presence_penalty=2
    )
    image_prompt = response["choices"][0]["message"]["content"]
    print('Image Prompt:', image_prompt)

    #add custom words to image prompt
    additionalIdeas = ". minimalist, delicate line-drawing, not filled in, some symmetry"
    image_prompt += additionalIdeas

    #targeting image size 1024p or 512p
    target_size = 1024

    #generate image
    image = CustomTools.generate_image_from_prompt_with_dims(image_prompt ,target_size,target_size)
    os.chdir("/tmp") #this only works in lambda env, adding a ./ breaks the lambda version
    image.save("ai_tat_pic.jpg")
    image.show()

    # add border
    black_border_size = 5
    white_border_size = 105
    buffer = black_border_size + white_border_size
    img = Image.open('ai_tat_pic.jpg')
    width,height = img.size
    cropped_img = img.crop((buffer,buffer,width-buffer,height-buffer)) #left up right lower tuple -- cropping buffer number of pixels (0,0,width,height) is no cropping
    img_with_border_1 = ImageOps.expand(cropped_img, border=black_border_size, fill='black')
    img_with_border_2 = ImageOps.expand(img_with_border_1, border=white_border_size, fill='white')
    img_with_border_2.save('ai_tat_pic_with_border.jpg')

    #Generate a caption
    response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {
        "role": "system",
        "content": "You are an Instagram caption generator. Your goal is to promote an instagram tattoo account through poetry and humor. "
        },
        {
        "role": "user",
        "content": "Write an original short poem about some human emotion. Use evocative language. The poem should promote environmentalism, mysticism, OR be humorous. Make it no longer than 15 words."
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

    poem = response["choices"][0]["message"]["content"]
    print('Caption:', poem)

    #Declare Hashtags
    hashtags_list = [ "#sanantoniotattoo", "#austintattoo", "#freetattoo","#finelinetattoo", "#handpoked", "#stickandpoke", "#stickandpoketattoo", "#minimalisttattoo", "#diytattoo", "#singleneedletattoo" ]
    hashtags_string = " ".join(str(x) for x in hashtags_list)

    #Make compound caption:
    caption = """{one}

    {three}
    """.format(one=poem, two=image_prompt, three= hashtags_string)

    #Post image to instagram
    CustomTools.post_image_and_caption( "./ai_tat_pic_with_border.jpg" , caption, instagrapi_client )

    #-----------------------------------
    return "success"  # Echo back the first key value
    #raise Exception('Something went wrong')