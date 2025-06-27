from fpdf import FPDF
import os

def generate_pdf(image_dir, output_pdf, image_filter=None):
    pdf = FPDF()
    image_files = [f for f in os.listdir(image_dir) if f.endswith('.png')]

    if image_filter:
        image_files = [f for f in image_files if image_filter in f]

    if not image_files:
        print("⚠ No matching PNG files found in the directory.")
        return

    for img in sorted(image_files):
        pdf.add_page()
        pdf.image(os.path.join(image_dir, img), x=10, y=10, w=190)
    
    pdf.output(output_pdf)
    print(f" PDF report saved to {output_pdf}")
