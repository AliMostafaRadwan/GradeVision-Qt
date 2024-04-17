import sys
import json
from pathlib import Path
import cv2
import time  # Import the time module
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QThread
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QStackedWidget
from PyQt5.QtGui import QPixmap, QImage
from qfluentwidgets import PrimaryPushButton, InfoBar, InfoBarPosition,setThemeColor, setTheme, Theme
from .GradingWidget_UI import Ui_Form
from .AnalyzeBubbleSheet import analyze_bubble_sheet
from .merges import merge_json_files
from .Model import ObjectDetection
import csv
# from qfluentwidgets import StateToolTip, PushButton, setTheme, Theme


class StartWidget(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        # self.path = json.load(open('JSON/folder_path.json'))
        # if the path is not provided

        self.initUI() 

    def initUI(self): 
        layout = QVBoxLayout()
        
        self.start_button = PrimaryPushButton('Start')
        self.start_button.clicked.connect(self.start_button_clicked)
        #read the model_status.json file to check if the model is loaded
        
            
        
            
        layout.addWidget(self.start_button, alignment=Qt.AlignCenter)
        self.setLayout(layout)

    def start_button_clicked(self):
        # Show the main grading page
        while True:
            self.path = json.load(open('GradeVision/app/view\JSON/folder_path.json'))
            if self.path == '':
                InfoBar.error(
                    title='no folder selected',
                    content=f'please select a folder to start grading',
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3400,
                    parent=self
                )
                print('no folder selected', self.path, 'path')

                return
            else:
                
                self.hide()
                grading_app = GradingApp(self.path)
                self.stacked_widget.addWidget(grading_app)
                self.stacked_widget.setCurrentWidget(grading_app)
                #merge the json files
                merge_json_files(r'GradeVision\app\view\JSON\meta.json', r'GradeVision\app\view\JSON\output.json', r'GradeVision\app\view\JSON\merged.json')
                break


class GradingApp(QWidget, Ui_Form):
    progress_changed = pyqtSignal(int)
    
    def update_images_label(self, roi_img):
        # Convert the BGR image to RGB and resize for uniformity
        height, width, channel = roi_img.shape

        # resize the image with keeping the aspect ratio
        new_width = 250
        new_height = int(new_width * height / width)

        # Resize the image with the new dimensions
        roi_img_resized = cv2.resize(roi_img, (250, 250), interpolation=cv2.INTER_AREA)
        height, width, channel = roi_img_resized.shape
        bytesPerLine = 3 * width
        qImg = QImage(roi_img_resized.data, width, height, bytesPerLine, QImage.Format_RGB888)

        pixmap = QPixmap.fromImage(qImg)
        self.images_label.setPixmap(pixmap)
        self.images_label.setAlignment(Qt.AlignCenter)

    def __init__(self, path):
        super().__init__()
        self.setupUi(self)
        self.setObjectName("grading")
        self.grading_logic = GradingLogic(self)

        # showing the interface
        self.ProgressRing.setValue(0)

        self.PlainTextEdit.setReadOnly(True)
        self.CaptionLabel.setText("")
        # self.StateToolTip('loaded', 'the model is loaded', self)
        # self.StateToolTip.hide()

        
        # Connect the output signal from GradingLogic to display in the PlainTextEdit
        self.grading_logic.output_changed.connect(self.update_output)

        # connect the caption signal from GradingLogic to display in the CaptionLabel
        self.grading_logic.caption_changed.connect(self.update_caption)

        # Connect the roi_img signal from GradingLogic to display in the images_label
        self.grading_logic.roi_img_changed.connect(self.update_images_label)

        # Start the grading process in a separate thread
        self.grading_logic.progress_changed.connect(self.update_progress)
        self.grading_thread = GradingThread(self.grading_logic, path)
        self.grading_thread.start()
        self.show()

        self.grading_logic.number_of_completed_work.connect(self.update_number_of_completed_work)

    def update_progress(self, value):
        # Update the progress ring value
        self.ProgressRing.setValue(value)

    def update_output(self, text):
        # Update the output text using cursor
        self.PlainTextEdit.moveCursor(1)
        self.PlainTextEdit.insertPlainText(text)
        self.PlainTextEdit.moveCursor(1)
        

    def update_caption(self, text):
        # Update the caption text
        self.CaptionLabel.setText(text)
    
    def update_number_of_completed_work(self, value):
        if value > 1:
            self.StateToolTip.hide()

class GradingThread(QThread):
    def __init__(self, grading_logic, path):
        super().__init__()
        self.grading_logic = grading_logic
        self.path = path

    def run(self):
        # Perform grading
        self.grading_logic.grade(self.path)


class GradingLogic(QObject):
    progress_changed = pyqtSignal(int)
    output_changed = pyqtSignal(str)
    caption_changed = pyqtSignal(str)
    roi_img_changed = pyqtSignal(object)
    number_of_completed_work = pyqtSignal(int)
    
    
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.detection = ObjectDetection()
        self.merged_data = json.load(open('GradeVision/app/view\JSON\merged.json')) # Load the merged data

        # New attribute to store data
        self.grading_data = {}

    def grade(self, path):
        image_files = [str(i) for i in Path(path).glob('*')]

        iterationCount = 0
        for merged_item in self.merged_data:
            x, y, width, height = merged_item[0]
            num_columns = merged_item[1]
            num_rows = merged_item[2]
            column_data = merged_item[3]
            roi_info = x, y, width, height

            for idx, images in enumerate(image_files):
                start_time = time.time()  # Record the start time
                img = cv2.imread(images)
                img = cv2.resize(img, (1000, 1000), interpolation=cv2.INTER_AREA)
                bubbles, roi_img, CHOICE, duplicated_row = analyze_bubble_sheet(images, roi_info, num_columns,
                                                                               num_rows)

                wrong_answers = []  # New list for storing wrong answers

                for row in duplicated_row:
                    print(roi_img.shape, num_columns, num_rows, row + 1, roi_info)
                    self.output_changed.emit(f'{roi_img.shape}, {num_columns}, {num_rows}, {row + 1}, {roi_info}')

                    detected_bubble = self.detection.Analize_Dublicates(img, num_columns, num_rows, row + 1, roi_info)
                    if detected_bubble:
                        CHOICE = CHOICE[:row] + CHOICE[row + 1:]
                        
                        
                        for i in range(len(CHOICE)):
                            if CHOICE[i][0] == row:
                                if detected_bubble == 'D':
                                    CHOICE[i] = (CHOICE[i][0], 3)
                                elif detected_bubble == 'C':
                                    CHOICE[i] = (CHOICE[i][0], 2)
                                elif detected_bubble == 'B':
                                    CHOICE[i] = (CHOICE[i][0], 1)
                                elif detected_bubble == 'A':
                                    CHOICE[i] = (CHOICE[i][0], 0)

                lang = json.load(open('GradeVision/app/view\JSON\lang.json'))
                student_answers = []
                if lang == 'English':
                    for row, ans in CHOICE:
                        if ans == 0:
                            student_answers.append('A')
                        elif ans == 1:
                            student_answers.append('B')
                        elif ans == 2:
                            student_answers.append('C')
                        elif ans == 3:
                            student_answers.append('D')
                elif lang == 'Arabic':
                    for row, ans in CHOICE:
                        if ans == 0:
                            student_answers.append('D')
                        elif ans == 1:
                            student_answers.append('C')
                        elif ans == 2:
                            student_answers.append('B')
                        elif ans == 3:
                            student_answers.append('A')
                    
                print(column_data, 'column_data')
                print(student_answers, len(student_answers))

                def score(student_answers, column_data):
                    score = 0
                    wrong_answers = []
                    for i in range(len(student_answers)):
                        if student_answers[i] == column_data[i]:
                            score += 1
                        else:
                            wrong_answers.append((i + 1, student_answers[i]))  # Store the question number and answer
                    return score, wrong_answers

                self.output_changed.emit(f'=============={duplicated_row}===============')
                self.output_changed.emit(f'{student_answers}')
                self.output_changed.emit(f'{column_data}')

                self.caption_changed.emit(f'{iterationCount + 1}/{len(self.merged_data)}')
                try:
                    score_value, wrong_answers_list = score(student_answers, column_data)
                    print(f'Score: {score_value}')
                except:
                    print('score error')
                    pass
                self.roi_img_changed.emit(roi_img)

                processing_time = time.time() - start_time  # Calculate processing time

                percentage_of_completed_work = (image_files.index(images) / len(image_files)) * 100
                self.progress_changed.emit(int(percentage_of_completed_work))
                self.number_of_completed_work.emit(image_files.index(images) + 1)

                try:
                    output_text = f"Processing: {images}\nScore: {score_value}\n" \
                                  f"Wrong Answers: {wrong_answers_list}\n" \
                                  f"Processing Time: {processing_time:.2f} seconds\n"
                    self.output_changed.emit(output_text)

                    # Add data to the storage attribute
                    if images not in self.grading_data:
                        self.grading_data[images] = {
                            'Student Answers': [],
                            'Answer Key': [],
                            'Score': 0,
                            'Wrong Answers': [],
                            'Processing Time': 0.0
                        }

                    self.grading_data[images]['Student Answers'].extend(student_answers)
                    self.grading_data[images]['Answer Key'].extend(column_data)
                    self.grading_data[images]['Score'] += score_value
                    self.grading_data[images]['Wrong Answers'].extend(wrong_answers_list)
                    self.grading_data[images]['Processing Time'] += processing_time

                except:
                    pass
            iterationCount += 1

        # Save data to CSV after grading is complete
        csv_filename = 'GradeVision/app/view\grading_data.csv'
        with open(csv_filename, 'w', newline='') as csvfile:
            fieldnames = ['Image', 'Student Answers', 'Answer Key', 'Score', 'Wrong Answers', 'Processing Time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write header
            writer.writeheader()

            # Write data
            for image, data_entry in self.grading_data.items():
                writer.writerow({
                    'Image': image,
                    'Student Answers': ','.join(data_entry['Student Answers']),
                    'Answer Key': ','.join(data_entry['Answer Key']),
                    'Score': data_entry['Score'],
                    'Wrong Answers': data_entry['Wrong Answers'],
                    'Processing Time': data_entry['Processing Time']
                })

        print(f'Data saved to {csv_filename}')
        


if __name__ == "__main__":
    app = QApplication(sys.argv)

    stacked_widget = QStackedWidget()

    start_widget = StartWidget(stacked_widget)
    stacked_widget.addWidget(start_widget)

    stacked_widget.show()

    sys.exit(app.exec_())
