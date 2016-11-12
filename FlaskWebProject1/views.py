"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, Flask, request, send_from_directory
from FlaskWebProject1 import app
# import base64
# import json
# # from imgurpython import ImgurClient
# import threading
# import random
# from random import gauss
# import os
# #from rapid import overall_classification
# import pickle
# from collections import Counter, defaultdict
# import urllib.request


# rpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "reactions")
# ipath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "image_set")
# face_demo_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "face-demo")
# images_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")



# with open(rpath, "rb") as reactions_file:
#     image_reactions = pickle.load(reactions_file)

# def cache_reactions():
#     with open(rpath, "wb") as reactions_file:
#         pickle.dump(image_reactions, reactions_file)

# with open(ipath, "rb") as images_file:
#     image_set = pickle.load(images_file)

# def cache_image_set():
#     with open(ipath, "wb") as images_file:
#         pickle.dump(image_set, images_file)


@app.route('/')
def root():
    return "bobby"#send_from_directory(face_demo_path, 'index.html')



# @app.route('/emojis/<string:path>', methods=['GET'])
# def static_proxy2(path):
#     return send_from_directory(face_demo_path+'/emojis', path)


# counter = 0
# counter_lock = threading.Lock()

# # @app.route('/image', methods=['POST'])
# # def upload_image():
# #     #print(request.form['image'])
# #     global counter
# #     with counter_lock:
# #         filename = "images/image%d.jpeg" % counter
# #         counter += 1
# #     with open(filename, "wb") as fh:
# #         fh.write(base64.decodestring(bytes(request.form['image'][23:], 'utf-8')))
# #     link = upload_to_imgur(filename)
# #     os.remove(filename)
# #     emotion = classify_image(link)[0]
# #     return emotion


# @app.route('/content', methods=['GET'])
# def serve_content():
#     return random.choice(tuple(image_set))


# @app.route('/images', methods=['POST'])
# def upload_images():
#     #print(request.form['image'])
#     global counter
#     print("flag0")
#     images = json.loads(request.form['images'])
#     content = request.form['content']
#     filenames = []
#     print("flag1")

#     for image in images:
#         with counter_lock:
#             filename = images_path+"/image%d.jpeg" % counter
#             counter += 1
#         with open(filename, "wb") as fh:
#             fh.write(base64.decodestring(bytes(image[23:], 'utf-8')))
#         filenames.append(filename)
#     print("flag2")

#     result = rapid.overall_classification(filenames)
#     print("flag3")

#     if result:
#         image_reactions[content][result] += 1
#         cache_reactions()
#         print(image_reactions)
#         print(result)
#         return result
#     else:
#         return "none"
#         # link = upload_to_imgur(filename)
#         # os.remove(filename)
#         # emotion = classify_image(link)[0]
#         # return emotion

# @app.route('/suggestion', methods=['POST'])
# def suggest_image():
#     url = request.form['url']
#     try:
#         with urllib.request.urlopen(url) as response:
#             info = response.info()
#             if info.get_content_maintype() == "image":
#                 image_set.add(url)
#                 cache_image_set()
#                 print("added image %s" % url)
#                 return "success"
#             else:
#                 print("%s is not a valid image!!!" % url)
#                 return "failure"
#     except Exception as error:
#         print("%s is not a valid image!!!" % url)
#         return "failure"       
# @app.route('/<string:path>', methods=['GET'])
# def static_proxy(path):
#     return send_from_directory('face-demo', path)
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

# if __name__ == "__main__":
#     app.run(debug=False)
