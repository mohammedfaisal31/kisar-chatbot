from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

def write_qr_to_pdf(source_canvas_path, img_path, destination_path, x, y, w, h):
    # Open the template image to get its dimensions
    with open(source_canvas_path, 'rb') as template_file:
        img = ImageReader(template_file)
        width, height = img.getSize()
        print(img.getSize())

    # Create a canvas with dimensions matching the template image
    c = canvas.Canvas(destination_path, pagesize=(width, height))
    
    # Load your PDF template
    c.drawImage(source_canvas_path, 0, 0, width, height)  # Place the template at the bottom-left corner
    
    # Load your QR code image
    c.drawImage(img_path, x, y, width=w, height=h)  # Position QR code based on x, y, w, h
 
    c.save()
def write_text_to_pdf(source_canvas_path, img_path, destination_path, x, y, w, h):
    # Open the template image to get its dimensions
    with open(source_canvas_path, 'rb') as template_file:
        img = ImageReader(template_file)
        width, height = img.getSize()
        print(img.getSize())

    # Create a canvas with dimensions matching the template image
    c = canvas.Canvas(destination_path, pagesize=(width, height))
    
    # Load your PDF template
    c.drawImage(source_canvas_path, 0, 0, width, height)  # Place the template at the bottom-left corner
    
    # Draw three lines of black text
    c.setFont("Helvetica", 32)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(x,y,"")
    
    c.save()

write_text_to_pdf("./images/canvas.jpg","","./images/written_canvas.pdf",500,300,100,100)

