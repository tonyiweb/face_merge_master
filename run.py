# -*- coding: utf-8 -*-
# @Time    : 2018/05/18 13:40
# @Author  : Tony Wang

import core
import datetime
import json
import os
import random
import requests
import time
import tornado as tornado
import tornado.ioloop
import tornado.web
import core
import oss2
# 配置OSS
# Access Key ID 和 Access Key Secret
auth = oss2.Auth('****************', '***************************************')
# EndPoint
service = oss2.Service(auth, 'oss-cn-shenzhen.aliyuncs.com')
# 球星库和太太库
stars_img=['lws','kwhe','wln','bsks','msml','asxa','yske','msl','lmsl','kls','mdlq','ber','benzm','cl','mna','krwsl','mll','kly','fdk','lfl','lln','wne','hds','men','zbll','amlz','mn','meml','slh']
stars_name=['纳瓦斯','卡瓦哈尔','瓦拉内','巴斯克斯','卡塞米罗','阿森西奥','伊斯科','马塞洛','拉莫斯','克罗斯','莫德里奇','贝尔','本泽马','C罗',
            '米尼奥莱','卡里乌斯','莫雷诺','克莱因','范迪克','洛夫伦','拉拉纳','维纳尔杜姆','亨德森','米尔纳','张伯伦','埃姆雷詹','马内','菲尔米诺','萨拉赫']
stars_des=['世界最好的门将之一，反应神速，总在关键时刻力挽狂澜','世界上最好的右后卫之一',
'欧洲2000年以来最强大的中后卫，皇马未来十年可以依靠的后防擎天柱','典型的角色球员，低调、勤勉、谦虚','世界级兽腰，最佳中场之一',
'可能是梅西之后最好的左脚球员，天分过人却谦虚自律，实力颜值情商爆表','充满创造力的金童，总能成就他人所不能成之事','目前世界第一左后卫，皇马的实力队宠',
'皇马顶级后卫，球队的精神领袖，球场上的铮铮铁汉','球队的心脏，中场发动机，后哈维时代世界第一中场','球队的遥控器，创造型的无私中场',
'疾如闪电，总把球传给n秒后的自己，最好的比赛终结者','传射俱佳、注重配合、顾全大局的团队攻击手','霸气王者，独一无二的进球永动机',
'一个很会玩的门将，个性开朗的大个子让人又爱又恨','观察力一流的门将，超强的阅读比赛能力','攻防俱佳的左后卫，无往而不利',
'就是一辆跑车，速度快身体壮，而且头脑聪明','史上最贵后卫，红军历史最贵球员','球场上以钢铁后卫的硬汉形象示人，生活里是一个童心未泯的大男孩',
'球风潇洒，球技超群，灵气逼人！要被你迷倒啦(^_-)','冷静从容，最出色的边锋之一，要被你迷倒啦(^_-)','球员的楷模，拥有成为伟大队长的潜质，要被你迷倒啦(^_-)',
'球商很高的足坛万金油，绿茵场上少有的绅士','足坛新一代“梗王”，从尴尬大龄新秀到华丽蜕变的励志哥','核心中前卫，总能突破各种限制',
'火燎的金刚，烟熏的太岁，勇猛、迅速且致命','自带防守属性的前场润滑剂，重新定义了中锋','红色法老王，红军新晋偶像，埃及的民族英雄'
           ]
mrstars_img=['wlnn','asx','ysk','lms','bzm','clp','clt','krws','zbl','fel']
mrstars_name=['瓦拉内妻子卡梅莉','阿森西奥女友玛琳娜','伊斯科女友萨拉蒙','拉莫斯女友皮拉尔','本泽马女友科拉','C罗前女友伊莲娜','C罗太太乔治娜','卡里乌斯女友阿尔伯特','张伯伦女友佩莉','菲尔米诺妻子佩雷拉']
mrstars_short_name=['卡梅莉','玛琳娜','萨拉蒙','皮拉尔','科拉','伊莲娜','乔治娜','阿尔伯特','佩莉','佩雷拉']
mrstars_des=['明目皓齿，珠圆玉润的气质美人','一笑倾人城，再笑倾人国的sunshine girl',
'一心负责貌美如花','才华颜值兼具的绝色佳人','热情似火，野性十足的性感女神',
'长腿蜂腰身材棒，性感妩媚气质佳的世界超模','该吃就吃，该有肉就有肉的邻家女孩','少女的脸蛋，妖精的身材',
'性感火辣的邻家坏女孩','阳刚和美貌并存的性感女神'
             ]

 # 上传图片文件到OSS上，返回网络路径，上传完之后删除本地的文件
def uploadFileToOSS(output_file):
    bucket = oss2.Bucket(auth, 'http://oss-cn-shenzhen.aliyuncs.com', 'sp-image')
    filePath = 'https://sp-image.oss-cn-shenzhen.aliyuncs.com/'
    fileName = 'worldcup/'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S')+'_'+str(random.randint(0,9))+'.jpg'
    bucket.put_object_from_file(fileName, output_file)
    if os.path.exists(output_file):
        # 删除文件
        os.remove(output_file)
    return filePath+fileName

  # 将OSS上的图片下载到本地文件夹
def downloadImageFromUrl(imageUrl):
    #临时文件，后面取得文件名的方式自己修改
    tempFileName = 'images/temp_'+imageUrl.split('/')[5].split('.')[0]+'.jpg'
    if os.path.exists(tempFileName):
        pass
    else:
        imageData = requests.get(imageUrl)
        with open(tempFileName, 'wb') as file:
            file.write(imageData.content)
    return tempFileName

 # 将模特的图片下载到本地文件夹，如果已经存在model的图片就不再下载
def getModelImage(gender,deltaData):
    index=0
    url=''
    modelName=''
    modelShortName=''
    modelDescription=''
    if int(gender)==1:
        if float(deltaData)>=540:
            index=13
        elif float(deltaData)>=520 and float(deltaData)<540:
            inddex=0
        elif float(deltaData) >= 510 and float(deltaData) < 520:
            index=27
        elif float(deltaData) >= 504 and float(deltaData) < 510:
            index=25
        elif float(deltaData) >= 495 and float(deltaData) < 504:
            index=11
        elif float(deltaData) >= 470 and float(deltaData) < 495:
            index=4
        elif float(deltaData) >= 464 and float(deltaData) < 470:
            index=10
        elif float(deltaData) >= 461 and float(deltaData) < 464:
            index=23
        elif float(deltaData) >= 458 and float(deltaData) < 461:
            index=2
        elif float(deltaData) >= 451 and float(deltaData) < 458:
            index=21
        elif float(deltaData) >= 446 and float(deltaData) < 451:
            index=22
        elif float(deltaData) >= 442 and float(deltaData) < 446:
            index=9
        elif float(deltaData) >= 440 and float(deltaData) < 442:
            index=14
        elif float(deltaData) >= 435 and float(deltaData) < 440:
            index=16
        elif float(deltaData) >= 428 and float(deltaData) < 435:
            index=5
        elif float(deltaData) >= 415 and float(deltaData) < 428:
            index=15
        elif float(deltaData) >= 408 and float(deltaData) < 415:
            index=1
        elif float(deltaData) >= 403 and float(deltaData) < 408:
            index=6
        elif float(deltaData) >= 400 and float(deltaData) < 403:
            index=3
        elif float(deltaData) >= 392 and float(deltaData) < 400:
            index=19
        elif float(deltaData) >= 370 and float(deltaData) < 392:
            index=8
        elif float(deltaData) >= 340 and float(deltaData) < 370:
            index=26
        elif float(deltaData) >= 322 and float(deltaData) < 340:
            index=12
        elif float(deltaData) >= 300 and float(deltaData) < 322:
            index=28
        elif float(deltaData) >= 270 and float(deltaData) < 300:
            index=18
        elif float(deltaData) >= 258 and float(deltaData) < 270:
            index=20
        elif float(deltaData) >= 230 and float(deltaData) < 258:
            index=7
        else:
            index=24
        url = 'http://res.pro365.cn/worldcup_star/' +str(stars_img[index]) +'.jpg'
        modelName = str(stars_name[index])
        modelShortName = str(stars_name[index])
        modelDescription = str(stars_des[index])
    elif int(gender)==2:
        if float(deltaData)>=2000:
            index=4
        elif float(deltaData)>=1000 and float(deltaData)<2000:
            index=6
        elif float(deltaData)>=700 and float(deltaData)<1000:
            index=8
        elif float(deltaData)>=500 and float(deltaData)<700:
            index=7
        elif float(deltaData)>=350 and float(deltaData)<500:
            index=0
        elif float(deltaData)>=280 and float(deltaData)<350:
            index=5
        elif float(deltaData)>=210 and float(deltaData)<280:
            index=9
        elif float(deltaData)>=170 and float(deltaData)<210:
            index=3
        elif float(deltaData)>=148 and float(deltaData)<170:
            index=2
        else:
            index=1
        url = 'http://res.pro365.cn/worldcup_star/' + str(mrstars_img[index]) + '.jpg'
        modelName = str(mrstars_name[index])
        modelShortName = str(mrstars_short_name[index])
        modelDescription = str(mrstars_des[index])
    # 临时文件，后面取得文件名的方式自己修改
    tempFileName = 'images/model_' + url.split('/')[4].split('.')[0] + '.jpg'
    if os.path.exists(tempFileName):
        pass
    else:
        imageData = requests.get(url)
        with open(tempFileName, 'wb') as file:
            file.write(imageData.content)
    return tempFileName,url,modelName,modelShortName,modelDescription

def getTriangleData(dst_img):
    src_matrix, src_points, src_faces, err = core.face_points(dst_img)
    # 计算人脸三角形面积(双眼球和下巴最中间点)，保证同一张脸多次访问结果一致
    result = 0
    if isinstance(src_faces, dict):
        x1 = src_faces['face_shape']['pupil'][0]['x'] - src_faces['face_shape']['pupil'][1]['x']
        x2 = src_faces['face_shape']['pupil'][0]['x'] - src_faces['face_shape']['face_profile'][10]['x']
        x3 = src_faces['face_shape']['pupil'][1]['x'] - src_faces['face_shape']['face_profile'][10]['x']
        y1 = src_faces['face_shape']['pupil'][0]['y'] - src_faces['face_shape']['pupil'][1]['y']
        y2 = src_faces['face_shape']['pupil'][0]['y'] - src_faces['face_shape']['face_profile'][10]['y']
        y3 = src_faces['face_shape']['pupil'][1]['y'] - src_faces['face_shape']['face_profile'][10]['y']
        result= (x1*x1 + x2*x2 + x3*x3 + y1*y1 + y2*y2 + y3*y3)/100
    else:
        rTemp = src_faces.replace("u'", "\"")
        rTemp = rTemp.replace("'", "\"")
        src_faces = json.loads(rTemp)
        x1 = src_faces['face_shape']['pupil'][0]['x'] - src_faces['face_shape']['pupil'][1]['x']
        x2 = src_faces['face_shape']['pupil'][0]['x'] - src_faces['face_shape']['face_profile'][10]['x']
        x3 = src_faces['face_shape']['pupil'][1]['x'] - src_faces['face_shape']['face_profile'][10]['x']
        y1 = src_faces['face_shape']['pupil'][0]['y'] - src_faces['face_shape']['pupil'][1]['y']
        y2 = src_faces['face_shape']['pupil'][0]['y'] - src_faces['face_shape']['face_profile'][10]['y']
        y3 = src_faces['face_shape']['pupil'][1]['y'] - src_faces['face_shape']['face_profile'][10]['y']
        result = (x1 * x1 + x2 * x2 + x3 * x3 + y1 * y1 + y2 * y2 + y3 * y3)/100
    return result,src_matrix, src_points

# 人脸融合
def merge_one(dst_img,deltaData,gender,alpha,dst_matrix, dst_points):
    nowTime =time.time()
    # 参数
    src_img,src_url,modelName,modelShortName,modelDescription = getModelImage(gender,deltaData)
    out_img = 'result/output'+str(int(time.time() * 1000))+'.jpg'
    face_area = [100, 50, 500, 500]

    # src_img —— 模特图片
    # dst_img —— 待融合的图片
    # out_img —— 结果图片输出路径
    # face_area —— 指定模板图中进行人脸融合的人脸框位置。四个正整数数组，依次代表人脸框左上角纵坐标（top），左上角横坐标（left），人脸框宽度（width），人脸框高度（height），通过设定改参数可以减少结果的大范围变形，把变形风险控制在人脸框区域
    # alpha —— 融合比例，范围 [0,1]。数字越大融合结果包含越多融合图 (dst_img) 特征。
    # blur_size—— 模糊核大小，用于模糊人脸融合边缘，减少融合后的违和感
    # mat_multiple —— 缩放获取到的人脸心型区域
    # 头像融合
    core.face_merge(src_img=src_img,
                    dst_img=dst_img,
                    out_img=out_img,
                    face_area=face_area,
                    alpha=alpha,
                    k_size=(10, 5),
                    mat_multiple=0.95,dst_matrix=dst_matrix, dst_points=dst_points)
    final_img = uploadFileToOSS(out_img)
    print('Face Merge Success: ',final_img)
    endTime = time.time()
    print('Time Cost: ',(endTime - nowTime))
    return final_img,src_url,modelName,modelShortName,modelDescription

 #访问方式：http://127.0.0.1:9010/merge?gender=1&url=http://sp-image.oss-cn-shenzhen.aliyuncs.com/worldcup/1805/f6e94247-65a4-4cf1-aa2d-941b80c360ee.jpg
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        nowTime = time.time()
        url = self.get_argument("url")
        gender = self.get_argument("gender")
        print('======Begin Face Merge ======: ', str(gender)+'==='+url)
        # 要融合的图片下载一次就够了
        dst_img = downloadImageFromUrl(url)
        deltaData,dst_matrix, dst_points = getTriangleData(dst_img)

        # 生成不同融合度的图片
        images = []
        # images.append(url)
        output_image,src_url,modelName,modelShortName,modelDescription = merge_one(dst_img,deltaData, gender, 1,dst_matrix, dst_points)
        images.append(output_image)
        output_image2,src_url,modelName,modelShortName,modelDescription = merge_one(dst_img,deltaData, gender, 0.7,dst_matrix, dst_points)
        images.append(output_image2)
        output_image3, src_url, modelName, modelShortName, modelDescription = merge_one(dst_img, deltaData, gender, 0.4,dst_matrix, dst_points)
        images.append(output_image3)
        images.append(src_url)
        print(images)
        # 返回结果
        self.write({"imageUrl": images,"modelName":modelName,'modelShortName':modelShortName,'description':modelDescription})
        # 删除文件
        tempImage = str(dst_img)
        if os.path.exists(tempImage):
            # 删除文件
            os.remove(tempImage)
        endTime = time.time()
        print ('Total Cost: ',(endTime-nowTime))

class HealthHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.write({"status": 'up'})


def make_app():
    return tornado.web.Application([
        (r"/merge", MainHandler),
        (r"/health", HealthHandler)
    ])

def main():
    try:
        #通过127.0.0.1:9010来访问
        app = make_app()
        app.listen(9010)
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt as e:
        print (e)

if __name__ == "__main__":
        main()



