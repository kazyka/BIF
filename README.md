# BIF

A project that reads from a Database. It will then get the path to a PDF and use OCR to scan the text and pushes the data to another table.

# To Run

Create a database named `OCR`

Have a scanned PDF file that you can use if you wish to test the code.

In the `main()` file change `core_ocr('config.json', 'TestBIFDB', base_path)` to `core_ocr('config.json', 'localDB', base_path)`

In `create_tables.py` and `insert_data.py` set `database_type = "localDB"`

In `insert_data.py` set the correct path to your PDF file


# Links


https://www.google.com/search?q=pytesseract+vs+easyocr&oq=pytesseract+vs+eas&aqs=chrome.1.69i57j33i22i29i30.4972j0j7&sourceid=chrome&ie=UTF-8

https://www.pyimagesearch.com/2020/09/14/getting-started-with-easyocr-for-optical-character-recognition/

https://www.google.com/search?q=easy+ocr+not+detecting+gpu&oq=easy+ocr+not+detecting+gpu&aqs=chrome..69i57.6247j0j7&sourceid=chrome&ie=UTF-8

https://www.google.com/search?q=Deep+learning+python+pdf+ocr&oq=Deep+learning+python+pdf+ocr&aqs=chrome..69i57j33i22i29i30.5637j0j7&sourceid=chrome&ie=UTF-8

https://github.com/jaidedai/easyocr

https://pypi.org/project/pdf2image/

https://pypi.org/project/pytesseract/#description

https://towardsdatascience.com/extracting-text-from-scanned-pdf-using-pytesseract-open-cv-cd670ee38052

https://www.geeksforgeeks.org/python-reading-contents-of-pdf-using-ocr-optical-character-recognition/

https://www.youtube.com/watch?v=bcmEMcEzV9M

https://www.google.com/search?q=python+pdf+ocr&oq=python+pdf+ocr&aqs=chrome..69i57j0i512l2j0i22i30l7.4868j0j7&sourceid=chrome&ie=UTF-8
