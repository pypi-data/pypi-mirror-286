import sys
import os
sys.path.append(os.path.abspath('..'))
from csdnuploadimage.utils.getUploadValidInfo import *
from csdnuploadimage.utils.uploadImage import *


def uploadImage(validData, filePath):
    validData = get_valid_info(validData)
    if validData == None:
        return None
    
    imageUrl = get_image_url(validData, filePath)
    if imageUrl == None:
        return None
    
    return imageUrl


if __name__ == "__main__":
    cookie = "UserToken=e203bba2196d4536ab8bd0233fd1aa20;UserName=abccbatqw;https_waf_cookie=4dfda1fb-dc56-4d9821cc6fea484b9fce15d0d40690324e29;"
    filePath = 'C:/Users/LENOVO/Desktop/0_0_0(1).png'
    imageUrlInfo = uploadImage(cookie, filePath)
    print(imageUrlInfo)
