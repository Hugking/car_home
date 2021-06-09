def strength_pic(pic_path):
    from PIL import Image

    old_im = Image.open(pic_path)
    old_size = old_im.size

    new_size = (300, 300)
    new_im = Image.new("RGB", new_size, color='white')
    new_im.paste(old_im, (int((new_size[0] - old_size[0]) / 2),
                          int((new_size[1] - old_size[1]) / 2)))

    new_im.save(pic_path.replace('output', 'output_str'))


for png in png_list:
    strength_pic('./fontforge_output/' + png)


def baidu_ocr(pic_path: str):
    '''
    文字识别(百度)
    pic_path:图片的地址, 如./font_pic/uni3075.png
    '''
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    #     request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/webimage"
    f = open(pic_path, 'rb')
    img = base64.b64encode(f.read())

    params = {"image": img}
    # 将accessToken替换为自己的
    access_token = 'AT'
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        time.sleep(1)
        print(pic_path, response.json())
        result = response.json()
        if 'error_code' in result.keys():
            print('error', pic_path, result)
        elif result['words_result_num'] == 1:
            return result['words_result'][0]['words']
        elif result['words_result_num'] == 0:
            return ''
        else:
            print(pic_path, result)
            return None
    return None


def tencent_ocr(pic_path):
    """
    文字识别(腾讯)
    """
    import json
    from tencentcloud.common import credential
    from tencentcloud.common.profile.client_profile import ClientProfile
    from tencentcloud.common.profile.http_profile import HttpProfile
    from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
    from tencentcloud.ocr.v20181119 import ocr_client, models
    try:
        # 将SecretId和SecretKey替换为自己的
        cred = credential.Credential("SecretId", "SecretKey")
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ocr.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = ocr_client.OcrClient(cred, "ap-shanghai", clientProfile)

        #         req = models.GeneralAccurateOCRRequest()
        req = models.GeneralBasicOCRRequest()
        with open(pic_path, 'rb') as f:
            img = base64.b64encode(f.read())
        params = {
            "ImageBase64": img.decode(),
            "LanguageType": "zh"
        }
        req.from_json_string(json.dumps(params))

        #         resp = client.GeneralAccurateOCR(req)
        resp = client.GeneralBasicOCR(req)
        resp_json = json.loads(resp.to_json_string())
        time.sleep(0.1)
        return resp_json['TextDetections'][0]['DetectedText']

    except TencentCloudSDKException as err:
        print(err)


png_list = [foo for foo in os.listdir('./fontforge_output_str/') if foo.endswith('png')]

res_str_basic = {png[:-4]: tencent_ocr('./fontforge_output/' + png) for png in png_list}
