import requests
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os
import re
import ollama

# Instruction templates
system_prompt = """Act as an algorithm that responds only in CSV format, ensuring two columns: "category" and "information". Each row must contain a category and its respective information. If there is no information, respond with "N/A". The separator must be a comma (,)."""

user_instruction = """Extract the following information from the text: 
- Year 
- Area
- English title (If not in English, provide an accurate translation of the original title into English) 
- Authors 
- Contact
- University by author 
- Keywords
- Highlights
- Software used 
- Methods applied 
- Basis set 
- Related reactions 
- Molecules or atoms used 
- Conclusion summarized in a single sentence
- Study relevance
- Acknowledgments (Funding institutions) 

**Important:** Some acronyms in the text may appear without context. If they match the following list, classify them as "funding institutions": CAPES, CNPq, FAPESP, FINEP, FAPEMIG, FAPERJ, FAPDF, FAPEG, FAPESB, FAPESQ, FACEPE, FAPEMA, FAPESQ-PB.

Provide your response in CSV format with exactly two columns: "category" and "information". Separate each row with a new line. put all the options in English (Keywords, Highlights, Software used, Methods applied, Basis set, Related reactions, Molecules or atoms used). If information is missing, use "N/A". 
"""

def load_texts_from_folder(folder_path):
    documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    # Extract only the text between the delimiters ##-## and ##--##
                    matches = re.findall(r'#-#(.*?)#---#', content, re.DOTALL)
                    for match in matches:
                        lines = match.strip().splitlines()
                        if len(lines) >= 5:
                            documents.append(match.strip())
            except Exception as e:
                with open("error.txt", "a", encoding="utf-8") as txt_file:
                    txt_file.write(f"ERROR: {e} \n")
                    txt_file.write(f"{documents[i]} \n")
    return documents


if __name__ == "__main__":
    folder_path = 'Texts'
    documents = load_texts_from_folder(folder_path)

    for i in range(len(documents)):
        response = ollama.chat(
            model='phi4',
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': f"{user_instruction}/n/nText -> {documents[i]}"}
            ]
        )
        api_response = str(response['message']['content'])
        
        # Creating the dictionary structure to save in JSON
        if i % 10 == 0:
            print(i)
        
        result = f"{api_response}\n"
        # Add the result to the list
        if 'Authors, "N/A"' not in api_response and 'Authors, N/A' not in api_response and 'Authors, (N/A)' not in api_response and 'Authors,N/A' not in api_response and 'Authors,(N/A)' not in api_response and 'Authors,"N/A"' not in api_response:
            #print("\n\n**********************************************************************")
            # Saving the dictionary directly as text
            try:
                with open("answers/full_csv.txt", "a", encoding="utf-8") as txt_file:
                    txt_file.write(str(result + "\n").encode("utf-8", "replace").decode("utf-8"))
            except Exception as e:
                with open("error.txt", "a", encoding="utf-8") as txt_file:
                    txt_file.write(f"ERROR: {e} \n")
                    txt_file.write(f"{documents[i]} \n")

                    
        else:
            try:
                with open("error_csv.txt", "a", encoding="utf-8") as txt_file:
                    txt_file.write(str(result + "\n").encode("utf-8", "replace").decode("utf-8"))
            except Exception as e:
                with open("error.txt", "a", encoding="utf-8") as txt_file:
                    txt_file.write(f"ERROR: {e} \n")
                    txt_file.write(f"{documents[i]} \n")
                
    print("Responses successfully saved in 'answers' folder")
        
