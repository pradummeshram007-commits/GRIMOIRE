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

    if result.returncode == 0:
        print("Download complete")
        return True

    print("Download failed")
    return False