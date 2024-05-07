import cv2
from deepface import DeepFace
import flask
import numpy as np
import tempfile
import json

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
        frame = cv2.imdecode(np.frombuffer(tmp_file.read(), np.uint8), cv2.IMREAD_COLOR)

        result = analyze_deepface(frame)

        return json.dumps(result) if result != 'Error' else result


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
