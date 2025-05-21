# extract_Data
extract_Data

# PDF Month-Year Extractor

This project is a Python script that extracts **month** and **year** information from a PDF file using the `PyPDF3` library and saves the results to a CSV file.

## 🧠 Features

- Parses a PDF file page by page
- Extracts months and years using regular expressions
- Records the page number along with each extracted date
- Saves the output into a structured CSV file

## 📁 File Structure

├── your_script.py \n
├── extracted_month_year.csv \n
└── README.md \n


## 🛠️ Requirements

- Python 3.x
- PyPDF3
- re (built-in)
- csv (built-in)

Install PyPDF3 via pip if not already installed:

```bash
pip install PyPDF3


▶️ How to Use
Place the PDF file in your working directory or provide the full path.

Update the pdf_path variable in the script:

pdf_path = "path/to/your/file.pdf"


Run the script:

python your_script.py

The results will be saved in a CSV file named extracted_month_year.csv.


