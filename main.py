from deepface import DeepFace
import cv2
from playsound import playsound
from time import time

src = 0

# if len(sys.argv) > 1:
#     src = int(sys.argv[1])

vid = cv2.VideoCapture(src)

in_progress = False
results = ['neutral']
current_emotion = None

TIMESPAN = 20
TOLERANCE = 0.3

WEIGHTS = {
    "angry": 1.2,
    "disgust": 1,
    "fear": 0.5,
    "happy": 1,
    "neutral": 0.5,
    "sad": 1,
    "surprise": 1,
}

detection_time_total = 0
detections = 0

def analyze_deepface():
    global detection_time_total, detections
    t = time()
    try:
        result = DeepFace.analyze(frame, actions=["emotion"])[0]["emotion"]
        for emotion in WEIGHTS:
            if emotion not in result:
                continue
            result[emotion] *= WEIGHTS[emotion]
        return max(result, key=result.get)
    except ValueError:
        return
    finally:
        detection_time_total += time() - t
        detections += 1


while True:
    _, frame = vid.read()

    # if cv2.waitKey(1) == ord("2") and not in_progress:
    #     playsound("audio/start.ogg")
    #     in_progress = True

    # if time_deepface >= 1 and time_fer >= 1 and time_tf >= 1:
    #     in_progress = False
    #     time_deepface, time_fer, time_tf = 0, 0, 0
    #     average_deepface = {
    #         emotion: sum(
    #             [attempt[0]["emotion"][emotion] for attempt in results_deepface]
    #         )
    #         for emotion in results_deepface[0][0]["emotion"]
    #     }
    #     average_fer = {
    #         emotion: sum(
    #             [attempt[0]["emotions"][emotion] for attempt in results_fer]
    #         )
    #         for emotion in results_fer[0][0]["emotions"]
    #     }
    #     average_tf = {
    #         emotion: sum(
    #             [list(attempt)[0][i] for attempt in results_tf]
    #         )
    #         for i, emotion in enumerate(tf_labels)
    #     }
    #
    #     print(
    #         sorted(average_deepface.items(), key=lambda x: x[1], reverse=True),
    #         sorted(average_fer.items(), key=lambda x: x[1], reverse=True),
    #         sorted(average_tf.items(), key=lambda x: x[1], reverse=True),
    #         sep="\n",
    #     )
    #
    # if in_progress:
    #     analyze_deepface()
    #     analyze_fer()
    #     analyze_tf()

    result_deepface = analyze_deepface()

    if result_deepface is not None:
        results.append(result_deepface)

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
            print("\n" + most_common_emotion + ' (avg. time: ' + str(detection_time_total / detections) + 's)')
        current_emotion = most_common_emotion

    # print(
    #     "Deepface:",
    #     (
    #         result_deepface[0]["dominant_emotion"]
    #         if result_deepface
    #         else "\033[31mNo face\033[0m"
    #     ),
    #     end=" | ",
    # )
    # print(
    #     "FER:",
    #     (
    #         max(result_fer[0]["emotions"], key=result_fer[0]["emotions"].get)
    #         if result_fer
    #         else "\033[31mNo face\033[0m"
    #     ),
    #     end=" | ",
    # )
    # print("TensorFlow:", max(result_tf, key=result_tf.get) if result_tf else "\033[31mNo face\033[0m")

    # print()

    cv2.imshow("Camera input", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

vid.release()
cv2.destroyAllWindows()
