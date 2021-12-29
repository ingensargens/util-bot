# util-bot

Util bot is a personal bot used for testing with the pycord api and image uploading. [Prefix: u!] **readme is still a wip**

## Current functions:
* avatar: (parameters: userID - optional) If no user id is provided, returns the authors' discord avatar. Otherwise, returns the discord avatar of the user provided in the userID. If the avatar is animated, it is returned in the `.gif` format.

* emote: (parameters: emote - required) [aliases = 'av']

* pixelate (parameters: scale - optional) [aliases = 'emoji']

* grayscale (parameters: an attached image) [aliases = 'gray', 'grey', 'greyscale']

* blend (parameters: 2 different attached images, both with the same pixel size) 
