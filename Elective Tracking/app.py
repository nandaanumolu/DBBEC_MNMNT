from sqlite3 import Cursor
from flask import Flask, request, jsonify, render_template, redirect, session, url_for, flash
from flask_cors import CORS
import mysql.connector
import bcrypt



app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
# Database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'student'
}

CORS(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    error_occurred = False
    error_message = ""
    if request.method == 'POST':
        name = request.form['yourName']
        email = request.form['yourEmail']
        password = request.form['yourPassword']
        repeat_password = request.form['repeatPassword']

        # Check if passwords match
        if password != repeat_password:
            flash("Passwords do not match. Please try again.", "error")
            return redirect(request.url)

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Connect to MySQL server and insert data into the registration table
        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()

            # Check if the registration number or email already exists
            select_query = "SELECT * FROM register WHERE reg = %s OR email = %s"
            cursor.execute(select_query, (name, email))
            existing_user = cursor.fetchone()

            if existing_user:
                error_occurred = True  # Set error flag to True
                error_message = "Account with the provided registration number or email already exists."

            else:
                # If not already registered, proceed with insertion
                insert_query = "INSERT INTO register (reg, email, hashed_password) VALUES (%s, %s, %s)"
                cursor.execute(insert_query, (name, email, hashed_password))
                connection.commit()

                flash("Registration successful!", "success")
                return redirect(url_for('index'))  # Redirect to homepage after successful registration

            cursor.close()
            connection.close()

        except Exception as e:
            flash("An error occurred while processing your registration. Please try again later.", "error")
            return redirect(request.url)

    return render_template('register.html', error_occurred=error_occurred, error_message=error_message)

@app.route('/studentlogin', methods=['GET', 'POST'])
def studentlogin():
    if request.method == 'POST':
        username = request.form.get('yourRegd')  # Assuming the input field name is 'yourRegd'
        password = request.form.get('form3Example4c')  # Assuming the input field name is 'form3Example4c'

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        query = f"SELECT * FROM register WHERE reg = '{username}'"
        cursor.execute(query)
        student = cursor.fetchone()

        cursor.close()
        connection.close()

        if student and bcrypt.checkpw(password.encode('utf-8'), student[2].encode('utf-8')):
            # Student authenticated, redirect to student dashboard or any desired page
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('studentdashboard'))
        else:
            error_message = "Invalid registration number or password. Please try again."
            return render_template('studentlogin.html', error=error_message)

    return render_template('studentlogin.html', error='')  # Pass an empty error message initially


@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        username = request.form.get('adminUsername')
        password = request.form.get('adminPassword')

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        query = f"SELECT * FROM admin WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(query)
        admin = cursor.fetchone()

        cursor.close()
        connection.close()

        if admin:
            # Admin authenticated, redirect to admin dashboard or any desired page
            return redirect(url_for('admindashboard',login_success=True))
        else:
            error_message = "Invalid username or password. Please try again."
            return render_template('adminlogin.html', error=error_message)

    return render_template('adminlogin.html')

@app.route('/admindashboard')
def admindashboard():
    return render_template('admindashboard.html')

@app.route('/addRecord')
def addRecord():
    return render_template('addRecord.html')

@app.route('/studentdashboard')
def studentdashboard():
    return render_template('studentdashboard.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')



@app.route('/students/reg/<reg_id>', methods=['GET'])
def get_electives_by_registration_number(reg_id):
    try:
        connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="student"
    )
        cursor = connection.cursor()
        query = f"SELECT SUB_CODE, SUB_NAME, Sem,Reg_Id FROM student_details2 WHERE Reg_Id = '{reg_id}'"
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        electives = []
        for row in results:
            print(row)
            elective = {
                'SUB_CODE': row[0],
                'SUB_NAME': row[1],
                'Sem': row[2],
                'Reg_Id':row[3]
            }
            electives.append(elective)

        return jsonify({'records': electives}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/students/branch/<branch>', methods=['GET'])
def get_students_by_branch(branch):
    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Maneesha@123",
        database="student"
    )
        cursor = connection.cursor()
        query = f"SELECT Name, Reg_Id, SUB_NAME FROM student_details2 WHERE Dept = '{branch}'"
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        students = []
        for row in results:
            student = {
                'Name': row[0],
                'Reg_Id': row[1],
                'Elective': row[2]
            }
            students.append(student)

        return jsonify({'records': students}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/students/elective/<elective>', methods=['GET'])
def get_students_by_elective(elective):
    try:
        connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Maneesha@123",
        database="student"
    )
        cursor = connection.cursor()
        query = f"SELECT Name, Reg_Id FROM student_details2 WHERE SUB_NAME = '{elective}'"
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        students = []
        for row in results:
            student = {
                'Name': row[0],
                'Reg_Id': row[1]
            }
            students.append(student)

        return jsonify({'records': students}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/students/add_records', methods=['POST'])
def add_elective():
    try:
        data = request.json
        connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="student"
    )
        cursor = connection.cursor()
        insert_query = f"""
            INSERT INTO student_details2 (Reg_Id, Name, SUB_CODE, SUB_NAME, Dept, Sem, Year)
            VALUES ('{data['Reg_Id']}', '{data['Name']}', '{data['SUB_CODE']}', '{data['SUB_NAME']}',
                    '{data['Dept']}', '{data['Sem']}', '{data['Year']}')
        """
        cursor.execute(insert_query)
        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({'message': 'Elective added successfully.'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    
@app.route('/register_elective', methods=['GET', 'POST'])
def register_elective():
    if request.method == 'POST':
        reg_id = session.get('username')  # Get registration number from session
        name = request.form['name']
        dept = request.form['dept']
        sem = request.form['sem']
        year = request.form['year']
        num_subjects = int(request.form['numSubjects'])

        elective_data = []
        for i in range(num_subjects):
            sub_code = request.form[f'sub_code_{i}']
            sub_name = request.form[f'sub_name_{i}']
            elective_data.append((reg_id, name, sub_code, sub_name, dept, sem, year))

        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()

            insert_query = """
                INSERT INTO student_details2 (Reg_Id, Name, SUB_CODE, SUB_NAME, Dept, Sem, Year)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.executemany(insert_query, elective_data)
            connection.commit()
            cursor.close()
            connection.close()

            flash("Electives registered successfully!", "success")
            return redirect(url_for('studentdashboard'))

        except Exception as e:
            flash(f"An error occurred: {str(e)}", "error")
            return redirect(url_for('studentdashboard'))

    return render_template('studentdashboard.html')

@app.route('/students/update_elective', methods=['POST'])
def update_elective():
    try:
        data = request.json

        # Connect to MySQL server
        connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="student"
    )
        cursor = connection.cursor()
        update_query = f"""
            UPDATE student_details2
            SET SUB_NAME = '{data['new_SUB_NAME']}', SUB_CODE = '{data['new_SUB_CODE']}'
            WHERE Reg_Id = '{data['Reg_Id']}' AND Sem = '{data['Sem']}'
            AND SUB_NAME = '{data['old_SUB_NAME']}' AND SUB_CODE = '{data['old_SUB_CODE']}'
        """
        cursor.execute(update_query)
        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({'message': 'Elective updated successfully.'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
