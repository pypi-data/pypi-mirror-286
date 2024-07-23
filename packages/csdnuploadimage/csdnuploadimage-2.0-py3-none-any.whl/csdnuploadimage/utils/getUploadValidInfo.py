import requests
import json





def get_valid_info(cookie):
  url = "https://imgservice.csdn.net/direct/v1.0/image/obs/upload?"
  params = {
    "type": "blog",
    "rtype": "blog_picture",
    "x-image-template": "standard",
    "x-image-app": "direct_blog",
    "x-image-dir": "direct",
    "x-image-suffix": "png"
  }

  for key in params.keys():
      url += f"{key}={params[key]}&"
  url = url[:-1]
  # print(url)

  headers = {
    "Host": "imgservice.csdn.net",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "sec-ch-ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Microsoft Edge\";v=\"126\"",
    "Accept": "*/*",
    "Content-Type": "application/json",
    "sec-ch-ua-mobile": "?0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
    "sec-ch-ua-platform": "Windows",
    "Origin": "https://mp.csdn.net",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://mp.csdn.net/mp_blog/creation/editor?spm=1000.2115.3001.4503",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Cookie": cookie
  }
  try:
    response = requests.get(url, headers=headers)
    # 检查响应
    if response.ok:
      # print('Success:', response.text)
      # print(type(response.text))
      res = json.loads(response.text)
      # print(res)
      return res['data']
    else:
      print('Error:', response.status_code, response.text)
      return None
  except Exception as e:
    print('Error:', e)
    return None