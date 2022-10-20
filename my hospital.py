import hashlib
import csv

#User Registration and User Login

def register():

    print("\n-------------------Sign Up--------------------\n")

    #username should not exist in the system
    username = input("Enter a UserName: ").strip()
    if isRegistered(username):
        print("!!--User already exists!! Please select a different UserName--!!")
        isContinue = input("Press 'Y' to continue.. Press any other key to exit..")
        if (isContinue == 'Y' or isContinue == 'y'):
            register()
        else:
            print("!!--Exiting..GoodBye--!!")
        
    else:
        
        userType = input("Select a user type\n1:PATIENT\n2:STAFF\n\n(1/2)?:").strip()
        if(userType == "1" or userType == "2"):
            if(userType == "1"):
                userType = "Patient"
                priviledgeLevel = 4

                #personal details are collected if user is a patient
                name = input("Enter the name: ").strip()
                while (True):
                    gender = input("Enter the gender(F/M): ").strip()
                    if (gender in ["F","f"]):
                        gender = "Female"
                        break
                    elif(gender in ["M","m"]):
                        gender = "Male"
                        break
                    else:
                        print("!!--Please select a valid gender--!!\n")
                while(True):
                    try:
                        age = int(input("Enter the age: ").strip())
                        if age >0:
                            break
                        else:
                            print("!!--Age should be a positive integer--!!")
                    except:
                        print("!!--Please enter a valid age--!!")
            elif(userType == "2"):
                staffType = input("Select staff type\n1:DOCTOR\n2:NURSE\n3:LAB ASSISTANT\n\n(1/2/3)?:").strip()
                if (staffType == "1"):
                    priviledgeLevel = 1
                    userType = "Doctor"
                elif (staffType == "2"):
                    priviledgeLevel = 2
                    userType = "Nurse"
                elif (staffType == "3"):
                    priviledgeLevel = 3
                    userType = "LabAssistant"
                else:
                    print("!!--INVALID ENTRY--!!")
                    return
                
            password = input("Enter a password: ")
            hashedPassword = hashlib.md5(password.encode('utf8')).hexdigest()

            with open("UserDetails.csv", "a", newline="") as file:
                fileWriter = csv.writer(file, delimiter=",")
                fileWriter.writerow([username, hashedPassword,userType,priviledgeLevel])

            if(userType == "Patient"):
                with open("PersonalDetails.csv", "a", newline="\n") as file:
                    fileWriter = csv.writer(file, delimiter=",")
                    fileWriter.writerow([username,name,gender,age])
            
                
            print("\n!!--Registration Successfull--!!\n")
        else:
            print("\n!!--INVALID ENTRY--!!")

def isRegistered(username):
    file = open("UserDetails.csv", "r", encoding="utf8")
    fileReader = csv.DictReader(file)
    for row in fileReader:
        if row['UserName'] == username:
            return True
    else:
        return False


def login():
    
    loginAttempt = 0
    isValidUser = False
    isLogged = False
    isExit = False

    print("\n---------------------Login---------------------\n")

    while (loginAttempt < 3):
        username = input("Enter your UserName: ").strip()

        isValidUser = isRegistered(username)

        if(isValidUser):
            password = input("Enter the password: ")
            hashedPassword = hashlib.md5(password.encode('utf8')).hexdigest()
            file = open("UserDetails.csv", "r", encoding="utf8")
            reader = csv.DictReader(file)
            for row in reader:
                if row['UserName'] == username:
                    if row['Password'] == hashedPassword:
                        userType = row['UserType']
                        priviledgeLevel = int(row['PriviledgeLevel'])
                        isLogged = True
                        #break
                    else:
                        loginAttempt+=1
                        if(loginAttempt < 3):
                            print("\n!!--Incorrect Password--Please Retry--You have",3-loginAttempt,"attempts left--!!\n")
                            exitInput = input("If you want to exit, please enter 'E': ").strip()
                            if(exitInput in ['E','e']):
                                isExit = True
                                #break
                        #break
                    break
            if(isExit):
                break
        else:
            loginAttempt+=1
            print("\n!!--User does not exist--Try Again--You have",3-loginAttempt,"attempts left--!!")
        if (isLogged):
            print("\n!!--Login Success--!!\n")
            if(priviledgeLevel == 1):
                doctorInterface(username)
            elif (priviledgeLevel == 2):
                nurseInterface(username)
            elif (priviledgeLevel == 3):
                labAssistantInterface(username)
            elif (priviledgeLevel == 4):
                patientInterface(username)
            break
        
    if(loginAttempt>=3):
        print("\n!!--You have made 3 invalid login attempts--System terminating--!!")
        return -1
    else:
        print("\n!!--Redirecting to welcome page--!!")
        
#user interfaces
def padUsername(username,prefix):
    totLen = 47
    padLen = totLen - len(username)-len(prefix)
    paddedUsername = prefix+username
    paddedUsername = paddedUsername.rjust(totLen-padLen//2,"=")
    paddedUsername = paddedUsername.ljust(totLen,"=")

    return paddedUsername

#DOCTOR
def doctorInterface(username):
    priviledgeLevel = 1
    
    print ("--------------------Welcome--------------------\n"+padUsername(username,"Dr.")+"\n-------------------Dashboard-------------------")
    while (True):
        mainOption = input("--------------------Options--------------------\n1: View Details\n2: Edit Details\n3: Log Out\n\nSelect an option: ").strip()
        #view details
        if (mainOption == "1"):
            subOption = input("1: View Patient's Personal Details\n2: View All Appointment Details\n3: View a Single Appointment Details\n\nSelect an option: ").strip()
            
            if (subOption == "1"):
                patientUserName = input("Please Enter Patient's Username: ")
                if(getPersonalDetails(patientUserName)):
                    name,age,gender = getPersonalDetails(patientUserName)
                    print("Name: ",name,"|Age: ",age,"|Gender: ",gender)
                else:
                    print("No such patient exist!\n")
            elif (subOption == "2"):
                appointmentDetails = getAllAppointmentDetails(username,priviledgeLevel)
                if (len(appointmentDetails)>0):
                    for appointment in appointmentDetails:
                        print("AppointmentId: ",appointment[0],"|UserName: ",appointment[1],"|SicknessDetails: ",appointment[2],"|Drug Prescriptions: ",appointment[3],"|Lab Prescriptions: ",appointment[4])
                else:
                    print("No Records found")
            elif (subOption == "3"):
                appointmentId = input("Please Enter the appointment Id: ")
                appointment = getOneAppointmentDetails(appointmentId,priviledgeLevel)
                if (len(appointment)>0):
                    print("AppointmentId: ",appointment[0],"|UserName: ",appointment[1],"|SicknessDetails: ",appointment[2],"|Drug Prescriptions: ",appointment[3],"|Lab Prescriptions: ",appointment[4])
                else:
                    print("No Records found")
            else:
                print("\n!!--INVALID ENTRY--!!")

        #edit details
        elif(mainOption == "2"):
            subOption = input("1: Add new appointment\n2: Edit Appointment Details\n\nSelect an option: ").strip()

            if (subOption == "1"):
                addNewAppointment()
            elif (subOption == "2"):
                appointmentId = input("Please Enter the appointment Id: ").strip()
                editAppointmentDetails(appointmentId,priviledgeLevel)
            else:
                print("\n!!--INVALID ENTRY--!!")

        elif(mainOption == "3"):
            print("Logging out!")
            break
        else:
            print("Please select a valid option..")


#PATIENT
def patientInterface(username):
    priviledgeLevel = 4
    
    print ("--------------------Welcome--------------------\n"+padUsername(username,"Patient:")+"\n-------------------Dashboard-------------------")
    while (True):
        mainOption = input("\n--------------------Options--------------------\n1: View Details\n2: Edit Personal Details\n3: Log Out\n\nSelect an option: ").strip()
        #view details
        if (mainOption == "1"):
            subOption = input("\n---------------View Options--------------------\n1: View Personal Details\n2: View All Appointment Details\n\n\nSelect an option: ").strip()
            
            if (subOption == "1"):
                if(getPersonalDetails(username)):
                    name,age,gender = getPersonalDetails(username)
                    print("Name: ",name,"|Age: ",age,"|Gender: ",gender)
                else:
                    print("!!--No such patient exist--!!\n")
            elif (subOption == "2"):
                appointmentDetails = getAllAppointmentDetails(username,priviledgeLevel)
                if (len(appointmentDetails)>0):
                    print()
                    for appointment in appointmentDetails:
                        print("AppointmentId: ",appointment[0],"|SicknessDetails: ",appointment[1],"|Drug Prescriptions: ",appointment[2],"|Lab Prescriptions: ",appointment[3])
                else:
                    print("!!--No Records found--!!")
            else:
                print("\n!!--INVALID ENTRY--!!")

        #edit details
        elif(mainOption == "2"):
            editPersonalDetails(username)
        elif(mainOption == "3"):
            print("Logging out..")
            break
        else:
            print("Please select a valid option..")

#NURSE
def nurseInterface(username):
    priviledgeLevel = 2
    
    print ("--------------------Welcome--------------------\n"+padUsername(username,"Nurse:")+"\n-------------------Dashboard-------------------")
    while (True):
        mainOption = input("\n--------------------Options--------------------\n1: View Details\n2: Log Out\n\nSelect an option: ").strip()
        #view details
        if (mainOption == "1"):
            subOption = input("1: View Patient's Personal Details\n2: View All Appointment Details\n3: View a Single Appointment Details\n\nSelect an option: ").strip()
            
            if (subOption == "1"):
                patientUserName = input("Please Enter Patient's Username: ")
                if(getPersonalDetails(patientUserName)):
                    name,age,gender = getPersonalDetails(patientUserName)
                    print("Name: ",name,"|Age: ",age,"|Gender: ",gender)
                else:
                    print("No such patient exist!\n")
            elif (subOption == "2"):
                appointmentDetails = getAllAppointmentDetails(username,priviledgeLevel)
                if (len(appointmentDetails)>0):
                    for appointment in appointmentDetails:
                        print("AppointmentId: ",appointment[0],"|UserName: ",appointment[1],"|SicknessDetails: ",appointment[2],"|Drug Prescriptions: ",appointment[3])
                else:
                    print("No Records found")
            elif (subOption == "3"):
                appointmentId = input("Please Enter the appointment Id: ").strip()
                appointment = getOneAppointmentDetails(appointmentId,priviledgeLevel)
                if (len(appointment)>0):
                    print("AppointmentId: ",appointment[0],"|UserName: ",appointment[1],"|SicknessDetails: ",appointment[2],"|Drug Prescriptions: ",appointment[3])
                else:
                    print("\n!!--No Records found--!!")
            else:
                print("\n!!--INVALID ENTRY--!!")

        elif (mainOption == "2"):
            print("Logging out..")
            break
        else:
            print("Please select a valid option")

#LAB ASSISTANT
def labAssistantInterface(username):
    priviledgeLevel = 3
    
    print ("--------------------Welcome--------------------\n"+padUsername(username,"Lab Assistant:")+"\n-------------------Dashboard-------------------")
    while (True):
        mainOption = input("--------------------Options--------------------\n1: View Details\n2: Edit Appointment Details\n3: Log Out\n\nSelect an option: ").strip()
        #view details
        if (mainOption == "1"):
            subOption = input("1: View All Appointment Details\n2: View a Single Appointment Details\n\nSelect an option: ").strip()
            
            if (subOption == "1"):
                appointmentDetails = getAllAppointmentDetails(username,priviledgeLevel)
                if (len(appointmentDetails)>0):
                    print()
                    for appointment in appointmentDetails:
                        print("AppointmentId: ",appointment[0],"|UserName: ",appointment[1],"|Lab Prescriptions: ",appointment[2])
                else:
                    print("No Records found")
                    
            elif (subOption == "2"):
                appointmentId = input("Please Enter the appointment Id: ").strip()
                appointment = getOneAppointmentDetails(appointmentId,priviledgeLevel)
                if (len(appointment)>0):
                    print("AppointmentId: ",appointment[0],"|UserName: ",appointment[1],"|Lab Prescriptions: ",appointment[2])
                else:
                    print("No Records found")
            else:
                print("\n!!--INVALID ENTRY--!!")

        #editDetails
        elif(mainOption == "2"):
            appointmentId = input("Please Enter the appointment Id: ")
            editAppointmentDetails(appointmentId,priviledgeLevel)
        elif(mainOption == "3"):
            print("Logging out..")
            break
        else:
             print("Please select a valid option..")
                
#--------Personal Details-------#
def getPersonalDetails(username):
    file = open("PersonalDetails.csv", "r", encoding="utf8")
    reader = csv.DictReader(file)
    for row in reader:
        if row['UserName'] == username:
            name = row['Name']
            gender = row['Gender']
            age = row['Age']

            return name,age,gender
    else:
        return False

def editPersonalDetails(username):
    isAUser = False
    
    file = open("PersonalDetails.csv", "r", encoding="utf8")
    reader = csv.DictReader(file)
    for row in reader:
        if row['UserName'] == username:
            isAUser = True
            print("\nCurrent Details are as follows: \nName:",row['Name'],"\nGender:",row['Gender'],"\nAge:",row['Age'],"\n")
            break
    if (isAUser):
        newName = input("\nEnter new name: ").strip()
        while (True):
            newGender = input("Enter new gender(F/M): ").strip()
            if (newGender in ["F","f"]):
                newGender = "Female"
                break
            elif(newGender in ["M","m"]):
                newGender = "Male"
                break
            else:
                print("\n!!--Please select a valid gender--!!\n")
        while(True):
            try:
                newAge = int(input("Enter new age: ").strip())
                if newAge >0:
                    break
                else:
                    print("\n!!--Age should be a positive integer--!!")
            except:
                print("\n!!--Please enter a valid age--!!")

        personalDetails = []
        file = open("PersonalDetails.csv", "r", encoding="utf8")
        reader = csv.DictReader(file)
        for row in reader:
            if row['UserName'] == username:
                row['Name'] = newName
                row['Gender'] = newGender
                row['Age'] = newAge
            personalDetails.append(row)

        with open('PersonalDetails.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['UserName', 'Name', 'Gender', 'Age'])

            for user in personalDetails:
                writer.writerow([user['UserName'], user['Name'], user['Gender'], user['Age']])

        print("\n!!--Personal details modified--!!\n")
    

#--------Appointment Details-------#
def getAllAppointmentDetails(username,priviledgeLevel):
    file = open("AppointmentDetails.csv", "r", encoding="utf8")
    reader = csv.DictReader(file)
    appointmentDetails = []

    if(priviledgeLevel == 4):
        for row in reader:
            if row['UserName'] == username:
                rowDetails = [row['AppointmentId'],row['SicknessDetails'],row['DrugPrescriptions'],row['LabPrescriptions']]
                appointmentDetails.append(rowDetails)
    else:
        for row in reader:
            rowDetails = []
            rowDetails.extend([row['AppointmentId'],row['UserName']])

            if (priviledgeLevel == 1):
                rowDetails.extend([row['SicknessDetails'],row['DrugPrescriptions'],row['LabPrescriptions']])
            elif (priviledgeLevel == 2):
                rowDetails.extend([row['SicknessDetails'],row['DrugPrescriptions']])
            elif (priviledgeLevel == 3):
                rowDetails.append(row['LabPrescriptions'])
            #else:
                #if (row['UserName'] == username):
                    #rowDetails = [row['AppointmentId'],row['SicknessDetails'],row['DrugPrescriptions'],row['LabPrescriptions']]

            appointmentDetails.append(rowDetails)
    return appointmentDetails

def getOneAppointmentDetails(appointmentId,priviledgeLevel):
    isAnAppointment = False
    file = open("AppointmentDetails.csv", "r", encoding="utf8")
    reader = csv.DictReader(file)
    appointmentDetails = []
    
    for row in reader:
        if row['AppointmentId'] == appointmentId:
            isAnAppointment = True
            UserName = row['UserName']
            SicknessDetails = row['SicknessDetails']
            DrugPrescriptions = row['DrugPrescriptions']
            LabPrescriptions = row['LabPrescriptions']

            if (priviledgeLevel == 1):
                appointmentDetails=[appointmentId,UserName,SicknessDetails,DrugPrescriptions,LabPrescriptions]
            elif (priviledgeLevel == 2):
                appointmentDetails=[appointmentId,UserName,SicknessDetails,DrugPrescriptions]
            elif (priviledgeLevel == 3):
                appointmentDetails=[appointmentId,UserName,LabPrescriptions]
            else:
                pass
            break
    return appointmentDetails

def addNewAppointment():
    isAUser = False
    file = open("AppointmentDetails.csv", "r", encoding="utf8")
    reader = csv.DictReader(file)
    rows = list(reader)
    appointmentId  = len(rows)

    #validate patient's user name
    while(not isAUser):
        patientUserName = input("\nEnter Patient's user name: ").strip()
        file1 = open("PersonalDetails.csv", "r", encoding="utf8")
        myReader = csv.DictReader(file1)
        for row in myReader:
            if row['UserName'] == patientUserName:
                isAUser = True
                break
        else:
            print("Please enter a valid patient's user name")
    
    sicknessDetails = input("Enter sickness details: ")
    drugPrescriptions = input("Enter drug prescriptions: ")
    labPrescriptions = input("Enter Lab prescriptions: ")
    
    with open("AppointmentDetails.csv", "a", newline="\n") as file:
        fileWriter = csv.writer(file, delimiter=",")
        fileWriter.writerow([appointmentId,patientUserName,sicknessDetails,drugPrescriptions,labPrescriptions])
    print("\n!!--New appointment added successfully--!!")

def editAppointmentDetails(appointmentId,priviledgeLevel):
    isAnAppointment = False
    
    file = open("AppointmentDetails.csv", "r", encoding="utf8")
    reader = csv.DictReader(file)
    for row in reader:
        if row['AppointmentId'] == appointmentId:
            isAnAppointment = True
            newUserName = row['UserName']
            newSicknessDetails = row['SicknessDetails']
            newDrugPrescriptions = row['DrugPrescriptions']
            newLabPrescriptions = row['LabPrescriptions']
            
            print("\nCurrent Details are as follows:\nUserName:",newUserName)
            break
    if (isAnAppointment):
        if (priviledgeLevel == 1 ):
            print("Sickness Details:",newSicknessDetails,"\nDrug Prescriptions:",newDrugPrescriptions,"\nLab Prescriptions:",newLabPrescriptions)
            newSicknessDetails = input("\nEnter new Sickness Details: ").strip()
            newDrugPrescriptions= input("Enter new Drug Prescriptions: ").strip()
            newLabPrescriptions = input("Enter new Lab Prescriptions: ").strip()

        if (priviledgeLevel == 3 ):
            print("Lab Prescriptions:",newLabPrescriptions)
            newLabPrescriptions = input("\nEnter new Lab Prescriptions: ")

        appointmentDetails = []
        file = open("AppointmentDetails.csv", "r", encoding="utf8")
        reader = csv.DictReader(file)
        for row in reader:
            if row['AppointmentId'] == appointmentId:
                row['UserName'] = newUserName
                row['SicknessDetails'] = newSicknessDetails
                row['DrugPrescriptions'] = newDrugPrescriptions
                row['LabPrescriptions'] = newLabPrescriptions
            appointmentDetails.append(row)

        with open('AppointmentDetails.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['AppointmentId','UserName','SicknessDetails','DrugPrescriptions','LabPrescriptions'])

            for appointment in appointmentDetails:
                writer.writerow([appointment['AppointmentId'], appointment['UserName'], appointment['SicknessDetails'], appointment['DrugPrescriptions'], appointment['LabPrescriptions']])

        print("\n!!--Appointment details modified--!!\n")
    
#--------Medical Data Processing System---------#

while (True):
    print("\n--------------------Welcome---------------------")
    print("\n1:Sign Up\n2:Log In\n3:Exit\n")
    
    try :
        loginOrsignup = int(input("Please select an option: "))
        if (loginOrsignup == 1):
            register()
        elif (loginOrsignup == 2):
            returnValue = login()
            if(returnValue == -1):
                break
        elif (loginOrsignup == 3):
            print("!!--System Terminating...GoodBye--!!")
            break
        else:
            print("!!--Please Enter a Valid Input--!!")
    except:
        print("!!--Please Enter a Valid Input--!!")


