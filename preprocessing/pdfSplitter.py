from PyPDF2 import PdfFileWriter, PdfFileReader

inputpdf = PdfFileReader(open("Fundamental_Neuroscience_2008.pdf", "rb"))

range_pages=150
for i in range(inputpdf.numPages):
    if i%range_pages==0:
        print('creating file writer')
        output = PdfFileWriter()

    output.addPage(inputpdf.getPage(i))

    if ((i+1)%range_pages==0 or (i==(inputpdf.numPages-1))):
        newFileName="Fundamental_Neuroscience_2008_{}.pdf".format(int(i//range_pages))
        print(newFileName)
        with open( newFileName, "wb") as out:
            output.write(out)