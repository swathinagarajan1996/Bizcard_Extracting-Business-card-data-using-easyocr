import easyocr
import pandas as pd
from PIL import Image
import numpy as np
import cv2
import streamlit as st
import sqlite3


mydb=sqlite3.connect("Bizcard.db")
mycursor = mydb.cursor()
mycursor.execute("""Create Table IF NOT EXISTS OCR_Card(id INT PRIMARY KEY, 
                    name VARCHAR(255), job_title VARCHAR(255),address VARCHAR(255),
                     postcode VARCHAR(255),phone VARCHAR(255), 
                     email VARCHAR(255), website VARCHAR(255), 
                     company_name VARCHAR(225))""")
reader = easyocr.Reader(['en'])
st.set_page_config(page_title="BIZCARD",page_icon=":card_index:")
st.markdown(f""" <style>.stApp{{ 
            background-image: url("https://cdn.wallpapersafari.com/53/63/pnd4MG.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,unsafe_allow_html=True)
st.sidebar.title(":purple[Bizcard:card_file_box:]")
st.title(":blue[Extracting Business card data using easyocr]")
menu=['Home','Add','View','Update','Delete']
choice=st.sidebar.selectbox("Select an option",menu)
if choice=="Home":
    col1,col2=st.columns(2)
    with col1:
        st.markdown("## :green[**Technologies Used:**] Python,easy OCR, Streamlit, SQL, Pandas")
        st.markdown("## :green[**Overview :**] In this streamlit web app you can upload an image of a business card and extract relevant information from it using easyOCR.You can view, modify or delete the extracted data in this app. This app would also allow users to save the extracted information into a database along with the uploaded business card image. The database would be able to store multiple entries, each with its own business card image and extracted information.")
    with col2:
        img=Image.open("C:\swathi\git\BIZIMG.png")
        st.image(img)
if choice=="Add":
    uploaded_file = st.file_uploader("Upload business card image", type=['jpg', 'jpeg', 'png'])
    if uploaded_file is not None:
        image=cv2.imdecode(np.fromstring(uploaded_file.read(),np.uint8),1)
        st.image(image,caption="Upload business card image",use_column_width=True)
        if st.button("Extract Information"):
            bounds=reader.readtext(image,detail=0)
            #st.write(bounds)
            text="\n".join(bounds)
            query="INSERT INTO OCR_Card(name,job_title,address,postcode,phone,email,website,company_name) VALUES (?,?,?,?,?,?,?,?)"
            val=(bounds[0],bounds[1],bounds[2],bounds[3],bounds[4],bounds[5],bounds[6],bounds[7])
            mycursor.execute(query,val)
            mydb.commit()
            st.success("Information added to database succesfully.")
elif choice == "View":
    mycursor.execute("SELECT * FROM OCR_Card")
    result=mycursor.fetchall()
    df=pd.DataFrame(result,columns=['id','name','job_title','address','postcode','phone','email','website','company_name'])
    st.write(df)
elif choice == "Update":
    mycursor.execute("SELECT name FROM OCR_Card")
    result = mycursor.fetchall()
    business_cards = {}
    for row in result:
        business_cards[row[0]] = row[0]
    selected_card_name = st.selectbox("Select a business card to update", list(business_cards.keys()),
                                          key="card_selection")
    selected_card_id = business_cards[selected_card_name]

    # Fetch the existing details of the selected card based on the ID
    mycursor.execute("SELECT * FROM OCR_Card WHERE name = ?", (selected_card_id,))
    card_details = mycursor.fetchone()

    # Display the current details of the selected card
    st.write(f"**Name:** {card_details[1]}")
    st.write(f"**Job_title:** {card_details[2]}")
    st.write(f"**Address:** {card_details[3]}")
    st.write(f"**Postcode:** {card_details[4]}")
    st.write(f"**Phone:** {card_details[5]}")
    st.write(f"**E-mail:** {card_details[6]}")
    st.write(f"**Website:** {card_details[7]}")
    st.write(f"**Company Name:** {card_details[8]}")

    # Allow the user to update the details
    name = st.text_input("Name", value=card_details[1])
    job_title= st.text_input("Job_Title", value=card_details[2])
    address= st.text_input("Address", value=card_details[3])
    postcode = st.text_input("Postcode", value=card_details[4])
    phone = st.text_input("Phone", value=card_details[5])
    email = st.text_input("E-mail", value=card_details[6])
    website = st.text_input("Website",  value=card_details[7])
    company_name = st.text_input("Company Name", value=card_details[8])
        # Button to update the card
    if st.button("Update Card"):
        # Perform the update in the database using the new details
        mycursor.execute( "UPDATE OCR_Card set name=?,job_title=?,address=?,postcode=?,phone=?,email=?,website=?,company_name=? WHERE name=?",
                          (name, job_title, address, postcode, phone, email, website, company_name, selected_card_id))
        mydb.commit()
        st.success("Business card updated successfully!")

elif choice == "Delete":
    mycursor.execute("SELECT name FROM OCR_Card")
    result=mycursor.fetchall()
    business_cards = {}
    for row in result:
        business_cards[row[0]] = row[0]
    selected_card_name = st.selectbox("Select a business card to update", list(business_cards.keys()),
                                          key="card_selection")
    selected_card_id = business_cards[selected_card_name]
    mycursor.execute("Select * from OCR_Card WHERE name=?",(selected_card_id,))
    card_details=mycursor.fetchone()

    st.write(f"**Name:** {card_details[1]}")
    st.write(f"**Job_title:** {card_details[2]}")
    st.write(f"**Address:** {card_details[3]}")
    st.write(f"**Postcode:** {card_details[4]}")
    st.write(f"**Phone:** {card_details[5]}")
    st.write(f"**E-mail:** {card_details[6]}")
    st.write(f"**Website:** {card_details[7]}")
    st.write(f"**Company Name:** {card_details[8]}")
    if st.button("Delete Card"):
        mycursor.execute(f"DELETE FROM OCR_Card WHERE name='{selected_card_id}'")
        mydb.commit()
        st.success("Business card deleted successfully!")
