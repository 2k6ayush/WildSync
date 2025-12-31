from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_pdf(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Forest Data Report - WildSync Sample")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, "Forest ID: F-2025-001")
    c.drawString(50, height - 100, "Location: 28.5983 N, 83.9310 E (Annapurna Conservation Area)")
    c.drawString(50, height - 120, "Date: 2025-10-01")

    c.line(50, height - 130, width - 50, height - 130)

    y = height - 160
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Ecosystem Metrics")
    y -= 20
    c.setFont("Helvetica", 12)
    c.drawString(50, y, "- Tree Count: 12,500")
    y -= 15
    c.drawString(50, y, "- Dominant Species: Rhododendron, Oak")
    y -= 15
    c.drawString(50, y, "- Canopy Cover: 75%")
    y -= 15
    c.drawString(50, y, "- Soil pH: 6.2 (Slightly Acidic)")
    y -= 15
    c.drawString(50, y, "- Soil Moisture: 45%")

    y -= 40
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Wildlife Sightings (Recent)")
    y -= 20
    c.setFont("Helvetica", 12)
    c.drawString(50, y, "- Snow Leopard: 2 sightings")
    y -= 15
    c.drawString(50, y, "- Himalayan Monal: 15 sightings")
    y -= 15
    c.drawString(50, y, "- Red Panda: 1 sighting")

    y -= 40
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Risk Factors")
    y -= 20
    c.setFont("Helvetica", 12)
    c.drawString(50, y, "- Landslide Probability: Moderate (East Slope)")
    y -= 15
    c.drawString(50, y, "- Illegal Logging Activity: Low")

    c.save()
    print(f"Generated {filename}")

if __name__ == "__main__":
    create_pdf("sample_forest_data.pdf")
