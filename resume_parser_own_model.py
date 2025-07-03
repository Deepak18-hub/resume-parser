# -*- coding: utf-8 -*-
"""
Created on Tue Jun 24 19:20:23 2025

@author: Deepa
"""
#Keeping the function self-contained in the example context Ensuring the function has everything it needs, in case it's copy-pasted elsewhere
def resume_parser(resume_path):
    import re
    from pdfminer.high_level import extract_text
    import spacy

    # # Load spaCy model
    nlp = spacy.load("en_core_web_sm")

    # Load resume text
    text = extract_text(resume_path)
    # here I have take text1 since if Name is written in Upper case then it is difficult for spacy to recognize the person name.
    text1 = extract_text(resume_path).lower().title()

    # 1. Extract Name (first PERSON entity in the first few lines)
    doc = nlp(text1[:1000])
    name = ""
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text
            break

    #Extract Email
    email = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    if email:
        email=email[0]
    else: 
        email=""
        

    #Extract Phone Number
    phone = re.findall(r'\+?\d[\d\-\(\) ]{8,}\d', text)
    phone = phone[0] if phone else ""


    #Extract Location (First GPE entity)
    loc_list = ["Mumbai", "Navi Mumbai","Pune","Banglore","Noida","Thane","Chennai","Kolkata","Delhi","Hyderabad","Vasai, Mumbai","Panvel","Kalyan"]
    #set (for faster lookup and to avoid duplicates)
    valid_locations = set()
    for loc in loc_list:
        valid_locations.add(loc.lower())
    location = None
    for ent in doc.ents:
        ent_text = ent.text.strip().lower()
        if ent.label_ == "GPE" and ent_text in valid_locations:
            location = ent.text.strip()
            break  # Take the first found location and exit loop
            
    #If NER failed
    if location is None:
        #match = re.search(r'Place:\s*(.+)', text)
        match = re.search(r'Place:\s*([A-Za-z\s]+?)(?:\s+Date:|\s+Name:|$)', text)
        if match:
            location = match.group(1).strip()

    #If regex also failed
    if location is None:
        for loc in loc_list:
            if loc in text:
                location = loc
                break  # Stop at first match
            

    # 5. Extract Skills using a skill keywords list
    skills_list = [
        'Python', 'Java', 'SQL', 'Machine Learning', 'Deep Learning', 'C++', 'JavaScript', 'Data Science',"Data Analyst",
        'Communication', 'Leadership', 'Teamwork', 'Project Management', 'HTML', 'CSS', 'React', 'Node.js' , "Pandas","Numpy"
    ,"Pyspark","C",".Net","C#","Hadoop","Devoops","ETL","R","Rstudio","Streamlit","Matplotlib"]

    #skills_found = [skill for skill in skills_list if re.search(rf'\b{re.escape(skill)}\b', text, re.IGNORECASE)]
    skills_found = []  # start with empty list
    for skill in skills_list:
        if re.search(rf'\b{re.escape(skill)}\b',text,re.IGNORECASE):
            skills_found.append(skill) # ONLY append if found
       

    # Output all extracted info
    return {
        "Name": name,
        "Email": email,
        "Phone": phone,
        "Location": location,
        "Skills": ', '.join(sorted(skills_found))
    }
  
    

