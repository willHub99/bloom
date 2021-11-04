#===============================================================================
# Autores: Eduarda Simonis Gavião (RA: 1879472), Willian Rodrigo Huber(RA: 1992910)
# Universidade Tecnológica Federal do Paraná
#===============================================================================


#importando bibliotecas
import cv2

#definindo altura e largura da janela deslizante
ALTURA = 5
LARGURA = 5

#define o limiar para bright-pass
THRESHOLD = 129

#define o valor do desvio padrao para o filtro gaussiano
SIGMA = 2

#define a quantidade de vezes que a imagem sera borrada no filtro gaussiano
N_GAUSS = 4

#Número de vezes que a imagem será processada filtro da média
N_MEDIA = 3 

#define o nome da imagem
INPUT_IMAGE = 'GT2.BMP'

def mascara (img, threshold):  
    row,col, _ = img.shape
    for y in range(row):
        for x in range(col):
            if img[y][x][1] < threshold:
                img[y][x] = 0
                
    return img

#define filtro gaussiano
#entra com imagem, altura, largura da janela e quantidaade de vezes que será aplicado o filtro gaussiano
def gaussianBlur(img, altura, largura, sigma, n):

    img1 = cv2.GaussianBlur(img, (altura,largura), sigma)#borra a imagem original
    ini = 2 #define a variavel auxiliar para dobrar o valor do desvio padrão
    for i in range(n): #laço de repetição para borrar a imagem N-1 vezes
        img1 = cv2.GaussianBlur(img1, (altura,largura), ini*sigma)#borra a imagem borrada até terminar o laço 
        ini *=2
    return img1 #retorna imagem borrada pelo filtro da media 

#define filtro da média
#entra com imagem, altura, largura da janela  e quantidaade de vezes que será aplicado o filtro da média
def media(img,altura,largura,n):
    borrada=cv2.blur(img,(altura,largura)) #borra a imagem original
    for y in range (n): #laço de repetição para borrar a imagem N-1 vezes
        borrada=cv2.blur(borrada,(altura,largura)) #borra a imagem borrada até terminar o laço 
    return borrada #retorna imagem borrada pelo filtro da media 


def main ():

    #abre a imagem dados.jpg com sinalizador IMREAD_COLOR (imagem colorida)
    img = cv2.imread(INPUT_IMAGE, cv2.IMREAD_COLOR)
    #converte a imagem img de RGB para HLS
    img_HLS = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)

    #chama a função que faz o bright-pass
    img_mask = mascara(img_HLS, THRESHOLD)
    #converte a imagem img_mask de HLS para RGB
    img_RGB = cv2.cvtColor(img_mask, cv2.COLOR_HLS2BGR)

    #chama a função que realiza o filtro gaussiano
    img_gaussian = gaussianBlur(img_RGB, ALTURA,LARGURA, SIGMA, N_GAUSS)
    #realiza a soma da imagem original com a imagem após ser realizado o filtro gaussiano
    bloom_gaussian = cv2.add(img, img_gaussian)
    cv2.imshow('bloom - filtro gaussiano', bloom_gaussian)

    #chama media, com os parametros, máscara, altura e largura da janela e NMedia
    img_blur= media(img_RGB,ALTURA,LARGURA,N_MEDIA)
    bloom_media= cv2.add(img,img_blur) #faz o efeito bloom apartir da soma da máscara tradada com filtro da média e imagem original 
    cv2.imshow('bloom - filtro media', bloom_media) #apresenta imagem com Bloom
    
    cv2.waitKey()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()