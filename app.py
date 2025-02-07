from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector as mq
from mysql.connector import Error
from markupsafe import Markup
from datetime import datetime
import embeddings
import recognition
import threading
import os
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

ATTENDANCE_FOLDER = 'attendancesheets'

def dbconnection():
    con = mq.connect(host='localhost', database='stattendance',user='root',password='root')
    return con

@app.route('/')
def home():
    return render_template('index.html', title='home')

@app.route('/loginpage')
def loginpage():
    return render_template('login.html',title='login')

@app.route('/enatpage')
def enatpage():
    return render_template('enatt.html',title='enable attendance')

@app.route('/checkattpage')
def checkattpage():
    return render_template('checkatt.html',title='check attendance', subject = session['subject'])


@app.route('/addstudentpage')
def addstudentpage():
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("select * from staff left join subject on staff.sid=subject.id")
    res = cursor.fetchall()
    if res==[]:
        message = Markup("<h3>Please Add Staff TO Add Student</h3>")
        flash(message)
        return redirect(url_for('addstudent'))
    else:
        return render_template('addstudent.html',res=res)

@app.route('/addsubjectpage')
def addsubjectpage():
    return render_template('addsubject.html')

@app.route('/addstaffpage')
def addstaffpage():
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("select * from subject")
    res = cursor.fetchall()
    if res==[]:
        message = Markup("<h3>Please Add Subject To Add Staff</h3>")
        flash(message)
        return redirect(url_for('addsubjectpage'))
    else:
        return render_template('addstaff.html',res=res)



@app.route('/viewstudents')
def viewstudents():
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("select * from students inner join staff on students.mid=staff.id ")
    res = cursor.fetchall()
    if res==[]:
        message = Markup("<h3>Failed! Details not found</h3>")
        flash(message)
        return render_template('viewstudents.html')
    else:
        return render_template('viewstudents.html',res=res)
    
@app.route('/viewstaffpage')
def viewstaffpage():
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("select * from staff left join subject on staff.sid=subject.id")
    res = cursor.fetchall()
    if res==[]:
        message = Markup("<h3>Failed! Details not found</h3>")
        flash(message)
        return render_template('viewstaff.html')
    else:
        return render_template('viewstaff.html',res=res)
    



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        ltype = request.form['ltype']
        email = request.form['email']
        password = request.form['password']
        con = dbconnection()
        cursor = con.cursor()
        if ltype=='admin':
        
            cursor.execute("select * from admin where email='{}' and pass='{}'".format(email,password))
            res = cursor.fetchall()
            if res==[]:
                message = Markup("<h3>Failed! Invalid Email or Password</h3>")
                flash(message)
                return redirect(url_for('loginpage'))
            else:
                return redirect(url_for('addsubjectpage'))
        elif ltype=="staff":
            cursor.execute("select * from staff where email='{}' and password='{}'".format(email,password))
            res = cursor.fetchall()
            if res==[]:
                message = Markup("<h3>Failed! Invalid Email or Password</h3>")
                flash(message)
                return redirect(url_for('loginpage'))
            else:
                session['sid']=res[0][0]
                cursor.execute("select * from subject where id={}".format(int(res[0][4])))
                res2 = cursor.fetchall()
                session['subject']=res2[0][1]
                return render_template('enatt.html')
            

@app.route('/savesubject', methods=['GET', 'POST'])
def savesubject():
    if request.method == 'POST':
        name = request.form['name']
        sem = request.form['sem']
        con = dbconnection()
        cursor = con.cursor()
        cursor.execute("select * from subject where name='{}' and sem='{}'".format(name,sem))
        res = cursor.fetchall()
        if res==[]:
                cursor.execute("insert into subject(name,sem)values('{}','{}')".format(
                    name,sem))
                con.commit()
                con.close()
                message = Markup("<h3>Success! Subject Added!</h3>")
                flash(message)
                return redirect(url_for('addsubjectpage'))
        else:
            message = Markup("<h3>Failed! subject already exists!</h3>")
            flash(message)
            return redirect(url_for('addsubjectpage'))

@app.route('/savestaff', methods=['GET', 'POST'])
def savestaff():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        subject = request.form['subject']
        password = request.form['password']
        con = dbconnection()
        cursor = con.cursor()
        cursor.execute("select * from staff where email='{}' and phone='{}'".format(email,phone))
        res = cursor.fetchall()
        if res==[]:
                cursor.execute("insert into staff(name,email,phone,sid,password)values('{}','{}','{}','{}','{}')".format(
                    name,email,phone,int(subject),password))
                con.commit()
                con.close()
                message = Markup("<h3>Success! Staff Added!</h3>")
                flash(message)
                return redirect(url_for('addstaffpage'))
        else:
            message = Markup("<h3>Failed! Email id or Phone number already exists!</h3>")
            flash(message)
            return redirect(url_for('addstaffpage'))


@app.route('/savestudent', methods=['GET', 'POST'])
def savestudent():
    if request.method == 'POST':
        name = request.form['name']
        usn = request.form['usn']
        email = request.form['email']
        phone = request.form['phone']
        gender = request.form['gender']
        address = request.form['address']
        mentor = request.form['mentor']
        password = request.form['password']
        con = dbconnection()
        cursor = con.cursor()
        cursor.execute("select * from students where email='{}' and phone='{}' and usn='{}'".format(email,phone,usn))
        res = cursor.fetchall()
        if res==[]:
                embeddings.trainPerson(name,usn)
                cursor.execute("insert into students(name,usn,email,phone,gender,address,mid,password)values('{}','{}','{}','{}','{}','{}','{}','{}')".format(
                    name,usn,email,phone,gender,address,int(mentor),password))
                con.commit()
                con.close()
                message = Markup("<h3>Success! Student Added!</h3>")
                flash(message)
                return redirect(url_for('addstudentpage'))
        else:
            message = Markup("<h3>Failed! Email id or Phone number or USN already exists!</h3>")
            flash(message)
            return redirect(url_for('addstudentpage'))

       
@app.route('/enableattendance', methods=['GET', 'POST'])
def enableattendance():
    thread = threading.Thread(target=recognition.detectPerson, args=(session['subject'],))
    thread.start()
    return render_template('enatt.html')

@app.route('/getattendance', methods=['POST'])
def getattendance():
    from_date = request.form['from_date']
    to_date = request.form['to_date']
    
    # Validate date range
    try:
        from_date = datetime.strptime(from_date, '%Y-%m-%d')
        to_date = datetime.strptime(to_date, '%Y-%m-%d')
    except ValueError:
        return "Invalid date format. Please try again."

    if from_date > to_date:
        return "From Date should be earlier than To Date."
    
    # Fetch the subject from session
    subject = session.get('subject', None)
    if not subject:
        return "Subject not found in session."

    # Filter files by subject and date range
    attendance_data = []
    for filename in os.listdir(ATTENDANCE_FOLDER):
        if subject in filename:
            # Extract date from filename
            try:
                date_str = filename.split('_')[1]  # Assuming format: SUBJECT_DATE_TIME.xlsx
                file_date = datetime.strptime(date_str, '%Y-%m-%d')
            except (IndexError, ValueError):
                continue  # Skip files that don't match the naming convention
            
            # Check if the file falls within the date range
            if from_date <= file_date <= to_date:
                filepath = os.path.join(ATTENDANCE_FOLDER, filename)
                
                # Read the file and calculate attendance
                df = pd.read_excel(filepath)
                student_attendance = process_attendance(df)
                attendance_data.extend(student_attendance)
    
    return render_template('attendance.html', attendance_data=attendance_data)

def process_attendance(df):
    """
    Process attendance data from the DataFrame and calculate attendance percentage.
    """
    attendance_summary = {}
    for index, row in df.iterrows():
        name = row['Name']
        usn = row['USN']
        attendance_status = row['Attendance']
        
        # Initialize or update attendance count
        if usn not in attendance_summary:
            attendance_summary[usn] = {'Name': name, 'Present': 0, 'Total': 0}
        attendance_summary[usn]['Total'] += 1
        if attendance_status == "On Time":
            attendance_summary[usn]['Present'] += 1
    
    # Calculate percentage for each student
    attendance_data = []
    for usn, data in attendance_summary.items():
        percentage = (data['Present'] / data['Total']) * 100
        attendance_data.append({
            'Name': data['Name'],
            'USN': usn,
            'Attendance Percentage': round(percentage, 2)
        })
    
    return attendance_data

    









    

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)
