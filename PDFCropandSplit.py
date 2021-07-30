import os
import os.path
import PySimpleGUI as sg
from PIL import Image
import fitz


image_file = ''
path =''

sg.theme('DarkBlue3')



layout = [  [sg.Text('')],
            [sg.Text('File (.pdf)'), sg.Input(size=(80,1),key=1)],
            [sg.Text('Visualizza pagina: '), sg.Input(size=(5,1), key=8), sg.Text('Se non specifichi nulla sarà visualizzata la prima pagina e potrai cambiare manualmente le pagine')],
            [sg.Text('''Salva come: '''), sg.Input(size=(80,1),key=9)],
            [sg.Text('''                      Se non specifichi un nome, il file si chiamerà <nomefile>_cropped.pdf''')],
            [sg.Button('Apri file...'), sg.Button("Ritaglia PDF"), sg.Button('Dividi PDF'), sg.Button("Esci"), sg.Text('                                                                            https://github.com/fla-pi')]]


window = sg.Window('PDF Cropper and Splitter', layout)
window2_active = False
window4_active = False


while True:
    event, values = window.read()
                
    if event in (None, 'Esci'):
        window.close()
        break
    elif event in (None, 'Apri file...'):
        def browse():
            
            window[8].update('')
            global path
            path = sg.popup_get_file(message = None,
            title='Browse File',
            default_path="",
            default_extension="",
            save_as=False,
            multiple_files=False,
            file_types=(("PDF Files", ".pdf .PDF"),("All Files", ".")),
            no_window=True,
            size=(50, 50),
            button_color=('Black','LightGrey'),
            background_color=('LightGrey'),
            text_color=('Black'),
            icon=None,
            font=None,
            no_titlebar=False,
            grab_anywhere=True,
            keep_on_top=False,
            location=(None, None),
            initial_folder=None)
            window[1].update(path)
            if type(path) == str:
                if len(path) > 0:
                    window[9].update(path[:-4]+'_crop.pdf')
                else:
                    window[9].update('')
        browse()
    elif event in (None, "Ritaglia PDF"):
        try:
            page_c = values[8]
            outpath = values[9]
            if os.path.exists(outpath):
                    sg.Popup('''Esiste già un file chiamato
    ''' + path[:-4]+'''_crop.pdf !!
Torna indietro e rinomina l'output o verrà sovrascritto!''', title = 'Attento!')
        
            window2_active = True
            
        except:
            pass

        i = 0
        window3 = None
        def cropper():
            try:
                os.remove('PDFCROP_TEMP.png')    
            except:
                pass
            #try:
            global i
            i = i
            if (len(path) > 0):
                if (len(page_c) > 0) and (page_c != '0'):
                    p = int(page_c) - 1
                elif i != 0:
                    p = i
                else:
                    p=0
                doc = fitz.open(path)
                page = doc.loadPage(p)  # number of page
                pix = page.getPixmap()
                output = 'PDFCROP_TEMP.png'
                pix.writePNG(output)
                global image_file
                image_file = output
                image = Image.open(image_file)
                
                image.close()
                pa = doc[p]
                
                sizes = pa.MediaBox #(0.0, 0.0, width, height)
                global width
                width = sizes[2]
                global height
                height = sizes[3]
              
                a, b = 600, 650
                if width > height:
                    a,b = 900,650
            
            #except:
                #pass
        
        
            try:
                column = [
                            [sg.Graph(
                            canvas_size=(width, height),
                            graph_bottom_left=(0, 0),
                            graph_top_right=(width, height),
                            change_submits=True,  
                            drag_submits=True,
                            key="graph")]]
                layout2 = [[sg.Button('Taglia PDF'), sg.Button('<'), sg.Button('>'), sg.Checkbox('''Crea file .txt della
sezione ritagliata''', size=(13, 1),change_submits = True, enable_events=True, default=False,key= 'check'), sg.Text("", key="info", size=(28,1)),sg.Button('Esci')],
                           
                           [ sg.Column(column, size=(width, height), scrollable=True)]]
            
                
                window2 = sg.Window('Taglia il PDF', layout2, size= (a,b),resizable=True)
                window2.finalize()
                global window3
                if window3 != None:
                    window3.close()
                
                graph = window2.Element("graph")
                graph.DrawImage(image_file, location=(0, height)) if image_file else None
                dragging = False
                start_point = end_point = prior_rect = None
            
                while True:
                    event1, values1 = window2.read()

                    if event == sg.WIN_CLOSED or event1 in (None, 'Esci'):
                        window2_active = False
                        window2.close()
                        
                        
                        try:
                            os.remove('PDFCROP_TEMP.png')     
                        except:
                            pass
                        break
                    
                    elif event1 in (None, '>'):
                        if i < ((doc.page_count)-1):
                            i +=1
                            window3 = window2
                            cropper()
                        

                    elif event1 in (None, '<'):
                        if i > 0:
                            i = i-1
                            window3 = window2
                            cropper()
                    elif event1 == "graph":
                        x, y = values1["graph"]
                        
                        if not dragging:
                            start_point = (x, y)
                            
                            dragging = True
                        else:
                            end_point = (x, y)
                        if prior_rect:
                            graph.DeleteFigure(prior_rect)
                        if None not in (start_point, end_point):
                            prior_rect = graph.DrawRectangle(start_point, end_point, line_color='blue')
                    elif event1 != None and event1.endswith('+UP'):
                        try:
                            if start_point[1] < end_point[1]:
                                y1 = end_point[1]
                                y2 = start_point[1]
                            else:
                                y1 = start_point[1]
                                y2 = end_point[1]
                            if start_point[0] < end_point[0]:
                                x1 = start_point[0]
                                x2 = end_point[0]
                            else:
                                x1 = end_point[0]
                                x2 = start_point[0]
                           
                            info = window2.Element("info")
                            info.Update(value=" (X1: " + str(x1) + ", Y1: " + str(y1) + "), (X2: " + str(x2) + ", Y2: " + str(y2)+ ")")
                            # enable grabbing a new rect
                            start_point, end_point = None, None
                            dragging = False
                            y_1 = height - y1
                            y_2 = height - y2
                           
                        except:
                            pass
                        
                    elif event1 == 'check':
                        outext = outpath[:-4]+'.txt'
                        if os.path.exists(outext):
                            while os.path.exists(outext):
                                outext = outext[:-4]+'_new.txt'
                            sg.Popup('''Esiste già un file chiamato
    ''' + outext +''' !!
    Il txt verrà rinominato ''' + outext[:-4] +'_new.txt' , title = 'Attento!')
                            
                    
                    elif event1 in (None, 'Taglia PDF'):
                        
                        try:
                            if os.path.exists(outext):
                                while os.path.exists(outext):
                                    outext = outext[:-4]+'_new.txt'
                                sg.Popup('''Esiste già un file chiamato
    ''' + outext +''' !!
    Il txt verrà rinominato ''' + outext[:-4] +'_new.txt' , title = 'Attento!')
                        except:
                            pass
                        try:
                            doc = fitz.open(path)
                            rect = fitz.Rect(x1, y_1, x2, y_2) #x1, y2, x2,y1
                        except:
                            sg.Popup('''Errore! 
Non hai selezionato un'area da tagliare''' , title = 'Attento!')
                        
                        else:
                            try:
                                rect2 = fitz.Rect(0, 0, sizes[2], rect[1])
                                rect3 = fitz.Rect(0, rect[3], sizes[2], sizes[3])
                                rect4 = fitz.Rect(0, rect[1], rect[0], rect[3])
                                rect5 = fitz.Rect(rect[2], rect[1], sizes[2], rect[3])
                            
                                for pagina in doc:
                                    try:
                                        if (values1['check']== True):    
                                            f_txt= open(outext,"a")
                                            txt = pagina.getTextbox(rect)
                                            f_txt.write(txt)
                                            f_txt.write("\n")
                                    except:
                                        pass
                                            
                                    pagina.add_redact_annot(rect2, text=" ")
                                    pagina.add_redact_annot(rect3, text=" ")
                                    pagina.add_redact_annot(rect4, text=" ")
                                    pagina.add_redact_annot(rect5, text=" ")
                                    pagina.apply_redactions()
                                    pagina.set_cropbox(rect)
                                doc.save(outpath)
                                sg.Popup('''Operazione portata a termine!''' , title = ' ')
                                try:
                                    f_txt.close()
                            
                                except:
                                    pass
                            except:
                                sg.Popup('''Errore! 
Il file potrebbe essere danneggiato!
Se vuoi, il file txt può comunque essere creato''' , title = 'Attento!')
                                pass                
            except:
                pass
        cropper()
    elif event in (None, "Dividi PDF"):
        try:
            page_c = values[8]
            outpath = values[9]
            if os.path.exists(outpath):
                    sg.Popup('''Esiste già un file chiamato
    ''' + path[:-4]+'''_crop.pdf !!
    Torna indietro e rinomina l'output o verrà sovrascritto!''', title = 'Attento!')
        
            window4_active = True
            
        except:
            pass

        i = 0
        window5 = None
        def splitter():
            try:
                os.remove('PDFCROP_TEMP.png')    
            except:
                pass
            
            global i
            i = i
            if (len(path) > 0):
                if (len(page_c) > 0) and (page_c != '0'):
                    p = int(page_c) - 1
                elif i != 0:
                    p = i
                else:
                    p=0
                doc = fitz.open(path)
                page = doc.loadPage(p)  # number of page
                pix = page.getPixmap()
                output = 'PDFCROP_TEMP.png'
                pix.writePNG(output)
                global image_file
                image_file = output
                image = Image.open(image_file)
               
                image.close()
                pa = doc[p]
                
                sizes = pa.MediaBox #(0.0, 0.0, width, height)
                global width
                width = sizes[2]
                global height
                height = sizes[3]
               
                a, b = 600, 650
                if width > height:
                    a,b = 900,650
            
           
        
        
            try:
                column = [
                            [sg.Graph(
                            canvas_size=(width, height),
                            graph_bottom_left=(0, 0),
                            graph_top_right=(width, height),
                            change_submits=True,  
                            drag_submits=True,
                            key="graphic")]]
                layout4 = [[sg.Button('Dividi PDF'), sg.Button('<<'), sg.Button('>>'), sg.Checkbox('''Crea file .txt della
    sezione ritagliata''', size=(13, 1),change_submits = True, enable_events=True, default=False,key= 'check1'), sg.Text("", key="info", size=(28,1)),sg.Button('Esci')],
                           
                           [ sg.Column(column, size=(width, height), scrollable=True)]]
            
                
                window4 = sg.Window('Dividi il PDF', layout4, size= (a,b),resizable=True)
                window4.finalize()
                global window5
                if window5 != None:
                    window5.close()
                
                graph = window4.Element("graphic")
                graph.DrawImage(image_file, location=(0, height)) if image_file else None
                dragging = False
                start_point = end_point = prior_rect  = None
                start_point2 = end_point2 = prior_rect2 = None
                d = 1
                e = 1
            
                while True:
                    event2, values2 = window4.read()

                    if event == sg.WIN_CLOSED or event2 in (None, 'Esci'):
                        window4_active = False
                        window4.close()
                        break
                        
                        try:
                            os.remove('PDFCROP_TEMP.png')     
                        except:
                            pass
                        break
                    
                    elif event2 in (None, '>>'):
                        if i < ((doc.page_count)-1):
                            i +=1
                            window5 = window4
                            splitter()
                        

                    elif event2 in (None, '<<'):
                        if i > 0:
                            i = i-1
                            window5 = window4
                            splitter()
                
                    
                    if event2 == "graphic" and d == 1:
                        x, y = values2["graphic"]
                       
                        if not dragging:
                            start_point = (x, y)
                          
                            dragging = True
                        else:
                            end_point = (x, y)
                        if prior_rect:
                            graph.DeleteFigure(prior_rect)
                        if None not in (start_point, end_point):
                            prior_rect = graph.DrawRectangle(start_point, end_point, line_color='blue')
                            e = 0
                    elif event2 != None and event2.endswith('+UP'):
                        try:
                            if e == 0:
                                if start_point[1] < end_point[1]:
                                    y1 = end_point[1]
                                    y2 = start_point[1]
                                else:
                                    y1 = start_point[1]
                                    y2 = end_point[1]
                                if start_point[0] < end_point[0]:
                                    x1 = start_point[0]
                                    x2 = end_point[0]
                                else:
                                    x1 = end_point[0]
                                    x2 = start_point[0]
                                
                                info = window4.Element("info")
                                info.Update(value=" (X1: " + str(x1) + ", Y1: " + str(y1) + "), (X2: " + str(x2) + ", Y2: " + str(y2)+ ")")
                                # enable grabbing a new rect
                                start_point, end_point = None, None
                                dragging = False
                                d = 0
                                y_1 = height - y1
                                y_2 = height - y2
                            elif e == 1:
                            
                                if start_point2[1] < end_point2[1] :
                                    y1b = end_point2[1]
                                    y2b = start_point2[1]
                                else:
                                    y1b = start_point2[1]
                                    y2b = end_point2[1]
                                if start_point2[0] < end_point2[0]:
                                    x1b = start_point2[0]
                                    x2b = end_point2[0]
                                else:
                                    x1b = end_point2[0]
                                    x2b = start_point2[0]
                                
                                info = window4.Element("info")
                                info.Update(value=" (X1: " + str(x1) + ", Y1: " + str(y1) + "), (X2: " + str(x2) + ", Y2: " + str(y2)+ ")")
                                # enable grabbing a new rect
                            
                                start_point2, end_point2 = None, None
                                dragging = False
                                d = 1
                                y_1b = height - y1b
                                y_2b = height - y2b
                        except:
                            pass
                    elif event2 == "graphic" and d == 0:
                        x, y = values2["graphic"]
                      
                        if not dragging:
                            start_point2 = (x, y)
                            
                            dragging = True
                        else:
                            end_point2 = (x, y)
                        if prior_rect2:
                            graph.DeleteFigure(prior_rect2)
                        if None not in (start_point2, end_point2):
                            prior_rect2 = graph.DrawRectangle(start_point2, end_point2, line_color='red')
                        e = 1
                    elif event2 == 'check1':
                        outext = outpath[:-4]+'.txt'
                        if os.path.exists(outext):
                            while os.path.exists(outext):
                                outext = outext[:-4]+'_new.txt'
                            sg.Popup('''Esiste già un file chiamato
''' + outext +''' !!
Il txt verrà rinominato ''' + outext[:-4] +'_new.txt' , title = 'Attento!')

                    elif event2 in (None, 'Dividi PDF'):
                        try:
                            if os.path.exists(outext):
                                while os.path.exists(outext):
                                    outext = outext[:-4]+'_new.txt'
                                sg.Popup('''Esiste già un file chiamato
''' + outext +''' !!
Il txt verrà rinominato ''' + outext[:-4] +'_new.txt' , title = 'Attento!')
                        except:
                            pass
                        
                        doc = fitz.open(path)
                        try:
                            rect = fitz.Rect(x1, y_1, x2, y_2)
                            rect_sec = fitz.Rect(x1b, y_1b, x2b, y_2b)
                        except:
                            sg.Popup('''Errore! 
Bisogna selezionare due aree per dividere la pagina in due''' , title = 'Attento!')
                        else:
                            try: 
                                rect2 = fitz.Rect(0, 0, sizes[2], rect[1])
                                rect3 = fitz.Rect(0, rect[3], sizes[2], sizes[3])
                                rect4 = fitz.Rect(0, rect[1], rect[0], rect[3])
                                rect5 = fitz.Rect(rect[2], rect[1], sizes[2], rect[3])

                                rect2_sec = fitz.Rect(0, 0, sizes[2], rect_sec[1])
                                rect3_sec = fitz.Rect(0, rect_sec[3], sizes[2], sizes[3])
                                rect4_sec = fitz.Rect(0, rect_sec[1], rect_sec[0], rect_sec[3])
                                rect5_sec = fitz.Rect(rect_sec[2], rect_sec[1], sizes[2], rect_sec[3])

                                num = ((doc.page_count)*2)-1
                                i = 0
                                while i <= num:
                                    doc.fullcopy_page(i,i)
                                    p1 = doc.load_page(i)
                                    p2 = doc.load_page(i+1)
                                    p1.add_redact_annot(rect2, text=" ")
                                    p1.add_redact_annot(rect3, text=" ")
                                    p1.add_redact_annot(rect4, text=" ")
                                    p1.add_redact_annot(rect5, text=" ")
                                    try:
                                        if (values2['check1']== True):    
                                            f_txt= open(outext,"a")
                                            txt = p1.getTextbox(rect)
                                            f_txt.write(txt)
                                            f_txt.write("\n")
                                    except:
                                        pass
                                    p1.apply_redactions()
                                    p1.set_cropbox(rect)
                                    p2.add_redact_annot(rect2_sec, text=" ")
                                    p2.add_redact_annot(rect3_sec, text=" ")
                                    p2.add_redact_annot(rect4_sec, text=" ")
                                    p2.add_redact_annot(rect5_sec, text=" ")
                                    try:
                                        if (values2['check1']== True):    
                                            f_txt= open(outext,"a")
                                            txt = p2.getTextbox(rect_sec)
                                            f_txt.write(txt)
                                            f_txt.write("\n")
                                    except:
                                        pass
                                    p2.apply_redactions()
                                    p2.set_cropbox(rect_sec)
                                    i +=2

                                doc.save(outpath)
                                i = 0
                                sg.Popup('''Operazione portata a termine!''' , title = ' ')
                                try:
                                    f_txt.close()

                                except:
                                    pass
                            except:
                                sg.Popup('''Errore! 
        Il file potrebbe essere danneggiato!
        Se vuoi, il file txt può comunque essere creato''' , title = 'Attento!')
                                pass                
            except:
                pass
        splitter()
                        




