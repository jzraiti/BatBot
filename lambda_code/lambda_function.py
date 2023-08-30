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
        "content": "You are a DallE prompt generator. Your goal is to create prompts that create original tattoo designs."
        },
        {
        "role": "user",
        "content": "I want you to generate some tattoo designs for a stick-and-poke tattoo. The tattoo should be smaller than a phone. The tattoos should be mostly black and white. If there are colors they are used sparingly for highlight. Make the tattoos as minimal and simple as possible. "
        },
        {
        "role": "assistant",
        "content": "A tattoo design. In black and white. Minimalist. Symmetrical \nminimalistic tattoo representing the emotion of awe. monochromatic lines , white background. Symmetrical\nA minimalist stick-and-poke tattoo design of a crescent moon intertwined with twinkling stars\nStick-and-poke styled wildflower bouquet tattoo. It is the size of a lighter and placed on the upper arm\nSmall silhouette of a miniaturized wave crashing, with touches of blue to highlight the foam\nA minimalistic geometric pattern made up purely of minuscule dots arranged in interesting shapes\nMinimalistic geometric dog silhouette in black ink with just a hint of red for the collar.\nAn incredibly simplified, abstract representation of mountains and an idyllic lakeside scenery solely through varying lines thicknesses. The lines are of different monochrome pigments. Shading is done by stipling alone. "
        },
        {
        "role": "user",
        "content": "Thank you. Please provide one more."
        }
    ],
    temperature=1,
    max_tokens=50,
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
    CustomTools.post_image_and_caption( "./ai_bat_pic.jpg" , caption, instagrapi_client )

    #-----------------------------------
    return "success"  # Echo back the first key value
    #raise Exception('Something went wrong')