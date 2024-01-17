import cv2
from fer import FER


vid = cv2.VideoCapture(0)
detector = FER()

recognising = False
total_percentages = {}
recognition_iters = 0

while True:
    _, frame = vid.read()

    if recognising and recognition_iters < 10:
        result = detector.detect_emotions(frame)
        if result:
            largest_box = max(
                result, key=lambda b: b["box"][2] * b["box"][3] if any(b["box"]) else 0
            )  # This returns the box with the largest area
            cv2.rectangle(
                frame,
                (largest_box["box"][0], largest_box["box"][1]),
                (
                    largest_box["box"][0] + largest_box["box"][2],
                    largest_box["box"][1] + largest_box["box"][3],
                ),
                (0, 255, 0),
                2,
            )
            total_percentages = {
                x: (total_percentages[x] if x in total_percentages else 0) + largest_box["emotions"][x]
                for x in largest_box["emotions"]
            }

        recognition_iters += 1
        print('.', end='')
    elif recognising and recognition_iters == 10:
        if total_percentages:
            top_emotion = max(total_percentages, key=lambda x: total_percentages[x])
            print(f'\033[32m{top_emotion.upper()}\033[00m')
        else:
            print('\033[31mNo face found!\033[00m')
        print()
        recognition_iters = 0
        recognising = False
        total_percentages = {}
    elif cv2.waitKey(1) == ord("r"):
        recognising = True
        print('Recognising', end='')

    cv2.imshow("Camera input", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

vid.release()
cv2.destroyAllWindows()
