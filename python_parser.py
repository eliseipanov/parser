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
downloadPath = "c:/Data/python/parser/downloads/"

# Url of the page where pdflink posted
app_url = 'https://kiew.diplo.de/ua-uk/service/05-VisaEinreise/teaser-abholbereite-visa/1241142'
# Base website URL
baseUrl = "https://kiew.diplo.de"
# Put your number at Deutsch diplo.de website here
myNumer = str(1234567) # This is example number! Put you own number here!

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
    savePath = downloadPath + datt + "_pdf-abholbereite-visa-neu-data.pdf"
    # Writing the content of PDF to file in subdirectory /downloads
    open(savePath, 'wb').write(myfile.content)
    # Using pdfMiner.six for extracting PDF to text
    if __name__ == '__main__':
        PDFtextblob = extract_text_from_pdf(savePath)
    # if number exists, find it and get result
    if PDFtextblob.find(myNumer) != -1:
        print('Номер ' + myNumer + ' знайдено в файлі! Відправляємо повідомлення')
        telegram_bot_sendtext("Вітаємо! Ваш ID " + myNumer +" знайдено за посиланням" + getPdf + "!")
        # If not - stuck with error and remove temporary file
    else:
        print('Номер ' + myNumer + ' не знайдено в файлі! Видаляємо i відправляємо повідомлення')
        telegram_bot_sendtext("Нажаль, Ваш ID " + myNumer +", поки що, не знайдено за посиланням" + getPdf + "!")
        os.remove(savePath)
        print("Файл PDF видалено!")

check_my_id()
# Lounching check on Schedule
#schedule.every().day.at("12:05").do(check_my_id)

#while True:
 #   schedule.run_pending()
  #  time.sleep(1)