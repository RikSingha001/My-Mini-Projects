import subprocess
import time

vlc = r"C:\Program Files\VideoLAN\VLC\vlc.exe"
audio = r"C:\Users\loade\Documents\python\code\count108\Om Namah Shivaya.mp3"
count = 108

for i in range(1, count + 1):
    print(f"Playing audio {i}/{count}")
    subprocess.run(
        [vlc, "--intf", "dummy", "--play-and-exit", audio],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(.08)

print("Finished playing audio.")
