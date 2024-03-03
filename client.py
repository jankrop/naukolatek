import requests
import cv2
from playsound import playsound
import numpy as np
import tempfile

video = cv2.VideoCapture(0)

in_progress = False
results = ['neutral']
current_emotion = None

TIMESPAN = 20
TOLERANCE = 0.3

while True:
    _, frame = video.read()
    cv2.imshow('Video', frame)

    result = None

    with tempfile.NamedTemporaryFile() as tmp_file:
        np.save(tmp_file, frame)
        tmp_file.seek(0)

        try:
            result = requests.post('http://127.0.0.1:5000/', files={'file': tmp_file}).text
            if result == 'Error':
                result = None
        except requests.RequestException as e:
            print("Error:", e)

    print(f'\033[90m{result}\033[0m')

    if result is not None:
        results.append(result)

    if len(results) > TIMESPAN:
        del results[0]

    most_common_emotion = max(results, key=results.count)

    # print('\033[90m', result_deepface, '|', current_emotion, '|', *results, '\033[0m')

    if (
            results.count(current_emotion) <= TIMESPAN * TOLERANCE
            and most_common_emotion != current_emotion
    ) or cv2.waitKey(1) & 0xFF == ord('2'):
        if most_common_emotion is not None:
            playsound("audio/" + most_common_emotion + ".wav")
        current_emotion = most_common_emotion

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
