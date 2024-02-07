# BatBot

## Requirements

### Required Files

tmp/credentials.txt:
username
password

tmp/apiKey.txt:
key

tmp/ClientSettings.json: (optional)
settings

### Required Libraries

OpenAI

PIL

Instagrapi

## All to support the greatest game of all time:

### Bat's Life

https://apps.apple.com/us/app/bats-life/id1584580569

## Creating lambda layers -

It is highly recommended to do so through ec2 instances because they have the same os as the lambdas - this avoids system conflicts that are otherwise a nightmare to resolve

see:
https://www.thelastdev.com/how-to-create-an-aws-lambda-layer-2/
https://tecadmin.net/how-to-install-python-3-11-on-amazon-linux-2/#:~:text=Using%20%60altinstall%60%20instead%20of%20%60,file%20to%20free%20some%20space.

Can try modifying and using the Makefile in lambda layer folder - it is designed to be used in an ec2 instance of Amazon Linux