import openai
# api_key="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"
import openai
# import json
# import requests
# import streamlit as st



openai.api_key = "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"

def BasicGeneration(userPrompt):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": userPrompt}]
    )
    
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content

prompt = "What is the meaning of life?"
response = BasicGeneration(prompt)
print(response)