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
    video_capture = VideoCapture()
    devices = video_capture.get_video_devices()
    if not devices:
        print("No video devices found.")
        sys.exit(1)
    
    index = video_capture.select_video_device(devices)
    print(f">You selected: {devices[index]}")
    video_capture.capture = imageio.get_reader(f"<video{index}>")
    #################################


    ########## Audio menu ##########
    print("\n*******************************\n")
    core = Core()
    print("Available audio devices:\n")
    core.list_devices()
    chosen_device_index = int(input("Enter the audio device index: "))
    print(f">You selected: {core.p.get_device_info_by_host_api_device_index(0, chosen_device_index).get('name')}\n\n")
    core.device_index = chosen_device_index
    #################################

    ########## LLM setup ##############
    llm = Llm(video_capture, url, headers, initial_chat_prompt)
    ###################################

    core.set_hotkey()
    core.llm = llm
    print('Press Ctrl-C to quit')

    print("\nvision-core-ai listening...")

    while True:
        time.sleep(2)
        

if __name__ == "__main__":
    main()
