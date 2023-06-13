from flask import Flask, render_template, request, flash, redirect, url_for, session
from pytube import YouTube
import os
import traceback
import requests
from bs4 import BeautifulSoup
from moviepy.editor import VideoFileClip, AudioFileClip

app = Flask(__name__)
app.config["SECRET_KEY"] = "12345"  # Set your secret key


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        session["link"] = request.form.get("youtube_url")
        session["destination"] = request.form.get("destination_folder")  # Set the destination folder path
        return redirect(url_for("grabbing"))
    return render_template("index.html")


@app.route("/grabbing")
def grabbing():
    try:
        url = YouTube(session["link"])
        video_id = url.video_id
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        # Send a GET request to the video URL and extract the HTML content
        response = requests.get(video_url)
        html_content = response.text

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")

        # Find the element that contains the number of likes
        likes_element = soup.find("yt-formatted-string", class_="ytd-toggle-button-renderer")
        video_likes = likes_element.text.strip() if likes_element else "Unknown"

        # Get video information
        video_title = url.title
        video_thumbnail = url.thumbnail_url if hasattr(url, "thumbnail_url") else None
        video_views = url.views
        session["video_title"] = video_title

        return render_template("grabbing.html", video_title=video_title, video_thumbnail=video_thumbnail,
                               video_views=video_views, video_likes=video_likes, converting=False)
    except Exception as e:
        flash(f"Failed to grab video info: {str(e)}")
        traceback_message = traceback.format_exc()  # Capture traceback information
        return render_template("grabbing.html", grabbing_failed=True)


@app.route("/convert", methods=["GET", "POST"])
def convert():
    try:
        url = YouTube(session["link"])
        # Get the high-quality audio stream
        stream = url.streams.get_audio_only()

        # Download the audio stream
        filename = f"{session['video_title']}.mp3"
        download_path = os.path.join(session["destination"], filename)
        stream.download(output_path=session["destination"], filename=filename)

        # Proceed to the saving route
        return redirect(url_for("saving"))
    except Exception as e:
        flash(f"Failed to convert the media file: {str(e)}")
        traceback_message = traceback.format_exc()  # Capture traceback information
        return redirect(url_for("error", error_message=str(e), traceback_message=traceback_message))

@app.route("/saving")
def saving():
    try:
        source_path = os.path.join(session["destination"], f"{session['video_title']}.mp3")
        destination_folder = session["destination"]
        destination_file = session["video_title"] + ".mp3"

        # Move the processed mp3 file to the user-selected destination folder
        file_number = 1
        while os.path.exists(os.path.join(destination_folder, destination_file)):
            destination_file = f"{session['video_title']} ({file_number}).mp3"
            file_number += 1

        destination_path = os.path.join(destination_folder, destination_file)
        os.rename(source_path, destination_path)

        return redirect(url_for("success"))
    except Exception as e:
        flash(f"Failed to save the processed mp3 file: {str(e)}")
        traceback_message = traceback.format_exc()  # Capture traceback information
        return redirect(url_for("error", error_message=str(e), traceback_message=traceback_message))


@app.route("/download")
def download():
    try:
        url = YouTube(session["link"])
        # Get the high-quality audio stream
        stream = url.streams.get_audio_only()

        # Download the audio stream
        filename = f"{session['video_title']}.mp3"
        download_path = os.path.join(session["destination"], filename)
        stream.download(output_path=session["destination"], filename=filename)

        return redirect(url_for("convert"))
    except Exception as e:
        flash(f"Failed to download the audio stream: {str(e)}")
        traceback_message = traceback.format_exc()  # Capture traceback information
        return redirect(url_for("error", error_message=str(e), traceback_message=traceback_message))


@app.route("/success")
def success():
    destination = session.get("destination")
    return render_template("success.html", destination=destination)


@app.route("/error")
def error():
    error_message = session.get("error_message", "Unknown error occurred.")
    traceback_message = session.get("traceback_message", "No traceback available.")
    return render_template("error.html", error_message=error_message, traceback_message=traceback_message)


if __name__ == "__main__":
    app.run()