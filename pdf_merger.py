import PyPDF2
import os

merger = PyPDF2.PdfMerger()

print(f"The following PDF files in {os.getcwd()} will be merged: ")
for file in os.listdir(os.curdir):
    if file.endswith(".pdf"):
        print(file)
        merger.append(file)

file_name = input("Please enter a new file name for the merged PDFs. Press enter to skip and use default file name.\n")
if (file_name == ''):
    # Use default file name for merged PDFs if no input
    file_name = 'merged.pdf'
else:
    file_name += '.pdf'

merger.write(file_name)
print(f"PDF files successfully merged! See file: {file_name}")
merger.close()
