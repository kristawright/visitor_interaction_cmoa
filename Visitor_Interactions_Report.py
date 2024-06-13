import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import pandas as pd

class Report_Generator(QMainWindow):

    ## creates the main application window
    def __init__(self):
        super(Report_Generator, self).__init__()
        self.setWindowTitle("Visitor Interaction Report Generator")
        self.setGeometry(1000, 300, 500, 600)
        self.initUI()

    ## formats the main application window
    def initUI(self):
        self.lbl_upload = QLabel(self)
        self.lbl_upload.move(50, 80)
        self.lbl_upload.resize(300, 32)

        self.btn_upload = QPushButton(self)
        self.btn_upload.setText("Upload File")
        self.btn_upload.move(50, 30)
        self.btn_upload.resize(100, 32)
        self.btn_upload.clicked.connect(self.clicker)

        self.lbl_options = QLabel(self)
        self.lbl_options.setText("Advanced Options")
        self.lbl_options.move(50, 130)
        self.lbl_options.resize(200, 32)
        self.lbl_options.setStyleSheet("font-weight: bold")

        self.lbl_start_date = QLabel(self)
        self.lbl_start_date.setText("Start Date\n(yyyy-mm-dd)")
        self.lbl_start_date.move(50, 180)

        self.start_date_input = QLineEdit(self)
        self.start_date_input.move(200, 180)
        self.start_date_input.resize(100, 32)

        self.lbl_end_date = QLabel(self)
        self.lbl_end_date.setText("End Date\n(yyyy-mm-dd)")
        self.lbl_end_date.move(50, 230)

        self.end_date_input = QLineEdit(self)
        self.end_date_input.move(200, 230)
        self.end_date_input.resize(100, 32)

        self.lbl_location = QLabel(self)
        self.lbl_location.setText("Gallery")
        self.lbl_location.move(50, 280)

        self.lbl_location_input = QLineEdit(self)
        self.lbl_location_input.move(150, 280)
        self.lbl_location_input.resize(200, 32)

        self.lbl_artwork = QLabel(self)
        self.lbl_artwork.setText("Artwork")
        self.lbl_artwork.move(50, 330)

        self.lbl_artwork_input = QLineEdit(self)
        self.lbl_artwork_input.move(150, 330)
        self.lbl_artwork_input.resize(200, 32)

        self.lbl_level = QLabel(self)
        self.lbl_level.setText("Level")
        self.lbl_level.move(50, 380)

        self.lbl_level_input = QLineEdit(self)
        self.lbl_level_input.move(150, 380)
        self.lbl_level_input.resize(200, 32)

        self.lbl_query = QLabel(self)
        self.lbl_query.setText("Query")
        self.lbl_query.move(50, 430)

        self.lbl_query_input = QLineEdit(self)
        self.lbl_query_input.move(150, 430)
        self.lbl_query_input.resize(200, 32)

        self.btn_generate = QPushButton(self)
        self.btn_generate.setText("Generate Report")
        self.btn_generate.clicked.connect(self.clicked)
        self.btn_generate.move(150, 480)
        self.btn_generate.resize(150, 32)

        self.lbl_footer = QLabel(self)
        self.lbl_footer.setText("Visitor Interaction Report Generator v1.0.0\n©2024 Krista Wright for use by Carnegie Museum of Art")
        self.lbl_footer.move(50, 530)
        self.lbl_footer.resize(400, 32)
        self.lbl_footer.setStyleSheet("font-size: 10pt")
    
    ## creates general dialog box for notifications
    def popUp(self, message):
        QMessageBox.information(self, "Notification", message, QMessageBox.Ok)

    ## function to display filename when uploaded
    def clicker(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Open File", "", "CSV Files (*.csv);; All Files (*)")
        if fname:
            self.lbl_upload.setText(fname)
    
    ## function to upload input from textboxes
    def clicked(self):
        if not self.lbl_upload.text():
            self.popUp("Please upload a file.")
            return

        params = {
            'query': self.lbl_query_input.text().lower(),
            'level': self.lbl_level_input.text().lower(),
            'artwork': self.lbl_artwork_input.text().lower(),
            'location': self.lbl_location_input.text().lower(),
            'start_date': self.start_date_input.text(),
            'end_date': self.end_date_input.text()
        }

        filename = self.lbl_upload.text()

        # checks to make sure dates are input and valid
        try:
            start_date = pd.to_datetime(params['start_date'], format='%Y-%m-%d')
            end_date = pd.to_datetime(params['end_date'], format='%Y-%m-%d')
            if start_date > end_date:
                self.popUp("Error. Start date must be before end date.")
                return
        except ValueError:
            self.popUp("Error. Please input valid dates in the format yyyy-mm-dd.")
            return

        self.generate_report(params, filename)

    ## reads in CSV file and notifies if file isn't .csv format
    def generate_report(self, params, filename):
        try:
            df = pd.read_csv(filename).reset_index()
        except Exception as e:
            self.popUp(f"Error loading file: {str(e)}")
            return

        ## cleaning
        try:
            df.columns = ['index', 'task_id', 'created_at', 'completed_at', 'last_modified', 'name', 'section', 'assignee', 'assignee_email', 'start_date', 'due_date', 'tags', 'notes', 'projects', 'parent_task', 'blocked_by', 'blocking', 'artwork', 'id_no', 'artist', 'interaction_level', 'date_of_interaction', 'date_found', 'form_submitter', 'interaction_witness', 'location', 'age_group', 'response_category', 'damaged', 'resolution_detail', 'visitor_reaction', 'corrective_measures', 'interaction_tagging', 'av', 'date', 'cmoa_location', 'type_of_issue', 'new_recurring', 'nearby_artwork', 'activity_type', 'task_progress', 'date_reported', 'priority', 'created_by', 'issue_type']
        except ValueError:
            self.popUp("Error. Please upload a valid CSV file.")
            return

        df = df.drop('index', axis=1)
        df = df.apply(lambda x: x.str.strip().str.lower() if x.dtype == 'object' else x)
        df['location'] = df['location'].replace('scaife gallery one', 'scaife gallery 01')
        df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
        df['completed_at'] = pd.to_datetime(df['completed_at'], errors='coerce')
        df['last_modified'] = pd.to_datetime(df['last_modified'], errors='coerce')
        df['start_date'] = pd.to_datetime(df['start_date'], errors='coerce')
        df['due_date'] = pd.to_datetime(df['due_date'], errors='coerce')

        ## filter by date range
        df = df[(df['created_at'] >= params['start_date']) & (df['created_at'] <= params['end_date'])]

        filters = {
            'location': params['location'],
            'artwork': params['artwork'],
            'interaction_level': params['level'],
            'notes': params['query']
        }

        for key, value in filters.items():
            if value:
                df = df[df[key].str.contains(value, na=False)]
        
        ## generating the new dataframe
        report_df = df[['created_at', 'artwork', 'artist', 'location', 'interaction_level', 'id_no', 'task_id']].dropna()
        report_df = report_df.groupby(['artwork', 'artist', 'location', 'interaction_level'])['task_id'].size().reset_index()
        report_df = report_df.sort_values('task_id', ascending=False)

        ## takes original file path and make it a new file name
        split = filename.split("/")
        for key in params:
            if params[key] != '':
                split[-1] = f'{params[key]}_{split[-1]}'

        split[-1] = f'report_{split[-1]}'
        new_path = "/".join(split)

        try:
            report_df.to_csv(new_path, index=False)
            self.popUp(f"Report Successful.\nSaved in original file location:\n{new_path}")
        except Exception as e:
            self.popUp(f"Error saving report: {str(e)}")

## creates application
def app():
    app = QApplication(sys.argv)
    win = Report_Generator()
    win.show()
    sys.exit(app.exec_())  

app()
