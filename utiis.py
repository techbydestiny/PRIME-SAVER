import os
import time
import random
import yt_dlp
from yt_dlp import YoutubeDL
import re

def sanitize_filename(name):
    return re.sub(r'[^\w\-_.]', '', name).replace(" ", "")

def download_video(link):
    if 'https://' in link:
        try:
            # Setup output template
            output_path = os.path.join("downloads", "%(title)s.%(ext)s")
            ydl_opts = {
                'outtmpl': output_path.strip(),
                'quiet': True,
                'noplaylist': True,
                'format': 'best[ext=mp4]/best',  # force mp4
            }

            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(link, download=True)
                filename = ydl.prepare_filename(info)

                new_filename = filename.replace(" ", "")
                if new_filename != filename:
                    os.rename(filename, new_filename)
                else:
                    new_filename = filename
            
            return new_filename # return full path to file

        except Exception as e:
            print (f"❌ Error occurred: {e}")
            return None
    else:
        print (f"❌ Error Please Provide a link")
        return (f"❌ Error please provide a link")


def download_audio(link):
    if 'https://' in link:
        try:
            output_dir = "downloads/audios"
            output_path = os.path.join("downloads/audios", "%(title)s.%(ext)s")

            ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': output_path.strip(),
                    'quiet': True,
                    'noplaylist': True,
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(link, download=True)

                title = info.get("title", "audio")
                filename = f"{title}.mp3"
                full_path = os.path.join(output_dir, filename)

                # Sanitize filename to avoid emoji/special character errors
                clean_filename = sanitize_filename(title) + ".mp3"
                clean_path = os.path.join(output_dir, clean_filename)

                # Rename if needed
                if full_path != clean_path and os.path.exists(full_path):
                    os.rename(full_path, clean_path)
                    return clean_path
                elif os.path.exists(clean_path):
                    return clean_path
                elif os.path.exists(full_path):
                    return full_path
                else:
                    print(f"❌ MP3 file not found.")
                    return None

        except Exception as e:
            print (f"❌ Error occurred: {e}")
            return (f"❌ Error occurred: {e}")
                
    else:
        print (f"❌ Error Please Provide a link")
        return (f"❌ Error please provide a link")