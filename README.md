# Agentic Document Assistant

A powerful, AI-powered document processing and analysis tool that can extract text from various file formats and provide intelligent responses to user queries. Built with FastAPI and modern AI technologies.

## 🌟 Features

- **Multi-Format Support**: Process various document types including:
  - 📄 PDF documents
  - 🖼️ Images (PNG, JPG, JPEG)
  - 📝 Plain text
  - 🎥 YouTube video transcripts

- **Advanced Processing**
  - Optical Character Recognition (OCR) for extracting text from images
  - PDF text extraction with layout preservation
  - YouTube video transcript fetching
  - AI-powered document analysis and question answering

- **Web Interface**
  - Interactive Streamlit-based UI for easy interaction
  - Real-time processing feedback
  - Responsive design for desktop and mobile

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Tesseract OCR (for better text recognition)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/agentic-document-assistant.git
   cd agentic-document-assistant
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

1. Create a `.env` file in the project root and add your API keys:
   ```
   GOOGLE_API_KEY=your_google_ai_key
   ```

## 🏃‍♂️ Running the Application

### Backend Server
Start the FastAPI backend:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Web Interface
Start the Streamlit interface:
```bash
streamlit run app_ui.py
```

Access the web interface at `http://localhost:8501`

## 🛠️ API Endpoints

- `POST /process` - Process documents and answer questions
  - Accepts: `multipart/form-data` with `file` and `query` parameters
  - Returns: JSON response with processed text and answers

## 📚 Supported File Types

| Format   | Support | Notes                                      |
|----------|---------|--------------------------------------------|
| PDF      | ✅       | Text extraction with layout preservation   |
| Images   | ✅       | PNG, JPG, JPEG with OCR                    |
| Text     | ✅       | Plain text files (.txt)                    |
| YouTube  | ✅       | Video transcript extraction                |

## 🤖 Technologies Used

- **Backend**: FastAPI
- **AI/ML**: Google Generative AI, EasyOCR
- **Document Processing**: pdfplumber, PyPDF2
- **Web Interface**: Streamlit

