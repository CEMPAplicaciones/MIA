import os

import openai

api_key = ""


def ask_gpt4(prompt, model="gpt-4o", max_tokens=600):
    try:

        client = openai.OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=max_tokens,
            temperature=0.7,
        )

        text = response.choices[0].message.content
        print(text)
    except Exception as e:
        return f"Error: {e}"


def ask_custom_assistant(prompt):
    try:

        client = openai.OpenAI(api_key=api_key)

        # Create a new thread
        my_thread = client.beta.threads.create()

        message = client.beta.threads.messages.create(
            thread_id=my_thread.id, role="user", content=prompt
        )

        run = client.beta.threads.runs.create_and_poll(
            thread_id=my_thread.id,
            assistant_id="asst_ArGR7zPdMtkTN0ShqKR7TCmH",
        )

        while run.status != "completed":
            os.wait(3)

        messages = client.beta.threads.messages.list(thread_id=my_thread.id)

        text = messages.data[0].content[0].text.value
        print("Response: ", text)

    except Exception as e:
        return f"Error: {e}"


# Example usage
if __name__ == "__main__":
    user_prompt = input("Enter your prompt: ")
    output = ask_gpt4(user_prompt)
    # print("GPT-4 Response:")
