import requests
import io
import os
import schedule
import time
from bs4 import BeautifulSoup as bs
from datetime import datetime
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from telebot import telegram_bot_sendtext
#----------------------------------------------------------------------------------------------
#define Variables and functions
app_url = 'https://kiew.diplo.de/ua-uk/service/05-VisaEinreise/teaser-abholbereite-visa/1241142'
# Base website URL
baseUrl = "https://kiew.diplo.de"
#find anchor for grepping right URL of the PDF
# Put your number at Deutsch diplo.de website here
myNumer = str(1914132) # This is example number! Put you own number here!

#----------------------------------------------------------------------------------------------
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

def check_my_id():
    page = requests.get(app_url)
    #Using soup and requests to get right and new daily PDF version from website
    soap = bs(page.content, 'html.parser')
    link = soap.find("a", class_="rte__anchor i-pdf")
    getPdf = baseUrl + link.get('href')
    #Getting  New PDF
    myfile = requests.get(getPdf)
    a = datetime.now()
    datt = str(int(a.timestamp()))
    savePath = "c:/Data/python/parser/downloads/" + datt + "_pdf-abholbereite-visa-neu-data.pdf"
    # Writing the content of PDF to file in subdirectory /downloads
    open(savePath, 'wb').write(myfile.content)
    # Using pdfMiner.six for extracting PDF to text
    if __name__ == '__main__':
        PDFtextblob = extract_text_from_pdf(savePath)
    # if number exists, find it and get result
    if PDFtextblob.find(myNumer) != -1:
        print('Номер ' + myNumer + ' знайдено в файлі!')
        print('Відправляємо повідомлення на вказану e-mail адресу!')
        telegram_bot_sendtext("Вітаємо! Ваш ID " + myNumer +" знайдено за посиланням" + getPdf + "!")
        # If not - stuck with error and remove temporary file
    else:
        print('Номер ' + myNumer + ' не знайдено в файлі! Видаляємо')
        telegram_bot_sendtext("Нажаль, Ваш ID " + myNumer +", поки що, не знайдено за посиланням" + getPdf + "!")
        os.remove(savePath)
        print("Файл PDF видалено!")

#check_my_id()
# Lounching check on Schedule
schedule.every().day.at("09:00").do(check_my_id)

while True:
    schedule.run_pending()
    time.sleep(1)