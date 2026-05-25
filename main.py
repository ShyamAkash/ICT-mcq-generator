from google import genai
from docx import Document
from docx.oxml.ns import qn
from copy import deepcopy
import json
from UnicodeToLegacy import ConvertToLegacy

topic=input("Topic: ")

client=genai.Client()

print("generating prompt")

with open(r"files\prompt", "r", encoding="utf-8") as f:
    prompt=f.read()

print("sending API call")

result=client.models.generate_content(
    model="gemini-3.5-flash",
    contents=prompt+topic
).text

print("writing json data to file")

with open(r"files\result.json", "w", encoding="utf-8") as f:
    f.write(result)

print("writing data to docx")

def replace_in_paragraph(paragraph, old, new):
    #Replace text while preserving the formatting of the first run.
    if old not in paragraph.text:
        return
    # Merge all runs' text, then rewrite into the first run
    full_text = "".join(run.text for run in paragraph.runs)
    full_text = full_text.replace(old, new)
    
    for i, run in enumerate(paragraph.runs):
        run.text = full_text if i == 0 else ""

def find_and_replace(filename, replacements: dict, output=None):
    doc = Document(filename)
    
    for paragraph in doc.paragraphs:
        for old, new in replacements.items():
            replace_in_paragraph(paragraph, old, new)
    
    # Also handle tables
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    for old, new in replacements.items():
                        replace_in_paragraph(paragraph, old, new)
    
    doc.save(output or filename)

#to copy format docx (not needed since the function saves separately)

#with open(r"files\Question.docx", "r", encoding="utf-8") as format:
#    with open(q_fileName, "w", encoding="utf-8") as copy:
#        copy.write(format.read())

with open(r"files\result.json", "r", encoding="utf-8") as f:
    resdict=json.loads(f.read())

find_and_replace(r"files\Question.docx", {"Question English": resdict["QEng"], 
                                   "Question Sinhala": ConvertToLegacy(resdict["QSin"]),

                                   "Answer 1 English": resdict["AnswersEng"][0],
                                   "Answer 2 English": resdict["AnswersEng"][1],
                                   "Answer 3 English": resdict["AnswersEng"][2],
                                   "Answer 4 English": resdict["AnswersEng"][3],
                                   "Answer 5 English": resdict["AnswersEng"][4],
                                   "Answer 1 Sinhala": ConvertToLegacy(resdict["AnswersSin"][0]),
                                   "Answer 2 Sinhala": ConvertToLegacy(resdict["AnswersSin"][1]),
                                   "Answer 3 Sinhala": ConvertToLegacy(resdict["AnswersSin"][2]),
                                   "Answer 4 Sinhala": ConvertToLegacy(resdict["AnswersSin"][3]),
                                   "Answer 5 Sinhala": ConvertToLegacy(resdict["AnswersSin"][4]),
                                   
                                   "Explanation 1 English": resdict["ExplEng"][0],
                                   "Explanation 2 English": resdict["ExplEng"][1],
                                   "Explanation 3 English": resdict["ExplEng"][2],
                                   "Explanation 4 English": resdict["ExplEng"][3],
                                   "Explanation 5 English": resdict["ExplEng"][4],
                                   "Explanation 1 Sinhala": ConvertToLegacy(resdict["ExplSin"][0]),
                                   "Explanation 2 Sinhala": ConvertToLegacy(resdict["ExplSin"][1]),
                                   "Explanation 3 Sinhala": ConvertToLegacy(resdict["ExplSin"][2]),
                                   "Explanation 4 Sinhala": ConvertToLegacy(resdict["ExplSin"][3]),
                                   "Explanation 5 Sinhala": ConvertToLegacy(resdict["ExplSin"][4]),
                                   
                                   "QNum": str(resdict["AnsNo"]),
                                   },
                output=topic+".docx")