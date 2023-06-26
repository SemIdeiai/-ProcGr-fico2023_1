import numpy as np
import cv2 as cv   

def resizeimg(imgNormal,escala):
    width = int (imgNormal.shape[1]*escala)
    height = int (imgNormal.shape[0]*escala)

    dimem =(width,height)
    return cv.resize(imgNormal,dimem,interpolation=cv.INTER_AREA)

def filtrosel(imgSemFiltro):
    fil = input("escolha o filtro\n1-gray 2-GaussianBlur(5x7) 3-invertecor\n 4- 5-Separar um canal 6-Detecção de Bordas: Canny\n 7-Detecção de Bordas: Sobel 8-Binarização  9-Colorização  \n 10-Dilatação 11-Erosão outro imput sair\n")
    if fil == "1":
        imgSemFiltro= cv.cvtColor(imgSemFiltro,cv.COLOR_BGR2GRAY)
    elif fil == "2":
        imgSemFiltro= cv.GaussianBlur(imgSemFiltro,(5,7),cv.BORDER_DEFAULT)
    elif fil == "3":
        imgSemFiltro= cv.cvtColor(imgSemFiltro,cv.COLOR_BGR2RGB)
    elif fil == "4":
       imgSemFiltro = cv.cvtColor(imgSemFiltro,cv.COLOR_BGR2LUV)
    elif fil == "5":
        azul,verde,vermelho = cv.split(imgSemFiltro)
        blank = np.zeros(imgSemFiltro.shape[:2],dtype='uint8')
        RGBsel=input("escolha o canal\nim GRAY 1-B 2-G 3-R\nim colours 4-B 5-G 6-R")
        if RGBsel =="1":
            imgSemFiltro = azul
        elif RGBsel =="2":
            imgSemFiltro = verde
        elif RGBsel =="3":
            imgSemFiltro = vermelho    
        elif RGBsel =="4":
            imgSemFiltro = cv.merge([azul,blank,blank])
        elif RGBsel =="5":
           imgSemFiltro = cv.merge([blank,verde,blank])
        elif RGBsel =="6":
            imgSemFiltro = cv.merge([blank,blank,vermelho])
    elif fil == "6":
        imgSemFiltro= cv.GaussianBlur(imgSemFiltro,(5,7),cv.BORDER_DEFAULT)
        imgSemFiltro= cv.Canny(imgSemFiltro,50,100)
    elif fil == "7":
        ddepth = cv.CV_16S
        scale=1
        delta=0
        grad_x = cv.Sobel(imgSemFiltro,ddepth ,0,1 ,ksize=3, scale=scale, delta=delta, borderType=cv.BORDER_DEFAULT)
        grad_y = cv.Sobel(imgSemFiltro,ddepth ,1,0 ,ksize=3, scale=scale, delta=delta, borderType=cv.BORDER_DEFAULT)
        abs_grad_x = cv.convertScaleAbs(grad_x)
        abs_grad_y = cv.convertScaleAbs(grad_y)
        imgSemFiltro = cv.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
    elif fil == "8":
        imgSemFiltro= cv.cvtColor(imgSemFiltro,cv.COLOR_BGR2GRAY)
        k2 =126
        for i in range(imgSemFiltro.shape[0]): #percorre linhas
	        for j in range(imgSemFiltro.shape[1]): #percorre colunas
                    if imgSemFiltro.item(i,j) < k2:
                        imgSemFiltro.itemset((i,j),0)
                    else :
                        imgSemFiltro.itemset((i,j),255)

    elif fil == "9":
        RGBsel=input("escolha o canal\n GRAY 1-B 2-G 3-R\nim Cor 4-B")
        cinza = False
        k2 =180
        corModificadora = [0, 0, 0]
        if RGBsel =="1":
            corModificadora = [255, 0, 0]
        elif RGBsel =="2":
            corModificadora = [0, 255, 0]
        elif RGBsel =="3":  
            corModificadora = [0, 0, 255]   
        elif RGBsel =="4":
                corModificadora = [255, 0, 0]
                cinza = True
        if cinza:
            for i in range(imgSemFiltro.shape[0]): #percorre linhas
                for j in range(imgSemFiltro.shape[1]): #percorre colunas
                    mediaPond = img.item(i,j,0) * 0.07 + img.item(i,j,1) * 0.71 + img.item(i,j,2) * 0.21
                    if imgSemFiltro.item(i,j,0)<k2:
                        B = imgSemFiltro.item(i,j,0) | corModificadora[0]
                        imgSemFiltro.itemset((i,j,0),B) # canal B
                        imgSemFiltro.itemset((i,j,1),mediaPond) # canal B
                        imgSemFiltro.itemset((i,j,2),mediaPond) # canal B
                    else:
                        imgSemFiltro.itemset((i,j,0),mediaPond) # canal B
                        imgSemFiltro.itemset((i,j,1),mediaPond) # canal B
                        imgSemFiltro.itemset((i,j,2),mediaPond) # canal B


            return imgSemFiltro
        for i in range(imgSemFiltro.shape[0]): #percorre linhas
	        for j in range(imgSemFiltro.shape[1]): #percorre colunas
                    B = imgSemFiltro.item(i,j,0) | corModificadora[0]
                    G = imgSemFiltro.item(i,j,1) | corModificadora[1]
                    R = imgSemFiltro.item(i,j,2) | corModificadora[2]
                    imgSemFiltro.itemset((i,j,0),B) # canal B
                    imgSemFiltro.itemset((i,j,1),G) # canal G
                    imgSemFiltro.itemset((i,j,2),R) # canal R
        
    elif fil == "10":
        imgSemFiltro = cv.dilate(imgSemFiltro,(5,5),iterations=2)
    elif fil == "11":
        imgSemFiltro = cv.erode(imgSemFiltro,(5,5),iterations=2)
    return imgSemFiltro

camOrImg = input("1-camera \n2-arquivo\n")
while(True):
    
    if camOrImg == "1":
        break
    elif camOrImg == "2":
        nomeArquivo=input("nome do arquivo + . e o tipo:\n")
        img = cv.imread(nomeArquivo)
        cv.imshow("Imagem escolhida", img)
        k = cv.waitKey(0)
        break
    else:
        print("opção inesistente")
        camOrImg = input("1-camera \n2-arquivo\n")
        
def overlay(background, foreground, x_offset=None, y_offset=None):
    bg_h, bg_w, bg_channels = background.shape
    fg_h, fg_w, fg_channels = foreground.shape

    assert bg_channels == 3, f'background image should have exactly 3 channels (RGB). found:{bg_channels}'
    assert fg_channels == 4, f'foreground image should have exactly 4 channels (RGBA). found:{fg_channels}'

    # center by default
    if x_offset is None: x_offset = (bg_w - fg_w) // 2
    if y_offset is None: y_offset = (bg_h - fg_h) // 2

    w = min(fg_w, bg_w, fg_w + x_offset, bg_w - x_offset)
    h = min(fg_h, bg_h, fg_h + y_offset, bg_h - y_offset)

    if w < 1 or h < 1: return

    # clip foreground and background images to the overlapping regions
    bg_x = max(0, x_offset)
    bg_y = max(0, y_offset)
    fg_x = max(0, x_offset * -1)
    fg_y = max(0, y_offset * -1)
    foreground = foreground[fg_y:fg_y + h, fg_x:fg_x + w]
    background_subsection = background[bg_y:bg_y + h, bg_x:bg_x + w]

    # separate alpha and color channels from the foreground image
    foreground_colors = foreground[:, :, :3]
    alpha_channel = foreground[:, :, 3] / 255  # 0-255 => 0.0-1.0

    # construct an alpha_mask that matches the image shape
    alpha_mask = np.dstack((alpha_channel, alpha_channel, alpha_channel))

    # combine the background with the overlay image weighted by alpha
    composite = background_subsection * (1 - alpha_mask) + foreground_colors * alpha_mask

    # overwrite the section of the background image that has been updated
    background[bg_y:bg_y + h, bg_x:bg_x + w] = composite
    out = background.copy()
    return out

def mouse_click(event, x, y, 
                flags, param):         
    # to check if right mouse 
    # button was clicked
    if event == cv.EVENT_RBUTTONDOWN:
        print("Stamp")
        out = overlay(imgf,stickertipe, x, y)
        cv.imshow('imgSemSticker', out)

def mouse_clickXY(event, x, y, 
                flags, param):         
    # to check if right mouse 
    # button was clicked
    if event == cv.EVENT_RBUTTONDOWN:
        print("Stamp")
        out = overlay(imgf,stickertipe, x, y)
        cv.imshow('imgSemSticker', out)
    return x,y 

if camOrImg == "1":
    while True:
        capture = cv.VideoCapture(0)
        if not capture.isOpened():
            print('Unable to open')
            exit(0)
        ret, frame = capture.read()
        if frame is None:
            camOrImg = 0
            break
        # Display the resulting frame
        cv.imshow('frame', frame)
    
        # the 'q' button is set as the
        # quitting button you may use any
        # desired button of your choice
        if cv.waitKey(1) & 0xFF == ord('q'):
            imgf = frame
            camOrImg = "2"
            break
if camOrImg == "2":
    imgf = img
    while True:
        selecione = input("escolha Colocar 1-Filtro 2-Sticker outro-finalisa\n")
        if selecione == "1":
           imgf= filtrosel(imgf)
        elif selecione == "2":
            
            stickersele = input ("escolha o sticker\n1-cogumeloVermelho 2-Bota 3-Casco Vermelho\n 4-Martelo 5-Flor de Fogo /Outro imput sair")
            if stickersele == "1":#diminuir para 10%
                stickertipe =cv.imread('CoguV.png', cv.IMREAD_UNCHANGED)
            elif stickersele == "2":
                stickertipe =cv.imread('Bota.png', cv.IMREAD_UNCHANGED)
            elif stickersele == "3":
                stickertipe =cv.imread('CascoV.png', cv.IMREAD_UNCHANGED)
            elif stickersele == "4":
                stickertipe =cv.imread('Martelo.png', cv.IMREAD_UNCHANGED)
            elif stickersele == "5":
                stickertipe =cv.imread('FlorF.png', cv.IMREAD_UNCHANGED)
            else:
                continue
            stickertipe = resizeimg(stickertipe,0.1)
            cv.imshow("imgSemSticker", img)
            cv.setMouseCallback('imgSemSticker', mouse_click)
            k = cv.waitKey(0)
        elif selecione == "3":
            camOrImg = "R"
        elif selecione == "4":
            camOrImg = "G"
        elif selecione == "5":
            camOrImg = "B"
        else:
            break
if camOrImg != 0:
    cv.imshow("Trabalho GB", imgf)

    k = cv.waitKey(0)
    cv.destroyAllWindows()
    cv.imwrite(input("nome do arquivo final sera salvo em png\n")+".png", imgf)
elif camOrImg == "R":
    cv.imshow("Trabalho GB", imgf)

    k = cv.waitKey(0)
    cv.destroyAllWindows()
    cv.imwrite(input("nome do arquivo final sera salvo em png\n")+".png", imgf)
elif camOrImg == "B":
    cv.imshow("Trabalho GB", imgf)

    k = cv.waitKey(0)
    cv.destroyAllWindows()
    cv.imwrite(input("nome do arquivo final sera salvo em png\n")+".png", imgf)

k = cv.waitKey(0)
cv.destroyAllWindows()

