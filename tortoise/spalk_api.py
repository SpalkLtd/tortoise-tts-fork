import os
from tortoise import api
import utils.audio
import torchaudio
import glob


if __name__ == '__main__':
    audio_folder = 'tortoise/voices/spalk_horse_game'
    clips_paths = glob.glob(f'{audio_folder}/*.wav')

    os.makedirs('results/', exist_ok=True)

    reference_clips = [utils.audio.load_audio(p, 22050) for p in clips_paths]
    tts = api.TextToSpeech(use_deepspeed=True, kv_cache=True, half=True)
    gen, dbg_state = tts.tts_with_preset("Aside from a mishap at the third obstacle, one could say the overall performance was executed quite smoothly", voice_samples=reference_clips, preset='fast')

    if isinstance(gen, list):
        for j, g in enumerate(gen):
            torchaudio.save(os.path.join('results/', f'result.wav'), g.squeeze(0).cpu(), 24000)
    else:
        torchaudio.save(os.path.join('results/', f'result.wav'), gen.squeeze(0).cpu(), 24000)