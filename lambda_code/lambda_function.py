import CustomTools

def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))
    print('Loading function')

    #-----------------------------------

    CustomTools.full_pipeline()

    #-----------------------------------
    return "success"  # Echo back the first key value
    #raise Exception('Something went wrong')