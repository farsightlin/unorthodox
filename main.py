import json
import os
from gptresponse import chat_with_gpt
from memory import simplify_prompt
import requests
import gen_pic
from io import BytesIO
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import scrolledtext
import pygame  # 引入pygame模块来播放音乐
import random

pygame.mixer.init()  # 初始化pygame mixer

##自定义选项
##选择使用哪个语言
localize = "context.json"
with open(localize, "r", encoding="utf-8") as file:
    context = json.load(file)
##选择是否采用压缩算法增加可容纳上下文数量（非英文勿选）
compression_option = 1
##是否使用自定义故事调料
background_emphasize = 1
##是否放BGM
play_bgm = 0

pic_generate = 1
music_folder = "./music/"  # 存放音乐文件的文件夹


def play_music():
    if play_bgm == 1:
        files = [f for f in os.listdir(music_folder) if f.endswith('.mp3')]  # 获取所有.mp3文件
        current_song = os.path.join(music_folder, random.choice(files))  # 随机选择一个播放
        pygame.mixer.music.load(current_song)
        pygame.mixer.music.play(-1)  # 循环播放
    


def main():
    game_prompt = context['DM_roleplay']
    conversation_history = ""
    if background_emphasize == 1:
        conversation_history = context['backgroundd_emphasize']

    def submit():
        nonlocal conversation_history
        user_input = user_entry.get()
        user_entry.delete(0, tk.END)

        # Added a newline for player input
        conversation_history += f"{context['pl_name']}:{user_input}\n\n"

        # Insert user input
        response_box.insert(tk.END, "You: ", 'player_bold')  # Insert "You: " with bold
        response_box.insert(tk.END, f"{user_input}\n\n", 'player')  # Insert user input without bold

        prompt = f"{game_prompt}\n{conversation_history}"
        response = chat_with_gpt(prompt)

        if pic_generate == 1:
            option_index = response.find("Here are some op")
            input_response = ""
            if option_index != -1:
                input_response = response[:option_index]
            picture_prompt = context['general_picture_prompt'] + input_response
            pic_prompt = "pixel art" + chat_with_gpt(picture_prompt)
            image_url = gen_pic.generate_image(pic_prompt)

            img_response = requests.get(image_url)
            img = Image.open(BytesIO(img_response.content))
            img_tk = ImageTk.PhotoImage(img)
            img_label.configure(image=img_tk)
            img_label.image = img_tk

        conversation_history += f"{response}\n\n"

        # Insert DM response
        response_box.insert(tk.END, "DM: ", 'dm_bold')  # Insert "DM: " with bold
        response_box.insert(tk.END, f"{response}\n\n", 'dm')  # Insert DM response without bold
        response_box.see(tk.END)

    window = tk.Tk()
    window.title("Unorthodox: AK's story teller")

    user_entry = tk.Entry(window)
    user_entry.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)  # 添加了padding

    submit_button = tk.Button(window, text="Submit", command=submit)
    submit_button.grid(row=0, column=1, sticky="nsew")

    response_box = scrolledtext.ScrolledText(window)
    response_box.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)  # 添加了padding

    # Configuring tag colors and fonts for 'dm', 'player', 'dm_bold', 'player_bold'
    response_box.tag_config('dm', foreground='dark red', font=("Comic Sans MS", 10))  # 使所有DM的对话都使用"Comic Sans MS"
    response_box.tag_config('player', foreground='green', font=("Comic Sans MS", 10))  # 使所有Player的对话都使用"Comic Sans MS"
    response_box.tag_config('dm_bold', foreground='dark red', font=("Comic Sans MS", 10, "bold"))  # 使"DM: "加粗
    response_box.tag_config('player_bold', foreground='green', font=("Comic Sans MS", 10, "bold"))  # 使"You: "加粗


    img_label = tk.Label(window)
    img_label.grid(row=0, column=2, rowspan=2, sticky="nsew", padx=10, pady=10)  # 添加了padding

    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=0)
    window.grid_columnconfigure(2, weight=0)
    window.grid_rowconfigure(0, weight=0)
    window.grid_rowconfigure(1, weight=1)

    # Insert opening DM message
    response_box.insert(tk.END, "DM: ", 'dm_bold')  # Insert "DM: " with bold
    response_box.insert(tk.END, f"{context['openings']}\n\n", 'dm')  # Insert DM message without bold

    play_music()  # 开始播放音乐

    window.mainloop()


if __name__ == "__main__":
    main()
