import argparse
import os
from pathlib import Path
import time, datetime

from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip, ColorClip
from moviepy.config import change_settings

change_settings({"IMAGEMAGICK_BINARY": r"C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})
start_time = time.time()

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
    # try:
    #     resolution = (1920, 1080)
    #     clips = []
    #     if item["filename"] == "BLANK":
    #         duration = 5
    #         black_clip = ColorClip(size=resolution, color=(0, 0, 0), duration=duration)
    #         clips.append(black_clip)
            
    #         offset = 0
    #         for text in item["texts"]:
    #             temp_clip = TextClip(text, fontsize=70, color='white', font='Arial-BoldMT', stroke_width=2, stroke_color='black').set_position('center', resolution[1] // 2 + offset).set_duration(duration)
    #             clips.append(temp_clip)
    #             offset += 60
    #     else:
    #         video_clip = VideoFileClip(item["filename"])
    #         if hasattr(video_clip, 'duration') and video_clip.duration is not None:
    #             offset = 0
    #             for text in item["texts"]:
    #                 temp_clip = TextClip(text, fontsize=70, color='white', font='Arial-BoldMT', stroke_width=2, stroke_color='black').set_position('left', resolution[1] - offset).set_duration(video_clip.duration)
    #                 clips.append(temp_clip)
    #                 offset += 60
    #         else:
    #             print(f"Warning: Could not determine the duration for {item['filename']}. Skipping this clip.")
    #             video_clip.close()
    #             return None
    #     final_clip = CompositeVideoClip(clips)
    #     return final_clip
    # except Exception as e:
    #     print(f"Error processing {item['filename']}: {e}")
    #     return None
    
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
            final_movie.write_videofile(str(Path(args.output)), codec="libx264", audio_codec="aac", fps=30)
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
