from rapidconnect import RapidConnect
rapid = RapidConnect('calhacks3', 'f58ef2cf-6cfa-4cd0-a653-beb778f317e1');

result = rapid.call('MicrosoftEmotionAPI', 'getEmotionRecognition', { 
	'subscriptionKey': 'eb8317cc011540c9b52cef81219dee60',
	'image': 'http://i.imgur.com/gUHZXOh.jpg'
})
print(type(result))
print(result)