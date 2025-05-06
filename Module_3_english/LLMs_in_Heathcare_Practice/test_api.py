import openai
import os
import pandas as pd
from io import StringIO

api_key = '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'

#content = "You are a helpful assistant"
def ask_custom_assistant(prompt):
    try:

        client = openai.OpenAI(api_key=api_key)

        # Create a new thread
        my_thread = client.beta.threads.create()

        message = client.beta.threads.messages.create(
                thread_id=my_thread.id,
                role="user",
                content=prompt
                )

        run = client.beta.threads.runs.create_and_poll(
                thread_id=my_thread.id,
                assistant_id='asst_9FLNf7n2aTJJ7tHr0OG14rzb',
                )

        while run.status != 'completed':
            os.wait(3)

        messages = client.beta.threads.messages.list(
                thread_id=my_thread.id
                )

        text = messages.data[0].content[0].text.value
        return text


    except Exception as e:
        return f"Error: {e}"

# Example usage
dir_texts = ('/Users/jsilva/repositories/MIA/Module_3_english/LLMs_in_Heathcare_Practice/final_dataset_v4_to_publish/train/text_files_en')

for file_ in os.listdir(dir_texts)[0:2]:

    file_name = file_
    content = open(os.path.join(dir_texts, file_), 'r').read()
    text = ask_custom_assistant(content)

    print(text)


