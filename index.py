# # # import os
# # # import cvzone
# # # import cv2
# # # from cvzone.PoseModule import PoseDetector
# # # import time
# # #
# # # from flask import Flask, Response
# # # import cv2
# # #
# # # # from app import generate_frames
# # #
# # # app = Flask(__name__)
# # #
# # # # Initialize webcam capture
# # # cap = cv2.VideoCapture(0)
# # #
# # # detector = PoseDetector()
# # #
# # #
# # # shirtsFolderPath = "C:/Users/dhruv/PycharmProjects/Walmart's virtual trial room/Resources/Shirts"
# # # listShirts = os.listdir(shirtsFolderPath)
# # # print(listShirts)
# # #
# # # imageNumber = 0
# # # imgButtonRight = cv2.imread("C:/Users/dhruv/PycharmProjects/Walmart's virtual trial room/Resources/button.png", cv2.IMREAD_UNCHANGED)
# # # imgButtonLeft = cv2.flip(imgButtonRight, 1)
# # # counterRight = 0
# # # counterLeft = 0
# # # selectionSpeed = 10
# # #
# # # # Add a debounce time for button clicks
# # # lastClickTime = time.time()
# # # clickDelay = 1  # 1 second delay
# # #
# # # def overlay_image(main_img, overlay_img, position):
# # #     """Overlay an image on another image with boundary checks."""
# # #     x, y = position
# # #     h, w, _ = overlay_img.shape
# # #     H, W, _ = main_img.shape
# # #
# # #     # Ensure the overlay fits within the main image dimensions
# # #     if x < 0 or y < 0 or x + w > W or y + h > H:
# # #         print(f"Overlay position out of bounds: {position}")
# # #         return main_img  # Do not overlay if the position is out of bounds
# # #
# # #     return cvzone.overlayPNG(main_img, overlay_img, (x, y))
# # #
# # # while True:
# # #     success, img = cap.read()
# # #     if not success:
# # #         break
# # #
# # #     img = detector.findPose(img)
# # #     lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False)
# # #
# # #     if lmList:
# # #         lm11 = lmList[11][1:3]
# # #         lm12 = lmList[12][1:3]
# # #
# # #         # Debug: Check if t-shirt image is being read correctly
# # #         try:
# # #             imgShirt = cv2.imread(os.path.join(shirtsFolderPath, listShirts[imageNumber]), cv2.IMREAD_UNCHANGED)
# # #             if imgShirt is None:
# # #                 print(f"Error: T-shirt image {listShirts[imageNumber]} not found or could not be read.")
# # #                 continue
# # #         except Exception as e:
# # #             print(f"Error reading t-shirt image: {e}")
# # #             continue
# # #
# # #         fixedRatio = 262 / 190
# # #         shirtRatioWidthHeight = 581 / 440
# # #         widthOfShirt = int((lm11[0] - lm12[0]) * fixedRatio)
# # #
# # #         # Debug: Check if resizing is working correctly
# # #         try:
# # #             imgShirt = cv2.resize(imgShirt, (widthOfShirt, int(shirtRatioWidthHeight * widthOfShirt)))
# # #         except Exception as e:
# # #             print(f"Error resizing t-shirt image: {e}")
# # #             continue
# # #
# # #         currentScale = (lm11[0] - lm12[0]) / 190
# # #         offset = int(44 * currentScale), int(48 * currentScale)
# # #
# # #         # Debug: Check if overlaying position is within bounds
# # #         try:
# # #             H, W, _ = img.shape
# # #             shirtH, shirtW, _ = imgShirt.shape
# # #             shirt_x, shirt_y = lm12[0] - offset[0], lm12[1] - offset[1]
# # #             if 0 <= shirt_x < W and 0 <= shirt_y < H and \
# # #                shirt_x + shirtW <= W and shirt_y + shirtH <= H:
# # #                 img = cvzone.overlayPNG(img, imgShirt, (shirt_x, shirt_y))
# # #             else:
# # #                 print(f"T-shirt position out of bounds: {(shirt_x, shirt_y)}")
# # #         except Exception as e:
# # #             print(f"Error overlaying t-shirt image: {e}")
# # #
# # #         # Ensure button positions fit within the image boundaries
# # #         H, W, _ = img.shape
# # #         buttonHeight = imgButtonRight.shape[0]
# # #         buttonWidth = imgButtonRight.shape[1]
# # #         buttonMargin = 10
# # #
# # #         buttonRightPosition = (W - buttonWidth - buttonMargin, H - buttonHeight - buttonMargin)
# # #         buttonLeftPosition = (buttonMargin, H - buttonHeight - buttonMargin)
# # #
# # #         if 0 <= buttonRightPosition[0] < W and 0 <= buttonRightPosition[1] < H:
# # #             img = overlay_image(img, imgButtonRight, buttonRightPosition)
# # #         else:
# # #             print(f"Right button position out of bounds: {buttonRightPosition}")
# # #
# # #         if 0 <= buttonLeftPosition[0] < W and 0 <= buttonLeftPosition[1] < H:
# # #             img = overlay_image(img, imgButtonLeft, buttonLeftPosition)
# # #         else:
# # #             print(f"Left button position out of bounds: {buttonLeftPosition}")
# # #
# # #         currentTime = time.time()
# # #
# # #         # Debug: Print hand positions
# # #         print(f"Hand Position Right Button: {lmList[16][1]}")
# # #         print(f"Hand Position Left Button: {lmList[15][1]}")
# # #
# # #         # Adjust detection logic based on button positions and hand positions
# # #         buttonRightYStart = H - buttonHeight - buttonMargin
# # #         buttonLeftYStart = H - buttonHeight - buttonMargin
# # #
# # #         handNearRightButton = (lmList[16][1] > buttonRightYStart and lmList[16][1] < buttonRightYStart + 100)
# # #         handNearLeftButton = (lmList[15][1] > buttonLeftYStart and lmList[15][1] < buttonLeftYStart + 100)
# # #
# # #         if handNearRightButton and (currentTime - lastClickTime > clickDelay):
# # #             counterRight += 1
# # #             cv2.ellipse(img, (buttonRightPosition[0] + buttonWidth // 2, buttonRightPosition[1] + buttonHeight // 2), (66, 66), 0, 0, counterRight * selectionSpeed, (0, 255, 0), 20)
# # #             if counterRight * selectionSpeed > 360:
# # #                 counterRight = 0
# # #                 lastClickTime = currentTime
# # #                 if imageNumber < len(listShirts) - 1:
# # #                     imageNumber += 1
# # #         elif handNearLeftButton and (currentTime - lastClickTime > clickDelay):
# # #             counterLeft += 1
# # #             cv2.ellipse(img, (buttonLeftPosition[0] + buttonWidth // 2, buttonLeftPosition[1] + buttonHeight // 2), (66, 66), 0, 0, counterLeft * selectionSpeed, (0, 255, 0), 20)
# # #             if counterLeft * selectionSpeed > 360:
# # #                 counterLeft = 0
# # #                 lastClickTime = currentTime
# # #                 if imageNumber > 0:
# # #                     imageNumber -= 1
# # #         else:
# # #             counterRight = 0
# # #             counterLeft = 0
# # #
# # #     cv2.imshow("Image", img)
# # #     if cv2.waitKey(1) & 0xFF == ord('q'):
# # #         break
# # #
# # # cap.release()
# # # cv2.destroyAllWindows()
# #
# # from flask import Flask, Response, render_template
# # import cv2
# # import os
# # import cvzone
# # from cvzone.PoseModule import PoseDetector
# # import time
# #
# # app = Flask(__name__)
# #
# # # Initialize webcam capture
# # cap = cv2.VideoCapture(0)
# #
# # detector = PoseDetector()
# #
# # shirtsFolderPath = "C:/Users/dhruv/PycharmProjects/Walmart's virtual trial room/Resources/Shirts"
# # listShirts = os.listdir(shirtsFolderPath)
# # print("Available shirts:", listShirts)
# #
# # imageNumber = 0
# # imgButtonRight = cv2.imread("C:/Users/dhruv/PycharmProjects/Walmart's virtual trial room/Resources/button.png", cv2.IMREAD_UNCHANGED)
# # imgButtonLeft = cv2.flip(imgButtonRight, 1)
# # counterRight = 0
# # counterLeft = 0
# # selectionSpeed = 10
# #
# # # Add a debounce time for button clicks
# # lastClickTime = time.time()
# # clickDelay = 1  # 1 second delay
# #
# # def overlay_image(main_img, overlay_img, position):
# #     """Overlay an image on another image with boundary checks."""
# #     x, y = position
# #     h, w, _ = overlay_img.shape
# #     H, W, _ = main_img.shape
# #
# #     # Ensure the overlay fits within the main image dimensions
# #     if x < 0 or y < 0 or x + w > W or y + h > H:
# #         print(f"Overlay position out of bounds: {position}")
# #         return main_img  # Do not overlay if the position is out of bounds
# #
# #     return cvzone.overlayPNG(main_img, overlay_img, (x, y))
# #
# # def gen_frames():
# #     global imageNumber, counterRight, counterLeft, lastClickTime
# #     while True:
# #         success, img = cap.read()
# #         if not success:
# #             break
# #
# #         img = detector.findPose(img)
# #         lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False)
# #
# #         if lmList:
# #             lm11 = lmList[11][1:3]
# #             lm12 = lmList[12][1:3]
# #
# #             # Debug: Check if t-shirt image is being read correctly
# #             try:
# #                 imgShirt = cv2.imread(os.path.join(shirtsFolderPath, listShirts[imageNumber]), cv2.IMREAD_UNCHANGED)
# #                 if imgShirt is None:
# #                     print(f"Error: T-shirt image {listShirts[imageNumber]} not found or could not be read.")
# #                     continue
# #             except Exception as e:
# #                 print(f"Error reading t-shirt image: {e}")
# #                 continue
# #
# #             fixedRatio = 262 / 190
# #             shirtRatioWidthHeight = 581 / 440
# #             widthOfShirt = int((lm11[0] - lm12[0]) * fixedRatio)
# #
# #             # Debug: Check if resizing is working correctly
# #             try:
# #                 imgShirt = cv2.resize(imgShirt, (widthOfShirt, int(shirtRatioWidthHeight * widthOfShirt)))
# #             except Exception as e:
# #                 print(f"Error resizing t-shirt image: {e}")
# #                 continue
# #
# #             currentScale = (lm11[0] - lm12[0]) / 190
# #             offset = int(44 * currentScale), int(48 * currentScale)
# #
# #             # Debug: Check if overlaying position is within bounds
# #             try:
# #                 H, W, _ = img.shape
# #                 shirtH, shirtW, _ = imgShirt.shape
# #                 shirt_x, shirt_y = lm12[0] - offset[0], lm12[1] - offset[1]
# #                 if 0 <= shirt_x < W and 0 <= shirt_y < H and \
# #                    shirt_x + shirtW <= W and shirt_y + shirtH <= H:
# #                     img = cvzone.overlayPNG(img, imgShirt, (shirt_x, shirt_y))
# #                 else:
# #                     print(f"T-shirt position out of bounds: {(shirt_x, shirt_y)}")
# #             except Exception as e:
# #                 print(f"Error overlaying t-shirt image: {e}")
# #
# #             # Ensure button positions fit within the image boundaries
# #             H, W, _ = img.shape
# #             buttonHeight = imgButtonRight.shape[0]
# #             buttonWidth = imgButtonRight.shape[1]
# #             buttonMargin = 10
# #
# #             buttonRightPosition = (W - buttonWidth - buttonMargin, H - buttonHeight - buttonMargin)
# #             buttonLeftPosition = (buttonMargin, H - buttonHeight - buttonMargin)
# #
# #             if 0 <= buttonRightPosition[0] < W and 0 <= buttonRightPosition[1] < H:
# #                 img = overlay_image(img, imgButtonRight, buttonRightPosition)
# #             else:
# #                 print(f"Right button position out of bounds: {buttonRightPosition}")
# #
# #             if 0 <= buttonLeftPosition[0] < W and 0 <= buttonLeftPosition[1] < H:
# #                 img = overlay_image(img, imgButtonLeft, buttonLeftPosition)
# #             else:
# #                 print(f"Left button position out of bounds: {buttonLeftPosition}")
# #
# #             currentTime = time.time()
# #
# #             # Debug: Print hand positions
# #             print(f"Hand Position Right Button: {lmList[16][1]}")
# #             print(f"Hand Position Left Button: {lmList[15][1]}")
# #
# #             # Adjust detection logic based on button positions and hand positions
# #             buttonRightYStart = H - buttonHeight - buttonMargin
# #             buttonLeftYStart = H - buttonHeight - buttonMargin
# #
# #             handNearRightButton = (lmList[16][1] > buttonRightYStart and lmList[16][1] < buttonRightYStart + 100)
# #             handNearLeftButton = (lmList[15][1] > buttonLeftYStart and lmList[15][1] < buttonLeftYStart + 100)
# #
# #             if handNearRightButton and (currentTime - lastClickTime > clickDelay):
# #                 counterRight += 1
# #                 cv2.ellipse(img, (buttonRightPosition[0] + buttonWidth // 2, buttonRightPosition[1] + buttonHeight // 2), (66, 66), 0, 0, counterRight * selectionSpeed, (0, 255, 0), 20)
# #                 if counterRight * selectionSpeed > 360:
# #                     counterRight = 0
# #                     lastClickTime = currentTime
# #                     if imageNumber < len(listShirts) - 1:
# #                         imageNumber += 1
# #             elif handNearLeftButton and (currentTime - lastClickTime > clickDelay):
# #                 counterLeft += 1
# #                 cv2.ellipse(img, (buttonLeftPosition[0] + buttonWidth // 2, buttonLeftPosition[1] + buttonHeight // 2), (66, 66), 0, 0, counterLeft * selectionSpeed, (0, 255, 0), 20)
# #                 if counterLeft * selectionSpeed > 360:
# #                     counterLeft = 0
# #                     lastClickTime = currentTime
# #                     if imageNumber > 0:
# #                         imageNumber -= 1
# #             else:
# #                 counterRight = 0
# #                 counterLeft = 0
# #
# #         _, buffer = cv2.imencode('.jpg', img)
# #         frame = buffer.tobytes()
# #         yield (b'--frame\r\n'
# #                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
# #
# # @app.route('/')
# # def index():
# #     return render_template('index.html')
# #
# # @app.route('/video_feed')
# # def video_feed():
# #     return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
# #
# # if __name__ == '__main__':
# #     app.run(debug=True, use_reloader=False)
#
from flask import Flask, Response, render_template
import cv2
import os
import cvzone
from cvzone.PoseModule import PoseDetector
import time

app = Flask(__name__)

# Initialize webcam capture
cap = cv2.VideoCapture(0)
detector = PoseDetector()

shirtsFolderPath = "/Resources/Shirts"
listShirts = os.listdir(shirtsFolderPath)
print("Available shirts:", listShirts)

imageNumber = 0
imgButtonRight = cv2.imread("/Resources/button.png", cv2.IMREAD_UNCHANGED)
imgButtonLeft = cv2.flip(imgButtonRight, 1)
counterRight = 0
counterLeft = 0
selectionSpeed = 10

# Add a debounce time for button clicks
lastClickTime = time.time()
clickDelay = 1  # 1 second delay

def overlay_image(main_img, overlay_img, position):
    """Overlay an image on another image with boundary checks."""
    x, y = position
    h, w, _ = overlay_img.shape
    H, W, _ = main_img.shape

    # Ensure the overlay fits within the main image dimensions
    if x < 0 or y < 0 or x + w > W or y + h > H:
        print(f"Overlay position out of bounds: {position}")
        return main_img  # Do not overlay if the position is out of bounds

    return cvzone.overlayPNG(main_img, overlay_img, (x, y))

def gen_frames():
    global imageNumber, counterRight, counterLeft, lastClickTime
    while True:
        success, img = cap.read()
        if not success:
            break

        img = detector.findPose(img)
        lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False)

        if lmList:
            lm11 = lmList[11][1:3]
            lm12 = lmList[12][1:3]

            # Debug: Check if t-shirt image is being read correctly
            try:
                imgShirt = cv2.imread(os.path.join(shirtsFolderPath, listShirts[imageNumber]), cv2.IMREAD_UNCHANGED)
                if imgShirt is None:
                    print(f"Error: T-shirt image {listShirts[imageNumber]} not found or could not be read.")
                    continue
            except Exception as e:
                print(f"Error reading t-shirt image: {e}")
                continue

            fixedRatio = 262 / 190
            shirtRatioWidthHeight = 581 / 440
            widthOfShirt = int((lm11[0] - lm12[0]) * fixedRatio)

            # Debug: Check if resizing is working correctly
            try:
                imgShirt = cv2.resize(imgShirt, (widthOfShirt, int(shirtRatioWidthHeight * widthOfShirt)))
            except Exception as e:
                print(f"Error resizing t-shirt image: {e}")
                continue

            currentScale = (lm11[0] - lm12[0]) / 190
            offset = int(44 * currentScale), int(48 * currentScale)

            # Debug: Check if overlaying position is within bounds
            try:
                H, W, _ = img.shape
                shirtH, shirtW, _ = imgShirt.shape
                shirt_x, shirt_y = lm12[0] - offset[0], lm12[1] - offset[1]
                if 0 <= shirt_x < W and 0 <= shirt_y < H and \
                   shirt_x + shirtW <= W and shirt_y + shirtH <= H:
                    img = cvzone.overlayPNG(img, imgShirt, (shirt_x, shirt_y))
                else:
                    print(f"T-shirt position out of bounds: {(shirt_x, shirt_y)}")
            except Exception as e:
                print(f"Error overlaying t-shirt image: {e}")

            # Ensure button positions fit within the image boundaries
            H, W, _ = img.shape
            buttonHeight = imgButtonRight.shape[0]
            buttonWidth = imgButtonRight.shape[1]
            buttonMargin = 10

            buttonRightPosition = (W - buttonWidth - buttonMargin, H - buttonHeight - buttonMargin)
            buttonLeftPosition = (buttonMargin, H - buttonHeight - buttonMargin)

            if 0 <= buttonRightPosition[0] < W and 0 <= buttonRightPosition[1] < H:
                img = overlay_image(img, imgButtonRight, buttonRightPosition)
            else:
                print(f"Right button position out of bounds: {buttonRightPosition}")

            if 0 <= buttonLeftPosition[0] < W and 0 <= buttonLeftPosition[1] < H:
                img = overlay_image(img, imgButtonLeft, buttonLeftPosition)
            else:
                print(f"Left button position out of bounds: {buttonLeftPosition}")

            currentTime = time.time()

            # Debug: Print hand positions
            print(f"Hand Position Right Button: {lmList[16][1]}")
            print(f"Hand Position Left Button: {lmList[15][1]}")

            # Adjust detection logic based on button positions and hand positions
            buttonRightYStart = H - buttonHeight - buttonMargin
            buttonLeftYStart = H - buttonHeight - buttonMargin

            handNearRightButton = (lmList[16][1] > buttonRightYStart and lmList[16][1] < buttonRightYStart + 100)
            handNearLeftButton = (lmList[15][1] > buttonLeftYStart and lmList[15][1] < buttonLeftYStart + 100)

            if handNearRightButton and (currentTime - lastClickTime > clickDelay):
                counterRight += 1
                cv2.ellipse(img, (buttonRightPosition[0] + buttonWidth // 2, buttonRightPosition[1] + buttonHeight // 2), (66, 66), 0, 0, counterRight * selectionSpeed, (0, 255, 0), 20)
                if counterRight * selectionSpeed > 360:
                    counterRight = 0
                    lastClickTime = currentTime
                    if imageNumber < len(listShirts) - 1:
                        imageNumber += 1
            elif handNearLeftButton and (currentTime - lastClickTime > clickDelay):
                counterLeft += 1
                cv2.ellipse(img, (buttonLeftPosition[0] + buttonWidth // 2, buttonLeftPosition[1] + buttonHeight // 2), (66, 66), 0, 0, counterLeft * selectionSpeed, (0, 255, 0), 20)
                if counterLeft * selectionSpeed > 360:
                    counterLeft = 0
                    lastClickTime = currentTime
                    if imageNumber > 0:
                        imageNumber -= 1
            else:
                counterRight = 0
                counterLeft = 0

        _, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/prev_shirt')
def prev_shirt():
    global imageNumber
    if imageNumber > 0:
        imageNumber -= 1
    return '', 204

@app.route('/next_shirt')
def next_shirt():
    global imageNumber
    if imageNumber < len(listShirts) - 1:
        imageNumber += 1
    return '', 204

# if __name__ == '__main__':
#     app.run(debug=True, use_reloader=False)
# from flask import Flask, Response, render_template
# import cv2
# import os
# import cvzone
# from cvzone.PoseModule import PoseDetector
# import time
#
# app = Flask(__name__)
#
# # Initialize webcam capture
# cap = cv2.VideoCapture(0)
# detector = PoseDetector()
#
# shirtsFolderPath = "C:/Users/dhruv/PycharmProjects/Walmart's virtual trial room/Resources/Shirts"
# listShirts = os.listdir(shirtsFolderPath)
# print("Available shirts:", listShirts)
#
# imageNumber = 0
# imgButtonRight = cv2.imread("/Resources/button.png", cv2.IMREAD_UNCHANGED)
# imgButtonLeft = cv2.flip(imgButtonRight, 1)
# counterRight = 0
# counterLeft = 0
# selectionSpeed = 10
#
# # Add a debounce time for button clicks
# lastClickTime = time.time()
# clickDelay = 1  # 1 second delay
#
# def overlay_image(main_img, overlay_img, position):
#     """Overlay an image on another image with boundary checks."""
#     x, y = position
#     h, w, _ = overlay_img.shape
#     H, W, _ = main_img.shape
#
#     # Ensure the overlay fits within the main image dimensions
#     if x < 0 or y < 0 or x + w > W or y + h > H:
#         print(f"Overlay position out of bounds: {position}")
#         return main_img  # Do not overlay if the position is out of bounds
#
#     return cvzone.overlayPNG(main_img, overlay_img, (x, y))
#
# def gen_frames():
#     global imageNumber, counterRight, counterLeft, lastClickTime
#     while True:
#         success, img = cap.read()
#         if not success:
#             break
#
#         img = detector.findPose(img)
#         lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False)
#
#         if lmList:
#             lm11 = lmList[11][1:3]
#             lm12 = lmList[12][1:3]
#
#             # Debug: Check if t-shirt image is being read correctly
#             try:
#                 imgShirt = cv2.imread(os.path.join(shirtsFolderPath, listShirts[imageNumber]), cv2.IMREAD_UNCHANGED)
#                 if imgShirt is None:
#                     print(f"Error: T-shirt image {listShirts[imageNumber]} not found or could not be read.")
#                     continue
#             except Exception as e:
#                 print(f"Error reading t-shirt image: {e}")
#                 continue
#
#             fixedRatio = 262 / 190
#             shirtRatioWidthHeight = 581 / 440
#             widthOfShirt = int((lm11[0] - lm12[0]) * fixedRatio)
#
#             # Debug: Check if resizing is working correctly
#             try:
#                 imgShirt = cv2.resize(imgShirt, (widthOfShirt, int(shirtRatioWidthHeight * widthOfShirt)))
#             except Exception as e:
#                 print(f"Error resizing t-shirt image: {e}")
#                 continue
#
#             currentScale = (lm11[0] - lm12[0]) / 190
#             offset = int(44 * currentScale), int(48 * currentScale)
#
#             # Debug: Check if overlaying position is within bounds
#             try:
#                 H, W, _ = img.shape
#                 shirtH, shirtW, _ = imgShirt.shape
#                 shirt_x, shirt_y = lm12[0] - offset[0], lm12[1] - offset[1]
#                 if 0 <= shirt_x < W and 0 <= shirt_y < H and \
#                    shirt_x + shirtW <= W and shirt_y + shirtH <= H:
#                     img = cvzone.overlayPNG(img, imgShirt, (shirt_x, shirt_y))
#                 else:
#                     print(f"T-shirt position out of bounds: {(shirt_x, shirt_y)}")
#             except Exception as e:
#                 print(f"Error overlaying t-shirt image: {e}")
#
#             # Ensure button positions fit within the image boundaries
#             H, W, _ = img.shape
#             buttonHeight = imgButtonRight.shape[0]
#             buttonWidth = imgButtonRight.shape[1]
#             buttonMargin = 10
#
#             buttonRightPosition = (W - buttonWidth - buttonMargin, H - buttonHeight - buttonMargin)
#             buttonLeftPosition = (buttonMargin, H - buttonHeight - buttonMargin)
#
#             if 0 <= buttonRightPosition[0] < W and 0 <= buttonRightPosition[1] < H:
#                 img = overlay_image(img, imgButtonRight, buttonRightPosition)
#             else:
#                 print(f"Right button position out of bounds: {buttonRightPosition}")
#
#             if 0 <= buttonLeftPosition[0] < W and 0 <= buttonLeftPosition[1] < H:
#                 img = overlay_image(img, imgButtonLeft, buttonLeftPosition)
#             else:
#                 print(f"Left button position out of bounds: {buttonLeftPosition}")
#
#             currentTime = time.time()
#
#             # Debug: Print hand positions
#             print(f"Hand Position Right Button: {lmList[16][1]}")
#             print(f"Hand Position Left Button: {lmList[15][1]}")
#
#             # Adjust detection logic based on button positions and hand positions
#             buttonRightYStart = H - buttonHeight - buttonMargin
#             buttonLeftYStart = H - buttonHeight - buttonMargin
#
#             handNearRightButton = (lmList[16][1] > buttonRightYStart and lmList[16][1] < buttonRightYStart + 100)
#             handNearLeftButton = (lmList[15][1] > buttonLeftYStart and lmList[15][1] < buttonLeftYStart + 100)
#
#             if handNearRightButton and (currentTime - lastClickTime > clickDelay):
#                 counterRight += 1
#                 cv2.ellipse(img, (buttonRightPosition[0] + buttonWidth // 2, buttonRightPosition[1] + buttonHeight // 2), (66, 66), 0, 0, counterRight * selectionSpeed, (0, 255, 0), 20)
#                 if counterRight * selectionSpeed > 360:
#                     counterRight = 0
#                     lastClickTime = currentTime
#                     if imageNumber < len(listShirts) - 1:
#                         imageNumber += 1
#             elif handNearLeftButton and (currentTime - lastClickTime > clickDelay):
#                 counterLeft += 1
#                 cv2.ellipse(img, (buttonLeftPosition[0] + buttonWidth // 2, buttonLeftPosition[1] + buttonHeight // 2), (66, 66), 0, 0, counterLeft * selectionSpeed, (0, 255, 0), 20)
#                 if counterLeft * selectionSpeed > 360:
#                     counterLeft = 0
#                     lastClickTime = currentTime
#                     if imageNumber > 0:
#                         imageNumber -= 1
#             else:
#                 counterRight = 0
#                 counterLeft = 0
#
#         _, buffer = cv2.imencode('.jpg', img)
#         frame = buffer.tobytes()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
#
# @app.route('/')
# def index():
#     return render_template('index.html')
#
# @app.route('/video_feed')
# def video_feed():
#     return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
#
# @app.route('/prev_shirt')
# def prev_shirt():
#     global imageNumber
#     if imageNumber > 0:
#         imageNumber -= 1
#     return '', 204
#
# @app.route('/next_shirt')
# def next_shirt():
#     global imageNumber
#     if imageNumber < len(listShirts) - 1:
#         imageNumber += 1
#     return '', 204
#
# if __name__ == '__main__':
#     app.run(debug=True, use_reloader=False)
