from django.shortcuts import render
import os 
import logging
from yt_dlp import * 
from django.http import HttpResponseNotFound, HttpResponseServerError


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("debug.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
logger.addHandler(file_handler)


def get_download_file():
    return os.path.join(os.path.expanduser("~"), "Downloads")

def download_video():
    message = ""
    download_path = get_download_file()
    ydl_opts = {}
    if request.method == "POST":


