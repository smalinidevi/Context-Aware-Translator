import streamlit as st
import fitz
import os
import tempfile
import vertexai
from vertexai.language_models import TextGenerationModel
from unidecode import unidecode
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
 
#location = "europe-west2"
#project_id = 'erudite-realm-416511'
temp_dir = tempfile.mkdtemp()
special_char = ['•', '●', '‣', '◦', '◘', '○', '▪', '▫', '■', '□', '□', '▪', '▫']
italics_flag = [2, 18, 22]
new_file_path = new_file_name = source_lang = target_lang = ''
 
# Path to your service account key file
key_path = r'#path to your service account key file'
 
# Create credentials object
credentials = Credentials.from_service_account_file(
    key_path,
    scopes=['https://www.googleapis.com/auth/cloud-platform'])
 
if credentials.expired:
    credentials.refresh(Request())
PROJECT_ID = '#your project id'
REGION = '#your region'
 
# initialize vertex
#vertexai.init(project = PROJECT_ID, location = REGION, credentials = credentials)
 
def invoke_translator(text):
    global source_lang
    global target_lang
    try:
        #vertexai.init(project=project_id, location=location)
       
        # initialize vertex
        vertexai.init(project = PROJECT_ID, location = REGION, credentials = credentials)
 
        parameters = {
            "temperature": 0.7,  # Temperature controls the degree of randomness in token selection.
            "max_output_tokens": 512,  # Token limit determines the maximum amount of text output.
            "top_p": 1,  # Tokens are selected from most probable to least until the sum of their probabilities equals the top_p value.
            "top_k": 40,  # A top_k of 1 means the selected token is the most probable among all tokens.
        }
 
        model = TextGenerationModel.from_pretrained("text-bison")
        prompt = f"Translate the following text from {source_lang} to {target_lang}: \n{text}"
        response = model.predict(
            prompt = prompt,
            **parameters,
        )
        return response.text
    except Exception as e:
        st.error(f'Exception raised: {str(e)}')
        return False
 
def process_document(file_path, skip_section_list):
    with fitz.open(file_path) as doc:  
        for page in doc:
            page_blocks = page.get_text("dict")["blocks"]
            skip_section_x0 = 0
            skip_section_status = False
            for block in page_blocks:
                if "lines" in block.keys():
                    spans = block['lines']                          
                    for span in spans:
                        span_info = span['spans']                                    
                        for text_info in span_info:
                            text = text_info['text'].strip()
                            if (text) and ((text not in special_char) and (text_info['flags'] not in italics_flag)):                                
                                # Check for section to be skipped
                                if (skip_section_list and (text.lower() in skip_section_list)):
                                    skip_section_x0 = text_info["bbox"][0]
                                    skip_section_status = True
                                else:
                                    text_x0 = text_info["bbox"][0]
                                    if (text_x0 <= skip_section_x0):
                                        skip_section_status = False
                                    if (skip_section_status == False):
                                        translated_text = invoke_translator(text)
                                        if translated_text:
                                            a = text_info["ascender"]
                                            d = text_info["descender"]
                                            r = fitz.Rect(text_info["bbox"])
                                            o = fitz.Point(text_info["origin"])  # its y-value is the baseline
                                            r.y1 = o.y - text_info["size"] * d / (a - d)
                                            r.y0 = r.y1 - text_info["size"]
                                            page.add_redact_annot(r)
                                            page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)
                                            page.insert_text(text_info["origin"], unidecode(translated_text), fontname = 'Helvetica', fontsize = text_info["size"])
                                   
        global new_file_name
        file_name_split = os.path.splitext(uploaded_file.name)
        new_file_name = file_name_split[0] + '-en' + file_name_split[1]
        new_file_path = os.path.join(temp_dir, new_file_name)
        doc.save(new_file_path, garbage=3, deflate=True)
        return new_file_path
       
 
st.header("Document Translator")
source_lang_select = st.selectbox(
    'Source language',
    ('German','Dutch' ))
target_lang_select = st.selectbox(
    'Target language',
    ('English','German' ))
skip_section = st.text_input("Section to be skipped", value="", max_chars=25, type="default", autocomplete=None, label_visibility="visible")
uploaded_file = st.file_uploader("Upload the Document", type=["pdf"])
 
 
if uploaded_file is not None:
    # next 3 lines save uploaded file in a temporary directory
    file_path = os.path.join(temp_dir, uploaded_file.name)    
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getvalue())
 
    source_lang = source_lang_select
    target_lang = target_lang_select    
    skip_section_list = []
    #skip_section = '1.1 Uitgangspunten'
    if skip_section.strip():
        skip_section_list = [skip_section.strip().lower()]
    new_file_path = process_document(file_path, skip_section_list)
 
if os.path.isfile(new_file_path):
    with open(new_file_path, "rb") as pdf_file:
        PDFbyte = pdf_file.read()
 
    st.download_button(
        label = "Download the Document",
        data = PDFbyte,
        file_name = new_file_name,
        mime = 'application/pdf',
    )