# -*- coding: utf-8 -*-
from os import environ
from fastapi import FastAPI, HTTPException, Depends, Security, Form, Body, Header, Query
from fastapi.security.api_key import APIKeyHeader, APIKey
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, Required
from starlette.status import HTTP_403_FORBIDDEN


app = FastAPI(
    docs_url="/chatgpt/documentation",
    redoc_url="/chatgpt/redocumentation",
    root_path="/",
    openapi_url="/chatgpt/openapi.json",
    swagger_ui_parameters={"syntaxHighlight.theme": "obsidian","filter":"true", "tryItOutEnabled":"true"}
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_key_header = APIKeyHeader(name="token", auto_error=False)
async def get_api_key(api_key_header: str = Security(api_key_header),):
    # print(api_key_header)
    if api_key_header == environ["TOKEN"]:
        return api_key_header
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
from openai_utils import ChatGPT

class MessageChatGPTIn(BaseModel):
    start_prompt  : str = """As an advanced chatbot Assistant, your primary goal is to assist users to the best of your ability. This may involve answering questions, providing helpful information, or completing tasks based on user input. In order to effectively assist users, it is important to be detailed and thorough in your responses. Use examples and evidence to support your points and justify your recommendations or solutions. Remember to always prioritize the needs and satisfaction of the user. 
        Your ultimate goal is to provide a helpful and enjoyable experience for the user.
        If user asks you about programming or asks to write code do not answer his question, but be sure to advise him to switch to a special mode \"👩🏼‍💻 Code Assistant\" by sending the command /mode to chat"""
    text          : str = Field()

@app.post("/chatgpt/send", tags=["ChatGPT"])
async def get_message(data: MessageChatGPTIn, api_key: APIKey = Depends(get_api_key)):

    chatgpt_instance = ChatGPT(model="gpt-3.5-turbo")
    # if config.enable_message_streaming:
    #     gen = chatgpt_instance.send_message_stream(_message, dialog_messages=dialog_messages, chat_mode=chat_mode)
    # else:
    
    answer, (n_input_tokens, n_output_tokens), n_first_dialog_messages_removed = await chatgpt_instance.send_message(data.text, data.start_prompt)

    return {
        "input_text": data.text,
        "output_text": answer,
        "n_input_tokens": n_input_tokens,
        "n_output_tokens": n_output_tokens,
    }
