from __future__ import print_function
import base64
import json
from imgurpython import ImgurClient
import threading
import random
from random import gauss
import os
from rapid import overall_classification
import pickle

from collections import Counter, defaultdict


import urllib.request



with open("reactions", "rb") as reactions_file:
    image_reactions = pickle.load(reactions_file)

def cache_reactions():
    with open("reactions", "wb") as reactions_file:
        pickle.dump(image_reactions, reactions_file)

with open("image_set", "rb") as images_file:
    image_set = pickle.load(images_file)

def cache_image_set():
    with open("image_set", "wb") as images_file:
        pickle.dump(image_set, images_file)

# imgur_client = "0f8ebdce6b83981"
# imgur_secret = "f5b5ca46e0ea44e94b5cc3f6e9ebe4dc4a8aa254"
# client = ImgurClient(imgur_client, imgur_secret)

from flask import Flask, request, send_from_directory
# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')

@app.route('/')
def root():
    return send_from_directory('face-demo', 'index.html')



@app.route('/emojis/<string:path>', methods=['GET'])
def static_proxy2(path):
    return send_from_directory('face-demo/emojis', path)


counter = 0
counter_lock = threading.Lock()

# @app.route('/image', methods=['POST'])
# def upload_image():
#     #print(request.form['image'])
#     global counter
#     with counter_lock:
#         filename = "images/image%d.jpeg" % counter
#         counter += 1
#     with open(filename, "wb") as fh:
#         fh.write(base64.decodestring(bytes(request.form['image'][23:], 'utf-8')))
#     link = upload_to_imgur(filename)
#     os.remove(filename)
#     emotion = classify_image(link)[0]
#     return emotion


@app.route('/content', methods=['GET'])
def serve_content():
    return random.choice(tuple(image_set))


@app.route('/images', methods=['POST'])
def upload_images():
    #print(request.form['image'])
    global counter
    print("flag0")
    images = json.loads(request.form['images'])
    content = request.form['content']
    filenames = []
    print("flag1")

    for image in images:
        with counter_lock:
            filename = "images/image%d.jpeg" % counter
            counter += 1
        with open(filename, "wb") as fh:
            fh.write(base64.decodestring(bytes(image[23:], 'utf-8')))
        filenames.append(filename)
    print("flag2")

    result = overall_classification(filenames)
    print("flag3")

    if result:
        image_reactions[content][result] += 1
        cache_reactions()
        print(image_reactions)
        print(result)
        return result
    else:
        return "none"
        # link = upload_to_imgur(filename)
        # os.remove(filename)
        # emotion = classify_image(link)[0]
        # return emotion

@app.route('/suggestion', methods=['POST'])
def suggest_image():
    url = request.form['url']
    try:
        with urllib.request.urlopen(url) as response:
            info = response.info()
            if info.get_content_maintype() == "image":
                image_set.add(url)
                cache_image_set()
                print("added image %s" % url)
                return "success"
            else:
                print("%s is not a valid image!!!" % url)
                return "failure"
    except Exception as error:
        print("%s is not a valid image!!!" % url)
        return "failure"       
@app.route('/<string:path>', methods=['GET'])
def static_proxy(path):
    return send_from_directory('face-demo', path)
# def upload_to_imgur(path):
#     link = client.upload_from_path(path)['link']
#     with open("links.txt", "a") as myfile:
#         myfile.write("%s\n" % link)
#     return link

# def classify_image(link):

#     # vec = [gauss(0, 1) for i in range(8)]
#     # mag = sum(x**2 for x in vec) ** .5
#     # vector = {emotion: score for emotion, score in zip(("anger","contempt","disgust","fear","happiness","neutral","sadness","surprise"), [x/mag for x in vec])}
#     return random.choice(["anger","contempt","disgust","fear","happiness","neutral","sadness","surprise"])
#     #return vector

if __name__ == "__main__":
    app.run(debug=False)