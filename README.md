# 📝 Task Extraction Using NLP  

This project extracts tasks, deadlines, and responsible entities from unstructured text using **Natural Language Processing (NLP)**. The system processes text using **spaCy** and **NLTK**, identifying tasks based on specific keywords, extracting deadlines, categorizing tasks, and structuring them into an easy-to-read format.

---

## 🚀 Features  
- **Task Extraction** – Detects task-related sentences based on predefined keywords.  
- **Entity Recognition** – Identifies the person responsible for the task.  
- **Deadline Extraction** – Recognizes dates, times, and deadline-related phrases.  
- **Task Categorization** – Classifies tasks into categories like Work, Shopping, Cleaning, etc.  
- **Flask Web Interface** – Allows users to input text and extract tasks via a simple UI.  

---

## ⚙️ Installation  

### 1️⃣ Clone the repository  
```bash
git clone https://github.com/yourusername/task-extraction-nlp.git
```

### 2️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Download NLP models
```bash
import nltk
nltk.download("stopwords")

```

## 🚀 How it works  
- **Preprocess Text** – Cleans text by removing punctuation, converting to lowercase, and filtering stopwords.
- **Sentence Segmentation** – Uses spaCy to break text into sentences.
- **Task Extraction** – Identifies sentences with task-related keywords (must, should, needs to).
- **Entity Recognition** – Extracts the responsible person using Named Entity Recognition (NER).
- **Deadline Detection** – Identifies dates and deadline-related words (before, by, until).
- **Task Categorization** – Assigns a category based on predefined keywords.

## 🖥 Run the Flask App
```bash
python app.py
```

## 🔬 Core NLP Techniques
- **Text Preprocessing** – Removes special characters, converts to lowercase, and filters stopwords.
- **Named Entity Recognition (NER)** – Extracts people, dates, and times using spaCy.
- **Dependency Parsing** – Identifies subjects (who is responsible for the task).
- **Regex Matching** – Detects deadline-related phrases (by, before, until).
- **Keyword Matching** – Classifies tasks into predefined categories.

## 📝 Challenges & Insights
- **Handling Pronouns**: If a task refers to "he/she/they," the script links it to the last known subject.
- **Deadlines with Ambiguous Dates**: Some phrases like "next Monday" require extra processing.
- **Categorization Limitations**: The current system uses keyword matching, which can be improved with machine learning-based classification.