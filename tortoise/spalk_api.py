from tortoise import api
import utils.audio
import glob


if __name__ == '__main__':
    audio_folder = './voices/spalk_horse_game'
    clips_paths = glob.glob(f'{audio_folder}/*.wav')

    reference_clips = [utils.audio.load_audio(p, 22050) for p in clips_paths]
    tts = api.TextToSpeech()
    pcm_audio = tts.tts_with_preset("Aside from a mishap at the third obstacle, one could say the overall performance was executed quite smoothly", voice_samples=reference_clips, preset='fast')