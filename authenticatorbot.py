import openai
import panel as pn  # GUI
import os
from langchain.agents import load_tools, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.agents import tool
import db_con

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", openai_api_key=os.getenv('OPEN_AI_KEY'))

tools = load_tools(["llm-math"], llm=llm)
pn.extension()

openai.api_key = os.getenv('OPEN_AI_KEY')
context = [{'role': 'system', 'content': """
You are AuthenticatorBot, an automated service to authenticate users. \
You first greet the customer \
then you ask for username \
and then you ask for password \
"""}]  # accumulate messages


def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,  # this is the degree of randomness of the model's output
    )

    return response.choices[0].message["content"]


def get_user(u):
    return db_con.get_user_by_username(u)


@tool
def time(text: str) -> str:
    """Returns the result of the authentication function, use this for any \
    questions related to authentication. \
    The input should be a string representing username, \
    and this function will call the get_user function and return its result \
    do not use the Calculator tool \
    date - any date mathmatics should occur \
    outside this function."""

    return str(get_user(text))


agent = initialize_agent(
    tools + [time],
    llm,
    handle_parsing_errors=True
)

messages = context.copy()
def main(matched):
    username = ""
    while not matched:
        response = get_completion_from_messages(messages, temperature=0)
        print(response)
        username = str(input())
        user_stored_password = agent.run(username)

        print("Enter your password please ")
        password = str(input())

        if user_stored_password == password:
            matched = bool(True)
            print("Authentication successfully completed")
            break
        else:
            print("Invalid password or username, please try again")


if __name__ == "__main__":
    main(False)