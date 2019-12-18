# ---------------------------------------------------------------------------------------------------------------------------
# This is python authomatization script for grabbing information about your documents ID case from the website kiew.diplo.de
# You can use Libriry called shedule to make reports every day  bitween 8:00-9:00 (Kyiv -1 timezone)
# on your own webserver 
# or make check manualy
# You can use the copy of this script as you wish and share it with somebody. Im' not care, no big deal
# 18 december 2019 by Elisei Paniv, Kyiv, Ukraine
# ---------------------------------------------------------------------------------------------------------------------------
import requests
import io
import os
from bs4 import BeautifulSoup as bs
from datetime import datetime
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from telebot import telegram_bot_sendtext

# define the URL to crawl & parse

app_url = 'https://kiew.diplo.de/ua-uk/service/05-VisaEinreise/teaser-abholbereite-visa/1241142'


# crawling the page. This might take a few seconds
page = requests.get( app_url )

#Using soup and requests to get right and new daily PDF version from website
soap = bs(page.content, 'html.parser')

# Base website URL
baseUrl = "https://kiew.diplo.de"
#find anchor for grepping right URL of the PDF

link = soap.find("a", class_="rte__anchor i-pdf")
getPdf = baseUrl + link.get('href')

#Getting  New PDF
myfile = requests.get(getPdf)
a = datetime.now()
datt = str(int(a.timestamp()))

# Debugging timestamp - print(datt)

savePath = "c:/Data/python/parser/downloads/" + datt + "_pdf-abholbereite-visa-neu-data.pdf"

# Debugging path for saved file print(savePath)

# Writing the content of PDF to file in subdirectory /downloads
open(savePath, 'wb').write(myfile.content)

# Put your number at Deutsch diplo.de website here
myNumer = str(1234567) # This is example number! Put you own number here!

# Using pdfMiner.six for extracting PDF to text

def extract_text_from_pdf(pdf_path):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)

        text = fake_file_handle.getvalue()

    # close open handles
    converter.close()
    fake_file_handle.close()

    if text:
        return text

if __name__ == '__main__':
    PDFtextblob = extract_text_from_pdf(savePath)

# if number exists, find it and get result
if PDFtextblob.find(myNumer) != -1:
    print('Номер ' + myNumer + ' знайдено в файлі!')
    print('Відправляємо повідомлення на вказану e-mail адресу!')
    telegram_bot_sendtext("Ваш ID " + myNumer +" знайдено за посиланням" + getPdf + "!")
# If not - stuck with error and remove temporary file
else:
    print('Номер ' + myNumer + ' не знайдено в файлі! Видаляємо')
    os.remove(savePath)
    print("Файл PDF видалено!")
    telegram_bot_sendtext("Ваш ID " + myNumer +" не знайдено за посиланням" + getPdf + "!")