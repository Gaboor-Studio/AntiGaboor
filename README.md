# AntiGaboor

A telegram bot that  analyzes posts from gaboor and detects if there is Miley content in it . 

## For detecting miley photos and videos and gifs:

1. we used opencv to crop faces in an image
2. predict faces with pretrained model from this repo : [Celebrity Face Recognition](https://github.com/Srikeshram/Celebrity-Face-Recognition)
3. for videos we used opencv to split video or gif into frames and then predict each one of those frames. if number of the frames that are miley divide by number of all of the frames was bigger than a ratio then we can say that this is a miley video or gif.
