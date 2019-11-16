#get geocoding data from address passed via command line
#has to do some funky stuff instead of just parsing webpage
#as an xml file because google puts api response data in
#a pre tag, which does not play nice with python... :(
#uses googles geocoding api
#ben jollymore 2019

import json
import urllib
import requests
import sys
import cv2
import tensorflow as tf
from PIL import Image

url = 'https://maps.googleapis.com/maps/api/geocode/json?address='
key = '&key='

address = sys.argv[1]
addressSendable = address.replace(" ", "+")

query = url + addressSendable + key
page = requests.get(query)
geoData = page.json()

lattitude = geoData['results'][0]['geometry']['location']['lat']
longitude = geoData['results'][0]['geometry']['location']['lng']
addressInfo = []

for i in geoData['results'][0]['address_components']:
	if (i['types'][0] != "route" and i['types'][0] != "street_number"):
		if i['long_name'] not in addressInfo:
			addressInfo.append(i['long_name'])

print("Lattitude: ", lattitude)
print("Longitude: ", longitude)
for i in addressInfo:
	print(i)

url = 'https://maps.googleapis.com/maps/api/staticmap?center='
key = '&zoom=15&size=400x400&maptype=satellite&key='
query = url + str(lattitude) + ',' + str(longitude) + key

urllib.request.urlretrieve(query, "testImage.png")
img = Image.open("testImage.png")
img.show()

CATEGORIES = ["city", "industrial", "rural", "suburban"]

model = tf.keras.models.load_model("CNN.model")
image = "testImage.png" 

img_array = cv2.imread(image, cv2.IMREAD_COLOR)
new_array = cv2.resize(img_array, (400, 400))
new_array = new_array.reshape(-1, 400, 400, 3)

prediction = model.predict(new_array)
prediction = list(prediction[0])
print(CATEGORIES[prediction.index(max(prediction))])
