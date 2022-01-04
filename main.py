from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter
from gtts import gTTS
import io
from time import sleep

# ---------------------------- pdfminer3 setup ------------------------------- #

resource_manager = PDFResourceManager()
fake_file_handle = io.StringIO()
converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
page_interpreter = PDFPageInterpreter(resource_manager, converter)

# Select the pdf file here

with open('pdfpaper.pdf', 'rb') as fh:

    for page in PDFPage.get_pages(fh,
                                  caching=True,
                                  check_extractable=True):
        page_interpreter.process_page(page)

    text = fake_file_handle.getvalue()

# Close open handles

converter.close()
fake_file_handle.close()

# OPTIONAL. Save the extracted text as a .txt file

f = open("raw_text.txt", "w", encoding='utf-8')
f.write(text)
f.close()

# Split the text into 3000 long characters. Useful to slowdown gTTS as long PDF's can send too many requests to
# google and get your ip temporarily banned

text_list = list(map(''.join, zip(*[iter(text)]*3000)))

# ---------------------------- gTTS requests ------------------------------- #

# Saves the .mp3 files in multiple parts.

part = 0

for i in text_list:

    language = 'en-uk'

    myobj = gTTS(text=i, lang=language, slow=False)
    part += 1
    myobj.save(f'part{part}.mp3')
    print(f'Part{part}.mp3 has been saved.')
    sleep(15)


