from flask import Flask, jsonify, request
import base64
from paddleocr import PaddleOCR
import numpy as np
import cv2
from PIL import Image
import io
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from entity.CocUserDateLog import CocUserDateLog
import uuid
import re


from entity.CocUserInfo import CocUserInfo


app = Flask(__name__)

ocr = PaddleOCR()

engine = create_engine('mysql+pymysql://root:9m99i52dLM@140.238.13.94:3306/coc', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/coc/api/ocr/zy', methods=['POST'])
def ocr_api():
    # 获取base64
    base64_str = request.json.get('image')
    if base64_str is None:
        return warn("图片获取失败")
    # ocr识别
    image = base64_to_image(base64_str)
    ocr_result = ocr.ocr(image)

    result_list = []
    for line in ocr_result:
        for i in line:
            temp = i[1][0]
            if temp is None or temp == '':
                temp = "0"
            result_list.append(re.sub(r'\D', '', temp))
    # 保存
    file_name = result_list[0] + "_" + result_list[1] + "_" + result_list[2]
    cv2.imwrite("images/attack/zy/" + str(file_name) + ".jpg", image)
    return success_data("操作成功", result_list)

@app.route('/coc/api/ocr/player/update', methods=['POST'])
def player_update():
    # 获取base64
    base64_str = request.json.get('image')
    user_id = request.json.get('user_id')
    # image_name = request.json.get('image_name')
    if base64_str is None:
        return warn("图片获取失败")
    
    # base64 转图片
    image = base64_to_image(base64_str)
    file_name = "images/player/images.png"
    cv2.imwrite(file_name, image)
    ocr_result = ocr.ocr(file_name)
    # 图片分割
    # split_image(image)
    
    user_info = get_user_info(ocr_result)
    print("================================================")
    print(user_info)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    if user_id is not None and user_id != "":
        user_info.id = user_id
    # 查询 
    user_info_list = session.query(CocUserInfo).filter(CocUserInfo.id==user_info.id).all()
    if user_info_list is None:
        user_info.create_time = datetime.now()
        session.add(user_info)
        user_info_log = CocUserDateLog(user_info)
        session.add(user_info_log)
    else:
        user_info.update_time = datetime.now()
        session.merge(user_info)
        user_info_log = CocUserDateLog(user_info)
        session.add(user_info_log)
    session.commit()
    return success("保存成功")


@app.route('/coc/api/ocr/player/getUserId', methods=['GET'])
def get_user_id():
    Session = sessionmaker(bind=engine)
    session = Session()
    user_info_list = session.query(CocUserInfo).all()
    result_list = []
    for user_info in user_info_list:
        result_list.append(user_info.id)
    return success_data("操作成功", result_list) 


def save_image(base64_str, file_path):
    pass

#  base64转image
def base64_to_image(base64_str):
    return cv2.imdecode(np.frombuffer(base64.b64decode(base64_str), np.uint8), cv2.IMREAD_COLOR)

# 分割图片
def split_image(img):
    with open('config') as f:
        positions = [l.strip().split(',') for l in f if l.strip() and not l.strip().startswith('#')]

    for i, pos in enumerate(positions):
        print(pos)
        file_name, x, y, w, h = map(str, pos)
        crop_img = img[int(y):int(y)+int(h), int(x):int(x)+int(w)]
        cv2.imwrite(f'images/split/{file_name}.jpg', crop_img)


# 识别
def get_user_info(ocr_result):
    new_user_info = CocUserInfo()
    with open('config') as f:
        positions = [l.strip().split(',') for l in f if l.strip() and not l.strip().startswith('#')]
    for i, pos in enumerate(positions):
        name, x, y, w, h = map(str, pos)
      #   print(name+","+x+","+y+","+str(int(x)+int(w))+","+str(int(y)+int(h)))
        if name=="等级":
            res = search_text(ocr_result, int(x), int(y), int(w), int(h))
            if res is not None:
                new_user_info.user_grade = res.replace(">", "")
        if name=="用户标签":
            new_user_info.id = search_text(ocr_result, int(x), int(y), int(w), int(h))
        if name=="用户名":
            res = search_text(ocr_result, int(x), int(y), int(w), int(h))
            if res is not None:
                new_user_info.user_name = res.replace("目","").replace("白", "").replace("百", "").replace("日", "").replace("曰", "")
        if name=="职位":
            new_user_info.user_position = search_text(ocr_result, int(x), int(y), int(w), int(h))
        if name=="部落名称":
            new_user_info.clan_name = search_text(ocr_result, int(x), int(y), int(w), int(h))
        if name=="部落等级":
            new_user_info.clan_grade = search_text(ocr_result, int(x), int(y), int(w), int(h))
        if name=="当前奖杯":
            res = search_text(ocr_result, int(x), int(y), int(w), int(h))
            if res is not None:
                res = res.replace("?","").replace("？","").replace("Y","").replace("Q","")
                if len(res) > 4:
                    new_user_info.current_trophy = res[1:]
                else:
                    new_user_info.current_trophy = res
        if name=="当前段位":
            new_user_info.current_level = search_text(ocr_result, int(x), int(y), int(w), int(h))
        if name=="历史最佳":
            res = search_text(ocr_result, int(x), int(y), int(w), int(h))
            if res is not None:
                res = res.replace("?","").replace("？","").replace("Y","").replace("Q","")
                if len(res) > 4:
                    new_user_info.all_time_best = res[1:]
                else:
                    new_user_info.all_time_best = res

        if name=="胜利之星":
            new_user_info.war_stars_won = search_text(ocr_result, int(x), int(y), int(w), int(h))
        if name=="近期捐赠":
            new_user_info.troops_donated = search_text(ocr_result, int(x), int(y), int(w), int(h))
        if name=="近期收到":
            new_user_info.troops_received = search_text(ocr_result, int(x), int(y), int(w), int(h))
        if name=="进攻获胜":
            new_user_info.attacks_won = search_text(ocr_result, int(x), int(y), int(w), int(h))
        if name=="防御获胜":
            new_user_info.defenses_won = search_text(ocr_result, int(x), int(y), int(w), int(h))
    return new_user_info

# 按坐标搜索内容
def search_text(ocr_result,x,y,w,h):
    if ocr_result is None:
        return None
    for text in ocr_result:
        for line in text:
            point_list = line[0]
            if point_list[0][0] >= x and point_list[0][1] >= y and point_list[2][0] <= x+w and point_list[2][1] <= y+h:
                return line[1][0]
    return None
# 替换特殊字符
def str_replace(str):
    if str is None :
        return ""
    else:
        return str.replace(" ", "").replace(".", "").replace("?", "").replace("-", "")

def warn(message):
    return jsonify({
        "code": "209",
        "message": message
    })


def success_data(message, data):
    return jsonify({
        "code": "200",
        "message": message,
        "data": data
    })

def success(message):
    return jsonify({
        "code": "200",
        "message": message
    })



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
