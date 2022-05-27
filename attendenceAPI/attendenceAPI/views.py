
# Imports
from django.http import Http404, JsonResponse
from rest_framework.views import APIView
import numpy as np
import cv2
import os
import face_recognition
import base64
from api.models import *
from django.shortcuts import redirect, render
from .reboot import *
from datetime import datetime



# Listing all the images
path = 'imges'
images = []
classNames = []
myList = os.listdir(path)
print(f"mylist -- > {myList}")
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
    print(f"className --> {classNames}")

# Function to find the encoding of the image
def findEncodings(images):
    encodeList=[]
    for img in images:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

encodeListKnown = None
# Encoding all the images in the list
encodeListKnown = findEncodings(images)
print('Encoding Complete')




# API view for image recognition
class ImageRecognition(APIView):
    def post(self, request):
        try:
            # Getting the base64 encoded image from the request and decoding it
            encoded_image = request.data['image']
            decoded_image = base64.b64decode(encoded_image)
            print(type(decoded_image))

            # Converting the image to numpy array
            im_arr = np.frombuffer(decoded_image, dtype=np.uint8)
            img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)

            # Converting the image to RGB
            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
            name = "none"

            # Finding the encoding and location of the image
            facesCurFrame = face_recognition.face_locations(imgS)
            encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)

            # Comparing the encoding of the image with the known encodings
            for encodeFace, faceLoc in zip(encodesCurFrame,facesCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
                print(faceDis)
                matchIndex = np.argmin(faceDis)
                
                if matches[matchIndex]:
                    name = classNames[matchIndex].upper()
                    print(name)
            
            # Creating Log if the image is recognized
            if name != 'none':
                id = name.split('_')[1]
                user = Attendee.objects.get(id=id)
                log = AttendanceLog.objects.create(attendee = user)
                log.save()
            
            # Creating the response
            now = datetime.now()
            message = f"{name.split('_')[0]} | {now.hour}:{now.minute}:{now.second}" 
            
            return JsonResponse({'success': True, 'name': name, 'msg': message})
        except KeyError:
            raise Http404

class ImageReconMonitor(APIView):
    def get(self, request):
        if request.user.is_authenticated & request.user.is_superuser:
            return render(request, 'index2.html')
        else:
            return redirect('/admin')


class Reboot(APIView):
    # ------------------------------------------------------#
    # API view for rebooting the server                     #
    # Everytime new training data is added,the server       #
    # needs to be rebooted to update the encodings.         #
    #                                                       #
    # this api view puts some code (timestamp) in reboot.py #
    # the file is imported in this views.py so each change  #
    # in reboot.py will cause a reboot in the server        #
    # ------------------------------------------------------#

    def get(Self, request):
        if request.user.is_authenticated & request.user.is_superuser:
            f = open("attendenceAPI/reboot.py", "a")
            f.write(f"d = '{datetime.now()}'\n")
            f.close()
            return render(request, 'redirect.html')
        else:
            return redirect('/admin')