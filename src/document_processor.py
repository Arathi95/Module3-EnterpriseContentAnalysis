import PyPDF2
import docx
import tiktoken
import os

class DocumentProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_type = self.get_file_type()
        self.file_size = os.path.getsize(file_path)
        self.tokenizer = tiktoken.get_encoding("cl100k_base")

    def get_file_type(self):
        _, extension = os.path.splitext(self.file_path)
        return extension.lower()

    def extract_text(self):
        text = ""
        if self.file_type == ".pdf":
            text = self._extract_text_from_pdf()
        elif self.file_type == ".docx":
            text = self._extract_text_from_docx()
        elif self.file_type == ".txt":
            text = self._extract_text_from_txt()
        else:
            raise ValueError(f"Unsupported file type: {self.file_type}")
        return self._clean_text(text)

    def _extract_text_from_pdf(self):
        text = ""
        with open(self.file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text()
        return text

    def _extract_text_from_docx(self):
        doc = docx.Document(self.file_path)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text

    def _extract_text_from_txt(self):
        with open(self.file_path, "r", encoding="utf-8") as f:
            return f.read()

    def _clean_text(self, text):
        return " ".join(text.split())

    def process(self):
        text = self.extract_text()
        tokens = self.tokenizer.encode(text)
        
        if len(tokens) > 3000:
            tokens = tokens[:3000]
            text = self.tokenizer.decode(tokens)

        return {
            "text": text,
            "metadata": {
                "file_type": self.file_type,
                "file_size": self.file_size,
                "token_count": len(tokens)
            }
        }
