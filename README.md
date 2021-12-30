# util-bot

Util bot is a personal bot used for testing with the pycord api and image uploading. [Prefix: u!] 

## Current functions:
* avatar: (parameters: userID - optional) If no user id is provided, returns the authors' discord avatar. Otherwise, returns the discord avatar of the user provided in the userID. If the avatar is animated, it is returned in the `.gif` format.

* emote: (parameters: emote - required) [aliases = 'av'] Returns the emote parameter as a png file. If the parameter is not a discord emote, an error will occur.

* pixelate (parameters: scale - optional) Returns a pixelated image with dimensions `scale` by `scale`. If no scale is provided, the output will be 16 by 16 image. 

* grayscale (parameters: an attached image) [aliases = 'gray', 'grey', 'greyscale'] Returns an B+W version of the attached RGB image.

* blend (parameters: 2 different attached images, **both with the same pixel size**) Returns an combined consisting of the two images. This function will be updated in the future for better QOL.

* tint (parameters: an attached RGB image, color - required) [aliases = 'overlay', 'colorize'] Returns the image with a color filter applied. If no color parameter is provided, a black tint is applied. If the color parameter is invalid, an error will occur. Otherwise, the color applied will be the color parameter. 

* contour (parameters: an attached image) [aliases = 'outline'] Returns a B+W image of the contour (outline of significant foregrounds).  