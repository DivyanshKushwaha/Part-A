

from flask import Flask, render_template, request
import spacy
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import pos_tag, word_tokenize
from nltk.chunk import ne_chunk

app = Flask(__name__)

# Load NLP models
nlp = spacy.load("en_core_web_lg")
nltk.download("stopwords")
stop_words = set(stopwords.words("english"))

# Task extraction functions
def preprocess_text(text):
    text = re.sub(r"[^a-zA-Z\s]", "", text).lower()
    tokens = [word for word in text.split() if word not in stop_words]
    return " ".join(tokens)

def get_sentences(text):
    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents]
    print("Extracted Sentences:", sentences)  # Debugging
    return sentences

task_keywords = {"must", "should", "has to", "needs to", "required to", "is to", "have to", "is supposed to"}

def extract_tasks(sentences):
    tasks = []
    last_subject = None
    for sentence in sentences:
        words = sentence.lower().split()
        doc = nlp(sentence)
        for token in doc:
            if token.pos_ == "PROPN" and not last_subject:
                last_subject = token.text
        if any(keyword in sentence for keyword in task_keywords):
            tasks.append((sentence, last_subject))
    print("Extracted Tasks:", tasks)  # Debugging
    return tasks


def get_task_entity(task_tuple, last_subject=None):
    sentence, last_subject = task_tuple
    doc = nlp(sentence)

    entities = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    if entities:
        return entities[0] 
   
    proper_nouns = [token.text for token in doc if token.pos_ == "PROPN"]
    if proper_nouns:
        return proper_nouns[0] 

    pronouns = [token.text for token in doc if token.pos_ == "PRON"]
    if pronouns and last_subject:
        return last_subject  

    return last_subject if last_subject else "Unknown"



def get_task_deadline(sentence):
    doc = nlp(sentence)
    deadlines = [ent.text for ent in doc.ents if ent.label_ in ["DATE", "TIME"]]
    match = re.search(r"(before|by|until)\s+([0-9A-Za-z\s]+)", sentence)
    if match:
        deadlines.append(match.group(0))
    return ", ".join(deadlines) if deadlines else "No deadline specified"

task_categories = {
    "Work": ["report", "assignment", "presentation", "submit", "form", "project"],
    "Shopping": ["buy", "purchase", "groceries"],
    "Cleaning": ["clean", "wash", "house"],
    "Communication": ["call", "email", "message"]
}

def categorize_task(sentence):
    sentence_lower = sentence.lower()
    for category, keywords in task_categories.items():
        if any(word in sentence_lower for word in keywords):
            return category
    return "Uncategorized"

def generate_task_summary(tasks):
    extracted_tasks = []
    for task in tasks:
        task_sentence = task[0]
        if task[1]:  # If a valid subject is found (e.g., Rahul)
            task_text = re.sub(rf"\b({re.escape(task[1])}|he|she|they|it)\b", "", task_sentence, flags=re.IGNORECASE).strip()
        who = get_task_entity(task)
        deadline = get_task_deadline(task_sentence)
        category = categorize_task(task_sentence)

        extracted_tasks.append({
            "Task": task_text, # Remove repeated subject
            "Who": who,
            "Deadline": deadline,
            "Category": category
})

    print("Final Tasks:", extracted_tasks)  # Debugging
    return extracted_tasks

@app.route("/", methods=["GET", "POST"])
def index():
    tasks = []
    if request.method == "POST":
        text = request.form.get("text")
        if text.strip():
            print("Input Text:", text)  # Debugging
            sentences = get_sentences(text)
            extracted_tasks = extract_tasks(sentences)
            tasks = generate_task_summary(extracted_tasks)
    return render_template("index.html", tasks=tasks)

if __name__ == "__main__":
    app.run(debug=True, port=5000)


