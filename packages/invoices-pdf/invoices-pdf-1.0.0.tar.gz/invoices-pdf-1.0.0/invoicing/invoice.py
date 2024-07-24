import os
import pandas as pd
import glob
import fpdf
from pathlib import Path


def generate(invoices_path, pdf_path, product_id, image_path,
             product_name, amount_purchased, price_per_unit, user_price):
    """
    This function convert excel files in pdf invoices
    :param invoices_path:
    :param pdf_path:
    :param product_id:
    :param image_path:
    :param product_name:
    :param amount_purchased:
    :param price_per_unit:
    :param user_price:
    :return:
    """
    filepaths = glob.glob(f"{invoices_path}/*.xlsx")

    for filepath in filepaths:
        pdf = fpdf.FPDF("P", "mm", "A4")
        pdf.add_page()
        filename = Path(filepath).stem
        invoice_nr = filename.split("-")[0]
        date = filename.split("-")[1]

        pdf.set_font("Times", "B", size=16)
        pdf.cell(0.0, 10.0, f"Invoice nr: {invoice_nr}", align="L", ln=1)
        pdf.cell(0.0, 10.0, f"Date: {date}", align="L", ln=1)

        df = pd.read_excel(filepath, sheet_name="Sheet 1", engine="openpyxl")

        # Add the column headers
        columns = list(df.columns)
        columns = [item.replace("_", " ").title() for item in columns]
        pdf.set_font("Times", style="B", size=10)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(30.0, 8.0, txt=columns[0], border=1)
        pdf.cell(70.0, 8.0, txt=columns[1], border=1)
        pdf.cell(30.0, 8.0, txt=columns[2], border=1)
        pdf.cell(30.0, 8.0, txt=columns[3], border=1)
        pdf.cell(30.0, 8.0, txt=columns[4], ln=1, border=1)

        # Add the rows to the table
        total_price = 0
        for index, row in df.iterrows():
            price = row[user_price]
            total_price = total_price + price
            pdf.set_font("Times", style="", size=10)
            pdf.set_text_color(80, 80, 80)
            pdf.cell(30.0, 8.0, txt=str(row[product_id]), border=1)
            pdf.cell(70.0, 8.0, txt=str(row[product_name]),  border=1)
            pdf.cell(30.0, 8.0, txt=str(row[amount_purchased]), border=1)
            pdf.cell(30.0, 8.0, txt=str(row[price_per_unit]), border=1)
            pdf.cell(30.0, 8.0, txt=str(row[user_price]), ln=1,  border=1)

        # Add total
        pdf.set_font("Times", style="B", size=10)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(30.0, 8.0, txt="", border=1)
        pdf.cell(70.0, 8.0, txt="", border=1)
        pdf.cell(30.0, 8.0, txt="", border=1)
        pdf.cell(30.0, 8.0, txt="", border=1)
        pdf.cell(30.0, 8.0, txt=str(total_price), ln=1, border=1)

        # add total sum sentence
        pdf.set_font("Times", style="B", size=10)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(0.0, 20.0, f"The total due amount is {total_price} Euros."
                 , ln=1)

        ## add company image logo
        pdf.cell(25.0, 5.0, f"PythonHow")
        pdf.image(image_path,  w=5.0, h=5.0)

        if not os.path.exists(pdf_path):
            os.makedirs(pdf_path)
        pdf.output(f"{pdf_path}/{filename}.pdf")


