import openai
import panel as pn  # GUI
import os
pn.extension()


openai.api_key  = os.getenv('OPEN_AI_KEY')
context = [ {'role':'system', 'content':"""
You are StockBot, an automated service to provide information about stocks. \
You first greet the customer, then answers to they questions, \
"""} ]  # accumulate messages


def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )

    return response.choices[0].message["content"]


messages =  context.copy()

prompt = ""
while(prompt != "0"):
    response = get_completion_from_messages(messages, temperature=0)
    print(response)
    prompt = str(input())
    messages.append({'role': 'user', 'content': prompt})

