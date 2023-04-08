
import Constants
import sys 
import openai
from PyQt5.QtCore import Qt 
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QTextEdit,
    QLineEdit
)

openai.api_key = Constants.API_KEY


class MainWindow(QWidget):
    def __init__(self):
      MainWindow(super).__init__()
      self.init_ui()
   
    def init_ui(self):
      #Create a widgets
      self.logo_lebel = QLabel()
      self.logo_pixmap = QPixmap('Large Hadran Collider.png').scaled(150,150, Qt.KeepAspectRatio. Qt.SmoothTransformation)
      self.logo_lebel.setPixmap(self.logo_pixmap)

      self.input_label = QLabel('Ask a question')
      self.input_field = QLineEdit()
      self.input_field.setPlaceholderText('Ask here...')
      self.answer_label = QLabel("Answer:")
      self.answer_field = QTextEdit()
      self.answer_field.setReadOnly(True)
      self.submit_button = QPushButton("Submit")
      self.submit_button.setStyleSheet(

       """
       QPushButton {
        background-color :#4CAF50;
        border: none;
        color : white;
        padding: 15px 32px;
        font-size : 18px;
        font-weight :bold;
        border-radius : 10px;
       }
       QPushButton : hover {
        background-color : #3e8e41;
       }
     """
      )

      self.popular_questions_group = QGroupBox('Popular Question')
      self.popular_questions_layout = QHBoxLayout()
      self.popular_questions = ["What is Machine Learning?" , "How do I become a Machine Learing Engineer?" , "What are some popular machine learning algorithm?"]
      self.question_buttons = [] 

      # Creating a layout for logic we used in the api 

      layout = QVBoxLayout()
      layout.setContentsMargins(20,20,20,20)
      layout.setSpacing(20)
      layout.setAlignment(Qt.AlignCenter)

      #Add Logo 
      layout.addWidget(self.logo_lebel, alignment=Qt.AlignCenter)

     # Add Input Field and Submit button 
      input_layout = QHBoxLayout()
      input_layout.addWidget(self.input_label)
      input_layout.addWidget(self.input_field)
      input_layout.addWidget(self.submit_button)
      layout.addLayout(input_layout)
 
      #Add Answer Field 
      layout.addWidget(self.answer_label)
      layout.addWidget(self.answer_field)

     #add the popular question button  
      for question in self.popular_questions:
        button = QPushButton(question)
        button.setStyleSheet("""
              QPushButton {
                background-color: #FFFFF;
                border: 2px solid #00AEFF;
                color: #00AEFF;
                padding : 10px 20px;
                font-size: 18px;
                font-weight: bold;
                border-radius: 5px;
              }
              QPushButton : hover{
                background-color: #00AEFF;
                color: #FFFFFF;
              }
        
        """)

       # Things happens while hover on the button 
        button.clicked.connect(lambda _, q=question: self.input_field.setText(question))
        self.popular_question_layout.addWidet(button)
        self.question_buttons.append(button)
        self.popular_question_group.setLayout(self.popular_question_layout)
        layout.addWidget(self.popular_question_group)

        
        #set the layout 
        self.setLayout(layout)

        #set the window properties 
        self.setWindowTitle("Machine Learing Carrer Advisor Bot")
        self.setGeometry(200,200,600,600)
        
        #connect the submit button to the function which queries openAI's API 
        self.submit_button.clicked.connect(self.get_answer)

        def get_answer(self):
            question = self.input_field.text()
            
            completion = openai.ChatCompletion.create(
                model = "gpt-3.5-turbo",
                messages = [{"role":"user", "content": "You are a machine learning engineering expert. Answer the following question in a concise way or with bullet points."}, 
                              {"role": "user", "content": f'{question}'}],
                max_tokens = 1024,
                n = 1,
                stop = None,
                temperature = 0.7             
            )

            #Extracting the write answer from the api 
            answer = completion.choice[0].message.content 

            self.answer_field.setText(answer)

if __name__== '_main_':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())