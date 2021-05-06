"""
Trabalho Final de Processamento de Imagens - 2021.1
Alunas: Paula Madeira, Thalia Ferreira e Luis Antonio

"""

import pytesseract
import cv2
from imutils import contours

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def cortaLetras(imagemComContraste, nomeDoArquivo):
	
	imagem = cv2.imread(nomeDoArquivo)

	if not imagemComContraste:
		if(imagem is None):
			print("Erro! Imagem não encontrada. Verifique o nome e o formato do arquivo e tente novamente.")
			exit()
		ROI_number = 0
		cv2.imshow('Imagem original', imagem)
	else:
		ROI_number = 1
			
	gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
	thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)[1]
	
	cv2.waitKey(1)

	cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if len(cnts) == 2 else cnts[1]
	cnts, _ = contours.sort_contours(cnts, method="left-to-right")

	for c in cnts:
		area = cv2.contourArea(c)

		if area > 1:
			x, y, w, h = cv2.boundingRect(c)		
			ROI = 255 - imagem[y: y + h, x: x + w]

			cv2.imwrite('ROI_{}.png'.format(ROI_number), ROI)
			cv2.rectangle(imagem, (x, y), (x + w, y + h), (36,255,12), 2)

			ROI_number += 1
	
	if ROI_number == 1:
		cortaLetras(imagemComContraste = True, nomeDoArquivo = 'ROI_0.png') 
		return
    
	cv2.imshow('Imagem original e letras recortadas', imagem)
	cv2.waitKey()

def contaFrequenciaDeCaracteres(nomeDoArquivo): 
    imagemParaTexto = cv2.imread(nomeDoArquivo)
    imagemParaTexto = cv2.cvtColor(imagemParaTexto, cv2.COLOR_RGB2GRAY) 

    textoDaImagem = pytesseract.image_to_string(imagemParaTexto)
    frequencias = {} 
    
    for char in textoDaImagem: 
        if char in frequencias: 
            frequencias[char] += 1
        else: 
            frequencias[char] = 1

    arquivoDeOutput = open(r"QuantidadeDeCaracteres.txt","w+")
    arquivoDeOutput.write("Arquivo inserido: " + nomeDoArquivo + '\n\n')
    arquivoDeOutput.write("A frequência de caracteres em '{}' é :\n {}".format(textoDaImagem, str(frequencias)))

nomeDaimagem = input('Digite o nome da imagem: ')
formatoDaImagem = input('Digite o formato da imagem: ')

cortaLetras(imagemComContraste = False, nomeDoArquivo = nomeDaimagem + '.' + formatoDaImagem)
contaFrequenciaDeCaracteres(nomeDoArquivo = nomeDaimagem + '.' + formatoDaImagem)

