from yt_dlp import YoutubeDL

def Download(link):
    ydl_opts = {}
    with YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([link])
        except Exception as e:
            print(f"An error has occurred: {e}")
        else:
            print("Download is completed successfully")

link = input("Enter the YouTube video URL: ")
Download(link)