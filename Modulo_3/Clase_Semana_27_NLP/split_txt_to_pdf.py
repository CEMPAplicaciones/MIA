
import os
from math import ceil
import argparse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def split_file_to_pdfs(input_file, num_splits=5, output_dir='.', prefix='part_', page_size=letter, margin_inch=1.0, line_height_pt=14):
    """
    Splits a text file into a specified number of PDF files.

    Parameters:
      input_file    Path to the original text file.
      Num_splits Number of PDF parts to generate.
      Output_dir Directory where the PDF files will be saved.
      Prefix Filename prefix for each PDF (e.g., 'part_' yields 'part_1.pdf').
      Page_size Tuple defining PDF page size in points (default is letter).
      Margin_inch Margin around text in inches (default 1").
      Line_height_pt Line spacing in points (default 14).
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Count total lines
    with open(input_file, 'r', encoding='utf-8') as f:
        total_lines = sum(1 for _ in f)
    if total_lines == 0:
        raise ValueError("Input file is empty.")

    # Determine lines per PDF
    lines_per_file = ceil(total_lines / num_splits)

    # Convert margin to points (1 inch = 72 points)
    margin = margin_inch * 72
    page_width, page_height = page_size

    # Split and write
    with open(input_file, 'r', encoding='utf-8') as f:
        for part in range(1, num_splits + 1):
            pdf_path = os.path.join(output_dir, f"{prefix}{part}.pdf")
            c = canvas.Canvas(pdf_path, pagesize=page_size)
            y = page_height - margin

            for _ in range(lines_per_file):
                line = f.readline()
                if not line:
                    break
                # Page break if we run out of vertical space
                if y < margin:
                    c.showPage()
                    y = page_height - margin
                # Draw the line of text
                c.drawString(margin, y, line.rstrip())
                y -= line_height_pt

            c.save()
            print(f"Created {pdf_path}")


input_file = "/Users/jsilva/repositories/MIA/Modulo_3/Clase_Semana_27_NLP/codiesp_codes/CIE10_procedure_codes.txt"
output_dir = "/Users/jsilva/repositories/MIA/Modulo_3/Clase_Semana_27_NLP/codiesp_codes"
prefix = "CIE10_procedure_codes_"
split_file_to_pdfs(input_file, num_splits=5, output_dir=output_dir, prefix=prefix)

