# YouTube Video Converter to MP3

This is a simple command-line tool that allows you to convert YouTube videos to MP3 audio format. It leverages the YouTube Data API and FFmpeg to perform the conversion. This tool can be useful if you want to extract the audio from YouTube videos and save it as a standalone MP3 file.

# Features
  1. Convert YouTube videos to MP3 audio format.
  2. Specify the video URL or video ID for conversion.
  3. Automatically fetch video metadata (title, author, duration).
  4. Output MP3 file with proper metadata tags (title, artist, album).
  5. Easy to use command-line interface.

# Prerequisites
Before using this tool, ensure that you have the following prerequisites installed on your system:

  1. Python 3.6+
  2. FFmpeg
 
# Installation

1. Clone this repository to your local machine:
  ```
  git clone https://github.com/andrei2timo/Youtube-Video-converter-to-MP3.git
  ```
2. Change into the cloned directory:
  ```
  cd Youtube-Video-converter-to-MP3
  ```
3. Install the required dependencies using pip:
  ```
  pip install -r requirements.txt
  ```

# Usage

  To convert a YouTube video to MP3, follow these steps:
    1. Obtain a YouTube Data API key by following the official documentation.
    2. Create a config.yaml file in the project directory and add the following content:
    ```
    api_key: YOUR_YOUTUBE_DATA_API_KEY
    ```
      Replace YOUR_YOUTUBE_DATA_API_KEY with the API key you obtained in step 1.
    3. Run the following command to convert a YouTube video to MP3:
    ```
    python convert.py --url YOUTUBE_VIDEO_URL
    ```
      Replace YOUTUBE_VIDEO_URL with the URL or video ID of the YouTube video you want to convert.
      The converted MP3 file will be saved in the project directory with the filename output.mp3.
