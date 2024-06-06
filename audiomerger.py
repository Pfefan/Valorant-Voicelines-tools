import os
import random
import argparse

from pydub import AudioSegment

def merge_audio_files(input_dir, output_file, filename="merged_audio"):
    out_file = os.path.join(output_file, filename + ".wav")
    merged_audio = AudioSegment.empty()
    files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
    for file in files:
        audio = AudioSegment.from_file(os.path.join(input_dir, file))
        merged_audio += audio + AudioSegment.silent(duration=random.randint(250, 500))
    print(out_file)
    merged_audio.export(out_file, format='wav', bitrate='320k')
    
    print("\nAudio files merged successfully!")
    print("\nStats:")
    print(f"  - Length: {len(merged_audio) / (1000 * 60):.2f} minutes")
    print(f"  - Size: {os.path.getsize(out_file) / (1024 * 1024):.2f} MB\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download Valorant agent voice lines.')
    parser.add_argument('in_path', type=str, help='The input path for the files which need to be merged.')
    parser.add_argument('out_path', type=str, help='The output path for the merged files.')
    parser.add_argument('--filename', type=str, default="merged_audio", help='The name of the merged audio file.')
    args = parser.parse_args()
    
    merge_audio_files(args.in_path, args.out_path, args.filename)
