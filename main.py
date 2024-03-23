from deepface import DeepFace
import cv2
from playsound import playsound
from time import time

src = 2

# if len(sys.argv) > 1:
#     src = int(sys.argv[1])

vid = cv2.VideoCapture(src)

in_progress = False
results = ['neutral']
current_emotion = None

TIMESPAN = 20
TOLERANCE = 0.2

WEIGHTS = {
    "angry": 1.1,
    "disgust": 1,
    "fear": 0.2,
    "happy": 1,
    "neutral": 0.3,
    "sad": 0.5,
    "surprise": 1,
}

detection_time_total = 0
detections = 0

def analyze_deepface():
    global detection_time_total, detections
    t = time()
    try:
        result = DeepFace.analyze(frame, actions=["emotion"])[0]
        region = result["region"]
        result = result["emotion"]
        for emotion in WEIGHTS:
            if emotion not in result:
                continue
            result[emotion] *= WEIGHTS[emotion]
        return (max(result, key=result.get), region)
    except ValueError:
        return
    finally:
        detection_time_total += time() - t
        detections += 1

start = False

recognising = False
total_percentages = {}
recognition_iters = 0

while True:
    _, frame = vid.read()

    # result_deepface = analyze_deepface()
    # region = result_deepface[1] if result_deepface else None
    # result_deepface = result_deepface[0] if result_deepface else None
    #
    # if region is not None:
    #     x, y, w, h = region["x"], region["y"], region["w"], region["h"]
    #     cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    #
    # if result_deepface is not None:
    #     results.append(result_deepface)
    #
    # if len(results) > TIMESPAN:
    #     del results[0]
    #
    # most_common_emotion = max(results, key=results.count)
    #
    # if cv2.waitKey(1) & 0xFF == ord('2'):
    #     if most_common_emotion is not None:
    #         playsound("audio/" + most_common_emotion + ".wav")
    #         print("\n" + most_common_emotion + ' (avg. time: ' + str(detection_time_total / detections) + 's)')
    #     current_emotion = most_common_emotion
    #
    # cv2.imshow("Camera input", frame)

    if recognising and recognition_iters < 10:
        try:
            result = DeepFace.analyze(frame, actions=["emotion"])
        except ValueError:
            result = None
        if result:
            largest_box = max(
                result, key=lambda b: b["region"]["w"] * b["region"]["w"] if any(b["region"]) else 0
            )  # This returns the box with the largest area
            cv2.rectangle(
                frame,
                (largest_box["region"]["x"], largest_box["region"]["y"]),
                (
                    largest_box["region"]["x"] + largest_box["region"]["w"],
                    largest_box["region"]["y"] + largest_box["region"]["h"],
                ),
                (0, 255, 0),
                2,
            )
            total_percentages = {
                x: (total_percentages[x] if x in total_percentages else 0) + largest_box["emotion"][x] * WEIGHTS[x]
                for x in largest_box["emotion"]
            }

        recognition_iters += 1
        print('.', end='')
    elif recognising and recognition_iters == 10:
        if total_percentages:
            top_emotion = max(total_percentages, key=lambda x: total_percentages[x])
            print(top_emotion)
            playsound('audio/' + top_emotion + '.wav')
        else:
            print("No face")
            playsound('audio/noface.wav')
        print()
        recognition_iters = 0
        recognising = False
        total_percentages = {}
    elif cv2.waitKey(1) == ord("2"):
        playsound('audio/start.ogg')
        recognising = True
        print('Recognising', end='')

    cv2.imshow("Camera input", frame)

    if not start:
        start = True
        playsound("audio/start.wav")

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

vid.release()
cv2.destroyAllWindows()
