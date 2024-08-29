#by essensuOFnull
import numpy as np
from sys import argv
from PIL import Image
from random import randint
from math import ceil
#создание массива словарей шрифтов (fonts)
font_dicts=[]
with open("fonts.py","r",encoding="utf-8")as fonts:
    while"fonts"not in fonts.readline().split("="):pass
    level=0;temp=[];i=-1
    while level>-1:
        symbol=fonts.read(1)
        if symbol=="[" or symbol=="(":
            if level==0:temp.append([]);font_dicts.append([]);i+=1
            level+=1
        elif symbol=="]" or symbol==")":level-=1
        elif symbol=="#":temp[i].append(fonts.readline().split())
    for i in range(len(temp)):
        for i1 in range(len(temp[i])):font_dicts[i].extend(temp[i][i1])
        font_dicts[i]=dict.fromkeys(font_dicts[i])
        for a in range(len(temp[i])):
            for b in range(len(temp[i][a])):font_dicts[i][temp[i][a][b]]=a
from fonts import*
for i in range(len(font_dicts)):
    for key in font_dicts[i].keys():
        symbol_matrix=np.zeros((len(fonts[i][font_dicts[i][key]]),len(fonts[i][font_dicts[i][key]][0])),dtype=np.bool_)
        for y in range(len(fonts[i][font_dicts[i][key]])):
            for x in range(len(fonts[i][font_dicts[i][key]][0])):
                symbol_matrix[y,x]=fonts[i][font_dicts[i][key]][y][x]
        font_dicts[i][key]=symbol_matrix
fonts=font_dicts;del font_dicts
#получение аргументов
mode=0
font=0
r,g,b,a=255,255,255,255
initial_coordinates_of_image_usage=None
r_substitution_range=[0,0]
g_substitution_range=[0,0]
b_substitution_range=[0,0]
a_substitution_range=[0,255]
negative=0
text=None
text_path="text.txt"
input_path="input.png"
color_path="input.png"
output_path="output.png"
for i in range(len(argv)):
    if argv[i]=="-m":#режим. 0 - простро субпиксельный текст, 1 - заполнение пространств цвета #000 субпиксельным текстом, 2 - превращение изображения в субпиксельный текст
        mode=int(argv[i+1])
    if argv[i]=="-f":#шрифт. 0 - шрифт минимального размера, 1 - шрифт из CODERROR-а
        font=int(argv[i+1])
    if argv[i]=="-hi":#горизонтальный отступ между символами в субпикселях
        horizontal_indent=int(argv[i+1])
    if argv[i]=="-vi":#вертикальный отступ между символами в пикселях
        vertical_indent=int(argv[i+1])
    if argv[i]=="-s":#ширина пробела или неподдерживаемого шрифтом символа в субпикселях (пишите на 2 -i меньше чем на самом деле хотите)
        space_width=int(argv[i+1])
    if argv[i]=="-r":#установить яркость красных субпикселей                                       #
        r=int(argv[i+1])                                                                           #
    if argv[i]=="-g":#установить яркость зелёных субпикселей                                       #
        g=int(argv[i+1])                                                                           #
    if argv[i]=="-b":#установить яркость синих субпикселей                                         #
        b=int(argv[i+1])                                                                           #
    if argv[i]=="-a":#установить прозрачность пикселей                                             #
        a=int(argv[i+1])                                                                           #
    if argv[i]=="-rr":#установить диапазон для случайной яркости красных субпикселей               #для режимов 0 и 1
        r=[int(j) for j in argv[i+1:i+3]]                                                          #
    if argv[i]=="-rg":#установить диапазон для случайной яркости зелёных субпикселей               #
        g=[int(j) for j in argv[i+1:i+3]]                                                          #
    if argv[i]=="-rb":#установить диапазон для случайной яркости синих субпикселей                 #
        b=[int(j) for j in argv[i+1:i+3]]                                                          #
    if argv[i]=="-ra":#установить диапазон для случайной прозрачности                              #
        a=[int(j) for j in argv[i+1:i+3]]                                                          #
    if argv[i]=="-c":#если задать координаты, будут использоваться цвета изображения начиная с них #
        initial_coordinates_of_image_usage=[int(j) for j in argv[i+1:i+3]]
    if argv[i]=="-rsr":#диапазон яркости красного субпикселя который будет заменяться на текст #
        r_substitution_range=[int(j) for j in argv[i+1:i+3]]                                   #
    if argv[i]=="-gsr":#диапазон яркости зелёного субпикселя который будет заменяться на текст #
        g_substitution_range=[int(j) for j in argv[i+1:i+3]]                                   #для режима 1
    if argv[i]=="-bsr":#диапазон яркости синего субпикселя который будет заменяться на текст   #
        b_substitution_range=[int(j) for j in argv[i+1:i+3]]                                   #
    if argv[i]=="-asr":#диапазон прозрачности пикселя который будет заменяться на текст        #
        a_substitution_range=[int(j) for j in argv[i+1:i+3]]
    if argv[i]=="-n":#наоборот, не будут гореть только субпиксели символов
        negative=1
    if argv[i]=="-t":#установить текст напрямую
        text=argv[i+1]
    if argv[i]=="-tp":#указать путь до текстового файла
        text_path=argv[i+1]
    if argv[i]=="-ip":#указать путь до исходного изображения, которое будет изменено (для режима 1)
        input_path=argv[i+1]
    if argv[i]=="-cp":#указать путь до изображения из которого будут браться цвета
        color_path=argv[i+1]
    if argv[i]=="-op":#указать путь для сохранения изображения
        output_path=argv[i+1]
if text is None:
    text=open(text_path,'r',encoding='utf-8').read()
if initial_coordinates_of_image_usage is None and mode==2:
    initial_coordinates_of_image_usage=[0,0]
symbol_height=len(list(fonts[font].values())[0])
start_symbol_index=0
#настройки шрифтов по умолчанию
if font==0:
    if not "-hi" in argv:
        horizontal_indent=1
    if not "-vi" in argv:
        vertical_indent=1
    if not "-s" in argv:
        space_width=0
elif font==1:
    if not "-hi" in argv:
        horizontal_indent=0
    if not "-vi" in argv:
        vertical_indent=0
    if not "-s" in argv:
        space_width=10
#
indent_line=[0]*horizontal_indent
def get_boolean_symbol_matrix(symbol,font=font):
    if symbol in fonts[font].keys():
        boolean_symbol_matrix=fonts[font][symbol].tolist()
    else:
        boolean_symbol_matrix=[[0 for i in range(space_width)]for j in range(symbol_height)]
    return boolean_symbol_matrix
def generate_boolean_matrix_line(text,boolean_matrix=None,font=font):
    if boolean_matrix is None:
        boolean_matrix=get_boolean_symbol_matrix(text[0])
        text=text[1:]
    for symbol in text:
        boolean_symbol_matrix=get_boolean_symbol_matrix(symbol)
        for i in range(len(boolean_matrix)):
            boolean_matrix[i].extend(indent_line)
            boolean_matrix[i].extend(boolean_symbol_matrix[i])
    return boolean_matrix
def negative_boolean_matrix(boolean_matrix):
    return[[1 if not x else 0 for x in row] for row in boolean_matrix]
def combine_boolean_matrix_lines(boolean_matrix_lines):
    max_len=max(len(boolean_matrix_line[0])for boolean_matrix_line in boolean_matrix_lines)
    for boolean_matrix_text_line in boolean_matrix_lines:
        for boolean_matrix_line in boolean_matrix_text_line:
            while len(boolean_matrix_line)<max_len:
                boolean_matrix_line.append(0)
    boolean_matrix=[]
    for i in range(len(boolean_matrix_lines)):
        for boolean_matrix_line in boolean_matrix_lines[i]:
            boolean_matrix.append(boolean_matrix_line)
        if i!=len(boolean_matrix_lines)-1:
            for i in range(vertical_indent):
                boolean_matrix.append([0]*len(boolean_matrix_lines[0][0]))
    return boolean_matrix
def complement_boolean_matrix(boolean_matrix):
    for i in range(len(boolean_matrix)):
        while len(boolean_matrix[i])%3!=0:
            boolean_matrix[i].append(0)
    return boolean_matrix
def get_color_pixel_instance(parameters=[r,g,b,a]):
    pixel=[]
    for parameter in parameters:
        if type(parameter)==int:
            pixel.append(parameter)
        else:
            pixel.append(randint(parameter[0],parameter[1]))
    return pixel
def boolean_matrix_to_image(boolean_matrix,coordinates_of_image_usage=initial_coordinates_of_image_usage):
    if negative:
        boolean_matrix=negative_boolean_matrix(boolean_matrix)
    image_size=[len(boolean_matrix[0])//3,len(boolean_matrix)]
    image=Image.new("RGBA",image_size,(0,0,0,255))
    pixels=image.load()
    for y in range(image_size[1]):
        for x in range(image_size[0]):
            color_pixel=get_color_pixel_instance()if coordinates_of_image_usage is None or coordinates_of_image_usage[0]+x>=color_image_size[0] or coordinates_of_image_usage[1]+y>=color_image_size[1] else color_pixels[coordinates_of_image_usage[0]+x,coordinates_of_image_usage[1]+y]
            pixel=[]
            for x1 in range(3):
                if boolean_matrix[y][x*3+x1]:
                    if color_pixel[x1]:
                        pixel.append(color_pixel[x1])
                    else:
                        pixel.append(1)
                else:
                    pixel.append(0)
            pixel.append(color_pixel[3])
            pixels[x,y]=tuple(pixel)
    return image
def get_boolean_matrix_width_in_pixels(boolean_matrix):
    return ceil(len(boolean_matrix[0])/3)
def get_fixe_sized_boolean_matrix(size,text=text,font=font):
    global start_symbol_index
    if mode==2:
        size=[size[i]-initial_coordinates_of_image_usage[i]for i in range(2)]
    boolean_matrix_lines=[]
    boolean_matrix_line=None
    current_height=0
    text_len=len(text)
    while 1:
        for symbol_index in range(start_symbol_index,text_len):
            symbol=text[symbol_index]
            next_boolean_matrix=generate_boolean_matrix_line(symbol,boolean_matrix_line,font)
            if get_boolean_matrix_width_in_pixels(next_boolean_matrix)>size[0] or symbol=="\n":
                next_height=current_height+len(next_boolean_matrix)+vertical_indent
                if next_height<=size[1]:
                    boolean_matrix_lines.append(boolean_matrix_line)
                    boolean_matrix_line=None
                    #boolean_matrix_line=generate_boolean_matrix_line(symbol,None,font) #по логике эта строка нужна вместо предыдущей, но почему-то нет. да в целом не понимаю что происходит
                    current_height=next_height
                else:
                    start_symbol_index=symbol_index
                    return complement_boolean_matrix(combine_boolean_matrix_lines(boolean_matrix_lines))if boolean_matrix_lines!=[None]else[]
            else:
                boolean_matrix_line=next_boolean_matrix
        start_symbol_index=0
def add_indents(boolean_matrix):
    for y in range(vertical_indent):
        boolean_matrix.append([0]*len(boolean_matrix[0]))#отступ снизу
    return boolean_matrix
def fill_image_with_subpixel_text(input_path=input_path,text=text,font=font):
    input_image=Image.open(input_path).convert("RGBA")
    input_pixels=input_image.load()
    input_image_size=input_image.size
    line_height=symbol_height+vertical_indent
    parameters=[r_substitution_range,g_substitution_range,b_substitution_range,a_substitution_range]
    line_width_in_pixels=0
    line_width_calculation_completed=0
    for y in range(0,input_image_size[1],line_height):
        x=0
        break_while=0
        while 1:
            for x1 in range(input_image_size[0]-x):
                for y1 in range(line_height):
                    if y+y1>=input_image_size[1]:
                        return input_image
                    pixel=input_pixels[x+x1,y+y1]
                    if False in[pixel[i]in range(parameters[i][0],parameters[i][1]+1) for i in range(4)]or x+x1+1>=input_image_size[0]:
                        if x+x1+1>=input_image_size[0]:
                            break_while=1
                        line_width_calculation_completed=1
                        break
                else:
                    line_width_in_pixels+=1
                if line_width_calculation_completed:
                    line_width_calculation_completed=0
                    horizontal_indents_count=1 if x==0 else 2
                    vertical_indents_count=1 if y==0 else 2
                    boolean_matrix=get_fixe_sized_boolean_matrix([line_width_in_pixels-horizontal_indents_count*horizontal_indent,line_height],text,font)
                    if boolean_matrix!=[]:
                        input_image.paste(boolean_matrix_to_image(add_indents(boolean_matrix),(x,y)),(x,y))
                    line_width_in_pixels=0
                    x+=x1+1
                    if x+x1>input_image_size[0]:
                        break_while=1
                    break
            if break_while:
                break
    return input_image
if initial_coordinates_of_image_usage is None:
    if mode==1:
        color_image_size=[0,0]
else:
    color_image=Image.open(color_path).convert("RGBA")
    color_pixels=color_image.load()
    color_image_size=color_image.size
if mode==0:
    boolean_matrix_lines=[]
    for text_line in text.split('\n'):
        boolean_matrix_lines.append(generate_boolean_matrix_line(text_line))
    boolean_matrix_to_image(complement_boolean_matrix(combine_boolean_matrix_lines(boolean_matrix_lines))).save(output_path)
if mode==1:
    fill_image_with_subpixel_text().save(output_path)
if mode==2:
    color_image=Image.open(color_path).convert("RGBA")
    color_pixels=color_image.load()
    boolean_matrix_to_image(get_fixe_sized_boolean_matrix(color_image_size)).save(output_path)