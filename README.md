# Vision Core AI

Demo python script app to interact with llama.cpp server using whisper API, microphone and webcam devices.

## Step 1: Install Llama C++ and package dependencies on your machine

Clone the Llama C++ repository from GitHub:
```bash
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
```
### On macOS:
 Build with make:
```
make
```
 Or, if you prefer cmake:
```
cmake --build . --config Release
```

### macOS requirements
you need to install these dependencies in your computer: ffmpeg and portaudio

```bash

brew install ffmpeg portaudio

```

Also be sure to provide permissions to the terminal in the Security & Privacy > Privacy options

## Step 2: Download the Model!
1.  Download from Hugging Face - [mys/ggml_bakllava-1](https://huggingface.co/mys/ggml_bakllava-1/tree/main) this 2 files:
* ggml-model-q4_k.gguf (or any other quantized model) - only one is required!
* mmproj-model-f16.gguf

2. Copy the paths of those 2 files.
3. Run this in the llama.cpp repository (replace YOUR_PATH with the paths to the files you downloaded):

    #### macOS
    ```
    ./server -m YOUR_PATH/ggml-model-q4_k.gguf --mmproj YOUR_PATH/mmproj-model-f16.gguf -ngl 1
    ```
    #### Windows
    ```
    server.exe -m REPLACE_WITH_YOUR_PATH\ggml-model-q4_k.gguf --mmproj REPLACE_WITH_YOUR_PATH\mmproj-model-f16.gguf -ngl 1

    ```
4.  The llama server is now up and running!
    
    ⚠️ NOTE: Keep the server running in the background.
5.  Let's run the script to use the webcam and microphone

## Step 3: Running the Demo
Open a new terminal window and clone the demo app:
```
git clone https://github.com/herrera-luis/vision-core-ai.git
cd vision-core-ai
```

### Install python dependencies

```bash

pip install -r requirements.txt
```

### Run the main script

```bash
python main.py
```

## How to interact with the app

When the application is running you need to press the keys `i` or `c` to enable the recording and a second time the same key to stop it

* `i` will use your webcam
* `c` will use chat

## Related project:

* [realtime-bakllava](https://github.com/Fuzzy-Search/realtime-bakllava)
* [llama.cpp](https://github.com/ggerganov/llama.cpp)
