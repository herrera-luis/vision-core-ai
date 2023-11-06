import sys
import requests
import json
import re

import imageio
import pyaudio
import wave
import threading
from pynput import keyboard
import whisper
import pyautogui
import time
import warnings
from video_capture import VideoCapture

# Suppress specific warnings from the Whisper library
warnings.filterwarnings('ignore', message='FP16 is not supported on CPU; using FP32 instead')
initial_chat_prompt = "This is a conversation between USER and ASSISTANT, a friendly chatbot. ASSISTANT is helpful, kind, honest, good at writing, and never fails to answer any requests immediately and with precision"
url = "http://localhost:8080/completion"
headers = {"Content-Type": "application/json"}
print("Starting vision-core-ai...")

class AudioRecorder:
    def __init__(self, chunk=1024, sample_format=pyaudio.paInt16, channels=1, fs=44100, filename="output.wav", device_index=None):
        self.chunk = chunk
        self.sample_format = sample_format
        self.channels = channels
        self.fs = fs
        self.filename = filename
        self.frames = []
        self.recording = False
        self.model = whisper.load_model("small")
        self.p = pyaudio.PyAudio()
        self.device_index = device_index  # Store the device index
        self.key_pressed = ""
        self.video_capture = None

    def list_devices(self):
        info = self.p.get_host_api_info_by_index(0)
        num_devices = info.get('deviceCount')
        for i in range(0, num_devices):
            if (self.p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                print("Input Device id ", i, " - ", self.p.get_device_info_by_host_api_device_index(0, i).get('name'))


    def toggle_recording(self):
        self.recording = not self.recording
        if self.recording:
            print('\nRecording....')
            self.frames = []  # Clear previous recording frames
            threading.Thread(target=self.record).start()
        else:
            print('\nStopped recording')


    def record(self):
        stream = self.p.open(
            format=self.sample_format,
            channels=self.channels,
            rate=self.fs,
            frames_per_buffer=self.chunk,
            input=True,
            input_device_index=self.device_index  # Use the selected device index
        )
        while self.recording:
            data = stream.read(self.chunk)
            self.frames.append(data)
        stream.stop_stream()
        stream.close()
        self.save_audio()

    def transcribe_recording(self):
        result = self.model.transcribe(self.filename)
        return result["text"]

    def save_audio(self):
        with wave.open(self.filename, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.p.get_sample_size(self.sample_format))
            wf.setframerate(self.fs)
            wf.writeframes(b''.join(self.frames))
        recording_text = self.transcribe_recording()
        pyautogui.write(f'\nUser >{recording_text}\n')
        if self.key_pressed == "'i'":
            self.video_capture.capture_image(recording_text)
        else:
            self.call_llm(recording_text)
        self.key_pressed = ""

    def set_hotkey(self):

        def on_press(key):
            if key == keyboard.KeyCode.from_char('i') or key == keyboard.KeyCode.from_char('c'):
                self.key_pressed = str(key)
                self.toggle_recording()

        self.current_keys = set()

        listener = keyboard.Listener(
            on_press=on_press)
        listener.start()


    def call_llm(self, query):
        data = {"prompt": f"{initial_chat_prompt}\n\nUSER:{query} \nASSISTANT:", "n_predict": -1, "cache_prompt": True, "stream": True,
                "stop": [
                            "</s>",
                            "ASSISTANT:",
                            "USER:"
                        ],
                }

        response = requests.post(url, headers=headers, json=data, stream=True)

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

def main():

    ########## Video menu ##########
    video = VideoCapture(url, headers)
    devices = video.get_video_devices()
    if not devices:
        print("No video devices found.")
        sys.exit(1)
    
    index = video.select_video_device(devices)
    print(f">You selected: {devices[index]}")
    video.cap = imageio.get_reader(f"<video{index}>")
    #################################


    ########## Audio menu ##########
    print("\n*******************************\n")
    recorder = AudioRecorder()
    print("Available audio devices:\n")
    recorder.list_devices()
    chosen_device_index = int(input("Enter the audio device index: "))
    print(f">You selected: {recorder.p.get_device_info_by_host_api_device_index(0, chosen_device_index).get('name')}\n\n")
    recorder.device_index = chosen_device_index
    #################################

    recorder.set_hotkey()
    recorder.video_capture = video
    print('Press Ctrl-C to quit')

    print("\nvision-core-ai listening...")

    while True:
        time.sleep(2)
        

if __name__ == "__main__":
    main()
