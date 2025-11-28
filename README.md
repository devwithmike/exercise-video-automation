# EVA - Exercise Video Automation

**EVA** (Exercise Video Automation) is a Python-based tool designed to automate the creation of exercise demonstration videos with text overlays. While built specifically for fitness content, EVA can be used for any video project that requires automated text overlays and clip concatenation.

## Features

- **Automated Video Concatenation**: Combine multiple video clips into a single output file
- **Dynamic Text Overlays**: Add multiple lines of text to each video segment
- **Blank Slides**: Insert black slides with centered text between video clips
- **Script-Based Workflow**: Define your entire video structure in a simple text-based script file
- **Flexible Configuration**: Use `.env` file for default settings or command-line arguments for one-off changes
- **Professional Styling**: Text overlays with customizable fonts, colors, and stroke effects

## Use Cases

- Exercise demonstration videos with movement descriptions
- Tutorial videos with step-by-step instructions
- Educational content with annotations
- Any video project requiring automated text overlays

## Prerequisites

- Python 3.7+
- [uv](https://docs.astral.sh/uv/) - Fast Python package installer
- ImageMagick
- FFmpeg

### Installing System Dependencies

```bash
# Install ImageMagick (Ubuntu/Debian)
sudo apt-get install imagemagick

# Install ImageMagick (macOS)
brew install imagemagick

# Install ImageMagick (Windows)
# Download from: https://imagemagick.org/script/download.php
```

### Installing uv

```bash
# macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or via pip
pip install uv
```

## Installation

1. Clone or download this repository
2. Install Python dependencies using uv:
   ```bash
   uv pip install moviepy python-dotenv
   ```

   Or if you have a `requirements.txt`:
   ```bash
   uv pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root (see Configuration section)

## Configuration

### .env File Setup

Create a `.env` file in your project directory with the following required settings:

```env
# Required: Path to ImageMagick binary
IMAGEMAGICK_BINARY=/usr/bin/convert

# Optional: Default paths (can be overridden by command-line arguments)
INPUT_DIR=/path/to/your/video/clips
SCRIPT_FILE=/path/to/your/script.txt
OUTPUT_FILE=/path/to/output.mp4
```

**Important**: The `IMAGEMAGICK_BINARY` path is required and the program will exit with an error if not present.

## Script File Format

Create a text file that defines your video structure. Each segment is separated by a blank line.

### Format

```
Text line 1
Text line 2
video_filename.mp4

Another text line
another_video.mp4

Title Slide
Subtitle or description
BLANK
```

### Example Script

```
Warm Up
Jumping Jacks - 30 seconds
warmup_jumpingjacks.mp4

Upper Body
Push-ups - 3 sets of 10
exercises_pushups.mp4

Rest Period
Take a 30 second break
BLANK

Cool Down
Stretching routine
cooldown_stretch.mp4
```

### Script Rules

- Each segment consists of one or more text lines followed by a filename
- Text lines will be displayed as overlays on the video
- The last line of each segment is the video filename
- Use `BLANK` as the filename to create a 5-second black slide with centered text
- Separate segments with blank lines
- Video files should be in your `INPUT_DIR`

## Usage

### Using .env Defaults

If all settings are configured in your `.env` file:

```bash
uv run eva.py
```

Or with standard Python:
```bash
python eva.py
```

### Using Command-Line Arguments

Override `.env` settings with command-line arguments:

```bash
uv run eva.py -i /path/to/videos -s script.txt -o output.mp4
```

### Mixed Approach

Use `.env` for some settings and override others:

```bash
uv run eva.py -o different_output.mp4
```

### Command-Line Options

- `-i, --input`: Directory containing input video files
- `-s, --script`: Path to script file
- `-o, --output`: Path and filename for output MP4 file

**Note**: Command-line arguments always take precedence over `.env` settings.

## Quick Start with uv

For a quick one-time run without installing dependencies globally:

```bash
# uv will automatically handle dependencies
uv run --with moviepy --with python-dotenv eva.py -i ./videos -s script.txt -o output.mp4
```

## Text Styling

Current default styling (can be modified in the code):

- **Font**: Arial Bold
- **Font Size**: 70pt
- **Color**: White
- **Stroke**: 2px black outline
- **Position**: Top-left with 10px margin (centered for BLANK slides)

## Output

EVA generates a single MP4 video file with:
- Codec: H.264 (libx264)
- Audio Codec: AAC
- Frame Rate: 30 FPS
- Resolution: Matches source videos (or 1920x1080 for BLANK slides)

## Troubleshooting

### "IMAGEMAGICK_BINARY not found in .env file"
Create a `.env` file with the correct path to your ImageMagick binary.

### "python-dotenv not installed"
Run: `uv pip install python-dotenv`

### Text not appearing on videos
Verify that ImageMagick is properly installed and the path in `.env` is correct.

### Video concatenation errors
Ensure all video files have compatible formats, codecs, and resolutions.

## Performance

Processing time depends on:
- Number and length of video clips
- Video resolution and quality
- System hardware capabilities

The program displays total processing time upon completion.

## Why uv?

EVA uses [uv](https://docs.astral.sh/uv/) for faster and more reliable Python package management:
- **10-100x faster** than pip for package installation
- **Reliable dependency resolution**
- **Drop-in replacement** for pip
- **No virtual environment conflicts**

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve EVA.

## Acknowledgments

Built with:
- [MoviePy](https://zulko.github.io/moviepy/) - Video editing library
- [python-dotenv](https://github.com/theskumar/python-dotenv) - Environment variable management
- [ImageMagick](https://imagemagick.org/) - Image processing
- [uv](https://docs.astral.sh/uv/) - Fast Python package installer

---

**EVA** - Making exercise video creation simple and automated.