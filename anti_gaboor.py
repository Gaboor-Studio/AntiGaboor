import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
import requests
import cv2
import json
from PIL import Image
import logging
import threading
import time
import numpy as np
from keras.models import load_model


model = load_model('Weights Face Recognitions.h5')


def faces_detected(pil_image):
    images = []
    try:
        image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=3,
            minSize=(30, 30))
        for (x, y, w, h) in faces:
            roi_color = image[y:y + h, x:x + w]
            images.append(roi_color)
        return images
    except:
        return images


def is_miley_in_text(txt):
    text=txt.lower()
    miley_dictionary=["miley","cyrus","سایرس","مایلی"]
    for word in miley_dictionary:
        if word in text:
            return True
    return False

def is_miley_in_photo(path,webp=False):
    global model
    print("checking if pic is miley...")
    imgpic = Image.open(requests.get(path, stream=True).raw)
    if webp:
        imgpic=imgpic.convert("RGB")
    imgpics = faces_detected(imgpic)
    if(len(imgpics)==0):
        print("no face detected")
    for img_face in imgpics:
        img = cv2.resize(np.uint8(img_face),(160,160))
        img_array =np.array(img)
        img_array=np.expand_dims(img_array, 0)
        img_array = img_array / 255.
        score = model.predict(img_array)
        if np.argmax(score) == 57:
            print("Yes it was")
            return True
        else:
            print("No it was'nt")
            return False

def is_miley_in_video(path):
    global model
    cap = cv2.VideoCapture(path)
    if(int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) < 700):
        frames, img = cap.read()
        miley=0
        sizee=0
        while frames:
            sizee+=1
            frm=Image.fromarray(np.uint8(img)).convert('RGB')
            imgpics=faces_detected(frm)
            if (len(imgpics) == 0):
                print("no face detected")
            for img_face in imgpics:
                imgg = cv2.resize(np.uint8(img_face),(160,160))
                imgg_array = np.array(imgg)
                imgg_array = np.expand_dims(imgg_array, 0)
                imgg_array = imgg_array / 255.
                score = model.predict(imgg_array)
                if np.argmax(score) == 57:
                    print("Yes it was")
                    miley+=1
                else:
                    print("No it was'nt")
            # read next frame
            frames, img = cap.read()
        print(sizee)
        print(miley)
        ratio=1.0*miley/sizee
        if ratio>0.035:
            return True
        else:
            return False
    else:
        print("Too large video")
        return False


TOKEN = "TOKEN"
gab_id="Salinaria"

updater = Updater(token=TOKEN, use_context=True)
bot = telegram.Bot(TOKEN)


def start(update: telegram.Update, context: telegram.ext.CallbackContext):
    update.message.reply_text(text='آنتی گبور محافظ اعصاب و حجم اینترنت شما')


def text_handler(update: telegram.Update, context: telegram.ext.CallbackContext):
    try:
        text=update.message.text
        if is_miley_in_text(text):
            update.message.reply_text("!bk")
    except:
        pass

def photo_handler(update: telegram.Update, context: telegram.ext.CallbackContext):
    try:

        if update.message.photo:
            imgpic_id = update.message.photo[-1].file_id
            picurl = f"https://api.telegram.org/bot{TOKEN}/getFile?file_id={imgpic_id}"
            tt = requests.get(picurl)
            tt = tt.json()
            file_path = tt["result"]["file_path"]
            pic_to_download = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"
            if is_miley_in_photo(pic_to_download):
                update.message.reply_text("⚠️ Miley detected! \nDon't download it")
            else:
                # update.message.reply_text("ok")
                pass
    except:
        pass

def photo_or_video_with_caption_handler(update: telegram.Update, context: telegram.ext.CallbackContext):
    try:
        text=update.message.caption

        if is_miley_in_text(text):
            update.message.reply_text("⚠️ miley detected! \nDon't download it")
        else:
            if update.message.photo:
                imgpic_id = update.message.photo[-1].file_id
                picurl = f"https://api.telegram.org/bot{TOKEN}/getFile?file_id={imgpic_id}"
                tt = requests.get(picurl)
                tt = tt.json()
                file_path = tt["result"]["file_path"]
                pic_to_download = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"
                if is_miley_in_photo(pic_to_download):
                    update.message.reply_text("⚠️ Miley detected! \nDon't download it")
                    return
                else:
                    # update.message.reply_text("ok")
                    pass
            if update.message.video:
                if update.message.video["thumb"]["file_size"] > 15000:
                    print("Too large file")
                    return
                print("this is a video of caption")
                imgpicc_id = update.message.video.file_id
                piccurl = f"https://api.telegram.org/bot{TOKEN}/getFile?file_id={imgpicc_id}"
                ttt = requests.get(piccurl)
                ttt= ttt.json()
                file_pathh = ttt["result"]["file_path"]
                video_to_downloadd = f"https://api.telegram.org/file/bot{TOKEN}/{file_pathh}"
                if is_miley_in_video(video_to_downloadd):
                    update.message.reply_text("⚠️ Miley detected! \nDon't download it")
                else:
                    pass

    except:
        pass

def sticker_handler(update: telegram.Update, context: telegram.ext.CallbackContext):
    try:

        if update.message.sticker:
            imgpic_id = update.message.sticker.file_id
            picurl = f"https://api.telegram.org/bot{TOKEN}/getFile?file_id={imgpic_id}"
            tt = requests.get(picurl)
            tt = tt.json()
            file_path = tt["result"]["file_path"]
            pic_to_download = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"
            if is_miley_in_photo(pic_to_download,webp=True):
                update.message.reply_text("!bk")
            else:
                # update.message.reply_text("ok")
                pass
    except:
        pass

def gif_handler(update: telegram.Update, context: telegram.ext.CallbackContext):
    try:

        if update.message.document.mime_type=='video/mp4':
            print("this is a gif")
            imgpic_id = update.message.document.file_id
            picurl = f"https://api.telegram.org/bot{TOKEN}/getFile?file_id={imgpic_id}"
            tt = requests.get(picurl)
            tt = tt.json()
            file_path = tt["result"]["file_path"]
            video_to_download = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"
            if is_miley_in_video(video_to_download):
                update.message.reply_text("⚠️ Miley detected! \nDon't download it")
    except:
        pass


def video_handler(update: telegram.Update, context: telegram.ext.CallbackContext):
    try:
        if update.message.video["thumb"]["file_size"]>15000:
            print("Too large file")
            return
        print("this is a video")
        imgpic_id = update.message.video.file_id
        picurl = f"https://api.telegram.org/bot{TOKEN}/getFile?file_id={imgpic_id}"
        tt = requests.get(picurl)
        tt = tt.json()
        file_path = tt["result"]["file_path"]
        video_to_download = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"
        if is_miley_in_video(video_to_download):
            update.message.reply_text("⚠️ Miley detected! \nDon't download it")
    except:
        pass

dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.user(username=gab_id) & Filters.text,text_handler)) # text
dispatcher.add_handler(MessageHandler(Filters.user(username=gab_id) & Filters.caption, photo_or_video_with_caption_handler)) # photo or video with caption
dispatcher.add_handler(MessageHandler(Filters.user(username=gab_id) & Filters.photo, photo_handler))  # photo
dispatcher.add_handler(MessageHandler(Filters.user(username=gab_id) & Filters.sticker, sticker_handler)) # sticker
dispatcher.add_handler(MessageHandler(Filters.user(username=gab_id) & Filters.document, gif_handler)) # Gif
dispatcher.add_handler(MessageHandler(Filters.user(username=gab_id) & Filters.video, video_handler)) # video
updater.start_polling()
