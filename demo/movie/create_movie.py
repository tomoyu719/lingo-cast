import os
from audio.text_to_speech import TextToSpeech
from pil_to_cv2 import pil_to_cv2
import moviepy.editor as mpy
from PIL import Image, ImageDraw, ImageFont
from pydub import AudioSegment

FPS = 30
W = 1920
H = 1080
X_MARGIN = W / 20
Y_WORD = H / 10 * 3
Y_TRANSLATE = H / 10 * 6
Y_EXAMPLE =  H / 10 * 8
SENT_FONT_SIZES = [96, 72, 48, 32]
font = '/Users/kitanotoshiyuki/Library/Fonts/FuturaNowHeadline-Bd.otf'

class CreateMovie():
    def __init__(self, source_language, target_language) -> None:
        self.tts_source = TextToSpeech(source_language)
        self.tts_target = TextToSpeech(target_language)
        self.small_interval = AudioSegment.silent(duration=750)
        self.large_interval = AudioSegment.silent(duration=1500)

    def create_audio(self, word, translate_sentence, example_sentence, output_dir):
        word_speech = self.tts_source.synthesize_text(word)
        translation_sentence_speech = self.tts_target.synthesize_text(translate_sentence)
        example_sentence_speech = self.tts_source.synthesize_text(example_sentence)
        audios = [word_speech, translation_sentence_speech, example_sentence_speech, example_sentence_speech]
        # TODO? save indivisual audios? 
        # word_speech_path = os.path.join(output_dir, word, 'word.mp3')
        # word_speech.export(word_speech_path, format="mp3")
        # translation_sentence_speech_path = os.path.join(output_dir, word, 'translate_sentence.mp3')
        # translation_sentence_speech.export(translation_sentence_speech_path, format="mp3")
        # example_sentence_speech_path = os.path.join(output_dir, word, 'example_sentence.mp3')
        # example_sentence_speech.export(example_sentence_speech_path, format="mp3")
        
        track = AudioSegment.empty()
        for au in audios:
            track += self.small_interval + au 
        track += self.large_interval
        # TODO if same word in same directory?
        track_path = os.path.join(output_dir, word + '.mp3')
        track.export(track_path, format="mp3")
        return track_path
        
    def create_image(self, word, sentence_translation, sentence_example):
        
        img = Image.new('RGB', (W, H),(0,0,0))
        draw = ImageDraw.Draw(img)
        word_font = ImageFont.truetype(font, 144)
        _, word_height = draw.textsize(word, font=word_font)

        for size in SENT_FONT_SIZES:
            sent_font = ImageFont.truetype(font, size)
            tr_width, tr_height = draw.textsize(sentence_translation, font=sent_font)
            ex_width, ex_height = draw.textsize(sentence_example, font=sent_font)
            if not (tr_width + 2 * X_MARGIN > W or ex_width + 2 * X_MARGIN > W):
                break

        draw.text((X_MARGIN, Y_WORD - word_height), word, (255,255,255), font=word_font, language='uk-UA')
        draw.text((X_MARGIN, Y_TRANSLATE - tr_height), sentence_translation, (255,255,255), font=sent_font, language='en-US')
        draw.text((X_MARGIN, Y_EXAMPLE - ex_height), sentence_example, (255,255,255), font=sent_font, language='uk-UA')
        
        return pil_to_cv2(img)

    def create_clip(self, img, track_path): 
        audio = mpy.AudioFileClip(track_path)
        track_length = audio.duration
        clip = mpy.ImageClip(img).set_duration(track_length)
        clip = clip.set_audio(audio)
        
        return clip
    
    def combine_audios(self, audios_path, path):
        audios = [AudioSegment.from_mp3(au) for au in audios_path]
        track = AudioSegment.empty()
        for au in audios:
            track += au 
        track.export(path, format="mp3")

    def create_movie(self, clips, path):
        movie = mpy.concatenate_videoclips(clips)
        movie.write_videofile(
            filename=path, 
            fps=FPS, 
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a', 
            remove_temp=True
        )
        movie.close()
