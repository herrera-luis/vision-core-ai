import requests
import json
import base64
import imageio
import requests
import json


class Llm:
    def __init__(self, video_capture=None, url="", headers="", initial_chat_prompt=""):
        self.video_capture=video_capture
        self.url = url
        self.headers = headers
        self.initial_chat_prompt = initial_chat_prompt

    def call_chat(self, query):
        data = {"prompt": f"{self.initial_chat_prompt}\n\nUSER:{query} \nASSISTANT:", "n_predict": -1, "cache_prompt": True, "stream": True,
                "stop": [
                            "</s>",
                            "ASSISTANT:",
                            "USER:"
                        ],
                }
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
        print("\n\n"+"---------------------"+ "\n")


    def call_image(self, query):
        frame = self.video_capture.get_next_data()
        imageio.imsave('temp.png', frame)
        with open('temp.png', 'rb') as file:
            encoded_string = base64.b64encode(file.read()).decode('utf-8')
        image_data = [{"data": encoded_string, "id": 12}]
        data = {"prompt": f"USER:[img-12] {query} \nASSISTANT:", "n_predict": -1, "image_data": image_data, "stream": True}
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
        print("\n\n"+"---------------------"+ "\n")