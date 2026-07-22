from fpdf import FPDF
import arabic_reshaper
from bidi.algorithm import get_display

words = [("Time", "وقت"), ("Love", "حب"), ("Book", "كتاب"), ("Cat", "قطة")]

pdf = FPDF()
pdf.add_page()
pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)  # Ensure the font file exists
pdf.set_font("DejaVu", "", 12)

# Header row
pdf.cell(60, 10, "English Word", 1, 0, 'C')
pdf.cell(60, 10, get_display(arabic_reshaper.reshape("المعنى بالعربية")), 1, 1, 'C')

# Data rows
for word, meaning in words:
    reshaped = get_display(arabic_reshaper.reshape(meaning))
    pdf.cell(60, 10, word, 1, 0, 'C')
    pdf.cell(60, 10, reshaped, 1, 1, 'C')

# Output the PDF
pdf.output("output.pdf")