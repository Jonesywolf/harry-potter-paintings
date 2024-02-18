import cv2
import numpy as np
import face_recognition

def load_images():
    global left_eye_image, right_eye_image, mouth_image
    # Load the overlay images
    left_eye_image = cv2.imread(r"image-filtering-test\left_eye.png", -1)  # -1 means load with alpha channel
    right_eye_image = cv2.imread(r"image-filtering-test\right_eye.png", -1)
    mouth_image = cv2.imread(r"image-filtering-test\mouth.png", -1)

def capture_kawaii_image():
    # Open the webcam
    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    # Capture the first frame
    ret, frame = cap.read()

    # Release the webcam after capturing the frame
    cap.release()

    if ret:
        # Convert the image to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Increase the saturation to get bright, pastel colors
        hsv[:,:,1] = hsv[:,:,1]*1.5

        # Convert the image back to BGR color space
        frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

        grayScaleImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #applying median blur to smoothen an image
        smoothGrayScale = cv2.medianBlur(grayScaleImage, 5)
        #retrieving the edges for cartoon effect
        getEdge = cv2.adaptiveThreshold(smoothGrayScale, 255, 
        cv2.ADAPTIVE_THRESH_MEAN_C, 
        cv2.THRESH_BINARY, 15, 15)
        
        # Define the structuring element
        # In this case, we're using a 3x3 rectangle
        kernel = np.ones((3,3), np.uint8)

        # Apply dilation
        getEdge = cv2.dilate(getEdge, kernel, iterations=3)

        #applying bilateral filter to remove noise
        colorImage = cv2.bilateralFilter(frame, 15, 500, 500)

        # Create a numpy array representing the color scalar
        scalar = np.array([0b11000000, 0b11000000, 0b11000000])

        # Apply the bitwise AND operation
        colorImage = colorImage & scalar
        
        # Convert the image to 8-bit unsigned integers
        colorImage = cv2.convertScaleAbs(colorImage)

        #masking edged image with our "BEAUTIFY" image
        cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=getEdge)
        
        # Convert the cartoonImage to the HSV color space
        hsv = cv2.cvtColor(cartoonImage, cv2.COLOR_BGR2HSV)

        # Increase the V channel to brighten the image
        hsv[:,:,2] = np.clip(hsv[:,:,2]*1.25, 0, 255)

        # Convert the image back to the BGR color space
        cartoonImage = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        
        # Add alpha channel to the image
        cartoonImage = cv2.cvtColor(cartoonImage, cv2.COLOR_BGR2BGRA)

        # Find all facial features in all the faces in the image
        face_landmarks_list = face_recognition.face_landmarks(frame)

        # Loop through each face
        for face_landmarks in face_landmarks_list:
            # Overlay image on each eye
            for eye, eye_image in [('left_eye', left_eye_image), ('right_eye', right_eye_image)]:
                points = face_landmarks[eye]
                x_min = min(points, key=lambda p: p[0])[0]
                x_max = max(points, key=lambda p: p[0])[0]
                y_min = min(points, key=lambda p: p[1])[1]
                y_max = max(points, key=lambda p: p[1])[1]
                eye_size = max(x_max - x_min, y_max - y_min) * 2
                resized_eye_image = cv2.resize(eye_image, (eye_size, eye_size))
                # Adjust the position to keep the eye image centered
                x_min -= eye_size // 4
                y_min -= eye_size // 4
                # Overlay the eye image
                for c in range(0, 3):
                    cartoonImage[y_min:y_min+eye_size, x_min:x_min+eye_size, c] = resized_eye_image[:,:,c] * (resized_eye_image[:,:,3]/255.0) +  cartoonImage[y_min:y_min+eye_size, x_min:x_min+eye_size, c] * (1.0 - resized_eye_image[:,:,3]/255.0)

            # Overlay image on mouth
            points = face_landmarks['bottom_lip']
            x_min = min(points, key=lambda p: p[0])[0]
            x_max = max(points, key=lambda p: p[0])[0]
            y_min = min(points, key=lambda p: p[1])[1]
            y_max = max(points, key=lambda p: p[1])[1]
            mouth_width = int((x_max - x_min) * 1.5)
            mouth_height = int((y_max - y_min) * 1.5)
            resized_mouth_image = cv2.resize(mouth_image, (mouth_width, mouth_height))
            # Adjust the position to keep the mouth image centered
            x_min -= mouth_width // 3
            y_min -= mouth_height // 3
            # Overlay the mouth image
            for c in range(0, 3):
                cartoonImage[y_min:y_min+mouth_height, x_min:x_min+mouth_width, c] = resized_mouth_image[:,:,c] * (resized_mouth_image[:,:,3]/255.0) +  cartoonImage[y_min:y_min+mouth_height, x_min:x_min+mouth_width, c] * (1.0 - resized_mouth_image[:,:,3]/255.0)

        # Save the cartoon image as a jpg
        cv2.imwrite(f"image-filtering-test\painting.jpg", cartoonImage)
    else:
        print("Can't receive frame (stream end?). Exiting ...")