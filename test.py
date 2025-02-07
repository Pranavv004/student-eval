from g4f.client import Client
import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a given PDF file.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Extracted text from the PDF.
    """
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def generate_qa_pairs(topic, num_pairs):
    """
    Generates specified number of question-answer pairs for a given topic

    Args:
        topic (str): The topic to generate questions about
        num_pairs (int): Number of Q&A pairs to generate
a
    Returns:
        list: List of dictionaries containing 'question' and 'answer' keys
    """
    client = Client()
    prompt = (
        f"Generate {num_pairs} questions and answers about {topic}. "
        "Format strictly as:\n\n"
        "Question: [your question here]\n"
        "Answer: [your answer here]\n\n"
        "Repeat this pattern for each pair. "
        "Do not include any numbers, headers, or additional text. "
        "Keep answers concise and factual."
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        web_search=False
    )

    content = response.choices[0].message.content
    return parse_qa_content(content)

def parse_qa_content(content):
    """
    Parses the raw text response into structured Q&A pairs

    Args:
        content (str): Raw text response from the API

    Returns:
        list: List of dictionaries with 'question' and 'answer' keys
    """
    qa_pairs = []
    current_q = None
    current_a = None

    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('Question:'):
            current_q = line.replace('Question:', '').strip()
        elif line.startswith('Answer:'):
            current_a = line.replace('Answer:', '').strip()
            if current_q and current_a:
                qa_pairs.append({
                    'question': current_q,
                    'answer': current_a
                })
                current_q = None
                current_a = None

    return qa_pairs