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
        Also returns links if needed
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

    @staticmethod
    def extract_links(pdf_path: str) -> list:
        """
        Extract hyperlinks (mailto, LinkedIn, GitHub, etc) from PDF using PyMuPDF
        Returns a list of dicts: {type, url}
        """
        links = []
        try:
            doc = fitz.open(pdf_path)
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                for link in page.get_links():
                    uri = link.get('uri', '')
                    if uri:
                        if uri.startswith('mailto:'):
                            links.append({'type': 'email', 'url': uri})
                        elif 'linkedin.com' in uri:
                            links.append({'type': 'linkedin', 'url': uri})
                        elif 'github.com' in uri:
                            links.append({'type': 'github', 'url': uri})
                        else:
                            links.append({'type': 'other', 'url': uri})
            doc.close()
        except Exception as e:
            logger.error(f"Failed to extract links: {e}")
        return links

    @staticmethod
    def extract_education(text: str) -> list:
        """
        Extract multiple education entries from resume text.
        Returns a list of dicts: {degree, institution, year, gpa}
        Always includes 'degree' (default 'Unknown') for Pydantic validation.
        """
        education_entries = []
        # Look for 'Education' section
        edu_section = re.split(r'(?i)education', text)
        if len(edu_section) < 2:
            return education_entries
        after_edu = edu_section[1]
        # Split into lines and look for degree/institution/year patterns
        lines = after_edu.split('\n')
        degree_pattern = re.compile(r'(Bachelor|Master|B\.?Sc|M\.?Sc|Ph\.?D|B\.?Tech|M\.?Tech|MBA|B\.A\.|M\.A\.|High School|Secondary|Diploma|Associate)', re.I)
        year_pattern = re.compile(r'(19|20)\d{2}')
        gpa_pattern = re.compile(r'GPA[:\s]*([0-9]\.?[0-9]*)', re.I)
        current = {'degree': 'Unknown'}
        for line in lines:
            line = line.strip()
            if not line:
                continue
            degree_match = degree_pattern.search(line)
            year_match = year_pattern.search(line)
            gpa_match = gpa_pattern.search(line)
            if degree_match:
                if current and any(v for k, v in current.items() if k != 'degree'):
                    education_entries.append(current)
                current = {'degree': degree_match.group()}
                # Try to extract institution (rest of line after degree)
                rest = line[degree_match.end():].strip(' ,:-')
                if rest:
                    current['institution'] = rest
            elif 'university' in line.lower() or 'college' in line.lower() or 'school' in line.lower() or 'institute' in line.lower():
                current['institution'] = line
            if year_match:
                current['year'] = str(year_match.group())
            if gpa_match:
                try:
                    current['gpa'] = str(gpa_match.group(1))
                except Exception:
                    pass
        if current and any(v for k, v in current.items() if k != 'degree'):
            education_entries.append(current)
        # Ensure all entries have 'degree'
        for entry in education_entries:
            if 'degree' not in entry or not entry['degree']:
                entry['degree'] = 'Unknown'
        return education_entries 