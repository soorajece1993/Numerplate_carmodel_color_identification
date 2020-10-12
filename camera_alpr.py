import cv2
import requests
import base64
import json
import cv2

cap=cv2.VideoCapture(0)

while 1:
    ret,frame=cap.read()

    if ret:
        cv2.imshow("NUMBER PLATE RECOGNITION",frame)
        k=cv2.waitKey(10)

        if k==27:
            cv2.imwrite("test.jpg",frame)


            ##### Please ad dyour secret key
            SECRET_KEY = '*****************************'
            with open("test.jpg", 'rb') as image_file:
                img_base64 = base64.b64encode(image_file.read())

            url = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=ind&secret_key=%s' % (
                SECRET_KEY)  # Replace 'ind' with  your country code
            r = requests.post(url, data=img_base64)

            try:
                print(r.json())

                with open('file.json', 'w') as f:
                    json.dump(r.json(), f)

                # Opening JSON file
                f = open('file.json', )

                # returns JSON object as
                # a dictionary
                data = json.load(f)

                # print(data)

                result = data['results'][0]

                x = data['results'][0]['coordinates'][0]['y']
                y = data['results'][0]['coordinates'][0]['x']

                plate = data['results'][0]['plate']
                vehicle_region = data['results'][0]['vehicle_region']
                color = data['results'][0]['vehicle']['color'][0]['name']
                model = data['results'][0]['vehicle']['make'][0]['name']

                print(plate)
                print(vehicle_region)
                print(color)
                print(model)

                img = frame

                font = cv2.FONT_HERSHEY_SIMPLEX
                fontColor = (255, 0, 0)
                fontSize = 0.5
                cv2.putText(frame, ' MODEL :  ' + model, (10, 30), font, fontSize, fontColor, 2)
                cv2.putText(frame, 'Vehicle Number :  ' + str(plate), (10, 60), font, fontSize, fontColor, 2)
                cv2.putText(frame, 'Vehicle Color :  ' + str(color), (10, 90), font, fontSize, fontColor, 2)

                frame = cv2.rectangle(img, (y, x), (y + 569, 400), (0, 255, 0), 3)

                cv2.imshow("NUMBER PLATE RECOGNITION", frame)
                cv2.waitKey(3000)



            except:
                print("No number plate found")