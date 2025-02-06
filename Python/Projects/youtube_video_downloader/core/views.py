import os
import logging
from django.shortcuts import render
from pytube import YouTube
from .forms import YouTubeDownloadForm
from django.http import HttpResponseNotFound, HttpResponseServerError
from pytube.exceptions import PytubeError
from yt_dlp import *



logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def get_download_path():
    """Downloads files at Current Directory."""
    #return os.getcwd()  
    """Downloads files at Downloads Directory"""
    return os.path.join(os.path.expanduser("~"), "Downloads")

def download_video(request):
    message = ""
    download_path = get_download_path()  
    ydl_opts = {}
    if request.method == "POST":
        form = YouTubeDownloadForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data["url"]
            logger.debug(f"Received URL for download: {url}")

            try:
                ydl_opts = {
                    'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
                }
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                logger.info(f"Download completed successfully for: {url}")
                message = f"Download Complete: {url}\n📂 Saved to {download_path}"
            except Exception as e:
                logger.error(f"Error occurred during download: {str(e)}")
                message = f"Error: {str(e)}"
    else:
        form = YouTubeDownloadForm()

    return render(request, "downloader/index.html", {"form": form, "message": message})

def custom_404_view(request, exception):
    logger.warning("404 error: Page not found")
    return HttpResponseNotFound("<h1>404 - Page Not Found</h1>")

def custom_500_view(request):
    logger.error("500 error: Internal Server Error")
    return HttpResponseServerError("<h1>500 - Internal Server Error</h1>")
