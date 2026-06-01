import subprocess

def download_reel(url):

    command = [
        "python",
        "-m",
        "yt_dlp",
        "-o",
        "downloads/%(id)s.%(ext)s",
        url
    ]

    result = subprocess.run(command)

    print("Download complete")


