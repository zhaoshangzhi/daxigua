import cv2
from numpy import *
import os
from PIL import Image, ImageDraw, ImageFilter
# 访问 文件夹 (假设图片都放在这里面)
def all2jpg(pic_directory):
    print("shit")
    pic_new=pic_directory+'_new'
    isExists=os.path.exists(pic_new)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(pic_new) 
        print (pic_new+' 创建成功')
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print (pic_new+' 目录已存在')
    for root, dirs, files in os.walk(pic_directory):
        # 按文件名排序
        files.sort()
        # 遍历所有文件
        for file in files:
            newfileName=file.strip('.png')
            file=pic_directory+'/'+file
            img = cv2.imread(file)
            h,v,_=img.shape
            if(h==v):
                print(h)
            r=int(h/2)
            newfileName=pic_new+'/'+newfileName+'.jpg'
            print(newfileName)
            cv2.imwrite(newfileName,img)
    return pic_new
def crop_max_square(pil_img):
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))


def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))

def mask_circle_transparent(pil_img, blur_radius, offset=0):
    offset = blur_radius * 2 + offset
    mask = Image.new("L", pil_img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((offset, offset, pil_img.size[0] - offset, pil_img.size[1] - offset), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(blur_radius))

    result = pil_img.copy()
    result.putalpha(mask)
    return result
def generateCircle(directoryNew):
    genDirectory=directoryNew+'Circle'
    isExists=os.path.exists(genDirectory)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(genDirectory) 
        print (genDirectory+' 创建成功')
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print (genDirectory+' 目录已存在')
    for root, dirs, files in os.walk(directoryNew):
        # 按文件名排序
        files.sort()
        # 遍历所有文件
        for file in files:
            genFile=genDirectory+'/'+file.strip('.jpg')+'.png'
            file=directoryNew+'/'+file
            img = cv2.imread(file)
            h,v,_=img.shape
            if h>v:
                h=v
            d=h

            markImg = Image.open(file)
            thumb_width = d
            im_square = crop_max_square(markImg).resize((thumb_width, thumb_width), Image.LANCZOS)
            im_thumb = mask_circle_transparent(im_square, 0)
            im_thumb.save(genFile)
if __name__ == "__main__":
    direct=all2jpg('./ok')
    generateCircle(direct)