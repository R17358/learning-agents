from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, lang='en')
result = ocr.ocr('story.jpg', cls=True)


for line in result:
    if line['type'] == 'table':
        print("Table detected:", line['res'])
    else:
        print("Text:", line['res'])