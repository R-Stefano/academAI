from xml.dom import minidom
import os
folder='xml2text'
targetFolder='texts'
totWords=0
for filename in os.listdir('xml2text'):
    xmldoc = minidom.parse(folder+'/'+filename)
    itemlist = xmldoc.getElementsByTagName('p')
    text=''
    for item in itemlist:
        text+=item.childNodes[0].data
    totWords += len(text)
    filename=filename[:filename.find('.pdf')]
    with open(targetFolder+'/'+filename+'.txt', 'w') as f:
        f.write(text)

print('length text', totWords)