from flask import Flask, render_template, request

app = Flask(__name__)

doctors = []
patients = []


def load_doctors():
    # Load the doctor details from the doctor.txt file
    with open('doctor.txt', 'r') as file:
        lines = file.readlines()

    doctors_list = []

    for line in lines:
        details = line.strip().split('|')
        name = details[0].split(': ')[1].strip()
        specialization = details[1].split(': ')[1].strip()
        email = details[2].split(': ')[1].strip()
        password = details[3].split(': ')[1].strip()
        hospital = details[4].split(': ')[1].strip()

        doctor = {
            'name': name,
            'specialization': specialization,
            'email': email,
            'password': password,
            'hospital': hospital
        }

        doctors_list.append(doctor)
    return doctors_list


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        hospital_choice = request.form.get('hospital_choice')
        if hospital_choice == '0':
            return 'Exiting the program...'
        elif hospital_choice in ['1', '2', '3']:
            if hospital_choice == '1':
                hospital_name = 'Apollo Hospital'
            elif hospital_choice == '2':
                hospital_name = 'LifeCare Hospital'
            else:
                hospital_name = 'Manipal Hospital'
            return render_template('menu.html', hospital_name=hospital_name)
    return render_template('index.html')


@app.route('/menu/<hospital_name>', methods=['GET', 'POST'])
def menu(hospital_name):
    if request.method == 'POST':
        choice = request.form.get('choice')
        if choice == '1':
            return render_template('doctor.html', hospital_name=hospital_name)
        elif choice == '2':
            return render_template('patient.html', hospital_name=hospital_name)
        elif choice == '3':
            return render_template('index.html')
    return render_template('menu.html', hospital_name=hospital_name)


@app.route('/doctor_menu/<hospital_name>', methods=['GET', 'POST'])
def doctor_menu(hospital_name):
    if request.method == 'POST':
        choice = request.form.get('choice')
        if choice == '1':
            return render_template('doctor_signup.html', hospital_name=hospital_name)
        elif choice == '2':
            return render_template('doctor_login.html', hospital_name=hospital_name)
        elif choice == '3':
            return render_template('index.html')
    doctors = load_doctors()
    return render_template('doctor_menu.html', hospital_name=hospital_name, doctors=doctors)


@app.route('/doctor_signup/<hospital_name>', methods=['POST'])
def doctor_signup(hospital_name):
    if request.method == 'POST':
        name = request.form.get('name')
        specialization = request.form.get('specialization')
        email = request.form.get('email')
        password = request.form.get('password')

        # Create a new Doctor object
        doctor = {
            'name': name,
            'specialization': specialization,
            'email': email,
            'password': password
        }

        # Append the doctor to the 'doctors' list
        doctors.append(doctor)

        # Save the doctor details to the doctor.txt file
        with open('doctor.txt', 'a') as file:
            file.seek(0,2)
            file.write(f"Name: {name}|Specialization: {specialization}|Email: {email}|Password: {password}|Hospital: {hospital_name}\n")

        return 'Doctor sign up successful!'

    return render_template('doctor.html', hospital_name=hospital_name)


@app.route('/doctor_login/<hospital_name>', methods=['POST'])
def doctor_login(hospital_name):
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Read data from the "doctor.txt" file
        with open('doctor.txt', 'r') as file:
            data = file.read()

        # Extract email and password from the file data
        doctors = data.split('\n')
        doctor_credentials = {}
        for doctor in doctors:
            doctor_info = doctor.split('|')
            for info in doctor_info:
                print(f'{info}')
                try:
                    key, value = info.split(': ')
                except ValueError:
                    pass
                doctor_credentials[key] = value

            if doctor_credentials['Hospital']==hospital_name and doctor_credentials['Email'] == email and doctor_credentials['Password'] == password:
                patients_list = load_patients()
                filtered_patients_list = [patient for patient in patients_list if patient['doctor_name'] == doctor_credentials['Name']]
                return render_template('doctor_dashboard.html', hospital_name=hospital_name, doctor=doctor_credentials,
                                       patients=filtered_patients_list)

        return 'Invalid doctor credentials'

    return render_template('doctor.html', hospital_name=hospital_name)


def load_patients():
    # Load the patient details from the patient.txt file
    with open('patient.txt', 'r') as file:
        lines = file.readlines()

    patients_list = []

    for line in lines:
        details = line.strip().split('|')
        name = details[0].split(': ')[1].strip()
        age = details[1].split(': ')[1].strip()
        dob = details[2].split(': ')[1].strip()
        doctor_name = details[3].split(': ')[1].strip()
        appointment_time = details[4].split(': ')[1].strip()

        patient = {
            'name': name,
            'age': age,
            'dob': dob,
            'doctor_name': doctor_name,
            'appointment_time': appointment_time
        }

        patients_list.append(patient)

    return patients_list


@app.route('/patient_menu/<hospital_name>', methods=['GET', 'POST'])
def patient_menu(hospital_name):
    if request.method == 'POST':
        choice = request.form.get('choice')
        if choice == '1':
            doctors = load_doctors()
            return render_template('patient_signup.html', hospital_name=hospital_name, doctors=doctors)
        elif choice == '2':
            return render_template('patient_login.html', hospital_name=hospital_name)
        elif choice == '3':
            return render_template('index.html')
    return render_template('patient_menu.html', hospital_name=hospital_name)


@app.route('/patient_signup/<hospital_name>', methods=['POST'])
def patient_signup(hospital_name):
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        dob = request.form.get('dob')
        doctor_name = request.form.get('doctor_name')
        appointment_time = request.form.get('appointment_time')

        # Create a new Patient object
        patient = {
            'name': name,
            'age': age,
            'dob': dob,
            'doctor_name': doctor_name,
            'appointment_time': appointment_time
        }

        # Append the patient to the 'patients' list
        patients.append(patient)

        # Save the patient details to the patient.txt file
        with open('patient.txt', 'a') as file:
            file.seek(0,2)
            file.write(f"Name: {name}|Age: {age}|dob: {dob}|Doctor: {doctor_name}|"
                       f"Appointment Time: {appointment_time}|Hospital: {hospital_name}\n")

        return 'Patient sign up successful!'

    return render_template('patient.html', hospital_name=hospital_name)


@app.route('/patient_login/<hospital_name>', methods=['POST'])
def patient_login(hospital_name):
    if request.method == 'POST':
        name = request.form.get('name')
        dob = request.form.get('dob')

        # Read data from the "patient.txt" file
        with open('patient.txt', 'r') as file:
            data = file.read()

        # Extract name and dob from the file data
        patients = data.split('\n')
        patient_credentials = {}
        for patient in patients:
            patient_info = patient.split('|')
            for info in patient_info:
                key, value = info.split(': ')
                patient_credentials[key] = value

            if patient_credentials['Name'] == name and patient_credentials['dob'] == dob:
                doctors_list = load_doctors()
                filtered_doctors_list = [doctor for doctor in doctors_list if doctor['name'] == patient_credentials['Doctor']]
                return render_template('patient_dashboard.html', patient=patient_credentials, doctors=filtered_doctors_list)

        return 'Invalid patient credentials'

    return render_template('patient.html', hospital_name=hospital_name)


if __name__ == '__main__':
    app.run()
