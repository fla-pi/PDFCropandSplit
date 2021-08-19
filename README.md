# PDFCrop and Split
Programma in Python che permette di ritagliare, dividere ed estrarre il testo di tutte le pagine di un file PDF.

Il testo è estraibile solo da PDF ricercabili, il programma non svolge alcun compito di OCR. 
Può essere però utile per preparare un file immagine 
all'OCR (se si vogliono rimuovere pié di pagina o intestazioni). 

Applica redaction sulle sezioni tagliate fuori, quindi dal file 
può essere estratto il testo in un secondo momento (con altri programmi) e 
non compariranno le sezioni cancellate, ma per quanto la redazione 
del PDF è efficace, si consiglia comunque di non usarla per nascondere 
informazioni sensibili.

## Istruzioni per l'installazione
Per utilizzare lo **script Python**, installare le dipendenze:
```
PySimpleGUI
PyMuPDF
Pillow
```
può essere fatto installandole direttamente da requirements.txt:

```
python pip install -r requirements.txt
```
Per l'utilizzo su macOS potrebbe essere necessario installare differentemente PyMuPDF:
```
brew install mupdf swig freetype
pip install https://github.com/pymupdf/PyMuPDF/archive/master.tar.gz
```
## Utilizzo
Aprire il file PDF e in caso non si voglia aprire la prima pagina, specificare il numero di pagina da visualizzare.

Selezionando **Taglia PDF** si aprirà una finestra in cui sarà possibile:
- cambiare pagina (tasti "<" e ">");
- decidere se creare automaticamente un file .txt con il testo estratto dalle aree ritagliate*;
- tracciare un rettangolo sulla pagina per decidere l'area da conservare (il ritaglio verrà applicato a tutte le pagine).

![alt text](https://github.com/fla-pi/PDFCropandSplit/blob/main/demo_crop.gif)

Selezionando **Dividi PDF** si aprirà una finestra in cui sarà possibile:
- cambiare pagina (tasti "<<" e ">>");
- decidere se creare automaticamente un file .txt con il testo estratto dalle pagine divise*;
- tracciare due rettangoli (pagina 1 = blu, pagina 2 = rosso) sulla pagina per decidere come dividere i PDF (la divisione e il ritaglio verranno applicati a tutte le pagine).

![alt text](https://github.com/fla-pi/PDFCropandSplit/blob/main/demo_split.gif)


\*nel caso in cui il PDF non contenga testo (ad es. un PDF immagine) il file .txt sarà vuoto (la funzione è ancora da migliorare, per ora si consiglia di estrarre il testo con un altro programma)
