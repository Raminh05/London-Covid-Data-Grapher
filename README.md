# Ontario-and-London-Covid-Case-Scraper

UPDATE MARCH 3rd 2021:
- Now scrapes data from MLUH using selenium (woo)
- Code restructuring (split into multiple files, sepearting Otnario and London functions into multiple .py)
- A heck of a lot more bugs

UPDATE APRIL 22nd 2021:
- TBA

Prerequitsies:
- Selenium (removed after switiching london.py over to the new excel files from MLHU)
- Chromedriver (yeah... you'll have to change the driver's PATH in the code (london.py) cause I suck)
- Pyplot from matplotlib
- csv (reader and writer)
- dateutil (parser)
- numpy
- requests
- openpyxl (*new*) (required to parse MLHU excel files)

Instructions for future me:
- Have all the .py files in the same dict
- Look at the dang prerequitsies
- Run get-choice to get choice
