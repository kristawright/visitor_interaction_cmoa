import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
#QApplication, QMainWindow, QFileDialog, QDialogButtonBox, QVBoxLayout, QLabel, QDialog, QLineEdit
from PyQt5.QtGui import *
import pandas as pd

class Report_Generator(QMainWindow):

## creates the main application window
    def __init__(self):
        super(Report_Generator, self).__init__()
        self.setWindowTitle("Visitor Interaction Report Generator")
        self.setGeometry(1000,300,500,600)
        self.initUI()

## formats the main application window
    def initUI(self):
        self.lbl_upload = QtWidgets.QLabel(self)
        self.lbl_upload.move(50,80)
        self.lbl_upload.resize(300,32)

        self.btn_upload = QtWidgets.QPushButton(self)
        self.btn_upload.setText("Upload File")
        self.btn_upload.move(50,30)
        self.btn_upload.resize(100,32)

        self.btn_upload.clicked.connect(self.clicker)

        self.lbl_options = QtWidgets.QLabel(self)
        self.lbl_options.setText('Advanced Options')
        self.lbl_options.move(50, 130)
        self.lbl_options.resize(200,32)
        self.lbl_options.setStyleSheet("font-weight: bold")

        self.lbl_date = QtWidgets.QLabel(self)
        self.lbl_date.setText("Month & Year")
        self.lbl_date.move(50,180)

        self.lbl_month = QtWidgets.QLineEdit(self)
        self.lbl_month.move(150,180)
        self.lbl_month.resize(80,32)

        self.lbl_year = QtWidgets.QLineEdit(self)
        self.lbl_year.move(265,180)
        self.lbl_year.resize(80,32)

        self.lbl_location = QtWidgets.QLabel(self)
        self.lbl_location.setText("Gallery")
        self.lbl_location.move(50,230)

        self.lbl_location = QtWidgets.QLineEdit(self)
        self.lbl_location.move(150,230)
        self.lbl_location.resize(200,32)

        self.lbl_artwork = QtWidgets.QLabel(self)
        self.lbl_artwork.setText("Artwork")
        self.lbl_artwork.move(50,280)

        self.lbl_artwork = QtWidgets.QLineEdit(self)
        self.lbl_artwork.move(150,280)
        self.lbl_artwork.resize(200,32)

        self.lbl_level = QtWidgets.QLabel(self)
        self.lbl_level.setText("Level")
        self.lbl_level.move(50,330)

        self.lbl_level = QtWidgets.QLineEdit(self)
        self.lbl_level.move(150,330)
        self.lbl_level.resize(200,32)

        self.lbl_query = QtWidgets.QLabel(self)
        self.lbl_query.setText("Query")
        self.lbl_query.move(50,380)

        self.lbl_query = QtWidgets.QLineEdit(self)
        self.lbl_query.move(150,380)
        self.lbl_query.resize(200,32)

        self.btn_generate = QtWidgets.QPushButton(self)
        self.btn_generate.setText("Generate Report")
        self.btn_generate.clicked.connect(self.clicked)
        self.btn_generate.move(150,430)
        self.btn_generate.resize(150,32)

        self.lbl_footer = QtWidgets.QLabel(self)
        self.lbl_footer.setText('Visitor Interaction Report Generator v1.0.0\n©2024 Krista Wright for use by Carnegie Museum of Art')
        self.lbl_footer.move(50, 530)
        self.lbl_footer.resize(400,32)
        self.lbl_footer.setStyleSheet("font-size: 10pt")
        


## creates general dialog box for notifications
    def popUp(self, message):
        self.dlg = QDialog(self)
        self.dlg.setWindowTitle('Notification')
        self.dlg.setGeometry(750,400,400,400)
        self.dlg.resize(500,150)
        self.lbl_dlg = QtWidgets.QLabel(self.dlg)
        self.lbl_dlg.setText(message)
        self.lbl_dlg.move(50,50)
        self.dlg.exec()
    
## function to display filename when uploaded
    def clicker(self):
        fname, _filter = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);; CSV Files (*.csv)")
        if fname:
            self.lbl_upload.setText(str(fname))
    
## function to upload input from textboxes
    def clicked(self):
        params = {
        }
        params['query'] = self.lbl_query.text().lower()
        params['level'] = self.lbl_level.text().lower()
        params['artwork'] = self.lbl_artwork.text().lower()
        params['location'] = self.lbl_location.text().lower()
        params['year'] = self.lbl_year.text()
        params['month'] = self.lbl_month.text()
        
        filename = self.lbl_upload.text()
        self.lbl_month.setText("")
        self.lbl_year.setText("")
        self.lbl_location.setText("")
        self.lbl_artwork.setText("")
        self.lbl_level.setText("")
        self.lbl_query.setText("")
        self.lbl_upload.setText("")
        print(filename)

## checks to make sure year is input
        try:
            int(params['year'])
        except:
            message = "Error. Please input year (yyyy)."
            self.popUp(message)
        #print(month, year, location, artwork, level, query, filename)
        self.generate_report(params, filename)

## reads in CSV file and notifies if file isn't .csv format
    def generate_report(self, params, filename):
        try:
            df = pd.read_csv(filename).reset_index()
        except:
            message = "Error. Please upload CSV."
            self.popUp(message)

## cleaning
        try:
            df.columns = ['index', 'task_id', 'created_at', 'completed_at', 'last_modified', 'name', 'section', 'assignee', 'assignee_email', 'start_date', 'due_date', 'tags', 'notes', 'projects', 'parent_task', 'blocked_by', 'blocking', 'artwork', 'id_no', 'artist', 'interaction_level', 'date_of_interaction', 'date_found', 'form_submitter', 'interaction_witness', 'location', 'age_group', 'response_category', 'damaged', 'resolution_detail', 'visitor_reaction', 'corrective_measures', 'interaction_tagging', 'av', 'date', 'cmoa_location', 'type_of_issue', 'new_recurring', 'nearby_artwork', 'activity_type', 'task_progress', 'date_reported', 'priority', 'created_by', 'issue_type']
        except ValueError:
            message2 = "Error. Please upload a valid csv file."
            self.popUp(message2)
        df = df.drop('index', axis=1)
        df = df.apply(lambda x: x.str.strip().str.lower() if x.dtype == 'object' else x)
        df['location'] = df['location'].replace('scaife gallery one', 'scaife gallery 01')
        df['created_at'] = pd.to_datetime(df['created_at'])
        df['completed_at'] = pd.to_datetime(df['completed_at'])
        df['last_modified'] = pd.to_datetime(df['last_modified'])
        df['start_date'] = pd.to_datetime(df['start_date'])
        df['due_date'] = pd.to_datetime(df['due_date'])
        print("intermediate")
        print(df)

        if params['month'] == '':
            year = int(params['year'])
            new_df = df.loc[(df.created_at.dt.year == year)].reset_index()
            print('here')
        else:
            year = int(params['year'])
            month = int(params['month'])
            new_df = df.loc[(df.created_at.dt.month == month) & (df.created_at.dt.year == year)].reset_index()
       
        print("next again")
        print(new_df)
        
## generating the new dataframe
        new_df = new_df[new_df.location.str.contains(params['location'], na=False)].reset_index()
        new_df = new_df[new_df.artwork.str.contains(params['artwork'], na=False)].rename_axis('test1').reset_index()
        new_df = new_df[new_df.interaction_level.str.contains(params['level'], na=False)].rename_axis('test2').reset_index()
        new_df = new_df[new_df.notes.str.contains(params['query'], na=False)].rename_axis('test3').reset_index()
        new_df = new_df[['created_at', 'artwork', 'artist', 'location', 'interaction_level', 'task_id']].dropna()
        new_df = new_df.groupby(['artwork', 'artist', 'location', 'interaction_level'])['task_id'].size().reset_index()
        new_df = new_df.sort_values('task_id', ascending=False)

        print("final")
        print(new_df)

## takes original file path and make it a new file name
        split = filename.split("/")
        for key in params:
            if params[key] != '':
                split[-1] = f'{params[key]}_{split[-1]}'

        split[-1] = f'report_{split[-1]}'
        new_path = "/".join(split)
        

        try:
            new_df.to_csv(new_path, sep=',')
            message = "Report Successful. \nSaved in original file location:\n" + new_path
            self.popUp(message)
            print(f"tadah: {new_path}")
        except:
            message = "Report errored"
            self.popUp(message)
            print("ohno")


## creates application
def app():
    app = QApplication(sys.argv)
    win = Report_Generator()
    win.show()
    sys.exit(app.exec_())    

app()      
