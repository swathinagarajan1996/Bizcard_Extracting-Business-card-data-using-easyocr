# Bizcard_Extracting-Business-card-data-using-easyocr
![image](https://github.com/swathinagarajan1996/Bizcard_Extracting-Business-card-data-using-easyocr/assets/127007232/334cb7c4-9f58-4c7a-b734-cd8407784107)
## Problem Statement:
Through this project I have been tasked with developing a Streamlit application that allows users to upload an image of a business card and 
extract relevant information from it using easyOCR.The extracted information should include the company name, card holder name, designation, mobile
number, email address, website URL, area, city, state, and pin code. The extracted information should then be displayed in the application's graphical 
user interface (GUI).In addition, the application should allow users to save the extracted information into a database along with the uploaded business card
image. The database should be able to store multiple entries, each with its own business card image and extracted information.
## Libraries to import:
import easyocr
import pandas as pd
from PIL import Image
import numpy as np
import cv2
import streamlit as st
import sqlite3
## Designing  the user interface:
Created a simple and intuitive user interface using Streamlit that guides users through the process of uploading the business_card image and extracting its information.
## Image processing using OCR and Streamlit:
By usinf easyOCR to extract the relevant information from the uploaded business card image.Once the information has been extracted,
display it in a clean and organized manner in the Streamlit GUI.
## Implement database integration:
Using a database management system like SQLite  to store the extracted information along with the uploaded business card image.With the help of SQL queries to create tables, insert data,
and retrieve data from the database, Update the data and allow the user todelete the data through the streamlit UI
