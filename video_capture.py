import subprocess
import re
import base64
import imageio
import sys
import requests
import json


class VideoCapture:
    def __init__(self, url, headers) -> None:
        self.cap = None
        self.url = url
        self.headers = headers

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

    def capture_image(self, instruction):
        frame = self.cap.get_next_data()
        imageio.imsave('temp.png', frame)
        with open('temp.png', 'rb') as file:
            encoded_string = base64.b64encode(file.read()).decode('utf-8')
        image_data = [{"data": encoded_string, "id": 12}]
        data = {"prompt": f"USER:[img-12] {instruction} \nASSISTANT:", "n_predict": -1, "image_data": image_data, "stream": True}
        response = requests.post(self.url, headers=self.headers, json=data, stream=True)
        print("core-ai | thinking...")

        with open("output.txt", "a") as write_file:
            write_file.write("\n\n"+"---------------------"+ "\n\n")

        
        for chunk in response.iter_content(chunk_size=3000):
            with open("output.txt", "a") as write_file:
                content = chunk.decode().strip().split('\n\n')[0]
                try:
                    content_split = content.split('data: ')
                    if len(content_split) > 1:
                        content_json = json.loads(content_split[1])
                        write_file.write(content_json["content"])
                        print(content_json["content"], end='', flush=True)
                    write_file.flush()  # Save the file after every chunk
                except json.JSONDecodeError as e:
                    print(f"JSONDecodeError: {e}")
        print("\n\n"+"---------------------"+ "\n\n")