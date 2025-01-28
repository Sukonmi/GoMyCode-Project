from huggingface_hub import InferenceClient
from extraction import extract_text_from_pdf
import streamlit as st  

client = InferenceClient(api_key=st.secrets["API_KEY"])

pdf_path = 'Uploaded_Resumes\\android-developer-1559034496.pdf'

extracted_text = extract_text_from_pdf(pdf_path)


def resume_parser(extracted_text):
    messages = [
    {
        "role": "system",
        "content": "You are a resume parser. You're to key information from resumes. like name, skills, objectives, email etc. if a part is missing put missing information"
    },
	{
		"role": "user",
		"content": extracted_text
	}
]
    print("--parsing resume--")
    stream = client.chat.completions.create(
    model="microsoft/Phi-3-mini-4k-instruct", 
	messages=messages)

    return stream.choices[0].message.content
    	
print(resume_parser(extracted_text))