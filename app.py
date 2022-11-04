#!/usr/bin/env python3
from fastapi import FastAPI

from PyPDF2 import PdfReader, PdfWriter

app = FastAPI()

@app.post('/pdf/{pdf_file}')
def rotate(pdf_file_path: str, page_no: int, rotation: int):

    reader = PdfReader(pdf_file_path)
    writer = PdfWriter()

    pdf_file = ""
    for path in pdf_file_path[::-1]:
        if path == '/':
            break;
        pdf_file = pdf_file + path
    pdf_file = pdf_file[::-1]

    if page_no > len(reader.pages):
        return "Page No. outside of length"

    page_no = page_no - 1

    if rotation%90 != 0:
        return "Rotation is not a multiple of 90"

    for page in reader.pages:
        if page == reader.pages[page_no]:
            page.rotate(rotation)
        writer.add_page(page)

    output_file = "/tmp/" + "output_" + pdf_file

    with open(output_file, "wb") as file:
        writer.write(file)

    return output_file
