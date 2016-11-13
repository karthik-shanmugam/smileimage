"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, Flask, request, send_from_directory
from FlaskWebProject1 import app, rapid
import sys
import base64
import json
# from imgurpython import ImgurClient
import threading
import random
from random import gauss
import os
#from rapid import overall_classification
import pickle
#from collections import Counter, defaultdict
import collections
import urllib2
# #import urllib.request


rpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "reactions")
ipath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "image_set")
face_demo_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "face-demo")
images_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")

hardcoded_content = [
"https://i.redd.it/hvzv42t0lvrx.jpg",
"http://i.imgur.com/ZyQtepc.jpg",
"https://i.redd.it/qmxry2ehz3xx.jpg",
"http://www.calhacks.io/assets/img/ddoski_head.png",
"http://i.imgur.com/1zqh2UF.jpg",
"http://i.imgur.com/L6YdThP.jpg",
"http://i.imgur.com/2poMXRO.gif",
"http://i.imgur.com/aGDrQTf.jpg",
"http://i.imgur.com/HG0I6BZ.jpg",
"http://i.imgur.com/Ov94zes.gif",
"http://i.imgur.com/40QmCBw.jpg",
"http://i.imgur.com/C7a3Xpk.jpg",
"http://i.imgur.com/sdAEN2H.jpg",
"http://i.imgur.com/3Ddp13Y.jpg",
"http://i.imgur.com/6OVNBfY.gif",
"http://2static.fjcdn.com/pictures/Were+in+a+star+wars+universe_24c312_6087169.jpg",
"https://fbcdn-photos-b-a.akamaihd.net/hphotos-ak-xlp1/v/t1.0-0/s480x480/14980635_1281568875218196_7120559648086095988_n.jpg?oh=8d3e8668e3a12e527e0e3af800304d36&oe=58C24F37&__gda__=1485858255_bf1620845fc7407aa3c2ec9e806a19ae",
"https://scontent-dft4-1.xx.fbcdn.net/v/t1.0-9/14724426_1326905380675866_867562820468210362_n.jpg?oh=938c13a15cb480f6819fa62faf4730b1&oe=58C1F0F2",
"https://fbcdn-sphotos-a-a.akamaihd.net/hphotos-ak-xpl1/v/t1.0-9/14642111_340737786270979_8973037306281854082_n.jpg?oh=8ffb0e80c641c702673eaf26ea61654d&oe=58D44960&__gda__=1490250988_5d7d3a282ec2c5cef25673b3da7a6457",
"http://quotesnhumor.com/wp-content/uploads/2015/08/Top-50-Funniest-Memes-Collection-images.jpg"
]

with open(rpath, "rb") as reactions_file:
    image_reactions = pickle.load(reactions_file)

def cache_reactions():
    with open(rpath, "wb") as reactions_file:
        pickle.dump(image_reactions, reactions_file)

with open(ipath, "rb") as images_file:
    image_set = pickle.load(images_file)

def cache_image_set():
    with open(ipath, "wb") as images_file:
        pickle.dump(image_set, images_file)

image_set.update(hardcoded_content)


@app.route('/')
def root():
    return send_from_directory(face_demo_path, 'index.html')

@app.route('/data')
def data():
    print(type(image_reactions))
    return str(image_reactions)



@app.route('/emojis/<string:path>', methods=['GET'])
def static_proxy2(path):
    return send_from_directory(face_demo_path+'/emojis', path)


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


@app.route('/images/uploads', methods=['POST'])
def upload_images():
    #print(request.form['image'])
    ret = ''
    try:
        global counter
        print("flag0")
        images = json.loads(request.form['images'])
        content = request.form['content']
        filenames = []
        print("flag1")

        for image in images:
            with counter_lock:
                filename = os.path.join(images_path, "image%d.jpeg" % counter)
                counter += 1
            with open(filename, "wb") as fh:
                fh.write(base64.decodestring(bytes(image[23:])))
            ret+=' open'

            filenames.append(filename)
        print("flag2")

        result = rapid.overall_classification(filenames)
        ret+='process'
        for filename in filenames:
            os.remove(filename)
        print("flag3")

        if result:
            if content not in image_reactions:
                image_reactions[content] = {}
            image_reactions[content][result] = image_reactions[content].get(result, 0) + 1
            cache_reactions()
            print(image_reactions)
            print(result)
            return result
        else:
            return "none"
    except Exception as e:
        return ret + str(e)
        # link = upload_to_imgur(filename)
        # os.remove(filename)
        # emotion = classify_image(link)[0]
        # return emotion

@app.route('/suggestion', methods=['POST'])
def suggest_image():
    url = request.form['url']
    try:
        response = urllib2.urlopen(url)
        info = response.info()
        if info.getmaintype() == "image":
            image_set.add(url)
            cache_image_set()
            print("added image %s" % url)
            return "success"
        else:
            print("%s is not a valid image!!!" % url)
            return "failure"
    except Exception as error:
        print(error)
        print("%s is not a valid image!!!" % url)
        return "failure"       
@app.route('/webcam.js', methods=['GET'])
def webcamjs():
    return send_from_directory('face-demo', 'webcam.js')

@app.route('/webcam.swf', methods=['GET'])
def webcamswf():
    return send_from_directory('face-demo', 'webcam.swf')

@app.route('/main.js', methods=['GET'])
def mainjs():
    return send_from_directory('face-demo', 'main.js')


def upload_to_imgur(path):
    link = client.upload_from_path(path)['link']
    with open("links.txt", "a") as myfile:
        myfile.write("%s\n" % link)
    return link

# def classify_image(link):

#     # vec = [gauss(0, 1) for i in range(8)]
#     # mag = sum(x**2 for x in vec) ** .5
#     # vector = {emotion: score for emotion, score in zip(("anger","contempt","disgust","fear","happiness","neutral","sadness","surprise"), [x/mag for x in vec])}
#     return random.choice(["anger","contempt","disgust","fear","happiness","neutral","sadness","surprise"])
#     #return vector

# if __name__ == "__main__":
#     app.run(debug=False)
