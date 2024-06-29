from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import qrcode
from PIL import Image, ImageDraw, ImageFont

def generate_pdf_with_qr_and_text(template_path, pdf_path, payment_id, honorific, first_name, middle_name, last_name, city, state):
    try:
        c = canvas.Canvas(pdf_path, pagesize=letter)
        print(pdf_path)
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
        print("Saved pdf")
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    

def generate_badge_with_qr_and_text(template_path, out_img_path, payment_id, honorific, first_name, middle_name, last_name, city, state):
    try:
        # Load the template image
        template = Image.open(template_path).convert("RGBA")
        draw = ImageDraw.Draw(template)

        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=1,
        )
        qr.add_data(payment_id)
        qr_img = qr.make_image(fill_color="#0b212f", back_color="#fdbd19").convert("RGBA")

        # Paste the QR code onto the template
        qr_size = (int(1.9 * inch), int(1.9 * inch))
        qr_img = qr_img.resize(qr_size, Image.ANTIALIAS)
        qr_x, qr_y = 237, 280
        template.paste(qr_img, (qr_x, qr_y), qr_img)

        # Prepare the name and location strings
        if middle_name:
            name_string = f"{honorific}.{first_name} {middle_name} {last_name}".upper()
        else:
            name_string = f"{honorific}.{first_name} {last_name}".upper()

        from_string = f"{city}, {state}".upper()

        # Load a font
        font_size_name = 18 if len(name_string) <= 19 else 15 if len(name_string) <= 25 else 12
        font = ImageFont.truetype("arial.ttf", font_size_name)
        font_from = ImageFont.truetype("arial.ttf", 10)

        # Calculate text position
        name_width, name_height = draw.textsize(name_string, font=font)
        from_width, from_height = draw.textsize(from_string, font=font_from)
        
        x_coordinate_name = (template.width - name_width) / 2
        y_coordinate_name = 180 + int(0.5 * inch)

        x_coordinate_from = (template.width - from_width) / 2
        y_coordinate_from = 160 + int(0.5 * inch)

        # Draw the text onto the template
        draw.text((x_coordinate_name, y_coordinate_name), name_string, font=font, fill="black")
        draw.text((x_coordinate_from, y_coordinate_from), from_string, font=font_from, fill="black")

        # Save the final image
        template.save(out_img_path)
        print("Saved image")
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


