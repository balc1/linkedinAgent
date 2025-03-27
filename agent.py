import streamlit as st
from groq import Groq
import getpass
import os



# Kullanıcının API anahtarını girmesi için giriş alanı
api_key = st.text_input("Enter your Groq API Key:", type="password")

# API anahtarını doğrula ve kaydet
if api_key:
    os.environ["GROQ_API_KEY"] = api_key
    st.success("API Key set successfully! You can now generate posts.")
else:
    st.warning("Please enter a valid API Key.")

# API anahtarı olmadan devam edemez
if not api_key:
    st.stop()


SYSTEM_PROMPT = "You are an AI assistant specialized in generating engaging, professional LinkedIn posts related to Data Science, AI, and Open Source technologies. Your goal is to create concise, informative, and engaging LinkedIn posts that provide value to professionals in the field.\n\nInstructions:\n\nWrite posts in an informative yet casual tone, similar to how tech professionals share insights on LinkedIn.\n\nEnsure posts are concise (between 150-300 words).\n\nUse bullet points for listing key features or steps.\n\nEnd posts with a call to action, encouraging engagement (e.g., asking a question or inviting discussion).\n\nInclude relevant hashtags at the end.\n\nThe post should be clear and readable for both beginners and experienced professionals.\n\nExample Post Structure:\n\nHook: Start with a compelling statement or question to grab attention.\n\nMain Content: Explain the topic concisely, highlighting key insights, benefits, or steps.\n\nCall to Action: Encourage interaction by asking a question or inviting discussion.\n\nHashtags: Include 5-7 relevant hashtags.\n\nExample Input:\n\"Write a LinkedIn post about using Ollama for running open-source LLMs without an API key. Mention supported models, ease of installation, and key benefits.\"\n\nExample Output:\n\nWant to build projects with Large Language Models (LLMs) but don’t want to deal with API keys?\n\nMeet Ollama – an open-source library that lets you run LLMs directly on your hardware. No cloud dependencies, no API fees!\n\n🌟 Why use Ollama?\n✅ Run open-source models locally.\n✅ Supports tool-usage & structured outputs for building AI agents.\n✅ Works without an API key or paid subscription.\n\n🚀 Getting started is super easy:\n\nbash\nKopyala\nDüzenle\npip install ollama  \nollama run deepseek-r1  \nSome supported models:\n\nGemma-3\n\nDeepSeek-v1\n\nLLaMA-3.3\n\nQwen\n\n⚠️ Keep in mind: Larger models require more powerful hardware for production use.\n\nWant to learn more? Check it out here 👉 https://ollama.com/\n\nLet’s connect! If you’re into Data Science & Generative AI, feel free to drop a message.\n\n#DataScience #GenerativeAI #OpenSource #AI #LLM #MachineLearning\n\n Postları benim anlamam için hem ingilizce hem türkçe olarak üretir misin?"

def generate_linkedin_post(USER_INPUT):
    client = Groq()
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": USER_INPUT
            },
        ],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )
    content = ""
    for chunk in completion:
        print(chunk.choices[0].delta.content or "", end="")
        content += chunk.choices[0].delta.content or ""
    
    return content
      

# Streamlit Arayüzü
st.title("LinkedIn Post Generator")
st.write("Enter a topic to generate a LinkedIn post.")

# Kullanıcıdan Girdi Al
USER_INPUT = st.text_input("Enter Topic:", "")

# Butona Basınca Post Oluştur
if st.button("Generate Post"):
    if USER_INPUT:
        post = generate_linkedin_post(USER_INPUT)
        st.subheader("Generated LinkedIn Post:")
        st.write(post)
    else:
        st.warning("Please enter a topic!")


