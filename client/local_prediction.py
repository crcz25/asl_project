import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
import depthai as dai
import signal
import pandas as pd
import time
import mediapipe as mp
from tensorflow import keras
import depthai
import sys
from multiprocessing import Process, Queue

# current_dir = os.path.dirname(os.path.abspath(__file__))
reconstructed_model = keras.models.load_model('../model/asl_model')
classes = ['a', 'b', 'c', 'close', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'open', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

# Define a function to crop the hand from the image
def crop_hand(image):
    # Detect the hand landmarks
    results = hands.process(image)
    # print('Handedness:', results.multi_handedness)
    # Get the bounding box of the hand
    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        x_min = min(l.x for l in hand_landmarks.landmark)
        x_max = max(l.x for l in hand_landmarks.landmark)
        y_min = min(l.y for l in hand_landmarks.landmark)
        y_max = max(l.y for l in hand_landmarks.landmark)
        # Crop the hand from the image
        extra_space = 0.08
        hand_image = image[int(y_min*image.shape[0] - extra_space*image.shape[0]):int(y_max*image.shape[0] + extra_space*image.shape[0]),
                            int(x_min*image.shape[1] - extra_space*image.shape[1]):int(x_max*image.shape[1] + extra_space*image.shape[1])]
        return hand_image
    return None

def process_frames(queue):
    # Define the Oak-D pipeline
    pipeline = depthai.Pipeline()
    cam_rgb = pipeline.createColorCamera()
    cam_rgb.setPreviewSize(640, 480)
    cam_rgb.setInterleaved(False)
    cam_rgb.setResolution(depthai.ColorCameraProperties.SensorResolution.THE_1080_P)
    cam_rgb.setBoardSocket(depthai.CameraBoardSocket.RGB)
    cam_rgb.setFps(30)
    cam_rgb_xout = pipeline.createXLinkOut()
    cam_rgb_xout.setStreamName('rgb')
    cam_rgb.preview.link(cam_rgb_xout.input)

    with depthai.Device(pipeline) as device:
        q = device.getOutputQueue(name='rgb', maxSize=4, blocking=False)
        # Process frames indefinitely
        while True:
            # Get the next available frame
            in_rgb = q.tryGet()
            if in_rgb is not None:
                # Convert the frame to a numpy array
                frame_og = in_rgb.getCvFrame()
                # Flip the frame horizontally
                frame = cv2.flip(frame_og, 1)
                # Convert the frame to RGB
                # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Crop the hand from the image
                frame_hand = crop_hand(frame)
                if frame_hand is not None and frame_hand.shape[0] > 0 and frame_hand.shape[1] > 0:
                    # Put the frame into the queue
                    queue.put(frame_hand)
                    # Show the frame
                    cv2.imshow('OAK-D Hand', frame_hand)
                    if cv2.waitKey(1) == ord('q'):
                        cv2.destroyAllWindows()
                else:
                    queue.put(None)
                cv2.imshow('OAK-D', frame_og)
                if cv2.waitKey(1) == ord('q'):
                    cv2.destroyAllWindows()


def send_frames(queue):
    # Process frames indefinitely
    frame_count = 0
    while True:
        # Get the next available frame from the queue
        frame = queue.get()
        # Send the frame to the server every 15th frame
        if frame is not None and frame_count % 15 == 0:
            frame_count = 0
            # Show the frame
            if frame.shape[0] > 0 and frame.shape[1] > 0:
                # Resize the frame
                frame = cv2.resize(frame, (150, 150))
                # Predict the class of the frame
                start_time = time.time()
                prediction = reconstructed_model.predict(np.array([frame]), verbose=0)
                end_time = time.time()
                elapsed_time = end_time - start_time
                # Get the class name
                class_name = classes[np.argmax(prediction)]
                # Get the confidence
                confidence = np.max(prediction)
                # Print the class name and confidence
                print(f'Letter: {class_name}, Confidence: {confidence:.2f}, Elapsed Time: {elapsed_time:.2f} seconds')
                # Add the class name and confidence to the frame
                cv2.putText(frame, f'{class_name} {confidence:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                # Show the frame
                cv2.imshow('OAK-D Response Hand', frame)
                if cv2.waitKey(1) == ord('q'):
                    cv2.destroyAllWindows()
                # Append the results to the csv file
                with open('results_local_prediction.csv', 'a') as f:
                    # Add the class name, confidence, and elapsed time to the csv file
                    f.write(f'{class_name},{confidence},{elapsed_time}\n')
        # Increment the frame count
        frame_count += 1

if __name__ == '__main__':
    try:
        # Create the queue
        queue = Queue()

        # Create the processes
        process_frames_process = Process(target=process_frames, args=(queue,))
        send_frames_process = Process(target=send_frames, args=(queue,))

        # Start the processes
        process_frames_process.start()
        send_frames_process.start()

        # Wait for the processes to finish
        process_frames_process.join()
        send_frames_process.join()
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
        # Close the queue
        queue.close()
        # Terminate the processes
        process_frames_process.terminate()
        send_frames_process.terminate()
        # Close cv2 windows
        cv2.destroyAllWindows()
        # Exit the script
        sys.exit(0)
