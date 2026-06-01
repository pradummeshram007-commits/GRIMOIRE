import easyocr

reader = easyocr.Reader(['en'])

result = reader.readtext(
    'frames/reel1/frame_001.jpg',
    detail=0
)

print(result)