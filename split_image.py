import cv2

img = cv2.imread('./base_info.jpg')

with open('config') as f:
    positions = [l.strip().split(',') for l in f if l.strip() and not l.strip().startswith('#')]

for i, pos in enumerate(positions):
    print(pos)
    file_name, x, y, w, h = map(str, pos)
    crop_img = img[int(y):int(y)+int(h), int(x):int(x)+int(w)]
    cv2.imwrite(f'images/split/{file_name}.jpg', crop_img)

