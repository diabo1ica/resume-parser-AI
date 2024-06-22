from django.shortcuts import render
from rest_framework.views import APIView
import os, sys
from pypdf import PdfReader 
import json
from openai import OpenAI

# Create your views here.

sys.path.insert(0, os.path.abspath(os.getcwd()))

UPLOAD_PATH = r"__DATA__"

# TODO:
# 1. OpenAI API Key
# 2. Environment variable
# 3. Supabase integration

def index(request):
    return render(request, 'index.html')

class ResumeParser(APIView):
    def post(self, request):
        doc = request.files['pdf_doc']
        # doc.save(os.path.join(UPLOAD_PATH, "file.pdf"))
        # doc_path = os.path.join(UPLOAD_PATH, "file.pdf")
        data = self.read_file_from_path(doc)
        data = self.ats_extractor(data)

        return render('index.html', json.loads(data))
    
    def read_file_from_path(file):
        reader = PdfReader(file) 
        data = ""
        for page_no in range(len(reader.pages)):
            page = reader.pages[page_no] 
            data += page.extract_text()
        return data
    
    def ats_extractor(resume_data):
        prompt = '''
        You are an AI bot designed to act as a professional for parsing resumes. You are given with resume and your job is to extract the following information from the resume:
        1. full name
        2. email id
        3. github portfolio
        4. linkedin id
        5. employment details
        6. technical skills
        7. soft skills
        Give the extracted information in json format only
        '''

        openai_client = OpenAI(
            api_key = ""
        )    

        messages=[
            {
                "role": "system", 
                "content": prompt
            }
        ]
        
        user_content = resume_data
        
        messages.append({"role": "user", "content": user_content})

        response = openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    temperature=0.0,
                    max_tokens=1500)
            
        data = response.choices[0].message.content

        #print(data)
        return data

