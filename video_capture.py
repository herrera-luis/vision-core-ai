import subprocess
import re
import sys
import imageio
import base64

class VideoCapture:
    def __init__(self) -> None:
        self.capture = None


    def get_video_devices(self):
        command = ["ffmpeg", "-f", "avfoundation", "-list_devices", "true", "-i", ""]
        result = subprocess.run(command, stderr=subprocess.PIPE, text=True)
        output = result.stderr
        devices = re.findall(r"\[AVFoundation indev @ .*\]\s\[\d+\]\s(.+)", output)
        # Filter out non-video devices if necessary
        video_devices = [device for device in devices if not device.startswith('Capture screen')]
        
        return video_devices

    # Function to select a video device
    def select_video_device(self,devices):
        print("Available video devices:")
        for i, device in enumerate(devices):
            print(f"{i}: {device}")
        index = int(input("Select the index of the video device: "))
        if 0 <= index < len(devices):
            return index
        else:
            print("Invalid index selected.")
            sys.exit(1)


    def get_encoded_image(self):
        frame = self.capture.get_next_data()
        imageio.imsave('temp.png', frame)
        with open('temp.png', 'rb') as file:
            encoded_string = base64.b64encode(file.read()).decode('utf-8')
        return encoded_string