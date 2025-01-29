import streamlit as st
from PyPDF2 import PdfReader
import io
from openai import OpenAI
from streamviz import gauge
from PIL import Image

# OpenAI client setup
openAIClient = OpenAI(
    api_key=st.secrets["API_KEY"]
)

tech_jobs = {
     "Data Scientist": {
        "Description": "Analyzes and interprets complex data to provide actionable insights. Builds machine learning models and data pipelines to solve business problems.",
        "Skills": ["Python/R", "Machine Learning", "Data Analysis", "SQL", "Visualization (Tableau, Matplotlib)"],
    },
    "Software Engineer": {
        "Description": "Designs, develops, tests, and maintains software applications. Collaborates with cross-functional teams to deliver high-quality, scalable solutions.",
        "Skills": ["Programming (Python, Java, C++)", "Problem-solving", "Version control (Git)", "Debugging"],
    },
   
    "Cloud Engineer": {
        "Description": "Designs, implements, and manages cloud infrastructure to ensure high availability, scalability, and security of applications and data.",
        "Skills": ["AWS/Azure/GCP", "Networking", "DevOps tools (Docker, Kubernetes)", "Infrastructure as Code (Terraform)"],
    },
    "Cybersecurity Analyst": {
        "Description": "Monitors and protects an organization's systems and data from security threats. Conducts vulnerability assessments and implements security measures.",
        "Skills": ["Network Security", "Threat Analysis", "Incident Response", "SIEM Tools", "Ethical Hacking"],
    },
    "Product Manager": {
        "Description": "Leads product development by defining requirements, prioritizing features, and collaborating with engineering and design teams to deliver value to users.",
        "Skills": ["Project Management", "Communication", "Market Research", "Agile Methodologies", "Roadmap Planning"],
    },
}




def extract_text_from_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

# Resume Parser function
def resumeParser(resume_content, selected_job):
    messages = [
        {
            "role": "system",
            "content": """You're a resume parser bot. You're to extract key information like
            email, phone number, skills, LinkedIn URL from the resume content given to you.
            Also given the job title, descriptions and skills, you are to compare it with the user's resume and return a match score of the
            user's strength to the job.
            Output your answer in dictionary format like this:
            {
                "Name": "User's name from resume",
                "Professional Summary": "Summary from resume",
                "Experience": ["Data Science Instructor at XYC company, Machine Learning intern at XYC Company],
                "Skills: ["Python", "SQL"],
                "Linkedin Url": "user's linkedin url",
                "Email": "User's email",
                "Match Score": "Return the score here indicating how fit the user is to the role. E.g 0.80"
            }
            """
        },
        {
            "role": "user",
            "content": f" User's resume:{resume_content}, Job: {selected_job}"
        }
    ]

    try:
        response = openAIClient.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Something went wrong. Could not get model response: {e}")
        return None


# Streamlit App
image = Image.open("Image.png")
st.image(image, width=400)
st.markdown("### Welcome to **:blue[ResumeSense]!** :wave:")
st.markdown("Upload a resume and select a job title to parse the resume and compare it with the selected job role.")
st.markdown("You can also ask questions about the resume to get more insights about the user's profile.")

# Sidebar
st.sidebar.title("About ResumeSense")
st.sidebar.info(
    """
    **ResumeSense** is an AI-powered resume parser and job matching tool. 
    Upload your resume, select a job title, and get insights on how well your profile matches the selected job role.
    """
)

st.sidebar.subheader("Tips")
if st.sidebar.button("How it works"):
    st.sidebar.markdown(
        """
        1. Upload your resume in PDF format.
        2. Select the job title you are interested in.
        3. Click on "Parse Resume" to analyze your resume.
        4. View the extracted information and match score.
        5. Ask specific questions about your resume in the chat section.
        """
    )

st.sidebar.subheader("Styling and Theme")
theme = st.sidebar.selectbox("Choose Theme", ["Light", "Dark"])
if theme == "Dark":
    st.markdown(
        """
        <style>
        .main {
            background-color: #333;
            color: #fff;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

st.sidebar.subheader("Contact Info")
st.sidebar.markdown(
    """
    **Email:** danielayomideh@gmail.com  
    **Phone:** +234 706 715 9089
    """
)

st.sidebar.subheader("Useful Links")
st.sidebar.markdown(
    """
    - [GitHub](https://github.com/yourprofile)
    - [LinkedIn](https://www.linkedin.com/in/yourprofile)
    """
)

st.sidebar.subheader("Feedback")
feedback = st.sidebar.text_area("We value your feedback!")
if st.sidebar.button("Submit Feedback"):
    st.sidebar.success("Thank you for your feedback!")

col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("Upload a resume", type="pdf")
    parse_button = st.button("Parse Resume")
    st.markdown("#")

with col2:
    job_role = st.selectbox("Select Job Title", list(tech_jobs.keys()))

    st.write(f"""
                :blue[Description]: {tech_jobs[job_role]["Description"]}\n
                :blue[Required Skills]: {", ".join(tech_jobs[job_role]["Skills"])}
                """)

# Store chat history and extracted text in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "extracted_text" not in st.session_state:
    st.session_state.extracted_text = None



if uploaded_file is not None and parse_button:
    pdf_file = io.BytesIO(uploaded_file.read())
    resume_texts = extract_text_from_pdf(pdf_file)
    with st.spinner('Parsing resume...'):
        extracted_text = resumeParser(resume_texts, tech_jobs[job_role])
        st.session_state.extracted_text = extracted_text
            
    

elif parse_button and uploaded_file is None:
    st.warning("Please upload a resume to parse")


# Display user info
if st.session_state.extracted_text:
         # Store extracted text in session state
        extracted_dict = eval(st.session_state.extracted_text)

        col3, col4 = st.columns([2,1])

        with col3:
            # Display stored extracted text if available
            st.subheader(" User Information")
            "---"
            st.markdown(f"""
                        **:orange[Applicant Name]:** {extracted_dict.get('Name', 'N/A')}\n
                        **:orange[Professional Summary]:** {extracted_dict.get("Professional Summary", 'N/A')}\n
                        **:orange[Experience]:**
                        """)
            for experience in extracted_dict.get("Experience", []):
                st.markdown(f"- {experience}")
            st.markdown(f"""
                        **:orange[Skills]**: {", ".join(extracted_dict.get("Skills", []))}\n
                        **:orange[Email]:** {extracted_dict.get('Email', 'N/A')}\n
                        **:orange[LinkedIn URL]:** {extracted_dict.get("Linkedin Url", 'N/A')}\n
                        """)
        
        with col4:
            st.subheader("Applicant's Fit with the Selected Job Role")
            gauge(
                float(extracted_dict["Match Score"]),
                gTitle="Job Match Score",
                gTheme="White",
                gSize="MED",
                sFix="%",
                gcHigh="#00FF00",  # Green
                gcMid="#FFFF00",   # Yellow
                gcLow="#FF0000"    # Red
            )


# Chat feature
st.subheader("Ask Questions About the Resume")

# Display chat messages from history on app rerun
for message in st.session_state.chat_history:
    if message["role"] == "system":
        continue
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

    
# Accept user input
if prompt := st.chat_input("Have specific questions about the user's resume?"):
 
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": prompt})

      # Display assistant response in chat message container
    with st.chat_message("assistant"):
        
        try:
             
             # Add system instructions to maintain context
            st.session_state.chat_history.insert(0, {
                "role": "system",
                "content": f"You are an HR assistant bot. Answer questions based on the parsed resume data provided here {st.session_state.extracted_text}."
                })

             
            stream = openAIClient.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
               
                {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.chat_history
                ],
                stream=True,
                
            )
            response = st.write_stream(stream)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
        except Exception as e:
            st.session_state.chat_history.append({"role": "assistant", "content": f"Something went wrong. {e}"})