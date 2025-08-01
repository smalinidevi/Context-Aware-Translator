# Document Translator

A Streamlit-based web application that translates PDF documents while preserving their original formatting. The application uses Google's Vertex AI Text-Bison model for high-quality translations with intelligent section skipping capabilities.

## Features

- Translate PDF documents between German, Dutch, and English
- Smart section skipping: Ability to skip specific sections during translation
  - Skip entire chapters or sections by their titles
  - Maintains document structure and formatting around skipped sections
  - Useful for keeping certain content in original language (e.g., technical terms, references)
- Preserve original document formatting including:
  - Font sizes and positions
  - Special characters and bullet points
  - Document layout and structure
- Intelligent translation using Google's Text-Bison model
  - Context-aware translations
  - Handles document-level coherence
  - Configurable translation parameters
- Easy-to-use web interface with:
  - Language selection dropdowns
  - Section skip input field
  - File upload and download functionality

## Prerequisites

- Python 3.7+
- Google Cloud Platform account with Vertex AI API enabled
- Service account key with appropriate permissions

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd Document_Translator
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Set up Google Cloud credentials:
   - Create a service account in Google Cloud Console
   - Download the JSON key file
   - Place the key file in the project directory
   - Update the `key_path` variable in `Translator.py` with your key file path
   - Set your `PROJECT_ID` and `REGION` in the code

## Usage

1. Run the Streamlit application:
```bash
streamlit run Translator.py
```

2. Open your web browser and navigate to the provided URL (typically http://localhost:8501)

3. Use the application:
   - Select source language (German or Dutch)
   - Select target language (English or German)
   - (Optional) Enter section titles to skip during translation
     - Example: Enter "1.1 Introduction" to skip that section
     - The section and its subsections will remain untranslated
   - Upload your PDF document
   - Wait for the translation to complete
   - Download the translated document

## Technical Details

### Translation Engine
- Uses Google's Text-Bison model through Vertex AI
- Configuration parameters:
  - Temperature: 0.7 (controls translation randomness)
  - Max output tokens: 512
  - Top-p: 1.0
  - Top-k: 40

### Document Processing
- Handles special characters: •, ●, ‣, ◦, ◘, ○, ▪, ▫, ■, □
- Preserves document structure using PyMuPDF (fitz)
- Maintains original formatting including font sizes and positions
- Smart section skipping based on document structure and x-coordinates

## Required Python Packages

- streamlit
- PyMuPDF (fitz)
- google-cloud-aiplatform
- vertexai
- unidecode
- google-auth

## Environment Variables

The following environment variables can be configured:

- `PROJECT_ID`: Your Google Cloud Project ID
- `REGION`: Google Cloud region (default: us-central1)

## Notes

- The application preserves special characters, bullet points, and formatting
- Documents with complex layouts might require manual review
- Translation quality depends on the Text-Bison model's capabilities
- Large documents may take longer to process
- Skipped sections maintain their original language and formatting
