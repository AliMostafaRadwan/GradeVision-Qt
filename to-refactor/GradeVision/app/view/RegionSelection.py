import streamlit as st
from PIL import Image
from streamlit_cropper import st_cropper
from Grider import get_row_image
import cv2
import json

def regionSelection():
    st.header("Template SetUp")
    img_file = st.file_uploader(label='Upload a file', type=['png', 'jpg', 'tiff', 'jpeg'])
    realtime_update = True
    box_color = '#0000FF'
    # aspect_choice = st.sidebar.radio(label="Aspect Ratio", options=["1:1", "16:9", "4:3", "2:3", "Free"])
    Number_of_Column_Groups = st.number_input(label="Number of Coulmn Groups", min_value=1, max_value=10, value=1, step=1)
    st.divider()
    aspect_dict = {
        "1:1": (1, 1),
        "16:9": (16, 9),
        "4:3": (4, 3),
        "2:3": (2, 3),
        "Free": None
    }
    aspect_ratio = aspect_dict['Free']

    if img_file:
        FILE_TYPE = img_file.name.split(".")[-1]
        print(FILE_TYPE)
        img = Image.open(img_file)
        #resize the image
        img = img.resize((1000,1000),Image.LANCZOS)
        if not realtime_update:
            st.write("Double click to save crop")
        # Get a cropped image from the frontend
        ROI_list = []
        for i in range(Number_of_Column_Groups):

            cropped_img, rect = st_cropper(img, realtime_update=realtime_update, box_color=box_color,
                                        aspect_ratio=aspect_ratio,key=i,return_type='image')
            
            x, y, width, height = rect['left'], rect['top'], rect['width'], rect['height']

            roi = (x, y, width, height)
            # st.write(x, y, width, height)
            try:
                num_columns = st.number_input(label="Number of Columns", min_value=1, max_value=100, value=4, step=1, key=x+y)
                
                num_rows = st.number_input(label="Number of Rows", min_value=1, max_value=100, value=1, step=1, key=x*y)

                row_number = st.number_input(label="Row Number", min_value=1, max_value=num_rows, value=1, step=1, key=x/y)
            except:
                st.write("Please select a region")
                
            ROI_list.append((roi, num_columns, num_rows))
            row_image = get_row_image(img, num_columns, num_rows, row_number, roi)
            
            
            maxsize = (250,150)
        #save the json file
        
        with open("JSON/meta.json", "w") as f:
            f.write(json.dumps(ROI_list))
            
            if FILE_TYPE != "tif" and FILE_TYPE != "tiff":
                # print(row_image)
                row_image = cv2.resize(row_image,maxsize,interpolation=cv2.INTER_AREA)
                st.image(row_image)
            else:
                # print(row_image)
                row_image = Image.fromarray(row_image)
                row_image.thumbnail(maxsize, Image.LANCZOS)
                st.image(row_image)

regionSelection()