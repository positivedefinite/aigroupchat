import openai, os
#$Env:openai='key'
openai.api_key = os.environ["openai"]
instruction = "Keep your answers short and to the point, while following the instructions and being helpful if they are unclear."

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": ""},
        {"role": "user", "content": "Hello?"},
    ]
)
#print(response)
response_text = response.choices[0].message.content
print(response_text)