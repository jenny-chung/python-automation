import PyPDF2
import os

merger = PyPDF2.PdfMerger()

print(f"The following PDF files in {os.getcwd()} will be merged: ")
for file in os.listdir(os.curdir):
    if file.endswith(".pdf"):
        print(file)
        merger.append(file)

file_name = "merged.pdf"
print("Please enter new file name for merged PDFs. Press enter to skip and use default file name.")
if (input() != ''):
    file_name = f"{input()}.pdf"

merger.write(file_name)
print(f"PDF files successfully merged! See file: {file_name}")
merger.close()
