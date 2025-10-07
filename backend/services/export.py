from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from flask import send_file


def generate_pdf_report(title: str, summary: dict):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 50
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, y, title)
    y -= 30

    c.setFont("Helvetica", 12)
    for k, v in summary.items():
        line = f"{k}: {v}"
        c.drawString(50, y, line[:100])
        y -= 18
        if y < 50:
            c.showPage()
            y = height - 50

    c.showPage()
    c.save()
    buffer.seek(0)
    return send_file(buffer, mimetype="application/pdf", as_attachment=True, download_name="wildsync_report.pdf")
