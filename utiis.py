import os
import time
import random
from yt_dlp import YoutubeDL


def Operator(link):
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
        

