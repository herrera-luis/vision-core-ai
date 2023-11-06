import sys
import imageio
import time
import warnings
from video_capture import VideoCapture
from core import Core
from llm import Llm

# Suppress specific warnings from the Whisper library
warnings.filterwarnings('ignore', message='FP16 is not supported on CPU; using FP32 instead')
initial_chat_prompt = "This is a conversation between USER and ASSISTANT, a friendly chatbot. ASSISTANT is helpful, kind, honest, good at writing, and never fails to answer any requests immediately and with precision"
url = "http://localhost:8080/completion"
headers = {"Content-Type": "application/json"}
print("Starting vision-core-ai...")


def main():
    ########## Video menu ##########
    video = VideoCapture(url, headers)
    devices = video.get_video_devices()
    if not devices:
        print("No video devices found.")
        sys.exit(1)
    
    index = video.select_video_device(devices)
    print(f">You selected: {devices[index]}")
    video_capture = imageio.get_reader(f"<video{index}>")
    #################################


    ########## Audio menu ##########
    print("\n*******************************\n")
    recorder = Core(url=url, headers=headers, initial_chat_prompt=initial_chat_prompt)
    print("Available audio devices:\n")
    recorder.list_devices()
    chosen_device_index = int(input("Enter the audio device index: "))
    print(f">You selected: {recorder.p.get_device_info_by_host_api_device_index(0, chosen_device_index).get('name')}\n\n")
    recorder.device_index = chosen_device_index
    #################################

    ########## LLM setup ##############
    llm = Llm(video_capture, url, headers, initial_chat_prompt)
    ###################################

    recorder.set_hotkey()
    recorder.llm = llm
    print('Press Ctrl-C to quit')

    print("\nvision-core-ai listening...")

    while True:
        time.sleep(2)
        

if __name__ == "__main__":
    main()
