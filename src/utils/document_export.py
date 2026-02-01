"""
Document export utilities for AI Practice Platform.

Provides export functionality for PDF, DOCX, and other formats.
"""

import os
import re
from io import BytesIO
from datetime import datetime
from typing import Optional, Dict, Any, List

# PDF generation
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, ListFlowable, ListItem
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

# DOCX generation
from docx import Document as DocxDocument
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE


class PDFExporter:
    """Export documents to PDF format."""

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Set up custom PDF styles."""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.HexColor('#1e3a5f'),
            alignment=TA_CENTER
        ))

        # Heading 1
        self.styles.add(ParagraphStyle(
            name='CustomHeading1',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceBefore=20,
            spaceAfter=12,
            textColor=colors.HexColor('#2c5282')
        ))

        # Heading 2
        self.styles.add(ParagraphStyle(
            name='CustomHeading2',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceBefore=15,
            spaceAfter=8,
            textColor=colors.HexColor('#4299e1')
        ))

        # Body text
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=8,
            alignment=TA_JUSTIFY,
            leading=14
        ))

        # Bullet style
        self.styles.add(ParagraphStyle(
            name='CustomBullet',
            parent=self.styles['Normal'],
            fontSize=11,
            leftIndent=20,
            spaceAfter=4
        ))

    def export(
        self,
        title: str,
        content: str,
        organization: str = "Organization",
        metadata: Optional[Dict] = None
    ) -> BytesIO:
        """
        Export content to PDF.

        Args:
            title: Document title
            content: Markdown content to convert
            organization: Organization name for header
            metadata: Optional metadata dict

        Returns:
            BytesIO buffer containing the PDF
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )

        story = []

        # Title
        story.append(Paragraph(title, self.styles['CustomTitle']))
        story.append(Spacer(1, 12))

        # Organization and date
        date_str = datetime.now().strftime("%B %d, %Y")
        story.append(Paragraph(
            f"Prepared for: {organization}",
            self.styles['Normal']
        ))
        story.append(Paragraph(f"Date: {date_str}", self.styles['Normal']))
        story.append(Spacer(1, 24))

        # Parse and add content
        self._add_markdown_content(story, content)

        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer

    def _add_markdown_content(self, story: List, content: str):
        """Parse markdown content and add to PDF story."""
        lines = content.split('\n')
        in_list = False
        list_items = []

        for line in lines:
            line = line.strip()

            if not line:
                if in_list and list_items:
                    story.append(ListFlowable(
                        [ListItem(Paragraph(item, self.styles['CustomBullet']))
                         for item in list_items],
                        bulletType='bullet'
                    ))
                    list_items = []
                    in_list = False
                story.append(Spacer(1, 6))
                continue

            # Headers
            if line.startswith('# '):
                story.append(Paragraph(
                    self._clean_markdown(line[2:]),
                    self.styles['CustomHeading1']
                ))
            elif line.startswith('## '):
                story.append(Paragraph(
                    self._clean_markdown(line[3:]),
                    self.styles['CustomHeading1']
                ))
            elif line.startswith('### '):
                story.append(Paragraph(
                    self._clean_markdown(line[4:]),
                    self.styles['CustomHeading2']
                ))
            elif line.startswith('#### '):
                story.append(Paragraph(
                    self._clean_markdown(line[5:]),
                    self.styles['CustomHeading2']
                ))
            # Lists
            elif line.startswith('- ') or line.startswith('* '):
                in_list = True
                list_items.append(self._clean_markdown(line[2:]))
            elif re.match(r'^\d+\.', line):
                in_list = True
                list_items.append(self._clean_markdown(re.sub(r'^\d+\.\s*', '', line)))
            else:
                # Regular paragraph
                story.append(Paragraph(
                    self._clean_markdown(line),
                    self.styles['CustomBody']
                ))

        # Flush remaining list items
        if list_items:
            story.append(ListFlowable(
                [ListItem(Paragraph(item, self.styles['CustomBullet']))
                 for item in list_items],
                bulletType='bullet'
            ))

    def _clean_markdown(self, text: str) -> str:
        """Remove markdown formatting for PDF."""
        # Bold
        text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
        # Italic
        text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
        # Code
        text = re.sub(r'`(.+?)`', r'<font face="Courier">\1</font>', text)
        # Links - just show text
        text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
        return text


class DOCXExporter:
    """Export documents to DOCX format."""

    def __init__(self):
        self.doc = None

    def export(
        self,
        title: str,
        content: str,
        organization: str = "Organization",
        metadata: Optional[Dict] = None
    ) -> BytesIO:
        """
        Export content to DOCX.

        Args:
            title: Document title
            content: Markdown content to convert
            organization: Organization name for header
            metadata: Optional metadata dict

        Returns:
            BytesIO buffer containing the DOCX
        """
        self.doc = DocxDocument()
        self._setup_styles()

        # Title
        title_para = self.doc.add_heading(title, 0)
        title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Organization and date
        date_str = datetime.now().strftime("%B %d, %Y")
        meta_para = self.doc.add_paragraph()
        meta_para.add_run(f"Prepared for: {organization}").bold = True
        meta_para.add_run(f"\nDate: {date_str}")
        meta_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

        self.doc.add_paragraph()  # Spacing

        # Parse and add content
        self._add_markdown_content(content)

        # Save to buffer
        buffer = BytesIO()
        self.doc.save(buffer)
        buffer.seek(0)
        return buffer

    def _setup_styles(self):
        """Configure document styles."""
        # Set default font
        style = self.doc.styles['Normal']
        font = style.font
        font.name = 'Calibri'
        font.size = Pt(11)

    def _add_markdown_content(self, content: str):
        """Parse markdown content and add to DOCX."""
        lines = content.split('\n')
        current_list = None

        for line in lines:
            original_line = line
            line = line.strip()

            if not line:
                if current_list:
                    current_list = None
                continue

            # Headers
            if line.startswith('# '):
                self.doc.add_heading(self._clean_markdown(line[2:]), 1)
            elif line.startswith('## '):
                self.doc.add_heading(self._clean_markdown(line[3:]), 1)
            elif line.startswith('### '):
                self.doc.add_heading(self._clean_markdown(line[4:]), 2)
            elif line.startswith('#### '):
                self.doc.add_heading(self._clean_markdown(line[5:]), 3)
            # Bullet lists
            elif line.startswith('- ') or line.startswith('* '):
                para = self.doc.add_paragraph(
                    self._clean_markdown(line[2:]),
                    style='List Bullet'
                )
            # Numbered lists
            elif re.match(r'^\d+\.', line):
                text = re.sub(r'^\d+\.\s*', '', line)
                para = self.doc.add_paragraph(
                    self._clean_markdown(text),
                    style='List Number'
                )
            else:
                # Regular paragraph
                para = self.doc.add_paragraph()
                self._add_formatted_text(para, line)

    def _add_formatted_text(self, paragraph, text: str):
        """Add text with markdown formatting to paragraph."""
        # Simple formatting parser
        parts = re.split(r'(\*\*.*?\*\*|\*.*?\*|`.*?`)', text)

        for part in parts:
            if not part:
                continue
            if part.startswith('**') and part.endswith('**'):
                run = paragraph.add_run(part[2:-2])
                run.bold = True
            elif part.startswith('*') and part.endswith('*'):
                run = paragraph.add_run(part[1:-1])
                run.italic = True
            elif part.startswith('`') and part.endswith('`'):
                run = paragraph.add_run(part[1:-1])
                run.font.name = 'Courier New'
            else:
                # Remove link markdown, keep text
                clean = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', part)
                paragraph.add_run(clean)

    def _clean_markdown(self, text: str) -> str:
        """Remove markdown formatting for plain text."""
        # Bold
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
        # Italic
        text = re.sub(r'\*(.+?)\*', r'\1', text)
        # Code
        text = re.sub(r'`(.+?)`', r'\1', text)
        # Links - just show text
        text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
        return text


class DocumentExporter:
    """Main document exporter with format selection."""

    def __init__(self):
        self.pdf_exporter = PDFExporter()
        self.docx_exporter = DOCXExporter()

    def export(
        self,
        title: str,
        content: str,
        format: str = 'pdf',
        organization: str = "Organization",
        metadata: Optional[Dict] = None
    ) -> BytesIO:
        """
        Export document to specified format.

        Args:
            title: Document title
            content: Markdown content
            format: Export format ('pdf', 'docx', 'markdown')
            organization: Organization name
            metadata: Optional metadata

        Returns:
            BytesIO buffer with exported content
        """
        if format == 'pdf':
            return self.pdf_exporter.export(title, content, organization, metadata)
        elif format == 'docx':
            return self.docx_exporter.export(title, content, organization, metadata)
        elif format == 'markdown' or format == 'md':
            buffer = BytesIO()
            buffer.write(content.encode('utf-8'))
            buffer.seek(0)
            return buffer
        else:
            raise ValueError(f"Unsupported format: {format}")

    def get_mime_type(self, format: str) -> str:
        """Get MIME type for format."""
        mime_types = {
            'pdf': 'application/pdf',
            'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'markdown': 'text/markdown',
            'md': 'text/markdown'
        }
        return mime_types.get(format, 'application/octet-stream')

    def get_extension(self, format: str) -> str:
        """Get file extension for format."""
        extensions = {
            'pdf': '.pdf',
            'docx': '.docx',
            'markdown': '.md',
            'md': '.md'
        }
        return extensions.get(format, '.txt')


# Singleton instance
_exporter = None


def get_document_exporter() -> DocumentExporter:
    """Get singleton DocumentExporter instance."""
    global _exporter
    if _exporter is None:
        _exporter = DocumentExporter()
    return _exporter
