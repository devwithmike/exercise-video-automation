import argparse
import os
from pathlib import Path
import time, datetime

from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip
from moviepy.config import change_settings

change_settings({"IMAGEMAGICK_BINARY": r"C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})
start_time = time.time()

def parse_script(script, video_src_dir):
    with open(script, "r") as f:
        script_data = f.read()
    items = []
    lines = script_data.strip().split('\n')
    i = 0
    
    while i < len(lines):
        title = lines[i].lstrip('# ').strip()
        description = lines[i + 1].strip()
        filename = os.path.join(Path(video_src_dir), lines[i + 2].strip())
        items.append({'title': title, 'description': description, 'filename': filename})
        i += 4
    return items

def process_video_item(item):
    try:
        video_clip = VideoFileClip(item["filename"])
        if hasattr(video_clip, 'duration') and video_clip.duration is not None:
            # Create the title text clip
            title_clip = TextClip(item["title"], fontsize=70, color='white', font='Arial-BoldMT', stroke_width=2, stroke_color='black', )
            title_clip = title_clip.set_pos(('left', 'top')).set_duration(video_clip.duration)

            # Create the description text clip
            description_clip = TextClip(item["description"], fontsize=70, color='white', font='Arial-BoldMT', stroke_width=2, stroke_color='black')
            description_clip = description_clip.set_pos(('left', title_clip.h + 5)).set_duration(video_clip.duration) # Position below the title

            # Composite the text onto the video
            final_clip = CompositeVideoClip([video_clip, title_clip, description_clip])
            return final_clip
        else:
            print(f"Warning: Could not determine the duration for {item['filename']}. Skipping this clip.")
            video_clip.close()
            return None
    except Exception as e:
        print(f"Error processing {item['filename']}: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(
                    prog='VideoAuto',
                    description='Automate basic video editing')
    
    requiredArgumentsGroup = parser.add_argument_group('required arguments')
    requiredArgumentsGroup.add_argument('-i', '--input', help='Directory to input videos', required=True)
    requiredArgumentsGroup.add_argument('-s', '--script', help='Markdown script file', required=True)
    requiredArgumentsGroup.add_argument('-o', '--output', help='Location and filename for mp4 file', required=True)
    args = parser.parse_args()
    
    script = parse_script(args.script, args.input)
    processed_clips = [process_video_item(item) for item in script if process_video_item(item) is not None]
    
    if processed_clips:
        try:
            final_movie = concatenate_videoclips(processed_clips, method="compose")
            final_movie.write_videofile(str(Path(args.output)), codec="libx264", audio_codec="aac")
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
