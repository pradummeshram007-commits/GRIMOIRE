import yt_dlp

url = "https://www.instagram.com/reel/DYPFRgoTeC3/?igsh=bGF6Mms3MGFjdDNi"

ydl_opts = {
    'outtmpl': 'downloads/%(id)s.%(ext)s'
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

print("Download complete")





