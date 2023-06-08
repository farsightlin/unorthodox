import openai
import secret
import time

openai.api_key = secret.chatgpt_api

def chat_with_gpt(prompt):
    messages = [{"role": "system", "content": "You are the Dungeon Master of a Dungeons & Dragons-like game."},
                {"role": "user", "content": prompt}]
    
    while True:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
            )
            break  # if the request is successful, we break the loop
        except:
            time.sleep(3)  # wait for 3 seconds before trying again

    message = response.choices[0].message['content']
    return message
