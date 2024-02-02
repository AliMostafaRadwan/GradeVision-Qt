import json
from pathlib import Path
import cv2
from .AnalyzeBubbleSheet import analyze_bubble_sheet
from .merges import merge_json_files
from .Model import ObjectDetection
from PyQt5.QtCore import QObject, pyqtSignal, QThread

# Load the merged data from merged.json

class Grading:
    def __init__(self):
        self.detection = ObjectDetection() 
        self.merged_data = json.load(open('JSON/merged.json'))
        
    def grade(self, path,progress_callback):
        image_files = [str(i) for i in Path(path).glob('*')]  # Get all jpg files in the current directory
        
        for merged_item in self.merged_data:
            x, y, width, height = merged_item[0]
            num_columns = merged_item[1]
            num_rows = merged_item[2]
            column_data = merged_item[3]
            roi_info =x, y, width, height

            for images in image_files:
                img = cv2.imread(images)
                img = cv2.resize(img, (1000, 1000), interpolation=cv2.INTER_AREA)
                bubbles, roi_img, CHOICE, duplicated_row = analyze_bubble_sheet(images, roi_info, num_columns, num_rows)
                
                for row in duplicated_row:
                    print(roi_img.shape,num_columns, num_rows, row+1, roi_info)
                
                    detected_bubble = self.detection.Analize_Dublicates(img, num_columns, num_rows, row+1, roi_info)
                    if detected_bubble:
                        # print("detected_bubble", detected_bubble)
                        # remove the extra row
                        CHOICE = CHOICE[:row] + CHOICE[row+1:]
                        
                        for i in range(len(CHOICE)):
                            if CHOICE[i][0] == row:
                                if detected_bubble == 'D':
                                    CHOICE[i] = (CHOICE[i][0], 3)
                                elif detected_bubble == 'C':
                                    CHOICE[i] = (CHOICE[i][0], 2)
                                # Add more conditions for other detected_bubble values
                                elif detected_bubble == 'B':
                                    CHOICE[i] = (CHOICE[i][0], 1)
                                elif detected_bubble == 'A':
                                    CHOICE[i] = (CHOICE[i][0], 0)
                                
                student_answers = []
                for row, ans in CHOICE:
                    if ans == 0:
                        student_answers.append('A')
                    elif ans == 1:
                        student_answers.append('B')
                    elif ans == 2:
                        student_answers.append('C')
                    elif ans == 3:
                        student_answers.append('D')
                
                print(column_data,'column_data')
                print(student_answers, len(student_answers))

                print(f'=============={duplicated_row}===============')

                # creating the score function
                def score(student_answers, column_data):
                    score = 0
                    for i in range(len(student_answers)):
                        if student_answers[i] == column_data[i]:
                            score += 1
                    return score
                try:
                    print(f'Score: {score(student_answers, column_data)}')
                except:
                    print('score error')
                    pass
                
                cv2.imshow("cropped", roi_img)
                cv2.waitKey(0)
            
                percentage_of_completed_work = (image_files.index(images) / len(image_files)) * 100
                
                progress_callback.emit(int(percentage_of_completed_work))





if __name__ == '__main__':
    grading_logic = Grading()
    grading_logic.grade('C:\Main\Code\GradeVision/test10', None)  # Replace with the actual path