import random
import math
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

class Centroid:
    def __init__(self, num):
        self.R = random.randint(0, 255)
        self.G = random.randint(0, 255)
        self.B = random.randint(0, 255)
        self.id = num
    def shuffle(self):
        self.R = random.randint(0, 255)
        self.G = random.randint(0, 255)
        self.B = random.randint(0, 255)
    r = 0
    g = 0
    b = 0
    cnt = 0

class Pixel:
    act_centroid = Centroid(-1)
    def __init__(self, R, G, B):
        self.R = R
        self.G = G
        self.B = B

class Photo:
    x = -1
    y = -1
    pixs = []
    def __init__(self, x, y):
        self.x = x
        self.y = y

def dist(p1, p2):
    tmp_dis = (p2.R - p1.R) ** 2
    tmp_dis += (p2.G - p1.G) ** 2
    tmp_dis += (p2.B - p1.B) ** 2
    tmp_dis = math.sqrt(tmp_dis)
    return tmp_dis

def compare_dist(p1, c2):
    c1 = p1.act_centroid
    if(dist(p1, c2) < dist(p1, c1) or c1.id == -1):
        return c2
    return c1

def change_table_into_photo(tab):
    img = Photo(len(tab[0]), len(tab))
    for i in range(len(tab)):
        for j in tab[i]:
            img.pixs.append(Pixel(j[0], j[1], j[2]))
    return img

def change_photo_into_table(photo):
    img = []
    cnt = 0
    for y in range(photo.y):
        tmp = []
        for x in range(photo.x):
            tmp2 = [photo.pixs[cnt].R, photo.pixs[cnt].G, photo.pixs[cnt].B]
            tmp.append(tmp2)
            cnt += 1
        img.append(tmp)
    return img

def generate_random_image(x, y):
    img = []
    for i in range(y):
        tmp = []
        for j in range(x):
            tmp2 = []
            for i in range(3):
                tmp2.append(random.randint(0, 255))
            tmp.append(tmp2)
        img.append(tmp)
    return img

def import_image(file_name):
    image = Image.open(file_name)
    RGB_image = image.convert('RGB')
    new_image = Photo(image.size[0], image.size[1])

    for i in range(new_image.y):
        for j in range(new_image.x):
            new_image.pixs.append(Pixel(RGB_image.getpixel((j, i))[0], RGB_image.getpixel((j, i))[1], RGB_image.getpixel((j, i))[2]))
    return new_image

def k_means(k, photo, cnt = 10):
    centroids = []
    for i in range(k):
        centroids.append(Centroid(i))

    while(cnt):
        print("num: ", cnt)
        cnt -= 1
        for i in photo.pixs:
            for j in centroids:
                i.act_centroid = compare_dist(i, j)
                centroids[i.act_centroid.id].r += i.R
                centroids[i.act_centroid.id].g += i.G
                centroids[i.act_centroid.id].b += i.B
                centroids[i.act_centroid.id].cnt += 1

        for i in centroids:
            if i.cnt != 0:
                i.R = i.r // i.cnt
                i.G = i.g // i.cnt
                i.B = i.b // i.cnt
            i.r, i.g, i.b, i.cnt = 0, 0, 0, 0

    for i in photo.pixs:
        i.R = i.act_centroid.R
        i.G = i.act_centroid.G
        i.B = i.act_centroid.B
    
    return photo

def init(): 
    k = int(input())
    cnt = int(input())
    file_name = input()

    img = change_photo_into_table(import_image(file_name))
    new_img = change_photo_into_table(k_means(k, import_image(file_name), cnt))

    f, axarr = plt.subplots(2,1)
    axarr[0].imshow(img, interpolation='none')
    axarr[1].imshow(new_img, interpolation='none')
    plt.show()

init()