from deepface import DeepFace
import flask
import numpy as np
import tempfile

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
        return max(result, key=result.get)
    except ValueError as e:
        print('Error:', e)
        return 'Error'

@app.route('/', methods=['POST'])
def index():
    file = flask.request.files['file']

    with tempfile.NamedTemporaryFile() as tmp_file:
        file.save(tmp_file.name)
        frame = np.load(tmp_file.name, allow_pickle=True)

        result = analyze_deepface(frame)
        return result


if __name__ == "__main__":
    app.run(debug=True)
