import base64
import os
from tortoise import api
import utils.audio
import torchaudio
import glob
from flask import Flask, jsonify, request, send_file


app = Flask(__name__)

@app.route('/generate_audio', methods=['POST'])
def generate_audio():
    if request.is_json:
        data = request.get_json()
        audio_folder = 'tortoise/voices/spalk_horse_game'
        outgoingText = data.get('OutgoingText', '')
        clips_paths = glob.glob(f'{audio_folder}/*.wav')

        os.makedirs('results/', exist_ok=True)

        reference_clips = [utils.audio.load_audio(p, 22050) for p in clips_paths]
        tts = api.TextToSpeech(use_deepspeed=True, kv_cache=True, half=True)
        gen = tts.tts_with_preset(outgoingText, voice_samples=reference_clips, preset='fast')

        if isinstance(gen, list):
            for j, g in enumerate(gen):
                torchaudio.save(os.path.join('results/', f'result.wav'), g.squeeze(0).cpu(), 24000)
        else:
            torchaudio.save(os.path.join('results/', f'result.wav'), gen.squeeze(0).cpu(), 24000)
        
        output_path = 'results/result.wav'
        with open(output_path, "rb") as audio_file:
            audio_data = audio_file.read()
        audio_data_base64 = base64.b64encode(audio_data).decode('utf-8')

        return jsonify({"message": "Audio generated successfully!", "WavAudioBase64" : audio_data_base64, "SampleRate": 24000}), 200
    else:
        return jsonify({"error": "Request must be JSON"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')