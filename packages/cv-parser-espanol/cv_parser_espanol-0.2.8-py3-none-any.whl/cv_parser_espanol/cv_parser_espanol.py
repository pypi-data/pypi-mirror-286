import spacy
import re
import fitz  # PyMuPDF
import docx  # python-docx
import es_core_news_sm

# Cargar el modelo en español de spaCy
nlp = es_core_news_sm.load()

def extract_email(text):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email = re.findall(email_pattern, text)
    return email[0] if email else ''

def extract_phone(text):
    phone_pattern = r'\+?\d[\d -]{8,14}\d'
    phone = re.findall(phone_pattern, text)
    return phone[0] if phone else ''

def extract_sections(text):
    sections = {}
    section_keywords = {
        'experiencia_laboral': ['experiencia laboral', 'experiencia', 'trabajo'],
        'educacion': ['educación', 'formación académica', 'formación'],
        'skills': ['skills', 'habilidades', 'competencias']
    }
    current_section = None
    
    for line in text.split('\n'):
        line = line.strip().lower()
        if not line:
            continue
        for section, keywords in section_keywords.items():
            if any(keyword in line for keyword in keywords):
                current_section = section
                sections[current_section] = []
                break
        if current_section:
            sections[current_section].append(line)
    return sections

def parse_cv(text):
    doc = nlp(text)
    
    # Extract entities using spaCy
    entities = {ent.label_: ent.text for ent in doc.ents}
    
    # Extract email and phone
    email = extract_email(text)
    phone = extract_phone(text)
    
    # Extract sections
    sections = extract_sections(text)
    
    # Join the lines of each section into a single string
    for key in sections:
        sections[key] = ' '.join(sections[key])
    
    # Organize the extracted information into a dictionary
    cv_info = {
        'nombre': entities.get('PER', ''),
        'direccion': entities.get('LOC', ''),
        'correo_electronico': email,
        'telefono': phone,
        'experiencia_laboral': sections.get('experiencia_laboral', ''),
        'educacion': sections.get('educacion', ''),
        'skills': sections.get('skills', '')
    }
    
    return cv_info

def pdf_to_text(file_bytes):
    doc = fitz.open(stream=file_bytes, filetype='pdf')
    text = ""
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

def docx_to_text(docx_path):
    doc = docx.Document(docx_path)
    text = []
    for paragraph in doc.paragraphs:
        text.append(paragraph.text)
    return '\n'.join(text)

def extract_text(file_path):
    if file_path.lower().endswith('.pdf'):
        return pdf_to_text(file_path)
    elif file_path.lower().endswith('.docx'):
        return docx_to_text(file_path)
    else:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()