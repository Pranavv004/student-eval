from flask import Flask, render_template, request, jsonify
import os
import tempfile
from test import extract_text_from_pdf, generate_qa_pairs  # Import from test.py

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'pdf_file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['pdf_file']
        num_questions = int(request.form.get('num_questions', 5))

        if file and file.filename != '':
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
                file.save(temp_file.name)
                pdf_path = temp_file.name

            # Extract text from PDF
            try:
                text = extract_text_from_pdf(pdf_path)
            except Exception as e:
                os.remove(pdf_path)  # Clean up temp file
                return jsonify({'error': f'Error processing PDF: {str(e)}'}), 500

            # Generate Q&A pairs
            try:
                qa_pairs = generate_qa_pairs(text, num_questions)
            except Exception as e:
                os.remove(pdf_path)
                return jsonify({'error': f'Error generating Q&A: {str(e)}'}), 500
            
            os.remove(pdf_path)

            return jsonify({'qa_pairs': qa_pairs})

        else:
            return jsonify({'error': 'No file selected'}), 400

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)