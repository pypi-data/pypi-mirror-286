# -*- coding: utf-8 -*-

import cv2
import numpy as np
import matplotlib.colors as mcolors

from PIL import Image


class ImageProcessing:
    def __init__(self):
        pass
    #KeyWord

    def detect_and_mask_objects(self, image_path , contour_area = 50, color = 'green' ):
        """
        ***|    Description     |***
        |   *`Detect And Mask Objects`*   |   ส่ง path รูปภาพ และ สี เพื่อไป mask object ที่เป็นสีดังกล่าวภายในภาพ |
 
        ***|    Example     |***
        | *`Detect And Mask Objects`* | image_path | color = String | contour_area = Int
 
        ***|    Parameters     |***
        -  image_path
        -  color (ณ ปัจจุบัน มีให้ทดสอบเฉพาะ color = green)
        -  contour_area (Minimum area to consider a contour valid | หากสนใจพวกเส้นหรือตัวอักษร min_contour_area = 50-100 
        หรือหากสนใจสิ่งที่ใหญ่กว่าเช่นกรอบหรือกล่อง Text Field ให้ min_contour_area = 3500 - 5000++)

 
 
        *`ทดสอบได้เฉพาะบางหน้าเท่านั้น บางรูปอาจจะไม่สามารถจับ mask ต้องกำหนดค่าเฉพาะ`*
        """
        #read image with cv2.imread
        image = cv2.imread(image_path)

        # Convert image to HSV color space
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Define the green color range for the mask
        lower_color = None
        upper_color = None
        if color == 'green':
            lower_green = np.array([35, 50, 50])
            upper_green = np.array([85, 255, 255])

            # Create the mask
            mask = cv2.inRange(hsv,lower_green,upper_green)

            # Find contours in the binary image
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Filter contours based on their size
            min_contour_area = contour_area  # Minimum area to consider a contour valid
 
            # Filter contours with an area greater than or equal to min_contour_area | กรอง contour ที่มีพื้นที่มากกว่าหรือเท่ากับ min_contour_area
            filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]

            # Draw contours on the original image with a thin red line | วาดเส้น ตาม filtered_contours ที่มี
            draw_contour_image = cv2.drawContours(image, filtered_contours, -1, (255, 0, 0), 2)  

            # Convert image back to PIL format  | หากต้องการดูรูปให้เปิด image_pil.show()  | COLOR_BGR2RGB , cv2.COLOR_BGR2RGB , cv2.COLOR_HSV2RGB
            # image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))   #(กรณีทดสอบดูรูปแรกสุด)
            # image_pil.show()
            image_pil = Image.fromarray(image)
            # image_pil.show()

            return  len(filtered_contours) , filtered_contours
        
        if color != 'green':
            return  'Error color'
        
    def highlight_contours_objects(self, image_path , contours, indices):
        """
        ***|    Description     |***
        |   *`Highlight Contours Objects`*   |   ส่ง path รูปภาพ , contours และ indices เพื่อไป highlight object ที่ต้องการตาม indices ที่กำหนด |
 
        ***|    Example     |***
        | *`Highlight Contours Objects`* | image_path = path | contours = data filtered_contours | indices  = [array or list contours]
        | *`Highlight Contours Objects`* | image_path = C/domain/log.png | contours = data filtered_contours | indices  = [0] 

        ***|    Parameters     |***
        -  image_path
        -  contours (data filtered_contours ที่ได้จาก keyword : 'Detect And Mask Objects')
        -  indices (array or list ของตัวที่ต้องการ ภายใน data filtered_contours )

 
 
        *`ทดสอบได้เฉพาะบางหน้าเท่านั้น ค่าบางค่าอาจเอาออกมาไม่ได้เนื่องจากขนาดใหญ่เกินไป`*
        """
        #read image with cv2.imread
        image = cv2.imread(image_path)

        # Draw specified contours on the image with different colors
        for index in indices:
            color = (0, 0, 255)
            result_image = cv2.drawContours(image, contours, index, color, 3)

        # Convert image back to PIL format
        result_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        # result_image.show()

        return result_image

    def get_average_bgr_color_within_contour(self, image_path , contour):
        """
        ***|    Description     |***
        |   *`Get Average Bgr Color Within Contour`*   |   ส่ง path รูปภาพ , contours เพื่อไปคำนวณค่าสีเฉลี่ยภายใน contour โดยใช้ mask ค่าที่ได้จะเป็น B , G , R , Alpha|
 
        ***|    Example     |***
        | *`Highlight Contours Objects`* | image_path = C/domain/log.png | contours = contour[0] (เลือกเฉพาะ array contour ที่ต้องการจะส่ง)

        ***|    Parameters     |***
        -  image_path
        -  contours (data filtered_contours ที่ได้จาก Keyword : 'Detect And Mask Objects')

        *`ทดสอบได้เฉพาะบางหน้าเท่านั้น ค่าบางค่าอาจเอาออกมาไม่ได้เนื่องจากขนาดใหญ่เกินไป`*
        """
        #read image with cv2.imread
        image = cv2.imread(image_path)

        # สร้าง mask ที่มีขนาดเท่ากับภาพ โดยมีค่าเริ่มต้นเป็นสีดำ (ค่า 0)
        mask = np.zeros(image.shape[:2], dtype=np.uint8)

        # วาด contour บน mask ด้วยสีขาว
        draw = cv2.drawContours(mask, [contour], -1, (255), thickness=cv2.FILLED)

        # คำนวณค่าสีเฉลี่ยภายใน contour โดยใช้ mask
        mean_color = cv2.mean(image, mask=mask)

        # Convert image back to PIL format
        # result_image = Image.fromarray(cv2.cvtColor(draw, cv2.COLOR_BGR2RGB))
        result_image = Image.fromarray(draw)
        # result_image.show()

        return mean_color
    
    def convert_bgr_2_rgb(self, average_bgra ):
        """
        ***|    Description     |***
        |   *`Convert Bgr 2 Rgb`*   |   ส่ง averages blue green red alpha เพื่อไปแปลงเป็น numpy array และแปลงจาก BGR เป็น RGB |
 
        ***|    Example     |***
        | *`Convert Bgr 2 Rgb`* | image_path = C/domain/log.png | contours = contour[0] (เลือกเฉพาะ array contour ที่ต้องการจะส่ง)

        ***|    Parameters     |***
        -  average_bgra (ค่า mean สี ที่ได้จาก Keyword : 'Get Average Bgr Color Within Contour')

        *`.....`*
        """
        #ลบค่า alpha ออกจาก list average_bgra
        bgr_values = tuple(list(average_bgra)[:-1])

        # แปลงเป็น numpy array และแปลงจาก BGR เป็น RGB
        #ทำการ reshape array ให้มีขนาด (1, 1, 3) ซึ่งหมายถึงมี 1 แถว, 1 คอลัมน์, และ 3 ช่องสี (BGR)
        average_color_bgr_array = np.array(bgr_values, dtype=np.float32).reshape((1, 1, 3))

        #ใช้ฟังก์ชัน cvtColor ของ OpenCV เพื่อแปลงค่าจากสี BGR เป็นสี RGB
        average_color_rgb_array = cv2.cvtColor(average_color_bgr_array, cv2.COLOR_BGR2RGB)

        #ทำการ flatten array ให้เป็นแถวเดียว (1-dimensional array)
        average_color_rgb = average_color_rgb_array.flatten()

        return  average_color_rgb

    def rgb_2_matplotlib_color_name_and_hex(self, rgb_tuple ):
        """
        ***|    Description     |***
        |   *`Rgb 2 Matplotlib Color Name And Hex`*   |   ส่ง averages red green blue เพื่อไปคำนวณหา ชื่อสี และ ค่า hex ของสีนั้น |
 
        ***|    Example     |***
        | *`Rgb 2 Matplotlib Color Name And Hex`* | rgb_tuple = data rgb  (Ex : [181.69142  240.91144   21.810137])

        ***|    Parameters     |***
        -  rgb_tuple (ค่า mean สี ที่ได้จาก Keyword : 'Get Average Bgr Color Within Contour' และแปลงเป็น rgb ด้วย Keyword : 'convert_bgr_2_rgb')

        *`.....`*
        """
        # Normalize the RGB values to be between 0 and 1 | ปรับค่า RGB ให้เป็นช่วง 0-1 โดยการหารค่าของแต่ละช่องสีด้วย 255 เพื่อทำให้ข้อมูลมีมาตรฐานเดียวกัน ซึ่งช่วยให้การคำนวณระยะทางระหว่างสี
        rgb_normalized = tuple([x / 255.0 for x in rgb_tuple])

        # Find the closest color name and hex |  เป็นการคำนวณระยะทางแบบ Euclidean ระหว่างสีที่ normalized และสี CSS4 แต่ละสี
        closest_name = None
        closest_hex = None
        min_distance = float('inf')
        for name, hex_value in mcolors.CSS4_COLORS.items():
            color_rgb = mcolors.hex2color(hex_value)
            # closest_hex = hex_value
            distance = sum((component1 - component2) ** 2 for component1, component2 in zip(rgb_normalized, color_rgb))
            if distance < min_distance:
                min_distance = distance
                closest_name = name
                closest_hex = hex_value

        #ส่งคืนชื่อสีและค่า hex ของสีที่ใกล้เคียงที่สุด
        return closest_name , closest_hex



    