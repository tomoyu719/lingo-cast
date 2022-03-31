import argparse
import json
import os

from create_movie import CreateMovie
from mytranslater import MyTransrator


def main():
    parser = argparse.ArgumentParser()
    
    # TODO raise error if blank
    parser.add_argument("-i", "--input_json_file_path")
    parser.add_argument("-o", "--output_file_dir", default='output')
    parser.add_argument("-s","--source_language")
    parser.add_argument("-t","--target_language", type=str, default='en')
    args = parser.parse_args()

    input_file_path = args.input_json_file_path
    input_file_name = os.path.basename(input_file_path).split('.')[0]

    output_dir = os.path.join(args.output_file_dir, args.source_language, args.target_language, input_file_name)
    output_audios_dir = os.path.join(output_dir, 'audios')
    
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(output_audios_dir, exist_ok=True)

    with open(args.input_json_file_path) as f:
        df = json.load(f)

    translator = MyTransrator(args.target_language)
    
    create_movie = CreateMovie(args.source_language, args.target_language)
    clips = []
    audios_path = []
    for d in df:
        word = d['word']
        example_sentence = d['example']
        translate_sentence = translator.translate(example_sentence)
        img = create_movie.create_image(word, translate_sentence, example_sentence)
        audio_path = create_movie.create_audio(word, translate_sentence, example_sentence, output_audios_dir)
        audios_path.append(audio_path)
        clip = create_movie.create_clip(img, audio_path)
        clips.append(clip)
        
    
    output_audio_path = os.path.join(output_dir , input_file_name + '.mp3')
    output_movie_path = os.path.join(output_dir , input_file_name + '.mp4')
    create_movie.combine_audios(audios_path, output_audio_path)
    create_movie.create_movie(clips, output_movie_path)



if __name__ == '__main__':
    main()
              