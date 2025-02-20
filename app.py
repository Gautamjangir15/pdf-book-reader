from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from gtts import gTTS
from io import BytesIO

app = Flask(__name__)
CORS(app)

@app.route('/tts', methods=['POST'])
def tts():
    try:
        data = request.get_json()
        text = data.get('text', '')
        if not text.strip():
            return jsonify({"error": "Text is empty"}), 400

        tts = gTTS(text, lang='en')
        audio_stream = BytesIO()
        tts.write_to_fp(audio_stream)
        audio_stream.seek(0)

        return send_file(
            audio_stream,
            mimetype='audio/mpeg',
            as_attachment=False,
            download_name='speech.mp3'
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Flask app is working!"

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))  
    app.run(host='0.0.0.0', port=port)

