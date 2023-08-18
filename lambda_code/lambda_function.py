import CustomTools
import openai
import os

def lambda_handler(event, context):
    print('Loading function')
    #-----------------------------------

    instagrapi_client = CustomTools.login("./secrets/apiKey.txt","./secrets/credentials.txt","./secrets/ClientSettings.json")

    #generate dalle prompt - using openai playground
    response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {
        "role": "system",
        "content": "a Dall E prompt generator"
        },
        {
        "role": "user",
        "content": "I am an artist trying to promote conservation of bat populations via interesting and novel art forms. Please generate 5 Dall E prompts that utilize art styles from history and have as their subjects bats rather than humans."
        },
        {
        "role": "assistant",
        "content": "Victorian-era painting of a masquerade ball with elaborate costumes, contrasting colors, and soft lighting. All of the attendees are humans with bat heads. \n\nEarly morning photography of a landscape shrouded in mist, with diffused light and long shadows. In the foreground a bat is silhouetted hanging from a perch.\n\nAn ancient chinese ink painting. The image shows a bat in a nature scene. The image evokes a feeling of zen. \n\nA greek statue of a bat.\n\na kaleidoscopic and psychedelic vision of the afterlife. The image shows that god is a bat. It is mysterious in tone."
        },
        {
        "role": "user",
        "content": "Generate one more prompt. Make it as original as possible."
        },
        {
        "role": "assistant",
        "content": "Surrealist style painting reminiscent of Salvador Dali, where the moon is replaced by a hyper-realistic, phosphorescent bat casting ethereal light on an otherworldly dreamscape. The stars appear as tiny bats dotting the night sky while"
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

    #Generate image based on image prompt
    image = CustomTools.generate_image_from_prompt( image_prompt )

    #Generate a caption
    response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {
        "role": "system",
        "content": "You are an Instagram caption generator. Your goal is to promote bat conservation through poetry and humor. "
        },
        {
        "role": "user",
        "content": "Write an original short poem about bats. Use evocative language. The poem should promote environmentalism OR be humorous. Make it no longer than 15 words."
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
    hashtags_list = [ "#savethebats", "#batsarecool", "#batsofinstagram", "#Bats", "#BatLove", "#fruitbat", "#aiart", "#ai", "#chatgpt", "#dalle", "#bat" ]
    hashtags_string = " ".join(str(x) for x in hashtags_list)

    #Make compound caption:
    caption = """{one}

    inspiration: {two}

    {three}
    """.format(one=poem, two=image_prompt, three= hashtags_string)

    #Post image to instagram
    os.chdir("/tmp")
    image.save("ai_bat_pic.jpg")
    CustomTools.post_image_and_caption( "./ai_bat_pic.jpg" , caption, instagrapi_client )

    max_number_of_likes = 4
    CustomTools.like_list_of_hashtag_medias(instagrapi_client, hashtags_list, max_number_of_likes)

    #-----------------------------------
    return "success"  # Echo back the first key value
    #raise Exception('Something went wrong')