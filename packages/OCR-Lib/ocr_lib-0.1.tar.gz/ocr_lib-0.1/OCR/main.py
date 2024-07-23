import subprocess, os, cv2, shutil
import json
import argparse
import math
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageEnhance, ImageFilter

from OCR.VietOCR.vietocr.tool.predictor import Predictor
from OCR.VietOCR.vietocr.tool.config import Cfg


from OCR.CRAFT_OCR.Craft_main import load_craft_model, test_image_with_craft



def Convert_Point(points):
    x_coords = points[:,0]
    y_coords = points[:,1]
    x_min = math.ceil(min(x_coords))
    x_max = math.ceil(max(x_coords))
    y_min = math.ceil(min(y_coords))
    y_max = math.ceil(max(y_coords))
    return x_min, y_min, x_max, y_max


def OCR_Line(image_path, polys, detector):
    text_dt =[]
    text_out =[]
    output_file = 'result/result_line.txt'

    image = cv2.imread(image_path)

    w,h,c = image.shape
    thres_x = int(w/62)
    thres_y = int(h/60)
    # print(thres_x, thres_y)

    with open(output_file, 'w') as file:
        for idx, point in enumerate(polys):
            x, y, xm, ym = Convert_Point(point)
            if idx == 0:
                ymin =y
                text_dt.append((x, y, xm, ym))
            else:
                if abs(y-ymin) <= thres_y:
                    text_dt.append((x, y, xm, ym))
                    ymin = y
                if abs(y-ymin) > thres_y or np.allclose(point, polys[-1]):
                    text_dt.sort(key=lambda bbox: (bbox[0]))
                    for i, line in enumerate(text_dt):
                        x0, y0, xm0, ym0 = line
                        if i == 0:
                            text_out.append((x0, y0, xm0, ym0))
                            xmin = xm0
                        else:
                            if abs(x0 - xmin) <= thres_x:
                                text_out.append((x0, y0, xm0, ym0))
                                xmin = xm0
                            else:
                                min_x1 = min(coord[0] for coord in text_out)
                                min_y1 = min(coord[1] for coord in text_out)
                                max_x1 = max(coord[2] for coord in text_out)
                                max_y1 = max(coord[3] for coord in text_out)


                                cropped_image = image[min_y1:max_y1, min_x1:max_x1]
                                cropped_image = np.array(cropped_image)

                                cropped_image = Image.fromarray(cropped_image)



                                # cropped_image.save(f"{output_crop}/{idx+1}.jpg")
                                
                                char = detector.predict(cropped_image)

                                # file.write(f"{char} {min_x1} {min_y1} {max_x1} {max_y1}\n")
                                file.write(f"{char}\n")


                                text_out = []
                                text_out.append((x0, y0, xm0, ym0))
                                xmin = xm0
                            if line == text_dt[-1]:
                                min_x1 = min(coord[0] for coord in text_out)
                                min_y1 = min(coord[1] for coord in text_out)
                                max_x1 = max(coord[2] for coord in text_out)
                                max_y1 = max(coord[3] for coord in text_out)


                                cropped_image = image[min_y1:max_y1, min_x1:max_x1]
                                cropped_image = np.array(cropped_image)

                                cropped_image = Image.fromarray(cropped_image)

                                # cropped_image.save(f"{output_crop}/{idx+1}.jpg")
                                
                                char = detector.predict(cropped_image)

                                # file.write(f"{char} {min_x1} {min_y1} {max_x1} {max_y1}\n")
                                file.write(f"{char}\n")


                                text_out = []
                    
                    text_dt = []
                    text_dt.append((x, y, xm , ym))
                    ymin = y


def OCR_Char(image_path, polys, detector):
    text_dt =[]
    text_out =[]
    output_file = 'result/result_char.txt'

    image = cv2.imread(image_path)
    # print(image)

    with open(output_file, 'w') as file:
        for idx, point in enumerate(polys):
            x, y, xm, ym = Convert_Point(point)
            cropped_image = image[y:ym, x:xm]
            cropped_image = np.array(cropped_image)

            cropped_image = Image.fromarray(cropped_image)



            # cropped_image.save(f"{output_crop}/{idx+1}.jpg")
            
            char = detector.predict(cropped_image)

            # file.write(f"{char} {x} {y} {xm} {ym}\n")
            # file.write(f"{char}\n")


            if idx == 0:
                ymin = y
                text_dt.append((char, x, y, xm, ym))
            else:
                if abs(y-ymin) <= 8:
                    text_dt.append((char, x, y, xm, ym))
                    ymin = y

                if abs(y-ymin) > 8 or Convert_Point(point) == Convert_Point(polys[-1]):
                    text_dt.sort(key=lambda bbox: bbox[1])
                    # print(text_dt)
                    for id, line in enumerate(text_dt):
                        text, x0, y0, xm0, ym0 = line

                        if id == 0:
                            text_out.append((text, x0, y0, xm0, ym0))
                            xmin = xm0
                            
                            
                        else:
                            if abs(x0 - xmin) <= 15:
                                text_out.append((text, x0, y0, xm0, ym0))
                                xmin = xm0
                                
                            else:
                                min_x1 = int(min(coord[1] for coord in text_out))
                                min_y1 = int(min(coord[2] for coord in text_out))
                                max_x1 = int(max(coord[3] for coord in text_out))
                                max_y1 = int(max(coord[4] for coord in text_out))

                                # cropped_image.save(f"{output_crop}/{idx+1}.jpg")
                                for y_i in text_out:
                                    char_out = y_i[0]
                                    file.write(f"{char_out} ")  
            
                                # file.write(f"{min_x1} {min_y1} {max_x1} {max_y1}\n")
                                file.write(f"\n")

                                text_out = []
                                text_out.append((text, x0, y0, xm0, ym0))
                                xmin = xm0
                            if line == text_dt[-1]:
                                min_x1 = int(min(coord[1] for coord in text_out))
                                min_y1 = int(min(coord[2] for coord in text_out))
                                max_x1 = int(max(coord[3] for coord in text_out))
                                max_y1 = int(max(coord[4] for coord in text_out))

                                for x_i in text_out:
                                    char_out = x_i[0]
                                    file.write(f"{char_out} ") 
            
                                # file.write(f"{min_x1} {min_y1} {max_x1} {max_y1}\n")
                                file.write(f"\n")
                                # cropped_image.save(f"{output_crop}/{idx+1}.jpg")
                                
                                text_out = []
                    
                    text_dt = []
                    text_dt.append((char, x, y, xm, ym))
                    ymin = y

def Crop_Image(polys):
    x_crop_min = 9999
    x_crop_max = 0
    y_crop_min = 9999
    y_crop_max = 0
    for poly in polys:
        x_mi, y_mi, x_ma, y_ma  = Convert_Point(poly)
        if x_mi < x_crop_min:
            x_crop_min = x_mi 
        if y_mi < y_crop_min:
            y_crop_min = y_mi 
        if x_ma > x_crop_max:
            x_crop_max = x_ma                                
        if y_ma > y_crop_max:
            y_crop_max = y_ma 
    w, h = y_crop_max - y_crop_min, x_crop_max-x_crop_min
    t_x, t_y = w/30, h/30
    x_crop_min, y_crop_min, x_crop_max, y_crop_max = int(x_crop_min - t_x), int(y_crop_min - t_y), int(x_crop_max + t_x), int(y_crop_max + t_y)
    return x_crop_min, y_crop_min, x_crop_max, y_crop_max


def Convert_File(input_file, output_file):
    data = {}

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for idx,line in enumerate(lines):
        if 'Số' in line:
            data['số'] = lines[idx+1].strip()
        if 'Họ và tên' in line:
            data['Họ và tên'] = lines[idx+1].strip()
        if 'Sinh ngày' in line:
            data['Sinh ngày'] = f"{lines[idx+1].strip()}/{lines[idx+2].strip()}/{lines[idx+3].strip()}"
        if 'Quê quán' in line:
            data['Quê quán'] = f"{lines[idx+1].strip()} {lines[idx+2].strip()}"
        if 'Vào Đảng ngày' in line:
            data['Vào Đảng ngày'] = f"{lines[idx+1].strip()}/{lines[idx+2].strip()}/{lines[idx+3].strip()}"
        if 'Chính thức ngày' in line:
            data['Chính thức ngày'] =f"{lines[idx+1].strip()}/{lines[idx+2].strip()}/{lines[idx+3].strip()}"
        if 'Nơi cấp thẻ' in line:
            data['Nơi cấp thẻ'] = lines[idx+1].strip()
        if 'Ngày' in line:
            data['Ngày cấp thẻ'] = lines[idx].strip()
        
        

        # Ghi các thông tin vào file JSON
        with open(output_file, 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4)
    return data


def Run_Main(image_path, model_craft, detector):
    path_name = image_path.split('/')[-1]

    image_crop_path = './imag_crop/' + path_name
    net = load_craft_model(model_craft, cuda=False)

    polys = test_image_with_craft(net, image_path, cuda=False)

    image = cv2.imread(image_path)
    # print(image.shape)
    x_crop_min, y_crop_min, x_crop_max, y_crop_max = Crop_Image(polys)
    cropped_image_b = image[y_crop_min:y_crop_max, x_crop_min:x_crop_max]
    cropped_image_b = cv2.resize(cropped_image_b, (1180,1280))
    print(cropped_image_b.shape)

    cropped_image_b = np.array(cropped_image_b)
    cropped_image_b = Image.fromarray(cropped_image_b)
    cropped_image_b.save(f"{image_crop_path}")

    polys = test_image_with_craft(net, image_crop_path, cuda=False)


    OCR_Line(image_crop_path, polys, detector)
    # OCR_Char(image_crop_path, polys, detector)

    # input_file ='result/result_char.txt'
    input_file ='result/result_line.txt'
    output_file = 'result/result_final.json'
    data = Convert_File(input_file, output_file)
    return data
    


if __name__ == '__main__':


    model_craft = './CRAFT_OCR/weights/craft_mlt_25k.pth'
    image_path = './image/temp_image.jpg'

    # config = Cfg.load_config_from_name('vgg_transformer')
    config = Cfg.load_config_from_file('./OCR/VietOCR/config.yml')

    config['cnn']['pretrained']= False
    config['device'] = 'cpu'
    config['weights'] = './OCR/VietOCR/weights/seq2seqocr.pth'
    detector = Predictor(config)
    # img = './VietOCR/image/test1.png'
    # img = Image.open(img)
    # plt.imshow(img)
    # s = detector.predict(img)
    # print(s)

    Run_Main(image_path, model_craft, detector)
