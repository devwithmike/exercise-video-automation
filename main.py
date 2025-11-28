import argparse
import os
from pathlib import Path
import time, datetime
import sys

from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip, ColorClip
from moviepy.config import change_settings
import moviepy.config as conf

# Try to import python-dotenv
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not installed. Install with: pip install python-dotenv")
    print("Continuing without .env file support...")

start_time = time.time()

def get_config():
    """Load configuration from .env file and validate IMAGEMAGICK_BINARY"""
    imagemagick_binary = os.getenv('IMAGEMAGICK_BINARY')

    if not imagemagick_binary:
        print("Error: IMAGEMAGICK_BINARY not found in .env file")
        print("Please create a .env file with: IMAGEMAGICK_BINARY=/path/to/imagemagick/binary")
        sys.exit(1)

    # Set the ImageMagick binary path
    conf.IMAGEMAGICK_BINARY = imagemagick_binary

    return {
        'input': os.getenv('INPUT_DIR'),
        'script': os.getenv('SCRIPT_FILE'),
        'output': os.getenv('OUTPUT_FILE')
    }

def parse_script(script, video_src_dir):
    with open(script, "r") as f:
        script_data = f.read()
    items = []
    segments = script_data.strip().split('\n\n')

    for segment in segments:
        lines = segment.strip().split('\n')
        video_text_list = []
        for line in lines[:-1]:
            video_text_list.append(line.strip())
        filename_text = lines[len(lines) - 1]
        if filename_text.upper() == "BLANK":
            filename = filename_text
        else:
            filename = os.path.join(Path(video_src_dir), filename_text.strip())
        items.append({'texts': video_text_list, 'filename': filename})
    return items

def process_video_item(item):
    font = "Arial-BoldMT"
    fontsize = 70
    color = "white"
    margin = 10
    stroke_width=2,
    stroke_color='black'

    text_clips = []
    y_position = margin
    if item["filename"] == "BLANK":
        resolution = (1920, 1080)
        duration = 5
        base_clip = ColorClip(size=resolution, color=(0, 0, 0), duration=duration)

        total_text_height = 0
        text_objs = []
        for text in item["texts"]:
            txt = TextClip(text, font=font, fontsize=fontsize, color=color, stroke_width=stroke_width, stroke_color=stroke_color)
            total_text_height += txt.h + 10  # small padding between lines
            text_objs.append(txt)

        y_start = (resolution[1] - total_text_height) // 2  # vertical center start

        for txt in text_objs:
            text_clip = txt.set_position(("center", y_start)).set_duration(base_clip.duration)
            text_clips.append(text_clip)
            y_start += txt.h + 10
    else:
        base_clip = VideoFileClip(item["filename"])
        for text in item["texts"]:
            text_clip = TextClip(text, font=font, fontsize=fontsize, color=color, stroke_width=stroke_width, stroke_color=stroke_color)
            text_clip = text_clip.set_position((margin, y_position))
            text_clip = text_clip.set_duration(base_clip.duration)
            text_clips.append(text_clip)
            y_position += text_clip.h + 5
    final_clip = CompositeVideoClip([base_clip] + text_clips)
    return final_clip

def main():
    # Load configuration from .env
    env_config = get_config()

    parser = argparse.ArgumentParser(
                    prog='VideoAuto',
                    description='Automate basic video editing')

    # Arguments are now optional if they exist in .env
    parser.add_argument('-i', '--input', help='Directory to input videos', required=False)
    parser.add_argument('-s', '--script', help='Markdown script file', required=False)
    parser.add_argument('-o', '--output', help='Location and filename for mp4 file', required=False)
    args = parser.parse_args()

    # Command line args take precedence over .env values
    input_dir = args.input if args.input else env_config['input']
    script_file = args.script if args.script else env_config['script']
    output_file = args.output if args.output else env_config['output']

    # Validate that all required parameters are present
    if not input_dir:
        print("Error: Input directory not specified. Provide via -i/--input or INPUT_DIR in .env")
        sys.exit(1)
    if not script_file:
        print("Error: Script file not specified. Provide via -s/--script or SCRIPT_FILE in .env")
        sys.exit(1)
    if not output_file:
        print("Error: Output file not specified. Provide via -o/--output or OUTPUT_FILE in .env")
        sys.exit(1)

    script = parse_script(script_file, input_dir)
    processed_clips = [process_video_item(item) for item in script if process_video_item(item) is not None]

    if processed_clips:
        try:
            final_movie = concatenate_videoclips(processed_clips, method="compose")
            final_movie.write_videofile(str(Path(output_file)), codec="libx264", audio_codec="aac", fps=30)
            final_movie.close()
            print("Successfully combined the video clips.")
        except Exception as e:
            print(f"Error during concatenation or writing: {e}")
            for clip in processed_clips:
                if clip:
                    clip.close()
    else:
        print("No valid video clips were processed, so no combined video was created.")

    print("Took", str(datetime.timedelta(seconds=time.time() - start_time)), "to run")


if __name__ == "__main__":
    main()