from fpdf import FPDF
from schemas import ItineraryResponse

class ItineraryPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 10, "AI Travel Itinerary", border=False, ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def clean_text(text: str) -> str:
    """Replaces Unicode symbols and bullets unsupported by standard Helvetica."""
    if not text:
        return ""
    
    # Replace non-ASCII symbols with standard text equivalents
    replacements = {
        "•": "-",
        "₹": "INR ",
        "€": "EUR ",
        "£": "GBP ",
        "–": "-",
        "—": "-",
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'"
    }
    
    for key, val in replacements.items():
        text = text.replace(key, val)
        
    # Ensure all remaining string characters fall within latin-1 range
    return text.encode('latin-1', 'replace').decode('latin-1')

def create_itinerary_pdf(itinerary):
    pdf = ItineraryPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Summary Section
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, clean_text(f"Destination: {itinerary.destination}"), ln=True)
    pdf.cell(0, 8, f"Duration: {itinerary.duration_days} Days", ln=True)
    pdf.cell(0, 8, clean_text(f"Estimated Budget: {itinerary.estimated_cost}"), ln=True)
    pdf.ln(5)

    # Days Breakdown
    for day in itinerary.days:
        pdf.set_font("Helvetica", "B", 14)
        pdf.set_fill_color(230, 230, 230)
        pdf.cell(0, 10, clean_text(f"Day {day.day_number}: {day.theme}"), ln=True, fill=True)
        pdf.ln(3)

        for activity in day.activities:
            pdf.set_font("Helvetica", "B", 10)
            pdf.cell(0, 6, clean_text(f"- {activity.time_slot} - {activity.location_name}"), ln=True)
            
            pdf.set_font("Helvetica", "", 10)
            pdf.multi_cell(0, 5, clean_text(activity.description))
            pdf.set_font("Helvetica", "I", 9)
            pdf.cell(0, 5, clean_text(f"Cost: {activity.estimated_cost}"), ln=True)
            pdf.ln(2)

        pdf.ln(4)

      return pdf.output(dest='S').encode('latin1')
