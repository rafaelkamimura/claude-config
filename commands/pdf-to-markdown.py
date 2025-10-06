#!/usr/bin/env python3
"""
PDF to Markdown Converter for Interview Generator
Uses IBM's Docling for high-quality document conversion
"""

import sys
import os
from pathlib import Path

def convert_with_docling(pdf_path, output_path=None):
    """
    Convert PDF resume to Markdown using IBM's Docling

    Args:
        pdf_path: Path to input PDF file
        output_path: Optional output path for markdown file

    Returns:
        str: Path to generated markdown file
    """
    try:
        from docling import DocumentConverter

        pdf_file = Path(pdf_path)
        if not pdf_file.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        if output_path is None:
            output_path = pdf_file.with_suffix('.md')

        # Initialize Docling converter
        converter = DocumentConverter()

        # Convert PDF to markdown
        print(f"🔄 Converting {pdf_path} with Docling...")
        result = converter.convert(str(pdf_file))

        # Export as markdown
        markdown_content = result.document.export_to_markdown()

        # Write to output file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

        print(f"✅ Successfully converted to: {output_path}")
        return str(output_path)

    except ImportError:
        print("⚠️ Docling not installed. Installing...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "docling"])

        # Retry after installation
        return convert_with_docling(pdf_path, output_path)

    except Exception as e:
        print(f"❌ Error with Docling conversion: {e}")
        print("Falling back to alternative method...")
        return fallback_pdf_conversion(pdf_path, output_path)

def fallback_pdf_conversion(pdf_path, output_path=None):
    """
    Fallback PDF conversion using PyPDF2 or pdfplumber

    Args:
        pdf_path: Path to input PDF file
        output_path: Optional output path for markdown file

    Returns:
        str: Path to generated markdown file
    """
    try:
        import PyPDF2

        pdf_file = Path(pdf_path)
        if output_path is None:
            output_path = pdf_file.with_suffix('.md')

        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""

            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()

        # Basic formatting to markdown
        markdown_content = f"# Resume - Converted from PDF\n\n{text}"

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

        print(f"✅ Converted with fallback method to: {output_path}")
        return str(output_path)

    except ImportError:
        try:
            import pdfplumber

            pdf_file = Path(pdf_path)
            if output_path is None:
                output_path = pdf_file.with_suffix('.md')

            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""

            markdown_content = f"# Resume - Converted from PDF\n\n{text}"

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)

            print(f"✅ Converted with pdfplumber to: {output_path}")
            return str(output_path)

        except ImportError:
            print("❌ No PDF processing library available")
            print("Please install one of: docling, PyPDF2, or pdfplumber")
            print("Run: pip install docling")
            sys.exit(1)

def extract_resume_sections(markdown_path):
    """
    Extract and structure resume sections from markdown

    Args:
        markdown_path: Path to markdown file

    Returns:
        dict: Structured resume sections
    """
    with open(markdown_path, 'r', encoding='utf-8') as f:
        content = f.read()

    sections = {
        'contact': extract_section(content, ['contact', 'contato', 'email', 'phone']),
        'experience': extract_section(content, ['experience', 'experiência', 'work', 'trabalho', 'professional']),
        'education': extract_section(content, ['education', 'educação', 'formação', 'academic']),
        'skills': extract_section(content, ['skills', 'habilidades', 'competências', 'technologies', 'ferramentas']),
        'languages': extract_section(content, ['languages', 'idiomas', 'línguas']),
        'certifications': extract_section(content, ['certifications', 'certificações', 'certificates']),
        'projects': extract_section(content, ['projects', 'projetos', 'portfolio'])
    }

    return sections

def extract_section(content, keywords):
    """
    Extract a section from content based on keywords

    Args:
        content: Full text content
        keywords: List of keywords to search for section headers

    Returns:
        str: Extracted section content
    """
    import re

    content_lower = content.lower()

    for keyword in keywords:
        # Look for section headers with the keyword
        patterns = [
            rf'#{1,3}\s*{keyword}.*?\n(.*?)(?=\n#{1,3}|\Z)',  # Markdown headers
            rf'\n{keyword}.*?\n[-=]+\n(.*?)(?=\n\w+.*?\n[-=]+|\Z)',  # Underlined headers
            rf'\n{keyword}.*?:\n(.*?)(?=\n\w+.*?:|\Z)'  # Colon-style headers
        ]

        for pattern in patterns:
            match = re.search(pattern, content_lower, re.IGNORECASE | re.DOTALL)
            if match:
                # Return the actual content (not lowercased)
                start = match.start(1)
                end = match.end(1)
                return content[start:end].strip()

    return ""

def main():
    if len(sys.argv) < 2:
        print("Usage: python pdf-to-markdown.py <pdf_path> [output_path]")
        print("\nThis script converts PDF resumes to Markdown using IBM's Docling")
        print("If Docling is not installed, it will attempt to install it or use fallback methods")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        # Convert PDF to Markdown
        markdown_path = convert_with_docling(pdf_path, output_path)

        # Extract sections for analysis
        sections = extract_resume_sections(markdown_path)

        print("\n📋 Extracted sections:")
        for section, content in sections.items():
            if content:
                preview = content[:50] + "..." if len(content) > 50 else content
                print(f"  - {section}: {preview}")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()