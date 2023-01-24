import os

from PIL import Image
from fpdf import FPDF


def SaveReport(FigArray, name):
    pdf = FPDF()
    logo = Image.open(r"IMAGES/LOGO.png").convert("RGBA")
    logo_M = Image.open(r"IMAGES/LOGO_MAIN.png").convert("RGBA")
    for plot in FigArray:
        try:
            plot.write_image("IMAGES/" + str(FigArray.index(plot)) + ".png", width=1122.5 * 2, height=794 * 2)
            cover = Image.open('IMAGES/' + str(FigArray.index(plot)) + ".png")
            cover.paste(logo, (20, 765 * 2,), logo)
            cover.paste(logo_M, (465 * 2, 30,), logo_M)
            cover.save("IMAGES/" + str(FigArray.index(plot)) + ".png", format='png')
            width, height = cover.size

            # convert pixel in mm with 1px=0.264583 mm
            width, height = float(width * 0.264583), float(height * 0.264583)

            # given we are working with A4 format size
            pdf_size = {'P': {'w': 210, 'h': 297}, 'L': {'w': 297, 'h': 210}}

            # get page orientation from image size
            orientation = 'P' if width < height else 'L'

            #  make sure image size is not greater than the pdf format size
            width = width if width < pdf_size[orientation]['w'] else pdf_size[orientation]['w']
            height = height if height < pdf_size[orientation]['h'] else pdf_size[orientation]['h']

            pdf.add_page(orientation=orientation)

            pdf.image('IMAGES/' + str(FigArray.index(plot)) + ".png", 0, 0, width, height)
        except:
            print("No data!")
    pdf.output("temp/" +str(name)+".pdf", "F")
