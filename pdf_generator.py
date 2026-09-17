from fpdf import FPDF

class ItineraryPDF(FPDF):
    def header(self):
        # Header title
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(15, 23, 42)
        self.cell(0, 10, "AI Travel Itinerary", 0, 1, "C")
        self.ln(5)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

def clean_text(text):
    if not text:
        return ""
    # Replace unsupported characters for standard FPDF fonts
    return str(text).encode('latin-1', 'replace').decode('latin-1')

def create_itinerary_pdf(itinerary):
    pdf = ItineraryPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Summary Section
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(15, 23, 42)
    
    destination = getattr(itinerary, 'destination', 'Trip')
    duration = getattr(itinerary, 'duration_days', 'N/A')
    budget = getattr(itinerary, 'estimated_cost', 'N/A')
    
    pdf.cell(0, 8, clean_text(f"Destination: {destination}"), 1, True)
    pdf.cell(0, 8, clean_text(f"Duration: {duration} Days"), 1, True)
    pdf.cell(0, 8, clean_text(f"Estimated Budget: {budget}"), 1, True)
    pdf.ln(5)

    # Days Breakdown
    if hasattr(itinerary, 'days'):
        for day in itinerary.days:
            pdf.set_font("Helvetica", "B", 14)
            pdf.set_fill_color(230, 230, 230)
            theme = getattr(day, 'theme', '')
            pdf.cell(0, 10, clean_text(f"Day {day.day_number}: {theme}"), 1, True, fill=True)
            pdf.ln(3)

            for activity in day.activities:
                pdf.set_font("Helvetica", "B", 10)
                time_slot = getattr(activity, 'time_slot', '')
                loc_name = getattr(activity, 'location_name', '')
                pdf.cell(0, 6, clean_text(f"- {time_slot} - {loc_name}"), 1, True)

                pdf.set_font("Helvetica", "", 10)
                desc = getattr(activity, 'description', '')
                pdf.multi_cell(0, 5, clean_text(desc))
                
                cost = getattr(activity, 'estimated_cost', None)
                if cost:
                    pdf.set_font("Helvetica", "I", 9)
                    pdf.cell(0, 5, clean_text(f"Cost: {cost}"), 1, True)
                pdf.ln(2)

            pdf.ln(4)

    return pdf.output(dest='S').encode('latin1')
