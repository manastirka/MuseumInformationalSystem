#!/usr/bin/env python3
"""
PDF Export Module for Museum Information System
Supports Serbian Cyrillic text and generates professional reports
"""

from io import BytesIO
from datetime import datetime
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.platypus import Frame, PageTemplate
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from typing import List, Dict, Optional


class MuseumPDFExporter:
    """Base class for PDF exports with Serbian Cyrillic support"""

    def __init__(self):
        """Initialize PDF exporter with Serbian font support"""
        # Try to register fonts that support Cyrillic
        # ReportLab has built-in support for some Unicode fonts
        self.setup_fonts()

        # Museum branding colors
        self.primary_color = colors.HexColor('#2C3E50')
        self.secondary_color = colors.HexColor('#3498DB')
        self.accent_color = colors.HexColor('#E74C3C')
        self.light_gray = colors.HexColor('#ECF0F1')
        self.dark_gray = colors.HexColor('#7F8C8D')

        # Museum information
        self.museum_name = "Природњачки музеј у Београду"
        self.museum_name_en = "Natural History Museum in Belgrade"
        self.museum_address = "Његошева 51, 11000 Београд, Србија"
        self.museum_phone = "011/344-5149"
        self.museum_email = "info@nhmbeo.rs"
        self.museum_website = "www.nhmbeo.rs"

    def setup_fonts(self):
        """Setup fonts for Serbian Cyrillic support"""
        try:
            # Register REAL Times New Roman (Microsoft Core Font)
            pdfmetrics.registerFont(TTFont('TimesNewRoman', '/usr/share/fonts/msttcore/times.ttf'))
            pdfmetrics.registerFont(TTFont('TimesNewRoman-Bold', '/usr/share/fonts/msttcore/timesbd.ttf'))
            pdfmetrics.registerFont(TTFont('TimesNewRoman-Italic', '/usr/share/fonts/msttcore/timesi.ttf'))
            pdfmetrics.registerFont(TTFont('TimesNewRoman-BoldItalic', '/usr/share/fonts/msttcore/timesbi.ttf'))
            
            # Register Georgia (Microsoft Core Font)
            pdfmetrics.registerFont(TTFont('Georgia', '/usr/share/fonts/msttcore/georgia.ttf'))
            pdfmetrics.registerFont(TTFont('Georgia-Bold', '/usr/share/fonts/msttcore/georgiab.ttf'))
            pdfmetrics.registerFont(TTFont('Georgia-Italic', '/usr/share/fonts/msttcore/georgiai.ttf'))
            pdfmetrics.registerFont(TTFont('Georgia-BoldItalic', '/usr/share/fonts/msttcore/georgiaz.ttf'))
            
            # Register Cambria (Microsoft Office font - Bold variants only, Regular missing)
            pdfmetrics.registerFont(TTFont('Cambria-Bold', '/usr/share/fonts/msttcore/cambriab.ttf'))
            pdfmetrics.registerFont(TTFont('Cambria-Italic', '/usr/share/fonts/msttcore/cambriai.ttf'))
            pdfmetrics.registerFont(TTFont('Cambria-BoldItalic', '/usr/share/fonts/msttcore/cambriaz.ttf'))
            
            # Register Calibri (Microsoft Office font)
            pdfmetrics.registerFont(TTFont('Calibri', '/usr/share/fonts/msttcore/calibri.ttf'))
            pdfmetrics.registerFont(TTFont('Calibri-Bold', '/usr/share/fonts/msttcore/calibrib.ttf'))
            pdfmetrics.registerFont(TTFont('Calibri-Italic', '/usr/share/fonts/msttcore/calibrii.ttf'))
            pdfmetrics.registerFont(TTFont('Calibri-BoldItalic', '/usr/share/fonts/msttcore/calibriz.ttf'))
            
            # Register Arial (Microsoft Core Font)
            pdfmetrics.registerFont(TTFont('Arial', '/usr/share/fonts/msttcore/arial.ttf'))
            pdfmetrics.registerFont(TTFont('Arial-Bold', '/usr/share/fonts/msttcore/arialbd.ttf'))
            pdfmetrics.registerFont(TTFont('Arial-Italic', '/usr/share/fonts/msttcore/ariali.ttf'))
            pdfmetrics.registerFont(TTFont('Arial-BoldItalic', '/usr/share/fonts/msttcore/arialbi.ttf'))
            
            # Register Verdana (Microsoft Core Font)
            pdfmetrics.registerFont(TTFont('Verdana', '/usr/share/fonts/msttcore/verdana.ttf'))
            pdfmetrics.registerFont(TTFont('Verdana-Bold', '/usr/share/fonts/msttcore/verdanab.ttf'))
            pdfmetrics.registerFont(TTFont('Verdana-Italic', '/usr/share/fonts/msttcore/verdanai.ttf'))
            pdfmetrics.registerFont(TTFont('Verdana-BoldItalic', '/usr/share/fonts/msttcore/verdanaz.ttf'))
            
            # Register Trebuchet MS (Microsoft Core Font)
            pdfmetrics.registerFont(TTFont('TrebuchetMS', '/usr/share/fonts/msttcore/trebuc.ttf'))
            pdfmetrics.registerFont(TTFont('TrebuchetMS-Bold', '/usr/share/fonts/msttcore/trebucbd.ttf'))
            pdfmetrics.registerFont(TTFont('TrebuchetMS-Italic', '/usr/share/fonts/msttcore/trebucit.ttf'))
            pdfmetrics.registerFont(TTFont('TrebuchetMS-BoldItalic', '/usr/share/fonts/msttcore/trebucbi.ttf'))
            
            # Register Liberation fonts (open source alternatives)
            pdfmetrics.registerFont(TTFont('LiberationSerif', '/usr/share/fonts/liberation-serif-fonts/LiberationSerif-Regular.ttf'))
            pdfmetrics.registerFont(TTFont('LiberationSerif-Bold', '/usr/share/fonts/liberation-serif-fonts/LiberationSerif-Bold.ttf'))
            pdfmetrics.registerFont(TTFont('LiberationSerif-Italic', '/usr/share/fonts/liberation-serif-fonts/LiberationSerif-Italic.ttf'))
            pdfmetrics.registerFont(TTFont('LiberationSerif-BoldItalic', '/usr/share/fonts/liberation-serif-fonts/LiberationSerif-BoldItalic.ttf'))
            
            # Register Liberation Sans (Arial equivalent)
            pdfmetrics.registerFont(TTFont('LiberationSans', '/usr/share/fonts/liberation-sans-fonts/LiberationSans-Regular.ttf'))
            pdfmetrics.registerFont(TTFont('LiberationSans-Bold', '/usr/share/fonts/liberation-sans-fonts/LiberationSans-Bold.ttf'))
            pdfmetrics.registerFont(TTFont('LiberationSans-Italic', '/usr/share/fonts/liberation-sans-fonts/LiberationSans-Italic.ttf'))
            pdfmetrics.registerFont(TTFont('LiberationSans-BoldItalic', '/usr/share/fonts/liberation-sans-fonts/LiberationSans-BoldItalic.ttf'))
            
            # Register Liberation Mono (Courier New equivalent)
            pdfmetrics.registerFont(TTFont('LiberationMono', '/usr/share/fonts/liberation-mono-fonts/LiberationMono-Regular.ttf'))
            pdfmetrics.registerFont(TTFont('LiberationMono-Bold', '/usr/share/fonts/liberation-mono-fonts/LiberationMono-Bold.ttf'))
            pdfmetrics.registerFont(TTFont('LiberationMono-Italic', '/usr/share/fonts/liberation-mono-fonts/LiberationMono-Italic.ttf'))
            pdfmetrics.registerFont(TTFont('LiberationMono-BoldItalic', '/usr/share/fonts/liberation-mono-fonts/LiberationMono-BoldItalic.ttf'))
            
            # Register DejaVu fonts as fallback
            pdfmetrics.registerFont(TTFont('DejaVuSans', '/usr/share/fonts/dejavu-sans-fonts/DejaVuSans.ttf'))
            pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', '/usr/share/fonts/dejavu-sans-fonts/DejaVuSans-Bold.ttf'))
            pdfmetrics.registerFont(TTFont('DejaVuSans-Oblique', '/usr/share/fonts/dejavu-sans-fonts/DejaVuSans-Oblique.ttf'))
            pdfmetrics.registerFont(TTFont('DejaVuSans-BoldOblique', '/usr/share/fonts/dejavu-sans-fonts/DejaVuSans-BoldOblique.ttf'))
            
            # Default to REAL Times New Roman (the classic serif font)
            self.font_name = 'TimesNewRoman'
            self.font_bold = 'TimesNewRoman-Bold'
            self.font_italic = 'TimesNewRoman-Italic'
            self.font_bold_italic = 'TimesNewRoman-BoldItalic'
            
            # Microsoft classic serif fonts
            self.font_times = 'TimesNewRoman'
            self.font_georgia = 'Georgia'
            self.font_georgia_bold = 'Georgia-Bold'
            self.font_cambria_bold = 'Cambria-Bold'  # Regular Cambria not available
            
            # Microsoft sans-serif fonts
            self.font_arial = 'Arial'
            self.font_arial_bold = 'Arial-Bold'
            self.font_calibri = 'Calibri'
            self.font_calibri_bold = 'Calibri-Bold'
            self.font_verdana = 'Verdana'
            self.font_verdana_bold = 'Verdana-Bold'
            self.font_trebuchet = 'TrebuchetMS'
            
            # Open source alternatives
            self.font_liberation_serif = 'LiberationSerif'
            self.font_sans = 'LiberationSans'
            self.font_sans_bold = 'LiberationSans-Bold'
            self.font_mono = 'LiberationMono'
            self.font_dejavu = 'DejaVuSans'
            
            print("✓ Classic Microsoft fonts loaded successfully:")
            print("  Serif: Times New Roman, Georgia, Cambria")
            print("  Sans:  Arial, Calibri, Verdana, Trebuchet MS")
            print("  Plus:  Liberation & DejaVu families")
        except Exception as e:
            # Fallback to Helvetica (limited Cyrillic support)
            self.font_name = 'Helvetica'
            self.font_bold = 'Helvetica-Bold'
            self.font_italic = 'Helvetica-Oblique'
            self.font_sans = 'Helvetica'
            self.font_mono = 'Courier'
            print(f"⚠ Font loading error: {e}")
            print("⚠ Using Helvetica font (limited Cyrillic support)")

    def create_styles(self):
        """Create custom paragraph styles for Serbian text"""
        styles = getSampleStyleSheet()

        # Title style
        styles.add(ParagraphStyle(
            name='MuseumTitle',
            parent=styles['Heading1'],
            fontName=self.font_bold,
            fontSize=18,
            textColor=self.primary_color,
            alignment=TA_CENTER,
            spaceAfter=12,
            spaceBefore=12
        ))

        # Subtitle style
        styles.add(ParagraphStyle(
            name='MuseumSubtitle',
            parent=styles['Heading2'],
            fontName=self.font_bold,
            fontSize=14,
            textColor=self.secondary_color,
            alignment=TA_CENTER,
            spaceAfter=8,
            spaceBefore=8
        ))

        # Section heading
        styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=styles['Heading2'],
            fontName=self.font_bold,
            fontSize=12,
            textColor=self.primary_color,
            spaceAfter=6,
            spaceBefore=10
        ))

        # Normal Serbian text
        styles.add(ParagraphStyle(
            name='SerbianNormal',
            parent=styles['Normal'],
            fontName=self.font_name,
            fontSize=10,
            alignment=TA_LEFT
        ))

        # Small text for footers
        styles.add(ParagraphStyle(
            name='Footer',
            parent=styles['Normal'],
            fontName=self.font_name,
            fontSize=8,
            textColor=self.dark_gray,
            alignment=TA_CENTER
        ))

        return styles

    def add_header_footer(self, canvas_obj, doc):
        """Add header and footer to each page"""
        canvas_obj.saveState()

        # Header
        canvas_obj.setFont(self.font_bold, 14)
        canvas_obj.setFillColor(self.primary_color)
        canvas_obj.drawCentredString(A4[0] / 2, A4[1] - 1.5*cm, self.museum_name)

        canvas_obj.setFont(self.font_name, 9)
        canvas_obj.setFillColor(self.dark_gray)
        canvas_obj.drawCentredString(A4[0] / 2, A4[1] - 2*cm, self.museum_name_en)

        # Draw line under header
        canvas_obj.setStrokeColor(self.secondary_color)
        canvas_obj.setLineWidth(2)
        canvas_obj.line(2*cm, A4[1] - 2.5*cm, A4[0] - 2*cm, A4[1] - 2.5*cm)

        # Footer
        canvas_obj.setFont(self.font_name, 8)
        canvas_obj.setFillColor(self.dark_gray)
        footer_text = f"{self.museum_address} | {self.museum_phone} | {self.museum_email}"
        canvas_obj.drawCentredString(A4[0] / 2, 1.5*cm, footer_text)

        # Page number
        page_num = canvas_obj.getPageNumber()
        canvas_obj.drawRightString(A4[0] - 2*cm, 1*cm, f"Страна {page_num}")

        canvas_obj.restoreState()

    def create_pdf_buffer(self):
        """Create a BytesIO buffer for PDF"""
        return BytesIO()

    def safe_str(self, value):
        """Safely convert value to string, handling None and empty values"""
        if value is None or value == '':
            return 'Н/Д'  # Not Available in Serbian
        return str(value)


class CollectionPDFExporter(MuseumPDFExporter):
    """Export collection reports to PDF"""

    def export_collection(self, collection_name: str, specimens: List[Dict],
                         statistics: Optional[Dict] = None) -> BytesIO:
        """
        Export collection specimens to PDF

        Args:
            collection_name: Name of the collection in Serbian
            specimens: List of specimen dictionaries
            statistics: Optional statistics dictionary

        Returns:
            BytesIO buffer containing PDF
        """
        buffer = self.create_pdf_buffer()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=2*cm,
            rightMargin=2*cm,
            topMargin=3*cm,
            bottomMargin=2.5*cm
        )

        # Build document content
        story = []
        styles = self.create_styles()

        # Title
        story.append(Paragraph(f"Извештај о збирци", styles['MuseumTitle']))
        story.append(Paragraph(escape(self.safe_str(collection_name)), styles['MuseumSubtitle']))
        story.append(Spacer(1, 0.3*cm))

        # Generation date
        current_date = datetime.now().strftime("%d.%m.%Y %H:%M")
        story.append(Paragraph(
            f"<i>Извештај генерисан: {current_date}</i>",
            styles['SerbianNormal']
        ))
        story.append(Spacer(1, 0.5*cm))

        # Statistics section if provided
        if statistics:
            story.append(Paragraph("Статистика збирке", styles['SectionHeading']))

            stats_data = []
            for key, value in statistics.items():
                if key != 'specimens':  # Skip specimens list in statistics
                    label = self._format_stat_label(key)
                    stats_data.append([label, self.safe_str(value)])

            if stats_data:
                stats_table = Table(stats_data, colWidths=[10*cm, 7*cm])
                stats_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), self.light_gray),
                    ('TEXTCOLOR', (0, 0), (-1, -1), self.primary_color),
                    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                    ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                    ('FONTNAME', (0, 0), (-1, -1), self.font_name),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                    ('TOPPADDING', (0, 0), (-1, -1), 8),
                    ('GRID', (0, 0), (-1, -1), 0.5, self.dark_gray)
                ]))
                story.append(stats_table)
                story.append(Spacer(1, 0.5*cm))

        # Specimens section
        story.append(Paragraph(
            f"Узорци у збирци (укупно: {len(specimens)})",
            styles['SectionHeading']
        ))
        story.append(Spacer(1, 0.3*cm))

        # Create table for specimens (max 20 per page, then page break)
        for i, specimen in enumerate(specimens):
            if i > 0 and i % 15 == 0:
                story.append(PageBreak())

            specimen_table = self._create_specimen_table(specimen)
            story.append(specimen_table)
            story.append(Spacer(1, 0.4*cm))

        # Build PDF
        doc.build(story, onFirstPage=self.add_header_footer, onLaterPages=self.add_header_footer)
        buffer.seek(0)
        return buffer

    def _format_stat_label(self, key: str) -> str:
        """Format statistics label to Serbian"""
        labels = {
            'total_specimens': 'Укупно узорака',
            'total_species': 'Укупно врста',
            'endemic_species': 'Ендемичне врсте',
            'protected_species': 'Заштићене врсте',
            'herbarium_specimens': 'Хербаријски узорци',
            'curators': 'Кустоси',
            'last_updated': 'Последњe ажурирање'
        }
        return labels.get(key, key.replace('_', ' ').title())

    def _create_specimen_table(self, specimen: Dict) -> Table:
        """Create formatted table for a single specimen"""
        data = []

        # Add specimen fields
        for key, value in specimen.items():
            if key not in ['id', 'curator', 'created_at', 'updated_at']:
                label = self._format_field_label(key)
                data.append([label, self.safe_str(value)])

        table = Table(data, colWidths=[6*cm, 11*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), self.light_gray),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), self.font_bold),
            ('FONTNAME', (1, 0), (1, -1), self.font_name),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, self.dark_gray),
            ('VALIGN', (0, 0), (-1, -1), 'TOP')
        ]))

        return table

    def _format_field_label(self, key: str) -> str:
        """Format field names to Serbian labels"""
        labels = {
            'catalog_number': 'Каталошки број',
            'scientific_name': 'Научно име',
            'common_name_sr': 'Народно име',
            'family': 'Фамилија',
            'location_found': 'Локалитет',
            'altitude': 'Надморска висина',
            'date_collected': 'Датум прикупљања',
            'collector': 'Прикупио',
            'herbarium_number': 'Број херб.',
            'condition': 'Стање',
            'endemic_status': 'Статус ендемизма',
            'conservation_status': 'Статус заштите',
            'description': 'Опис',
            'species': 'Врста',
            'specimen_type': 'Тип узорка',
            'habitat': 'Станиште',
            'coordinates': 'Координате',
            'depth': 'Дубина',
            'water_body': 'Водено тело',
            'conservation_state': 'Стање',
            'conservation_treatment': 'Конзервација',
            'project_name': 'Пројекат',
            'dna_barcode': 'ДНК баркод',
            'tissue_type': 'Тип ткива'
        }
        return labels.get(key, key.replace('_', ' ').title())


class VisitorPDFExporter(MuseumPDFExporter):
    """Export visitor statistics to PDF"""

    def export_visitor_report(self, visitor_records: List[Dict],
                             date_from: Optional[str] = None,
                             date_to: Optional[str] = None) -> BytesIO:
        """
        Export visitor statistics report to PDF

        Args:
            visitor_records: List of visitor record dictionaries
            date_from: Start date for report (optional)
            date_to: End date for report (optional)

        Returns:
            BytesIO buffer containing PDF
        """
        buffer = self.create_pdf_buffer()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=2*cm,
            rightMargin=2*cm,
            topMargin=3*cm,
            bottomMargin=2.5*cm
        )

        story = []
        styles = self.create_styles()

        # Title
        story.append(Paragraph("Извештај о посетиоцима", styles['MuseumTitle']))

        # Date range
        if date_from and date_to:
            date_range = f"Период: {date_from} - {date_to}"
        else:
            date_range = "Период: Сви подаци"
        story.append(Paragraph(date_range, styles['MuseumSubtitle']))
        story.append(Spacer(1, 0.3*cm))

        # Generation date
        current_date = datetime.now().strftime("%d.%m.%Y %H:%M")
        story.append(Paragraph(
            f"<i>Извештај генерисан: {current_date}</i>",
            styles['SerbianNormal']
        ))
        story.append(Spacer(1, 0.5*cm))

        # Calculate statistics
        total_visitors = sum(r.get('number_of_visitors', 0) for r in visitor_records)
        total_revenue = sum(r.get('total_revenue', 0) for r in visitor_records)
        total_visits = len(visitor_records)

        # Visitor type breakdown
        visitor_types = {}
        for record in visitor_records:
            vtype = record.get('visitor_type', 'Непознато')
            visitor_types[vtype] = visitor_types.get(vtype, 0) + record.get('number_of_visitors', 0)

        # Summary statistics
        story.append(Paragraph("Сажетак статистике", styles['SectionHeading']))

        summary_data = [
            ['Укупно посета', str(total_visits)],
            ['Укупно посетилаца', f"{total_visitors:,}"],
            ['Укупан приход', f"{total_revenue:,.2f} РСД"],
            ['Просечно посетилаца по посети', f"{total_visitors/total_visits:.1f}" if total_visits > 0 else "0"],
            ['Просечан приход по посети', f"{total_revenue/total_visits:,.2f} РСД" if total_visits > 0 else "0 РСД"]
        ]

        summary_table = Table(summary_data, colWidths=[10*cm, 7*cm])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), self.light_gray),
            ('BACKGROUND', (1, 0), (1, -1), colors.white),
            ('TEXTCOLOR', (0, 0), (-1, -1), self.primary_color),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (0, -1), self.font_bold),
            ('FONTNAME', (1, 0), (1, -1), self.font_name),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, self.dark_gray)
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 0.5*cm))

        # Visitor type breakdown
        story.append(Paragraph("Посетиоци по типу", styles['SectionHeading']))

        type_data = [['Тип посетиоца', 'Број посетилаца', 'Проценат']]
        for vtype, count in sorted(visitor_types.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total_visitors * 100) if total_visitors > 0 else 0
            type_data.append([vtype, f"{count:,}", f"{percentage:.1f}%"])

        type_table = Table(type_data, colWidths=[9*cm, 4*cm, 4*cm])
        type_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.secondary_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), self.font_bold),
            ('FONTNAME', (0, 1), (-1, -1), self.font_name),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, self.dark_gray),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, self.light_gray])
        ]))
        story.append(type_table)
        story.append(Spacer(1, 0.5*cm))

        # Detailed visitor records
        story.append(PageBreak())
        story.append(Paragraph("Детаљни записи о посетама", styles['SectionHeading']))
        story.append(Spacer(1, 0.3*cm))

        for i, record in enumerate(visitor_records):
            if i > 0 and i % 5 == 0:
                story.append(PageBreak())

            record_table = self._create_visitor_record_table(record)
            story.append(record_table)
            story.append(Spacer(1, 0.4*cm))

        # Build PDF
        doc.build(story, onFirstPage=self.add_header_footer, onLaterPages=self.add_header_footer)
        buffer.seek(0)
        return buffer

    def _create_visitor_record_table(self, record: Dict) -> Table:
        """Create formatted table for a single visitor record"""
        data = [
            ['Датум', self.safe_str(record.get('date'))],
            ['Тип посетиоца', self.safe_str(record.get('visitor_type'))],
            ['Назив групе', self.safe_str(record.get('group_name'))],
            ['Број посетилаца', self.safe_str(record.get('number_of_visitors'))],
            ['Узрасна група', self.safe_str(record.get('age_group'))],
            ['Водич', self.safe_str(record.get('guide'))],
            ['Посећена изложба', self.safe_str(record.get('exhibition_visited'))],
            ['Трајање (мин)', self.safe_str(record.get('duration_minutes'))],
            ['Тип карте', self.safe_str(record.get('ticket_type'))],
            ['Приход (РСД)', self.safe_str(record.get('total_revenue'))],
        ]

        if record.get('educational_program'):
            data.append(['Едукативни програм', self.safe_str(record.get('educational_program'))])

        if record.get('feedback'):
            data.append(['Повратна информација', self.safe_str(record.get('feedback'))])

        table = Table(data, colWidths=[6*cm, 11*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), self.light_gray),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), self.font_bold),
            ('FONTNAME', (1, 0), (1, -1), self.font_name),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, self.dark_gray),
            ('VALIGN', (0, 0), (-1, -1), 'TOP')
        ]))

        return table


class ResearchPDFExporter(MuseumPDFExporter):
    """Export research project summaries to PDF"""

    def export_research_project(self, project: Dict) -> BytesIO:
        """
        Export single research project summary to PDF

        Args:
            project: Research project dictionary

        Returns:
            BytesIO buffer containing PDF
        """
        buffer = self.create_pdf_buffer()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=2*cm,
            rightMargin=2*cm,
            topMargin=3*cm,
            bottomMargin=2.5*cm
        )

        story = []
        styles = self.create_styles()

        # Title
        story.append(Paragraph("Извештај о истраживачком пројекту", styles['MuseumTitle']))
        story.append(Spacer(1, 0.5*cm))

        # Project title
        project_title = escape(self.safe_str(project.get('project_name', 'Без назива')))
        story.append(Paragraph(project_title, styles['MuseumSubtitle']))
        story.append(Spacer(1, 0.3*cm))

        # Generation date
        current_date = datetime.now().strftime("%d.%m.%Y %H:%M")
        story.append(Paragraph(
            f"<i>Извештај генерисан: {current_date}</i>",
            styles['SerbianNormal']
        ))
        story.append(Spacer(1, 0.5*cm))

        # Basic information
        story.append(Paragraph("Основне информације", styles['SectionHeading']))

        basic_data = [
            ['Руководилац пројекта', self.safe_str(project.get('principal_investigator'))],
            ['Период', f"{self.safe_str(project.get('start_year'))} - {self.safe_str(project.get('end_year'))}"],
            ['Статус', self.safe_str(project.get('status'))],
            ['Буџет', f"{self.safe_str(project.get('budget'))} РСД"],
            ['Број узорака', self.safe_str(project.get('specimens_studied'))],
            ['Теренски излети', self.safe_str(project.get('field_trips'))]
        ]

        basic_table = Table(basic_data, colWidths=[6*cm, 11*cm])
        basic_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), self.light_gray),
            ('TEXTCOLOR', (0, 0), (-1, -1), self.primary_color),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), self.font_bold),
            ('FONTNAME', (1, 0), (1, -1), self.font_name),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, self.dark_gray)
        ]))
        story.append(basic_table)
        story.append(Spacer(1, 0.5*cm))

        # Description
        if project.get('description'):
            story.append(Paragraph("Опис пројекта", styles['SectionHeading']))
            story.append(Paragraph(
                escape(self.safe_str(project.get('description'))),
                styles['SerbianNormal']
            ))
            story.append(Spacer(1, 0.5*cm))

        # Key findings
        if project.get('key_findings'):
            story.append(Paragraph("Кључна открића", styles['SectionHeading']))
            story.append(Paragraph(
                escape(self.safe_str(project.get('key_findings'))),
                styles['SerbianNormal']
            ))
            story.append(Spacer(1, 0.5*cm))

        # Publications
        if project.get('publications'):
            story.append(Paragraph("Публикације", styles['SectionHeading']))
            publications = project.get('publications', [])
            if isinstance(publications, str):
                publications = [publications]

            for pub in publications:
                story.append(Paragraph(f"• {escape(str(pub))}", styles['SerbianNormal']))
            story.append(Spacer(1, 0.5*cm))

        # Collaborators
        if project.get('collaborators'):
            story.append(Paragraph("Сарадници", styles['SectionHeading']))
            collaborators = project.get('collaborators', [])
            if isinstance(collaborators, str):
                collaborators = [collaborators]

            for collab in collaborators:
                story.append(Paragraph(f"• {escape(str(collab))}", styles['SerbianNormal']))
            story.append(Spacer(1, 0.5*cm))

        # International collaborations
        if project.get('international_collaborations'):
            story.append(Paragraph("Међународне сарадње", styles['SectionHeading']))
            collabs = project.get('international_collaborations', [])
            if isinstance(collabs, str):
                collabs = [collabs]

            for collab in collabs:
                story.append(Paragraph(f"• {escape(str(collab))}", styles['SerbianNormal']))
            story.append(Spacer(1, 0.5*cm))

        # Build PDF
        doc.build(story, onFirstPage=self.add_header_footer, onLaterPages=self.add_header_footer)
        buffer.seek(0)
        return buffer


class SpecimenCertificatePDFExporter(MuseumPDFExporter):
    """Export individual specimen certificates"""

    def export_specimen_certificate(self, specimen: Dict, collection_name: str) -> BytesIO:
        """
        Export specimen certificate/label to PDF

        Args:
            specimen: Specimen dictionary
            collection_name: Name of the collection

        Returns:
            BytesIO buffer containing PDF
        """
        buffer = self.create_pdf_buffer()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=2*cm,
            rightMargin=2*cm,
            topMargin=3*cm,
            bottomMargin=2.5*cm
        )

        story = []
        styles = self.create_styles()

        # Title
        story.append(Paragraph("Сертификат о узорку", styles['MuseumTitle']))
        story.append(Paragraph(escape(self.safe_str(collection_name)), styles['MuseumSubtitle']))
        story.append(Spacer(1, 0.5*cm))

        # Catalog number (prominent)
        catalog_num = specimen.get('catalog_number', specimen.get('inventarni_broj', 'Н/Д'))
        story.append(Paragraph(
            '<b>Каталошки број: ' + escape(str(catalog_num)) + '</b>',
            styles['SectionHeading']
        ))
        story.append(Spacer(1, 0.3*cm))

        # Generation date
        current_date = datetime.now().strftime("%d.%m.%Y %H:%M")
        story.append(Paragraph(
            f"<i>Сертификат генерисан: {current_date}</i>",
            styles['SerbianNormal']
        ))
        story.append(Spacer(1, 0.5*cm))

        # Specimen details
        story.append(Paragraph("Подаци о узорку", styles['SectionHeading']))

        # Build specimen data dynamically
        specimen_data = []
        field_labels = {
            'scientific_name': 'Научно име',
            'naziv': 'Назив',
            'common_name_sr': 'Народно име',
            'predmet': 'Предмет',
            'family': 'Фамилија',
            'location_found': 'Локалитет',
            'lokalitet': 'Локалитет',
            'altitude': 'Надморска висина',
            'date_collected': 'Датум прикупљања',
            'datum_nabavljanja': 'Датум набављања',
            'collector': 'Прикупио',
            'legator': 'Легатор/Нашао',
            'herbarium_number': 'Број херб.',
            'condition': 'Стање',
            'endemic_status': 'Статус ендемизма',
            'conservation_status': 'Статус заштите',
            'description': 'Опис',
            'komentar': 'Коментар',
            'napomena': 'Напомена',
            'species': 'Врста',
            'gde_se_nalazi': 'Где се налази',
            'kolicina': 'Количина',
            'nacin_nabavljanja': 'Начин набављања'
        }

        for key, value in specimen.items():
            if key in field_labels and value and value != '':
                specimen_data.append([field_labels[key], self.safe_str(value)])

        if specimen_data:
            specimen_table = Table(specimen_data, colWidths=[6*cm, 11*cm])
            specimen_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), self.light_gray),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), self.font_bold),
                ('FONTNAME', (1, 0), (1, -1), self.font_name),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, self.dark_gray),
                ('VALIGN', (0, 0), (-1, -1), 'TOP')
            ]))
            story.append(specimen_table)

        story.append(Spacer(1, 1*cm))

        # Certificate footer
        story.append(Paragraph(
            "Овај сертификат потврђује да се наведени узорак налази у збирци Природњачког музеја у Београду.",
            styles['SerbianNormal']
        ))
        story.append(Spacer(1, 0.5*cm))

        # Signature line
        story.append(Spacer(1, 2*cm))
        story.append(Paragraph("_" * 50, styles['SerbianNormal']))
        story.append(Paragraph("Кустос збирке", styles['SerbianNormal']))

        # Build PDF
        doc.build(story, onFirstPage=self.add_header_footer, onLaterPages=self.add_header_footer)
        buffer.seek(0)
        return buffer


# Convenience functions for easy import
def export_collection_pdf(collection_name: str, specimens: List[Dict],
                         statistics: Optional[Dict] = None) -> BytesIO:
    """Export collection to PDF"""
    exporter = CollectionPDFExporter()
    return exporter.export_collection(collection_name, specimens, statistics)


def export_visitor_report_pdf(visitor_records: List[Dict],
                              date_from: Optional[str] = None,
                              date_to: Optional[str] = None) -> BytesIO:
    """Export visitor report to PDF"""
    exporter = VisitorPDFExporter()
    return exporter.export_visitor_report(visitor_records, date_from, date_to)


def export_research_project_pdf(project: Dict) -> BytesIO:
    """Export research project to PDF"""
    exporter = ResearchPDFExporter()
    return exporter.export_research_project(project)


def export_specimen_certificate_pdf(specimen: Dict, collection_name: str) -> BytesIO:
    """Export specimen certificate to PDF"""
    exporter = SpecimenCertificatePDFExporter()
    return exporter.export_specimen_certificate(specimen, collection_name)
