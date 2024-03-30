import requests
import cv2
from playsound import playsound
import numpy as np
import tempfile
import RPi.GPIO as GPIO
import json

GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.IN)

video = cv2.VideoCapture(0)

in_progress = False
results = ['neutral']
current_emotion = None

TIMESPAN = 20
TOLERANCE = 0.3

start = False

def analyze_deepface(fr):
    result = None

    with tempfile.NamedTemporaryFile() as tmp_file:
        np.save(tmp_file, fr)
        tmp_file.seek(0)

        try:
            result = requests.post('http://192.168.0.183:5000/', files={'file': tmp_file}).text
            if result == 'Error':
                result = None
            else:
                result = json.loads(result)
        except requests.RequestException as e:
            print("Error:", e)

    return result

recognising = False
total_percentages = {}
recognition_iters = 0

while True:
    _, frame = video.read()

    if recognising and recognition_iters < 5:
        result = analyze_deepface(frame)

        if result:
            total_percentages = {
                emotion: total_percentages.get(emotion, 0) + float(result[emotion])
                for emotion in result
            }

        recognition_iters += 1
    elif recognising and recognition_iters == 5:
        if total_percentages:
            top_emotion = max(total_percentages, key=total_percentages.get)
            playsound(f'audio/{top_emotion}.wav')
        else:
            playsound('audio/noface.wav')
        recognition_iters = 0
        recognising = False
        total_percentages = {}
    elif GPIO.input(2) == 0:  # pressed
        playsound('audio/start.ogg')
        recognising = True

    if not start:
        start = True
        playsound('audio/start.wav')

video.release()
