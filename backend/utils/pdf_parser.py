import fitz  # PyMuPDF
from pdfminer.high_level import extract_text as pdfminer_extract_text
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import TextConverter
from io import StringIO
import logging
from typing import Optional, Tuple
import re

logger = logging.getLogger(__name__)

class PDFTextExtractor:
    """Utility class for parsing PDF files and extracting text content"""
    
    @staticmethod
    def extract_text_with_pymupdf(pdf_path: str) -> Optional[str]:
        """
        Extract text from PDF using PyMuPDF (fitz)
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text or None if failed
        """
        try:
            doc = fitz.open(pdf_path)
            text = ""
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text += page.get_text()
            
            doc.close()
            return text.strip()
            
        except Exception as e:
            logger.error(f"PyMuPDF extraction failed: {str(e)}")
            return None
    
    @staticmethod
    def extract_text_with_pdfminer(pdf_path: str) -> Optional[str]:
        """
        Extract text from PDF using pdfminer.six
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text or None if failed
        """
        try:
            text = pdfminer_extract_text(pdf_path)
            return text.strip()
            
        except Exception as e:
            logger.error(f"pdfminer extraction failed: {str(e)}")
            return None
    
    @staticmethod
    def extract_text(pdf_path: str) -> Optional[str]:
        """
        Extract text from PDF using multiple methods with fallback
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text or None if all methods fail
        """
        # Try PyMuPDF first (faster and more reliable)
        text = PDFTextExtractor.extract_text_with_pymupdf(pdf_path)
        
        if text and text.strip():
            return text
        
        # Fallback to pdfminer.six
        text = PDFTextExtractor.extract_text_with_pdfminer(pdf_path)
        
        if text and text.strip():
            return text
        
        logger.error(f"Failed to extract text from PDF: {pdf_path}")
        return None
    
    @staticmethod
    def extract_basic_info(text: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Extract basic candidate information from resume text
        
        Args:
            text: Extracted text from PDF
            
        Returns:
            Tuple of (candidate_name, email) or (None, None) if not found
        """
        if not text:
            return None, None
        
        # Email extraction
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, text)
        email = email_match.group() if email_match else None
        
        # Name extraction (basic approach - can be enhanced)
        # Look for common name patterns at the beginning of the document
        lines = text.split('\n')
        candidate_name = None
        
        for line in lines[:10]:  # Check first 10 lines
            line = line.strip()
            if line and len(line) < 100:  # Reasonable name length
                # Basic name pattern: 2-4 words, mostly letters
                words = line.split()
                if 2 <= len(words) <= 4:
                    # Check if most words are alphabetic
                    if all(word.replace('-', '').replace('.', '').isalpha() for word in words):
                        candidate_name = line
                        break
        
        return candidate_name, email
    
    @staticmethod
    def validate_pdf_file(file_path: str) -> bool:
        """
        Validate if the file is a valid PDF
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if valid PDF, False otherwise
        """
        try:
            # Try to open with PyMuPDF
            doc = fitz.open(file_path)
            doc.close()
            return True
        except Exception:
            try:
                # Try with pdfminer
                with open(file_path, 'rb') as file:
                    parser = PDFParser(file)
                    doc = PDFDocument(parser)
                    return True
            except Exception:
                return False 