from g4f.client import Client
client = Client()
response = client.chat.completions.create(
    model="llama-3.1-70b",
    provider="DDG",
    messages=[{"role": "user", "content": "Hello"}],
    # Add any other necessary parameters
)
print(response.choices[0].message.content) #commentariy that commite!