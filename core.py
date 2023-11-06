import pyaudio
import wave
import threading
from pynput import keyboard
import whisper
import pyautogui


class Core:
    def __init__(self, chunk=1024, sample_format=pyaudio.paInt16, channels=1, fs=44100, filename="output.wav", device_index=0):
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
        self.llm = None

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
            self.llm.call_image(recording_text)
        else:
            self.llm.call_chat(recording_text)
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