from rapidconnect import RapidConnect
rapid = RapidConnect('Emotions', '24aa499b-e5a4-491e-90ce-9bb0f8d75c86');
import base64
import json
from FlaskWebProject1 import emotion
from collections import Counter
# result = rapid.call('MicrosoftEmotionAPI', 'getEmotionRecognition', { 
#   'subscriptionKey': '90febbecca1c462f871ea1d8e349d76a',
#   'image': 'http://i.imgur.com/shDtPNc.jpg'
 
# })

def faceArea(dct):
    area = dct['faceRectangle']['width']*dct['faceRectangle']['height']
    return area

# maxFace = max(result, key=faceArea)

def getEmotions(face):
    return rankedEmotions

def getMaxEmotion(face):
    emotionsList = dictToList(face)
    maxEmo = max(emotionsList, key=lambda x: x[1])
    return maxEmo

def dictToList(dct):
    keys = dct['scores'].keys()
    scores = dct['scores']
    tupList = []
    for key in keys:
        tupList.append((key, scores[key]))
    return tupList

def classifyImages(lst):
    classifications = []
    for imageStr in lst:
        lst = emotion.returnData(imageStr).decode('ascii')
        print(lst)
        data = json.loads(lst)
        if data and "error" not in data:
            maxFace = max(data, key=faceArea)
            maxEmo = getMaxEmotion(maxFace)
            classifications.append(maxEmo)
    return classifications

def overall_classification(lst):
    classifications = [classification for classification, confidence in classifyImages(lst)]
    if not classifications:
        return None
    for classification in classifications:
        if classification != "neutral":
            break
    else:
        return "neutral"
    classifications = Counter(classifications).most_common(2)
    if classifications[0][0] != 'neutral':
        return classifications[0][0]
    else:
        return classifications[1][0]


if __name__ == "__main__":
    lst = ["images/image0.jpeg", "images/image1.jpeg"]
    print(classifyImages(lst))
    #with open("images/image16.jpeg", "rb") as image_file:
    #    encoded_string = "data:image/jpeg;base64," + str(base64.b64encode(image_file.read()))
    #    print(classify_image(encoded_string))

