
import streamlit as st
import os
import zipfile
from io import BytesIO
from PIL import Image, ImageOps, ImageChops
import shutil
import pytesseract

import cv2
import numpy as np
from pytesseract import Output


#st.layout(width="80%")



def trim_image(image, border=10):
    # 使用 getbbox 來裁剪圖片周圍的空白部分
    bg = Image.new(image.mode, image.size, image.getpixel((0, 0)))
    diff = ImageOps.invert(ImageChops.difference(image, bg))
    bbox = diff.getbbox()
    if bbox:
        # 裁剪圖片
        image = image.crop(bbox)
        # 添加邊距
        return ImageOps.expand(image, border=border, fill=image.getpixel((0, 0)))
    return image

def clear_ocr_files_directory(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)


def save_uploaded_file(uploaded_file, directory):
    try:
        # 清空 ocr_files 目錄
        clear_ocr_files_directory(directory)
        
        # 保存上傳的 ZIP 文件到臨時緩存中
        with BytesIO(uploaded_file.read()) as zf:
            with zipfile.ZipFile(zf, 'r') as zip_ref:
                # 指定解壓縮時使用的編碼方式
                for zip_info in zip_ref.infolist():
                    zip_info.filename = zip_info.filename.encode('cp437').decode('big5')  # 修改這一行，根據實際情況調整編碼
                    zip_ref.extract(zip_info, directory)
        return True
    except Exception as e:
        st.error(f"出現錯誤: {e}")
        return False


def BSMI(item):

   
    with open(item, 'rb') as f:
        image_cv2 = cv2.imdecode(np.frombuffer(f.read(), np.uint8), cv2.IMREAD_COLOR)    
   
    assert image_cv2 is not None, "file could not be read, check with os.path.exists()"
    
    gray = cv2.cvtColor(image_cv2, cv2.COLOR_BGR2GRAY)
    
    img2 = gray.copy()
    
    
    template = cv2.imread('BSMIPNG.png', cv2.IMREAD_GRAYSCALE)
    assert template is not None, "file could not be read, check with os.path.exists()"
    
    #w, h = template.shape[::-1]
    # All the 6 methods for comparison in a list
    
    methods = ['TM_CCOEFF', 'TM_CCOEFF_NORMED', 'TM_CCORR',
     'TM_CCORR_NORMED', 'TM_SQDIFF', 'TM_SQDIFF_NORMED']

    meth = 'TM_CCOEFF_NORMED'
    img = img2.copy()
    method = getattr(cv2, meth)

    min_max_best = -99
    scale_best = -1
    top_left_best = []
    #bsmi_find = False
    w_best = -1
    h_best = -1

    for scale in np.arange(0.1, 1.0, 0.01):
        resized_template = cv2.resize(template, (0, 0), fx=scale, fy=scale)
        
        w, h = resized_template.shape[::-1]

        # Apply template Matching
        res = cv2.matchTemplate(img,resized_template,method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        top_left = max_loc
        min_max = max_val

        if(min_max_best > 0.7 and min_max < min_max_best):
            break
        
        if(min_max > min_max_best):
            min_max_best = min_max
            scale_best = scale
            top_left_best = top_left
            w_best = w
            h_best = h
            
            
            


    bottom_right = (top_left_best[0] + w_best, top_left_best[1] + h_best)
    cv2.rectangle(image_cv2, top_left_best, bottom_right, (255, 0, 0), 2)
    
    return image_cv2,min_max_best,scale_best,top_left_best


def list_files_in_directory(directory):
    # 遞迴列出目錄中的所有文件和子目錄
    files_and_dirs = []
    for root, dirs, files in os.walk(directory):
        for name in files:
            if name.lower().endswith('.png'):
                files_and_dirs.append(os.path.join(root, name))
        #for name in dirs:
        #    files_and_dirs.append(os.path.join(root, name))
    
	#return files_and_dirs
	
    #st.write("文件列表：")

	# 列出目錄中的所有文件和子目錄
    items = files_and_dirs

    if not items:
        st.write("目錄中沒有文件或子目錄。")
        return

    # 使用 st.selectbox 顯示文件和子目錄
    selected_file = st.selectbox('選擇要處理的文件：', items)


    if selected_file and os.path.isfile(selected_file) and selected_file.lower().endswith('.png'):
        cols = st.columns(2)

        cols[0].write(f"{selected_file}")    
			
        if cols[1].button(f"OCR&識別圖片 ", key=selected_file):
				
            image = Image.open(selected_file)
            # image2 = trim_image(image)

            #text = pytesseract.image_to_string(image, lang='chi_tra')
            
            #text_psm3 = pytesseract.image_to_string(image, lang='chi_tra', config='--psm 3')
            #st.write(text)
            #cols[0].markdown('*tesseract --psm 3:*')
            #cols[0].write(text_psm3)

            text_psm6 = pytesseract.image_to_string(image, lang='chi_tra', config='--psm 6')
				
            cols[0].markdown('*OCR 結果:*')
            cols[0].write(text_psm6)

            # 在兩欄之間插入一條分隔線
            st.markdown("""
            <style>
            div[data-testid="column"] {
                border-right: 1px solid #e6e6e6;
                padding-right: 20px;
            }
            </style>
            """, unsafe_allow_html=True)
                
            #BSMI start
                
            image_cv2,min_max_best,scale_best,top_left_best = BSMI(selected_file)
                
            BSMI_result = '不存在'
            if(min_max_best >= 0.7):
                BSMI_result = f'存在; 座標:{top_left_best}'
            
            
            cols[1].markdown('*BSMI識別結果:*')
            
            cols[1].write(f'最佳係數(TM_CCOEFF_NORMED):{min_max_best:.4f}')
            
            cols[1].write(f'最佳尺度(scale):{scale_best:.4f}')
            
            cols[1].write(f'BSMI圖形:{BSMI_result}')
            
            #BSMI end

            st.divider()

            st.markdown('*原圖檔:*')
            st.image(image, caption=os.path.basename(selected_file))
            
            st.markdown('*識別圖檔:*')
            st.image(image_cv2, caption=os.path.basename(selected_file))
            
            
            
            #cols[0].image(image2, caption=os.path.basename(item))
            

	

def main():
    #st.title("OCR Files Browser")

    directory = 'ocr_files'  # 這是你要顯示的目錄


    # 創建文件上傳控件
    
    
    
	#st.markdown("### 上傳並解壓縮 ZIP 檔案")
    
	#uploaded_file = st.file_uploader("選擇一個 ZIP 檔案", type=["zip"])

	#if uploaded_file is not None:
	#	if save_uploaded_file(uploaded_file, directory):
	#		st.success("文件上傳並解壓縮成功！")
     

            # 列出解壓縮後的文件
            # st.write("解壓縮後的文件列表：")
            # 列出目錄中的所有文件和子目錄


	#	else:
	#		st.error("文件上傳或解壓縮失敗。")
    
			
    list_files_in_directory(directory)

main()

