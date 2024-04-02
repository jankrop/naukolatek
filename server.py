from deepface import DeepFace
import flask
import numpy as np
import tempfile
import json
import cv2

app = flask.Flask(__name__)

WEIGHTS = {
    "angry": 1.2,
    "disgust": 1,
    "fear": 0.5,
    "happy": 1,
    "neutral": 0.5,
    "sad": 1,
    "surprise": 1,
}

def analyze_deepface(frame):
    try:
        result = DeepFace.analyze(frame, actions=["emotion"])[0]["emotion"]
        for emotion in WEIGHTS:
            if emotion not in result:
                continue
            result[emotion] *= WEIGHTS[emotion]
        print('\033[32m' + max(result, key=result.get) + '\033[0m')
        return result
    except ValueError:
        return 'Error'

@app.route('/', methods=['POST'])
def index():
    file = flask.request.files['file']

    with tempfile.NamedTemporaryFile() as tmp_file:
        file.save(tmp_file.name)
        frame = np.load(tmp_file.name, allow_pickle=True)

        result = analyze_deepface(frame)

        cv2.imshow('Received', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            pass

        return json.dumps(result) if result != 'Error' else result


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
