import face_recognition
import cv2
import numpy as np
import pickle
from datetime import datetime
import mysql.connector as mq
import pandas as pd
import mailing
import os
import time

def dbconnection():
    return mq.connect(host='localhost', database='stattendance', user='root', password='root')


def mailsend_alert(student_name, usn, subject_name, timestamp, staff_email):
    email_body = f"""
    Dear Staff,

    The following student has marked attendance late:
    Name: {student_name}
    USN: {usn}
    Subject: {stsubject}
    Time: {timestamp}
    Attendance: Late

    Regards,
    Attendance System
    """
    print("Email sent for late attendance.")
    # Uncomment to actually send the email
    try:
        mailing.mailsend(to_email=staff_email, subject=f"Late Attendance: {student_name}", body=email_body)
    except:
        print("Could Not Send Mail")


def process_faces(known_face_encodings, known_face_usns, duration=600, trigger_time=None):
    video_capture = cv2.VideoCapture(0)
    detected_usns = {}

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to capture video frame.")
            break

        # Resize frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Detect faces and their encodings
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_location, face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            if True in matches:
                best_match_index = matches.index(True)
                name = known_face_usns[best_match_index]

                # If the user is detected for the first time, record the detection time
                if name not in detected_usns:
                    detected_usns[name] = time.time()
                    process_single_attendance(name, detected_usns[name], trigger_time)  # Save attendance immediately

            # Draw a box around the face
            top, right, bottom, left = [v * 4 for v in face_location]
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

            # Display the name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.8, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow("Video", frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture and close the window
    video_capture.release()
    cv2.destroyAllWindows()


def process_single_attendance(usn, recognition_time, trigger_time):
    con = dbconnection()
    cursor = con.cursor()

    cursor.execute("""
        SELECT 
            students.name AS student_name, 
            students.usn AS student_usn, 
            subject.name AS subject_name, 
            subject.sem AS semester,
            staff.email AS staff_email
        FROM 
            students
        INNER JOIN 
            staff ON students.mid = staff.id
        INNER JOIN 
            subject ON staff.sid = subject.id
        WHERE 
            students.usn = %s
    """, (usn,))

    record = cursor.fetchone()

    if record:
        student_name = record[0]
        student_usn = record[1]
        subject_name = record[2]
        semester = record[3]
        staff_email = record[4]

        trigger_time_ts = trigger_time.timestamp()
        attendance_status = "On Time" if recognition_time - trigger_time_ts <= 10 else "Late"
        timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        trigger_time_str = trigger_time.strftime("%Y-%m-%d_%H-%M-%S")  # For filename
        excel_filename = f"{stsubject}_{trigger_time_str}.xlsx"

        try:
            df = pd.read_excel(excel_filename)
        except FileNotFoundError:
            df = pd.DataFrame(columns=["Name", "USN", "Subject", "Semester", "Date & Time", "Attendance"])

        if not ((df["USN"] == student_usn) & (df["Subject"] == stsubject)).any():
            new_record = {
                "Name": student_name,
                "USN": student_usn,
                "Subject": stsubject,
                "Semester": semester,
                "Date & Time": timestamp_str,
                "Attendance": attendance_status
            }
            df = df.append(new_record, ignore_index=True)
            df.to_excel("attendancesheets/"+excel_filename, index=False)
            print("Attendance saved:", new_record)

            if attendance_status == "Late":
                print("Sending late alert")
                # Uncomment the next line to enable email alerts
                mailsend_alert(student_name, student_usn, subject_name, timestamp_str, staff_email)

    cursor.close()
    con.close()



def detectPerson(subject):
    global stsubject
    stsubject=subject
    with open("ref_name.pkl", "rb") as f:
        ref_dict = pickle.load(f)

    with open("ref_embed.pkl", "rb") as f:
        embed_dict = pickle.load(f)

    known_face_encodings = []
    known_face_usns = []

    for ref_id, embed_list in embed_dict.items():
        for embed in embed_list:
            known_face_encodings.append(embed)
            known_face_usns.append(ref_id)

    trigger_time = datetime.now()  # Capture the camera trigger time
    process_faces(known_face_encodings, known_face_usns, duration=15, trigger_time=trigger_time)




if __name__ == "__main__":
    pass
    #detectPerson("DATA SCIENCE")
