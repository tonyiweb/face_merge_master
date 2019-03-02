# -*- coding: utf-8 -*-
# @Time    : 2018/05/18 13:40
# @Author  : Tony Wang
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
auth = oss2.Auth('你的阿里云AccessKeyId', '你的阿里云AccessKeySecret')
service = oss2.Service(auth, 'oss-cn-shenzhen.aliyuncs.com')

 # 上传图片文件到OSS上，返回网络路径，上传完之后删除本地的文件
def uploadFileToOSS(output_file):
    bucket = oss2.Bucket(auth, 'http://oss-cn-shenzhen.aliyuncs.com', 'ltian-2017')
    filePath = 'https://ltian-2017.oss-cn-shenzhen.aliyuncs.com/'
    fileName = 'timecamera/result_image/'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S')+'_'+str(random.randint(0,9))+'.png'
    bucket.put_object_from_file(fileName, output_file)
    if os.path.exists(output_file):
        # 删除文件
        os.remove(output_file)
    return filePath+fileName

# 将OSS上的图片下载到本地文件夹-用户上传的图片
def downloadImageFromUrl(imageUrl):
    tempFileName = 'users/user_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S')+'_'+str(random.randint(0,9))+'.png'
    if os.path.exists(tempFileName):
        pass
    else:
        imageData = requests.get(imageUrl)
        with open(tempFileName, 'wb') as file:
            file.write(imageData.content)
    return tempFileName

 # 将模特的图片下载到本地文件夹，如果已经存在model的图片就不再下载
def getModelImage(cityIndex,locationIndex,gender):
    tempFileName = 'images/city'+str(cityIndex)+'_location'+str(locationIndex)+'_gender'+str(gender)+'.png'
    return tempFileName

# 人脸融合
def merge_one(src_img,dst_img,alpha,dst_matrix, dst_points):
    nowTime =time.time()
    # 参数
    out_img = 'result/output'+str(int(time.time() * 1000))+'.png'
    # face_area = [100, 50, 500, 500]
    face_area = [50, 50, 500, 500]

    # 头像融合
    core.face_merge(src_img=src_img,
                    dst_img=dst_img,
                    out_img=out_img,
                    face_area=face_area,
                    alpha=alpha,
                    k_size=(10, 5),
                    mat_multiple=0.9, dst_matrix=dst_matrix, dst_points=dst_points)
    final_img = uploadFileToOSS(out_img)
    print('Face Merge Success: ',final_img)
    endTime = time.time()
    print('Time Cost: ',(endTime - nowTime))
    return final_img

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        nowTime = time.time()
        url = self.get_argument("url")
        cityIndex = int(self.get_argument("cityIndex"))
        locationIndex = int(self.get_argument("locationIndex"))
        gender=int(self.get_argument("gender"))
        print('======Begin Face Merge ======: ', str(cityIndex)+'==='+url+'==='+str(locationIndex)+"==="+str(gender))
        # 要融合的图片下载一次就够了——用户上传的图片
        dst_img = downloadImageFromUrl(url)
        dst_matrix, dst_points, dst_faces, err = core.face_points(dst_img)

        # 取得model的图片,下载一次就够了
        src_img = getModelImage(cityIndex,locationIndex,gender)

        # 生成不同融合度的图片
        # images.append(url)
        output_image = merge_one(src_img,dst_img, 1,dst_matrix, dst_points)
        self.write({"imageUrl": output_image})
#         tempImage = str(dst_img)
#         if os.path.exists(tempImage):
#             # 删除文件
#             os.remove(tempImage)
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
        app = make_app()
        app.listen(8001)
        # 定时任务
        # tornado.ioloop.PeriodicCallback(crontab_update, 30*60*1000).start()  # 这里的时间是毫秒
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt as e:
        print (e)

if __name__ == "__main__":
        main()




