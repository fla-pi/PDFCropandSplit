# PDFCrop and Split
Programma in Python che permette di ritagliare, dividere ed estrarre il testo di tutte le pagine di un file PDF.

Il testo è estraibile solo da PDF ricercabili, non svolge alcun compito da OCR. 
Può essere però utile per preparare un file immagine 
all'OCR (se si vogliono rimouvere pié di pagina o intestazioni). 

Applica redaction sulle sezioni tagliate fuori, quindi dal file 
può essere estratto il testo in un secondo momento e 
non compariranno le sezioni cancellate, ma per quanto la redazione 
del PDF è efficace, si consiglia comunque di non usarla per nascondere 
informazioni sensibili.

## Istruzioni per l'installazione
Per utilizzare lo **script Python**, installare le dipendenze:
```
PySimpleGUI
PyPDF2
Pillow
```
può essere fatto installandole direttamente da requirements.txt:

```
python pip install -r requirements.txt
```
## Utilizzo

![alt text](https://github.com/fla-pi/PDFCropandSplit/blob/main/demo_crop.gif)


![alt text](https://github.com/fla-pi/PDFCropandSplit/blob/main/demo_split.gif)
