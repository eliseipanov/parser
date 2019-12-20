# parser
Simple parser will grab for you Deutsch diplo.de PDF-file with results. Find your number and send you e-mail (or Viber\Telegram).
Command line, cron script. Diplo.de
It use Python 3.8.0 with Libraries:
requests, os, datetime, Pdfminer.six and BeautifulSoup4
_____________________________________________________________________
18.12.2019

Add Telegram Bot functional for reporting about Sucess or bad request.

Please, do not forget to change your ID of documents case on kiew.diplo.de
and telegram Bot chat ID and token. I put Example thats will not work for you!
_____________________________________________________________________
Still working with.
20.12.2019
Added file requirements.txt. You can use this file to install all libraries used in script

Remember: we are working with python version >= 3.*

Example:
# pip3 install -r requirements.txt

or if you use virtualenv with different versions of python:

# python3 -m venv /path/to/new/virtual/environment

Activate your new environment:

# source /path/to/new/virtual/environment/bin/Activate

Install requirements:

# pip install -r requirements.txt

Then change variables inside both of the scripts:

---------python_parser.py------------------------

##downloadPath  - and make sure path exists
##myNumer  - your case number you given by Deutsch embassy officer

---------telebot.py------------------------------

##bot_token  - your token you have from FatherBot
##bot_chatID - your own chat_id from response in URL  https://api.telegram.org/botYOUR_TOKEN_HERE/getUpdates