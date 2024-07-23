from urllib3 import encode_multipart_formdata
import random
import string
import requests
import json


def get_image_url(validData, filePath):
  # filePath: 要上传的文件路径

  # 打开文件并读取二进制内容
  with open(filePath, 'rb') as file:
      file_content = file.read() #这李file_content是二进制内容,<class,bytes>
      #计算文件大小
      file_size = file.tell()

  # 设置boundary,这里是自己设置的
  boundary = '----WebKitFormBoundary'+''.join(random.sample(string.ascii_letters+string.digits,16))

  #设置表单
  fields = []
  fields.append(("key", (None, validData['filePath'], None)))
  fields.append(("policy", (None, validData['policy'], None)))
  fields.append(("AccessKeyId", (None, validData['accessId'], None)))
  fields.append(("signature", (None, validData['signature'], None)))
  fields.append(("callbackUrl", (None, validData['callbackUrl'], None)))
  fields.append(("callbackBody", (None, validData['callbackBody'], None)))
  fields.append(("callbackBodyType", (None, validData['callbackBodyType'], None)))
  fields.append(("x:rtype", (None, validData['customParam']['rtype'], None)))
  fields.append(("x:watermark", (None, validData['customParam']['rtype'], None)))
  fields.append(("x:templateName", (None, validData['customParam']['rtype'], None)))
  fields.append(("x:filePath", (None, validData['filePath'], None)))
  fields.append(("x:isAudit", (None, validData['customParam']['isAudit'], None)))
  fields.append(("x:x-image-app", (None, validData['customParam']['x-image-app'], None)))
  fields.append(("x:type", (None, validData['customParam']['type'], None)))
  fields.append(("x:x-image-suffix", (None, validData['customParam']['x-image-suffix'], None)))
  fields.append(("x:username", (None, validData['customParam']['username'], None)))
  fields.append(("file", ("image.png", file_content, "image/png")))
  
  #设置表单格式为 'multipart/form-data'
  m = encode_multipart_formdata(fields, boundary=boundary)

  # 目标URL
  url = 'https://csdn-img-blog.obs.cn-north-4.myhuaweicloud.com/'

  headers = {
    "Host": "csdn-img-blog.obs.cn-north-4.myhuaweicloud.com",
    "Connection": "keep-alive",
    "Content-Length": str(file_size),
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Content-Type": 'multipart/form-data; boundary=' + boundary,
    "sec-ch-ua-mobile": "?0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
    "sec-ch-ua-platform": "Windows",
    "Origin": "https://mp.csdn.net",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://mp.csdn.net/mp_blog/creation/editor?spm=1000.2115.3001.4503",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
  }

  try:
    # 发送POST请求，包含表单数据和文件
    response = requests.post(url, headers=headers, data=m[0])

    # 检查响应
    if response.ok:
        # print('Success:', response.content)
        # print('Success:', response.text)
        return json.loads(response.text)
    else:
        print('Error:', response.status_code, response.text)
        return None
  except Exception as e:
      print('Error:', e)
      return None







