from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import qrcode

def generate_pdf_with_qr_and_text(template_path, pdf_path, payment_id, honorific, first_name, middle_name, last_name, city, state):
    try:
        c = canvas.Canvas(pdf_path, pagesize=letter)

        # Load the template image
        c.drawImage(template_path, 0, 0, width=letter[0], height=letter[1])

        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=1,
        )
        qr.add_data(payment_id)
        qr_img = qr.make_image(fill_color="#0b212f", back_color="#fdbd19")

        # Save the QR code to a temporary file
        qr_img_path = f"./images/{payment_id}.png"
        qr_img.save(qr_img_path)

        # Draw the QR code onto the canvas
        qr_size = 1.9 * inch
        qr_x, qr_y = 1.5 * inch, 10.5 * inch
        c.drawImage(qr_img_path, 237, 280, width=qr_size, height=qr_size)

        # Calculate the width of the name string
        name_string = ""
        if middle_name == "":
            name_string = f"{honorific}.{first_name} {last_name}".upper()
        else:
            name_string = f"{honorific}.{first_name} {middle_name} {last_name}".upper()
        font_size_name = 0
        if len(name_string) > 25:
            font_size_name = 12
        elif len(name_string) > 19:
            font_size_name = 15
        else:
            font_size_name = 18
        
        name_width = c.stringWidth(name_string, "Courier-Bold", font_size_name)
        
        # Calculate the x-coordinate dynamically based on the length of the name string
        x_coordinate_name = (letter[0] - name_width) / 2

        # Draw text
        c.setFont("Courier-Bold", font_size_name)
        c.drawString(x_coordinate_name, 180 + 0.5 * inch, name_string)
        

        from_string = f"{city},{state}".upper()
        font_size_from = 10
        
        
        from_width = c.stringWidth(from_string, "Courier-Bold", font_size_from)
        
        # Calculate the x-coordinate dynamically based on the length of the 'from' string
        x_coordinate_from = (letter[0] - from_width) / 2

        
        c.setFont("Courier-Bold", 10)
        c.drawString(x_coordinate_from, 160 + 0.5 * inch, from_string)
        
        c.save()
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    


