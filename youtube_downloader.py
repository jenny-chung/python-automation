from pytube import YouTube
from pytube.exceptions import VideoUnavailable
from sys import argv

# Get YouTube link from command line input
link = argv[1]

# Specify file path for downloads
path = '/Users/jennychung/Downloads/Youtube Downloads'

# Download YouTube video
try:
    yt = YouTube(f'"{link}"')

    print("Title: ", yt.title)
    print("Views: ", yt.views)
except VideoUnavailable:
    print(f'Video {link} is unavailable. Please try with another link.')
else:
    print(f'Downloading video: {link}')
    yd = yt.streams.get_highest_resolution()
    yd.download(path)
