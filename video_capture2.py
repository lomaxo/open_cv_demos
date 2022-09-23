import cv2, numpy as np
from PIL import Image, ImageFont, ImageDraw

cv2.namedWindow('Original Image', cv2.WINDOW_AUTOSIZE)
cv2.namedWindow('Ascii', cv2.WINDOW_AUTOSIZE)

def text_image(text: str, width: int, height: int):
    char_size = 6
    colour = (100, 255, 0)
    colour = (255, 255, 255)
    font = cv2.FONT_HERSHEY_PLAIN
    text_queue = text[:]
    image = np.zeros((height*char_size,width*char_size,3), np.uint8)
    text_x, text_y = 0, 10
    # print(text_queue)
    while text_queue:
        next_c, text_queue = text_queue[0], text_queue[1:]
        
        if next_c == '\n':
            # print(next_c)
            text_y += char_size
            text_x = 0
        else:
            text_x += char_size
            image = cv2.putText(image, next_c, (text_x,text_y), font, 0.5, colour, 1, cv2.LINE_AA)
    
    # while len(text_queue) > width:
    #     next_row = text_queue[:width]
    #     text_queue = text_queue[width:]
    #     for x, c in enumerate(next_row):
    #         image = cv2.putText(image, c, (x*char_size,text_y), font, 0.5, colour, 1, cv2.LINE_AA)
    #     text_y += char_size

    return image

def ascii_vid():
    cap = cv2.VideoCapture(0)
    chars = r'''$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'. '''[::-1]
    #chars = '''.:-=+*#%@'''
    if cap.isOpened():
        ret, frame = cap.read()
        orig_shape = frame.shape
        orig_height, orig_width = orig_shape[:2]
    else:
        ret = False

    ascii_width = 150
    ascii_height = int((ascii_width / orig_width) * orig_height)
    print(f'{ascii_width=}, {ascii_height=}')
    print(f'{orig_width=}, {orig_height=}')

    while ret:
        ret, frame = cap.read()
        resized = cv2.resize(frame, (ascii_width,ascii_height), interpolation = cv2.INTER_AREA)
        gray_scale = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        cv2.imshow('Original Image', gray_scale)
        text = ''
        for row in gray_scale:
            for p in row:
                text += chars[int(p/256 * len(chars))]
            text += '\n'
        cv2.imshow('Ascii', text_image(text, ascii_width, ascii_height))
        key = cv2.waitKey(1)
        if key == 27:
            break
        if key == 32:
            with open('./output/output.txt', 'w') as file:
                file.write(text)

            # print(text)
    cap.release()

ascii_vid()  
cv2.destroyAllWindows()
