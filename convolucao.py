# Aluno: Daniel Ortega de Carvalho, RA:170088
# Aluno: Gabriel Hiroaki da Silva Kanezaki, RA:179292

######### INSTRUÇÕES ##########
# Execute o programa

# 1 - Selecione o tipo de convolução, depois aperte
# 2 - em OK e arraste e veja a convolução sendo efetuada

# * * * * * * * * * * * * * * * * * * * * * * * * * * 
# Caso deseje efetuar outro tipo de convolução
# utilize a matriz de Kernel customizada e crie
# sua própria convolução, depois aperte em OK
# e arraste e veja a convolução sendo efetuada
# * * * * * * * * * * * * * * * * * * * * * * * * * *
# Toda a vez que você selecionar o tipo de convolução
# ou criar um Kernel existente, ele resetará sua
# convolução na etapa 0, possibilitando você refazer
# várias vezes a convolução

from tkinter import font
import numpy as np
import tkinter as tk
import cv2
import os
from PIL import Image, ImageTk

os.system('clear')

############################################################
#      ler a imagem a partir do caminho especificado       #
#   coloque o local da imagem dentro da função cv2.imread  #
img = cv2.imread('imagens_conv/mario.png', 0)
############################################################

iH, iL = img.shape

# se a imagem for maior que 128 (resolução)
# a mesma será enquadrada em resolução de 128
iHiLmax = np.max([iH,iL])
if iHiLmax>128:
    img = cv2.resize(img, (int(128/iHiLmax*iH),int(128/iHiLmax*iL)), fx=0, fy=0, interpolation = cv2.INTER_NEAREST)
    iH, iL = img.shape
    print(img.shape)

imgc = img.copy()
print(img.shape)

# kernels padrões já implementados no programa
kernel_ex=[
    ['Gaussian',   1/9*np.array([[1,1,1],[1,1,1],[1,1,1]])],
    ['Sharpen',    1/3*np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])],
    ['Right sobel',1/9*np.array([[-1,0,1],[-2,0,2],[-1,0,1]])],
    ['Emboss',     1/9*np.array([[-2,-1,0],[-1,1,1],[0,1,2]])],
    ['Outline',    1/5*np.array([[-1,-1,-1],[-1,8,-1],[-1,-1,-1]])],
    ['Laplacian',  1/9*np.array([[0,1,0],[1,-4, 1],[0,1,0]])],
]

# resolução do kernel
slidexy = 0, 0
kernel = kernel_ex[0][1]
kH, kL = kernel.shape
print(kH, kL)

# resolução da imagem
res = (1280,600)
root = tk.Tk()
root.title('Convolução de imagens')
root.geometry( f'{res[0]}x{res[1]}')

pos_slide = 0

reskmax = 5

xmm = [(reskmax-kL)//2,(reskmax-kL)//2+kL-1]
ymm = [(reskmax-kH)//2,(reskmax-kH)//2+kH-1]


xi, yi = 0, 0

imgc_antes = imgc.copy()

# função onde cria a imagem convoluida 
# até onde a barra de slide percorreu
def convoluir():
    global xi, yi, kernel, imgc, imgc_antes
    for k in range(slidexy-pos_slide,0,-1):

        # transformação de coordenadas lineares do slide
        # para coordenadas em 2 dimensões
        xi = (slidexy-k)%(iL-kL+1)
        yi = (slidexy-k)//(iL-kL+1)

        # pixel convoluído
        r = np.sum(np.multiply(imgc[yi:yi+kH,xi:xi+kL], kernel))

        # normalização da imagem, para os pixels estarem
        # entre 0 e 255 
        if r>255: r=255
        if r<0: r=0

        # cópia da imagem antes de ser convoluída, para
        # mostrar na tela o processo de pré-convolução
        imgc_antes = imgc.copy()
        imgc[yi+(kH+1)//2-1,xi+(kL+1)//2-1] = int(r)
        label_soma1.configure(text= f'→   Soma ( Imagem x Kernel )   =   {r:.3f}')
        botao_soma3.configure(bg = '#'+'%02x'%(int(r))*3)

    
# função slide é a nossa barra onde 
# o usuário irá arrastar e ver os
# processos de convolução passo a passo
def getslide(event):
    global pos_slide, slidexy, imgc
    if slide.get()>pos_slide:

        slidexy = slide.get()

        convoluir()
    
        imgc_copy = cv2.cvtColor(imgc.copy(), cv2.COLOR_GRAY2BGR)
        imgc_copy[yi+(kH+1)//2-1,xi+(kL+1)//2-1] = 255,0,0

        resized = cv2.resize(imgc_copy, (int(imgc.shape[1]*escala),int(imgc.shape[1]*escala)), fx=0, fy=0, interpolation = cv2.INTER_NEAREST)
        imgtksld = ImageTk.PhotoImage(Image.fromarray(resized))
        imgctk2.configure(image=imgtksld)
        imgctk2.image=imgtksld

        pos_slide = slide.get()
        
        button_img_update(reset=False)

    slide.set(pos_slide)

ultima_pos = (iH-kH+1)*(iL-kL+1)
print('ult', ultima_pos)
slide = tk.Scale(root, from_= 0, to=ultima_pos, length=res[0]*(1-0.1), orient=tk.HORIZONTAL, command=getslide)
slide.set(0)
slide.place(relx=0.022, rely=0.9)

# essa função serve para atualizar visualmente 
# a parte da nossa matriz de kernel, ao clicar
# em um kernel disponibilizado no programa
# ou no kernel customizado
def button_kernel_update():
    for y in range(0,reskmax):
        for x in range(0,reskmax):
            button_kernel[y][x].config(bg = '#D9D9D9', text='')

    for y in range(ymm[0],ymm[1]+1):
        for x in range(xmm[0],xmm[1]+1):
            button_kernel[y][x].config(text = f'{kernel[y-ymm[0],x-xmm[0]]:.2f}',bg = '#666666', fg = '#ffffff')

# essa função serve para mostrar quando
# estiver convoluindo o momento onde estiver 
# nosso ponto de localização, que é o pixel 
# vermelho, ela mostrará ao redor os valores 
# em relação a cor da imagem
def button_img_update(reset):
    imgc = imgc_antes

    if not reset:
        for y in range(ymm[0],ymm[1]+1):
            for x in range(xmm[0],xmm[1]+1):
                #print(y,x)
                xp, yp = x-xmm[0]+xi, y-ymm[0]+yi
                button_img[y][x].config(bg = '#'+'%02x'%(imgc[yp,xp])*3)
                button_img[y][x].config(text = f'{imgc[yp,xp]}', fg ='#'+'%02x'%(imgc[yp,xp]+127)*3, font='helvetica 8' )
    if reset:
        for y in range(0, reskmax):
            for x in range(0, reskmax):
                button_img[y][x].config(bg = '#D9D9D9', text='')

# função onde mostrará nossa imagem sendo
# convoluida passoa a passo
def img_update():
    global imgc, pos_slide
    pos_slide=0
    slide.set(0)
    slide.configure(to=(iH-kH+1)*(iL-kL+1))

    imgc = img.copy()

    resized = cv2.resize(imgc, (int(imgc.shape[1]*escala),int(imgc.shape[1]*escala)), fx=0, fy=0, interpolation = cv2.INTER_NEAREST)
    imgtk_reset = ImageTk.PhotoImage(Image.fromarray(resized))
    imgctk2.configure(image=imgtk_reset)
    imgctk2.image=imgtk_reset

# função onde está localizada nossos exemplos
# padrões do sistema (kernel)
def definir_kernel_ex(arr):
    global kernel, kH, kL, xmm, ymm

    kernel = arr
    kH, kL = kernel.shape

    xmm = [(reskmax-kL)//2,(reskmax-kL)//2+kL-1]
    ymm = [(reskmax-kH)//2,(reskmax-kH)//2+kH-1]

    img_update()
    button_img_update(reset=True)
    button_kernel_update()

# função onde o usuário irá poder digitar
# a matriz referente a kernel que ele queira, para
# efetuar a convolução, foi feita algumas 
# condições para que evite problemas como 
# digitar uma matriz não existente, uma matriz
# com letras ou faltando números em nossa matriz
def definir_kernel():
    global kernel, kH, kL, xmm, ymm

    arr = np.array([[l2.get() for l2 in l1] for l1 in entry])
    arrbool = arr.copy()
    arrbool[arrbool==''] = '-'
    arrbool[arrbool!='-'] = '1'
    arrbool[arrbool=='-'] = '0'
    arrbool = arrbool.astype('int')

    xmm_aux = [4,0]
    ymm_aux = [4,0]
    for y in range(arrbool.shape[1]):
        for x in range(arrbool.shape[0]):
            if arrbool[y,x]:
                if x<xmm_aux[0]: xmm_aux[0] = x
                if x>xmm_aux[1]: xmm_aux[1] = x
                if y<ymm_aux[0]: ymm_aux[0] = y 
                if y>ymm_aux[1]: ymm_aux[1] = y
    try:
        k = np.array(arr[ymm_aux[0]:ymm_aux[1]+1, xmm_aux[0]:xmm_aux[1]+1], dtype='float')
        #print(xmm,ymm)
        if k.size >0:
            xmm = xmm_aux
            ymm = ymm_aux
            kernel = k
            kH, kL = kernel.shape

            img_update()
            button_img_update(reset=True)
            button_kernel_update()
    except:
        return
    
# função do Tkinter em relação a criação do botão
bk1 = tk.Button(root, text = kernel_ex[0][0], height=2, width=10, command = lambda: definir_kernel_ex(kernel_ex[0][1]))
bk1.place(relx=0.04, rely=0.1)
bk2 = tk.Button(root, text = kernel_ex[1][0], height=2, width=10, command = lambda: definir_kernel_ex(kernel_ex[1][1]))
bk2.place(relx=0.04, rely=0.2)
bk3 = tk.Button(root, text = kernel_ex[2][0], height=2, width=10, command = lambda: definir_kernel_ex(kernel_ex[2][1]))
bk3.place(relx=0.04, rely=0.3)
bk4 = tk.Button(root, text = kernel_ex[3][0], height=2, width=10, command = lambda: definir_kernel_ex(kernel_ex[3][1]))
bk4.place(relx=0.04, rely=0.4)
bk5 = tk.Button(root, text = kernel_ex[4][0], height=2, width=10, command = lambda: definir_kernel_ex(kernel_ex[4][1]))
bk5.place(relx=0.04, rely=0.5)

# laços para criar os botões da nossa matriz de kernel usando o Tkinter
button_img = [[tk.Button() for j in range(reskmax)] for i in range(reskmax)]
for i in range(reskmax):
    for j in range(reskmax):
        button_img[i][j] = tk.Button(root, text='',width=4,height=3, borderwidth=1,font='helvetica 8')
        button_img[i][j].place(x=695+j*51, y=65+i*49)

button_kernel = [[tk.Button() for j in range(reskmax)] for i in range(reskmax)]
for i in range(reskmax):
    for j in range(reskmax):
        button_kernel[i][j] = tk.Button(root, text='',width=4,height=3, borderwidth=1,font='helvetica 8')
        button_kernel[i][j].place(x=1000+j*51, y=65+i*49)
# botão padrão do kernel
for y in range(ymm[0],ymm[1]+1):
    for x in range(xmm[0],xmm[1]+1):
        button_kernel[y][x].config(text = f'{kernel[y-ymm[0],x-xmm[0]]:.2f}', bg = '#666666', fg = '#ffffff')


##################### parte visual que mostra os cálculos da convolução ##################
botao_soma1 = tk.Button(root,width=4, height=3, borderwidth=0, bg = '#FF0000')
botao_soma1.place(x=750, y=65+300)
label_soma1 = tk.Label(root, text= f'→   Soma ( Imagem x Kernel )   =   ',anchor='w', font='helvetica 13', width=40,height=4)
label_soma1.place(x=825, y=357)

botao_soma2 = tk.Button(root,width=4,height=3, borderwidth=0, bg = '#FF0000')
botao_soma2.place(x=750, y=65+370)
label_soma2 = tk.Label(root, text= '→', anchor='w', font='helvetica 13', width=10,height=4, borderwidth=1)
label_soma2.place(x=825, y=424)

botao_soma3 = tk.Button(root,width=4,height=3, borderwidth=0, bg = '#D9D9D9')
botao_soma3.place(x=865, y=65+370)

label_kernel = tk.Label(root, text='X',width=2,height=2, borderwidth=1,font=('calibri', 15))
label_kernel.place(x=962, y=165)
############################################################################################

# função 'Entry' usado para que 
# o usuário possa digitar o kernel
entry = [[tk.Entry() for j in range(reskmax)] for i in range(reskmax)]
for i in range(reskmax):
    for j in range(reskmax):
        entry[i][j] = tk.Entry(root, text=f'{i+1}x{j+1}', width=4, font=('calibri', 9))
        entry[i][j].place(relx=0.015+j/40, rely=0.65+i/35)

# função label do Tkinter para parte 
# visual do programa
lbkernel = tk.Label(root, text= 'Kernel', anchor='w', font='helvetica 12', width=20,height=1, borderwidth=1)
lbkernel.place(x=1095, y = 40)

lbimg = tk.Label(root, text= 'Imagem', anchor='w', font='helvetica 12', width=20,height=1, borderwidth=1)
lbimg.place(x=800, y = 40)

lbkernel_custom = tk.Label(root, text= 'Kernel customizada', anchor='w', font='helvetica 10', width=15,height=1, borderwidth=1)
lbkernel_custom.place(relx=0.03, rely = 0.62)
btkernel = tk.Button(root, text = 'Ok', height=2, width=10, command= lambda: definir_kernel())
btkernel.place(relx=0.04, rely=0.8)

# algumas formatações do nosso programa
escala = int(res[1]/imgc.shape[1]*0.8)
resized = cv2.resize(imgc, (int(imgc.shape[1]*escala),int(imgc.shape[1]*escala)), fx=0, fy=0, interpolation = cv2.INTER_NEAREST)
imgctk = ImageTk.PhotoImage(Image.fromarray(resized))

#imgctk2 = canvas.create_image(150,(res[1]-resized.shape[1])//2, anchor=tk.NW, image=imgctk)
imgctk2 = tk.Label(root, image=imgctk)
imgctk2.place(x=200,y=(res[1]-resized.shape[1])//2)

root.resizable(False, False)
tk.mainloop()