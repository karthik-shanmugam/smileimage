import httplib, urllib, base64

headers = {
    # Request headers
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': 'eb8317cc011540c9b52cef81219dee60',
}

params = urllib.urlencode({
})



def returnData(imageString):
    with open(imageString, "rb") as image_file:
        encoded_string = image_file.read()
    try:
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/emotion/v1.0/recognize?%s" % params, encoded_string, headers)
        response = conn.getresponse()
        data = response.read()
        return data
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))