from paddleocr import PaddleOCR, draw_ocr

from entity.CocUserInfo import CocUserInfo
# Paddleocr目前支持中英文、英文、法语、德语、韩语、日语，可以通过修改lang参数进行切换
# 参数依次为`ch`, `en`, `french`, `german`, `korean`, `japan`。
# ocr = PaddleOCR(cls_model_dir="/home/ubuntu/app/ocr/model/ch_ppocr_mobile_v2.0_cls_infer",det_model_dir="/home/ubuntu/app/ocr/model/ch_ppocr_server_v2.0_det_infer",rec_model_dir="/home/ubuntu/app/ocr/model/ch_ppocr_server_v2.0_rec_infer") # need to run only once to download and load model into memory
ocr = PaddleOCR()

def main(img_path):
   result = ocr.ocr(img_path)

   # print("============================")
   # print(result)
   # for line in result:
   #    for i in line:
   #       print("x: " + str(i[0][0][0]) + " y: " + str(i[0][0][1])  + " w: " + str(abs(i[0][2][0])) + " h: " + str(i[0][2][1]) + "  value: " + str(i[1]))
   print(get_user_info(result))



def get_user_info(ocr_result):
    new_user_info = CocUserInfo()
    with open('config') as f:
        positions = [l.strip().split(',') for l in f if l.strip() and not l.strip().startswith('#')]
    for i, pos in enumerate(positions):
        name, x, y, w, h = map(str, pos)
      #   print(name+","+x+","+y+","+str(int(x)+int(w))+","+str(int(y)+int(h)))
        if name=="等级":
            new_user_info.user_grade = search_text(ocr_result, int(x), int(y), int(w), int(h))
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

import os

if __name__ == "__main__":
    # for root, dirs, files in os.walk("images/player"):
    #   for file_name in files:
    #      # 打印文件的绝对路径
    #      file_path = os.path.join(root, file_name)
    #      main(file_path)
     main("images/player191ce155b32f450aa526b0c49b484915.png")