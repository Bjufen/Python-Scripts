from io import BytesIO

import fitz  # PyMuPDF
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


# Function to extract specific images from specified pages and save to a directory
def extract_and_save_specific_images(pdf_path, output_directory, selected_pages):
    pdf_document = fitz.open(pdf_path)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    for i, page_num in enumerate(selected_pages):
        adjusted_page_num = page_num - 1  # Adjust the page number for indexing
        if adjusted_page_num <= pdf_document.page_count - 1:
            page = pdf_document.load_page(adjusted_page_num)
            image_list = page.get_images(full=True)
            if image_list:  # Check if there are images on the page
                xref = image_list[0][0]  # Extract the first image on the page
                base_image = pdf_document.extract_image(xref)
                image_bytes = base_image["image"]
                image_path = os.path.join(output_directory, f'image_{i}_0.png')
                with open(image_path, "wb") as image_file:
                    image_file.write(image_bytes)


# Modify extract_and_save_specific_images to return a list of image bytes
def extract_and_return_images(pdf_path, selected_pages):
    pdf_document = fitz.open(pdf_path)
    extracted_images = []
    for page_num in selected_pages:
        adjusted_page_num = page_num - 1
        if adjusted_page_num <= pdf_document.page_count - 1:
            page = pdf_document.load_page(adjusted_page_num)
            image_list = page.get_images(full=True)
            if image_list:
                xref = image_list[0][0]
                base_image = pdf_document.extract_image(xref)
                image_bytes = base_image["image"]
                extracted_images.append(image_bytes)
    return extracted_images


def extract_text_from_pages(pdf_path, selected_pages):
    pdf_document = fitz.open(pdf_path)
    extracted_text = []
    for page_num in selected_pages:
        adjusted_page_num = page_num - 1  # Adjust the page number for indexing
        if adjusted_page_num <= pdf_document.page_count - 1:
            page = pdf_document.load_page(adjusted_page_num)
            text = page.get_text("text")
            extracted_text.append(text)
    return extracted_text


def extract_names_ages(text_list):
    names_ages = []
    for string in text_list:
        s = string.split('\n')
        name_age = s[11:-3]
        if len(name_age) == 3:
            name_age = [name_age[0] + name_age[1], name_age[2]]
            cleaned_data = [name_age[0].replace(',', ''), name_age[1].replace('.', '')]
        elif len(name_age) == 5:
            temp = name_age[4][1:-1]
            temp1 = ', '.join(temp.split(','))
            cleaned_data = [name_age[2][:-2] + ' & ' + name_age[3] + ' ' + name_age[0][:-1], temp1]
        elif len(name_age) == 6:
            cleaned_data = [name_age[0] + name_age[1] + name_age[2][:-1] + name_age[3].replace(',', ''),
                            name_age[4] + name_age[5].replace('.', '')]
        else:
            cleaned_data = [name_age[0].replace(',', ''), name_age[1].replace('.', '')]
        cleaned_data[1] = cleaned_data[1].replace('years old', 'Jahre alt')
        cleaned_data[1] = cleaned_data[1].replace('year old', 'Jahr alt')
        cleaned_data[1] = cleaned_data[1].replace('months old', 'Monate alt')
        cleaned_data[1] = cleaned_data[1].replace('month old', 'Monate alte')
        cleaned_data[1] = cleaned_data[1].replace('quadruplets', 'Vierlinge')
        cleaned_data[0] = cleaned_data[0].replace('al-', 'Al-')
        cleaned_data[0] = cleaned_data[0].replace('-d', '-D')
        names_ages.append(cleaned_data)
    return names_ages


def create_pdf(data):
    extract_and_save_specific_images(input_pdf_path, output_directory, selected_pages)
    c = canvas.Canvas("resources/out/pdfs/output1.pdf", pagesize=letter)
    if not os.path.exists("resources/out/pdfs"):
        os.makedirs("resources/out/pdfs")
    pdfmetrics.registerFont(TTFont('FiraCode-SemiBold', 'resources/in/FiraCode-SemiBold.ttf'))
    pdfmetrics.registerFont(TTFont('FiraCode-Regular', 'resources/in/FiraCode-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('FiraCode-Light', 'resources/in/FiraCode-Light.ttf'))
    flag_path = 'resources/in/Flag.png'

    # Coordinates for placement
    x_center = letter[0] / 2
    y_top = letter[1] - 0.75 * inch

    for index, person in enumerate(data):

        # Draw flag at the top center
        c.drawImage(flag_path, x_center - (2 * inch), y_top - 1.5 * inch, width=4 * inch, height=2 * inch)

        # Load and resize the image
        image_path = f'resources/out/images/image_{index}_0.png'

        # Load and place the resized image
        c.drawImage(image_path, x_center - (3 * inch), y_top - (8 * inch), width=6 * inch, height=6 * inch)

        # Set font size and draw name
        c.setFont('FiraCode-SemiBold', 36)
        if len(person[0]) > 27:
            # Handling longer names by finding the last space within the character limit
            last_space_index = person[0][:27].rfind(' ')
            if last_space_index != -1:
                lines = [person[0][:last_space_index], person[0][last_space_index + 1:]]
                c.drawCentredString(x_center, y_top - (8.625 * inch), lines[0])
                c.drawCentredString(x_center, y_top - (9.25 * inch), lines[1])
            else:
                # No space found within the character limit, break at the character limit
                lines = [person[0][:27], person[0][27:]]
                c.drawCentredString(x_center, y_top - (8.625 * inch), lines[0])
                c.drawCentredString(x_center, y_top - (9.25 * inch), lines[1])
            c.setFont('FiraCode-Regular', 20)
            c.drawCentredString(x_center, y_top - (9.75 * inch), person[1])

            c.setFont('FiraCode-Light', 6)
            c.drawCentredString(x_center, y_top - (10 * inch), "freepalestineprinting.com")
        else:
            c.drawCentredString(x_center, y_top - (8.75 * inch), person[0])
            c.setFont('FiraCode-Regular', 20)
            c.drawCentredString(x_center, y_top - (9.25 * inch), person[1])

            c.setFont('FiraCode-Light', 6)
            c.drawCentredString(x_center, y_top - (9.75 * inch), "freepalestineprinting.com")
        # Add a new page if not the last entry
        if index != len(data) - 1:
            c.showPage()

    c.save()


# Modify create_pdf to use the list of image bytes directly
def create_pdf_2(data, images):
    c = canvas.Canvas("resources/out/pdfs/output2.pdf", pagesize=letter)
    if not os.path.exists("resources/out/pdfs"):
        os.makedirs("resources/out/pdfs")
    pdfmetrics.registerFont(TTFont('FiraCode-SemiBold', 'resources/in/FiraCode-SemiBold.ttf'))
    pdfmetrics.registerFont(TTFont('FiraCode-Regular', 'resources/in/FiraCode-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('FiraCode-Light', 'resources/in/FiraCode-Light.ttf'))
    flag_path = 'resources/in/Flag.png'

    x_center = letter[0] / 2
    y_top = letter[1] - 0.75 * inch

    for index, person in enumerate(data):
        c.drawImage(flag_path, x_center - (2 * inch), y_top - 1.5 * inch, width=4 * inch, height=2 * inch)

        # Use the image bytes directly from the list
        if index < len(images):
            image_bytes = images[index]
            c.drawImage(ImageReader(BytesIO(image_bytes)), x_center - (3 * inch), y_top - (8 * inch), width=6 * inch,
                        height=6 * inch)

        c.setFont('FiraCode-SemiBold', 36)
        if len(person[0]) > 27:
            # Handling longer names by finding the last space within the character limit
            last_space_index = person[0][:27].rfind(' ')
            if last_space_index != -1:
                lines = [person[0][:last_space_index], person[0][last_space_index + 1:]]
                c.drawCentredString(x_center, y_top - (8.625 * inch), lines[0])
                c.drawCentredString(x_center, y_top - (9.25 * inch), lines[1])
            else:
                # No space found within the character limit, break at the character limit
                lines = [person[0][:27], person[0][27:]]
                c.drawCentredString(x_center, y_top - (8.625 * inch), lines[0])
                c.drawCentredString(x_center, y_top - (9.25 * inch), lines[1])
            c.setFont('FiraCode-Regular', 20)
            c.drawCentredString(x_center, y_top - (9.75 * inch), person[1])

            c.setFont('FiraCode-Light', 6)
            c.drawCentredString(x_center, y_top - (10 * inch), "freepalestineprinting.com")
        else:
            c.drawCentredString(x_center, y_top - (8.75 * inch), person[0])
            c.setFont('FiraCode-Regular', 20)
            c.drawCentredString(x_center, y_top - (9.25 * inch), person[1])

            c.setFont('FiraCode-Light', 6)
            c.drawCentredString(x_center, y_top - (9.75 * inch), "freepalestineprinting.com")
        if index != len(data) - 1:
            c.showPage()
    c.save()


if __name__ == "__main__":
    # Input file path
    input_pdf_path = "resources/in/MurderedByIsrael-Web.pdf"  # Replace with your input PDF file path
    output_directory = "resources/out/images"  # Output directory for extracted images
    selected_pages = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21, 23, 25, 26, 27, 28, 34, 36,
                      39, 40, 42, 44, 45, 46, 47, 48, 50, 51, 53, 54, 57, 58, 60, 63, 68, 69, 71, 72, 73, 75, 76, 79,
                      81, 82, 83, 84, 86, 88, 91, 92, 93, 95, 96, 101, 102, 104, 105, 106, 107, 108, 110, 111, 112, 113,
                      114, 115, 116, 117, 119, 120, 121, 122, 123, 124, 125, 128, 129, 130, 132, 133, 136, 137, 139,
                      141, 142, 144, 146, 147, 148, 149, 150]

    create_pdf(
        extract_names_ages(extract_text_from_pages(input_pdf_path, selected_pages)))  # saves images before reusing them
    create_pdf_2(extract_names_ages(extract_text_from_pages(input_pdf_path, selected_pages)),
                 extract_and_return_images(input_pdf_path,
                                           selected_pages))  # does not save the images, but stores them temporarily

    # test = extract_names_ages(extract_text_from_pages(input_pdf_path,selected_pages))
    #extract_and_save_specific_images(input_pdf_path, output_directory, selected_pages)
