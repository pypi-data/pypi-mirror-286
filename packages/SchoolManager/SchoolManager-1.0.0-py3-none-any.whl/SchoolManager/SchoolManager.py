import random
 

class Human:
    def __init__(self, name , family , national_code) -> None:
        self.id = random.randint(1 , 9999)
        self.name = name
        self.family = family
        self.national_code = national_code
        

        
        
    def __str__(self) -> str:
        string = f"Id: {self.iD}\t Full Name : {self.name} {self.family} \t National Code : {self.national_code}"
        return string
    
    
class Book:
    def __init__(self, name_book,level_book , ) -> None :
        self.id = random.randint(1, 9999)
        self.name_book = name_book
        self.level_book = level_book
        
        
        
    def __str__(self) -> str:
        return f" Name Book : {self.name_book}\t Level : {self.level_book}"

class Student(Human):
    def __init__(self, name , family , national_code) -> None:
        self.student_code = random.randint(10000000,99999999)
        super().__init__(name, family, national_code)
        
        
        
    def __str__(self) -> str:
        output = f"Student Code : {self.student_code}"
        output += super().__str__()
        return output


class Teacher(Human):
    def __init__(self, name, family, national_code ,personal_code, salary, time_teach) -> None:
        super().__init__(name, family, national_code)
        self.personal_code = personal_code
        self.salary = salary
        self.time_teach = time_teach
        
    def __str__(self) -> str:
        output = super().__str__()
        output += f"Personal Code : {self.personal_code}\t Time Teach : {self.time_teach}"
        output += f"Salary : {self.salary}"
        return output



class Class:
    def __init__(self , title , level) -> None:
        self.id = random.randint(1, 9999)
        self.title = title
        self.level = level



    def __str__(self) -> str:
        return f"Title CLass : {self.title}\t Level Class : {self.level}"




#========================================================================================================================

class RSB:
    def __init__(self, fk_id_student , fk_id_book) -> None:
        self.id = random.randint(10000000,99999999)
        self.fk_id_student = fk_id_student
        self.fk_id_book = fk_id_book


class RSC:
    def __init__(self, fk_id_student , fk_id_class) -> None:
        self.id = random.randint(10000000,99999999)
        self.fk_id_student = fk_id_student
        self.fk_id_class = fk_id_class


class RTB:
    def __init__(self, fk_id_teacher , fk_id_book) -> None:
        self.iD = random.randint(10000000,99999999)
        self.fk_id_teacher = fk_id_teacher
        self.fk_id_book = fk_id_book


class RTC:
    def __init__(self, fk_id_teacher , fk_id_class) -> None:
        self.id = random.randint(10000000,99999999)
        self.fk_id_teacher = fk_id_teacher
        self.fk_id_class = fk_id_class
        
    
    
    


#========================================================================================================================

    
def RgisterClass() -> list:
    new_list = []
    while True:
        model_Book = Class(
            
            input("Enter Title of Class :"),
            input("Enter Level of Class :"),
            )
        
        new_list.append(model_Book)
        answer = input("Are You Continue(y/n) :")
        if answer.lower() == 'n' :
            break
        
    return new_list






def RgisterTeacher() -> list:
    new_list = []
    while True:
        model_Teacher = Teacher(
            input("Enter Name :"),
            input("Enter Family :"),
            input("Enter National Code :"),
            input("Enter Personal Code :"),
            input("Enter Salary:"),
            input("Enter Time Teach :")
            
            )
        
        new_list.append(model_Teacher)
        answer = input("Are You Continue(y/n) :")
        if answer.lower() == 'n' :
            break
        
    return new_list


    
    
def RgisterStudent() -> list:
    new_list = []
    while True:
        model_student = Student(
            
            input("Enter Name :"),
            input("Enter Family:"),
            input("Enter National Code Of Student :")
            )
        
        new_list.append(model_student)
        answer = input("Are You Continue(y/n) :")
        if answer.lower() == 'n' :
            break
        
    return new_list



def RgisterBook() -> list:
    new_list = []
    while True:
        model_Book = Book(
            
            input("Enter Name of Book :"),
            input("Enter level of Book:"),
            )
        
        new_list.append(model_Book)
        answer = input("Are You Continue(y/n) :")
        if answer.lower() == 'n' :
            break
        
    return new_list


#========================================================================================================================



def DataEntryStudentCSV(li:list) -> bool :
    count_save = 0
    with open('Student.csv' , '+a') as file_student:
        for Student in li:
            s_student = f"{Student.id},{Student.name},{Student.family},{Student.national_code}, {Student.student_code}"
            count_save += file_student.write(s_student+"\n")
    return count_save > 0

def DataEntryTeacherCSV(li:list) -> bool :
    count_save = 0
    with open('Teacher.csv' , '+a') as file_Teacher:
        for Teacher in li:
            s_Teacher = f"{Teacher.name},{Teacher.family},{Teacher.national_code},{Teacher.personal_code},{Teacher.salary},{Teacher.time_teach}"
            count_save += file_Teacher.write(s_Teacher+"\n")
    return count_save > 0

def DataEntryCLassCSV(li:list) -> bool :
    count_save = 0
    with open('Class.csv' , '+a') as file_Class:
        for Class in li:
            s_Class = f"{Class.id},{Class.title},{Class.level}"
            count_save += file_Class.write(s_Class+"\n")
    return count_save > 0  
                
def DataEntryBookCSV(li:list) -> bool :
    count_save = 0
    with open('Book.csv' , '+a') as file_Book:
        for Book in li:
            s_Book = f"{Book.id},{Book.name_book},{Book.level_book}"
            count_save += file_Book.write(s_Book+"\n")
    return count_save > 0      




#========================================================================================================================



def Get_id_teacher(nationalcode:int) -> int:
    Teacher_id = 0
    with open("Teacher.csv") as teach:
        data = teach.read()
        list_data = data.splitlines()
        for item in list_data:
            Teacher = item.split(',')
            print(Teacher[2])
            if nationalcode == int(Teacher[2]):
                Teacher_id = Teacher[0]
                print(Teacher_id)
                break
    return Teacher_id

def Get_id_student(nationalcode:int) -> int:
    std_id = 0
    with open("Student.csv") as std:
        data = std.read()
        list_data = data.splitlines()
        for item in list_data:
            Student = item.split(',')
            if nationalcode == int(Student[3]):
                std_id = Student[0]
                break
    return std_id


def Get_id_book(info_book):
    book_id = 0
    with open("Book.csv") as book:
        data = book.read()
        list_data = data.splitlines()
        for item in list_data:
            bo = item.split(',')
            print(bo)
            print(info_book)
            if info_book[0] == bo[1] and info_book[1] == bo[2]:
                book_id = bo[0]
                break
    return book_id



def Get_id_class(info_class):
    Class_id = 0
    with open("Class.csv") as Class:
        data = Class.read()
        list_data = data.splitlines()
        for item in list_data:
            cl = item.split(',')
            print(cl)
            print(info_class)
            if info_class[0] == cl[1] and info_class[1] == cl[2]:
                Class_id = cl[0]
                break
    return Class_id

#========================================================================================================================
def check_RSB(item:RSB) -> bool:
    with open("RSB.csv") as file:
        data_list = file.read().splitlines()
        for data in data_list:
            data_split = data.split(',')
            if item.fk_id_student == data_split[1] and item.fk_id_book == data_split[2]:
                return True
        
    return False







def check_RSC(item:RSC) -> bool:
    with open("RSC.csv") as file:
        data_list = file.read().splitlines()
        for data in data_list:
            data_split = data.split(',')
            if item.fk_id_student == data_split[1] and item.fk_id_class == data_split[2]:
                return True
        
    return False







def check_RTB(item:RTB) -> bool:
    with open("RTB.csv") as file:
        data_list = file.read().splitlines()
        for data in data_list:
            data_split = data.split(',')
            if item.fk_id_teacher == data_split[1] and item.fk_id_book == data_split[2]:
                return True
        
    return False








def check_RTC(item:RTC) -> bool:
    with open("RTC.csv") as file:
        data_list = file.read().splitlines()
        for data in data_list:
            data_split = data.split(',')
            if item.fk_id_teacher == data_split[1] and item.fk_id_class == data_split[2]:
                return True
        
    return False








#========================================================================================================================
def Register_Rsb() -> list:
    list_rsb = []
    while True:
        student_id = Get_id_student(int(input("Enter National Code :")))
        while True:
            info_book = (input("Enter Name Book :"),input("Enter Level Book :"))
            Book_id = Get_id_book(info_book)
            rsb = RSB(student_id , Book_id)
            list_rsb.append(rsb)
            answer = input("Are Want to You Continue Register Book for this Student(y/n) :")
            if answer.lower() == 'n' or answer.lower() == 'no' :
                break
        answer = input("Are Want to You Continue Register Book for Another Student(y/n) :")
        if answer.lower() == 'n' or answer.lower() == 'no' :
            break    
    return list_rsb

def RegisterRSB_csv(li:list) -> bool:
    count = 0
    with open('RSB.csv' , '+a') as rsb_csv:
        for RSB in li:
            if not check_RSB(RSB):
                str_save = f"{RSB.id},{RSB.fk_id_student},{RSB.fk_id_book}\n"
                count += rsb_csv.write(str_save)
            elif True:
                print("Your data has been Entered...\n")
                print(100*'=')
    return count != 0 





def Register_RSC() -> list:
    list_rsc = []
    while True:
        student_id = Get_id_student(int(input("Enter National Code :")))
        while True:
            info_class = (input("Enter title Class :"),input("Enter Level Class :"))
            class_id = Get_id_class(info_class)
            rsc = RSC(student_id , class_id)
            list_rsc.append(rsc)
            answer = input("Are Want to You Continue Register Class for this Student(y/n) :")
            if answer.lower() == 'n' or answer.lower() == 'no' :
                break
        answer = input("Are Want to You Continue Register Class for Another Student(y/n) :")
        if answer.lower() == 'n' or answer.lower() == 'no' :
            break    
    return list_rsc


def RegisterRSC_csv(li:list) -> bool:
    count = 0
    with open('RSC.csv' , '+a') as rsc_csv:
        for RSC in li:
            if not check_RSC(RSC):
                str_save = f"{RSC.id} , {RSC.fk_id_student} , {RSC.fk_id_class}\n"
                count += rsc_csv.write(str_save)
            elif True:
                print("Your data has been Entered...\n")
                print(100*'=')
    return count != 0 

def Register_RTC() -> list:
    list_rtc = []
    while True:
        teacher_id = Get_id_teacher(int(input("Enter National Code :")))
        while True:
            info_class = (input("Enter title Class :"),input("Enter Level Class :"))
            class_id = Get_id_teacher(info_class)
            rtc = RTC(teacher_id , class_id)
            list_rtc.append(rtc)
            answer = input("Are Want to You Continue Register Class for this Teacher(y/n) :")
            if answer.lower() == 'n' or answer.lower() == 'no' :
                break
        answer = input("Are Want to You Continue Register Teacher for Another Student(y/n) :")
        if answer.lower() == 'n' or answer.lower() == 'no' :
            break    
    return list_rtc


def RegisterRTC_csv(li:list) -> bool:
    count = 0
    with open('RTC.csv' , '+a') as rtc_csv:
        for RTC in li:
            if not check_RTC(RTC):
                str_save = f"{RTC.id} , {RTC.fk_id_teacher} , {RTC.fk_id_class}\n"
                count += rtc_csv.write(str_save)
            elif True:
                print("Your data has been Entered...\n")
                print(100*'=')
    return count != 0 
    





    
def Register_Rtb() -> list:
    list_rtb = []
    while True:
        teacher_id = Get_id_teacher(int(input("Enter National Code :")))
        while True:
            info_book = (input("Enter Name Book :"),input("Enter Level Book :"))
            Book_id = Get_id_book(info_book)
            rtb = RTB(teacher_id , Book_id)
            list_rtb.append(rtb)
            answer = input("Are Want to You Continue Register Book for this Teacher(y/n) :")
            if answer.lower() == 'n' or answer.lower() == 'no' :
                break
        answer = input("Are Want to You Continue Register Book for another Teacher(y/n) :")
        if answer.lower() == 'n' or answer.lower() == 'no' :
            break    
    return list_rtb

def RegisterRTB_csv(li:list) -> bool:
    count = 0
    with open('RTB.csv' , '+a') as rtb_csv:
        for RTB in li:
            if not check_RTB(RTB):
                str_save = f"{RTB.iD} , {RTB.fk_id_teacher} , {RTB.fk_id_book}\n"
                count += rtb_csv.write(str_save)
            elif True:
                print("Your data has been Entered...\n")
                print(100*'=')
    return count != 0 




#========================================================================================================================

def show_list_class(list_id:list) -> None:
    with open("Class.csv") as file:
        class_list = file.read().splitlines()
        for item in class_list:
            cl = item.split(',')
            if cl[0] in list_id:
                print(f"titel : {cl[1]}\tLevel : {cl[2]}")
                
                
                
                

def show_list_book(list_id:list) -> None:
    with open("Book.csv") as file:
        book_list = file.read().splitlines()
        for item in book_list:
            book = item.split(',')
            if book[0] in list_id:
                print(f"Name : {book[1]}\tLevel : {book[2]}")


def Get_List_Book_RSB(ID_student:str) -> list:
    list_id_book = []
    with open("RSB.csv") as rsb:
        data_list = rsb.read().splitlines()
        for item in data_list:
            split_rsb = item.split(',')
            if ID_student == split_rsb[1].strip():#'1591' == ' 1591'
                list_id_book.append(split_rsb[2].strip())
    return list_id_book


            

def show_list_student_book() -> None:
    while True:
        national_code = int(input("Enter national code student :"))
        student_id = Get_id_student(national_code)
        if student_id != 0:
            get_list_id_book = Get_List_Book_RSB(student_id)
            if len(get_list_id_book)!= 0:
             show_list_book(get_list_id_book)
        else:
            print(f"can not find student for national code :{national_code}")
        answer = input("Are Want Continue(y/n) :")
        if answer.lower() == 'n' or answer.lower() == 'no' :
            break
        
        
def Get_List_class_RSC(ID_student:str) -> list:
    list_id_class = []
    with open("RSC.csv") as rsc:
        data_list = rsc.read().splitlines()
        for item in data_list:
            split_rsc = item.split(',')
            if ID_student == split_rsc[1]:
                list_id_class.append(split_rsc[2])
    return list_id_class        
        

            

def show_list_student_class() -> None:
    while True:
        national_code = int(input("Enter national code student :"))
        student_id = Get_id_student(national_code)
        if student_id != 0:
            get_list_id_class = Get_List_class_RSC(student_id)
            if len(get_list_id_class)!= 0:
             show_list_class(get_list_id_class)
        else:
            print(f"can not find student for national code :{national_code}")
        answer = input("Are Want Continue(y/n) :")
        if answer.lower() == 'n' or answer.lower() == 'no' :
            break        
        
def Get_List_Book_RTB(ID_teacher:str) -> list:
    list_id_teacher = []
    with open("RTB.csv") as rtb:
        data_list = rtb.read().splitlines()
        for item in data_list:
            split_rsc = item.split(',')
            if ID_teacher == split_rsc[1]:
                list_id_teacher.append(split_rsc[2])
    return list_id_teacher        
        

            

def show_list_teacher_Book() -> None:
    while True:
        national_code = int(input("Enter national code Teacher :"))
        Teacher_id = Get_id_teacher(national_code)
        if Teacher_id != 0:
            get_list_id_Book = Get_List_Book_RTB(Teacher_id)
            if len(get_list_id_Book)!= 0:
             show_list_book(get_list_id_Book)
        else:
            print(f"can not find teacher for national code :{national_code}")
        answer = input("Are Want Continue(y/n) :")
        if answer.lower() == 'n' or answer.lower() == 'no' :
            break
        
        
def Get_List_class_RTC(ID_teacher:str) -> list:
    list_id_book = []
    with open("RTC.csv") as rtc:
        data_list = rtc.read().splitlines()
        for item in data_list:
            split_rtc = item.split(',')
            if ID_teacher == split_rtc[1]:
                list_id_book.append(split_rtc[2])
    return list_id_book


            

def show_list_teacher_class() -> None:
    while True:
        national_code = int(input("Enter national code student :"))
        teacher_id = Get_id_teacher(national_code)
        if teacher_id != 0:
            get_list_id_class = Get_List_class_RTC(teacher_id)
            if len(get_list_id_class)!= 0:
             show_list_class(get_list_id_class)
        else:
            print(f"can not find Teacher for national code :{national_code}")
        answer = input("Are Want Continue(y/n) :")
        if answer.lower() == 'n' or answer.lower() == 'no' :
            break





#========================================================================================================================               
           
        
def Menu() -> None:
    string_menu = '''
    1 ) Register Student
    2 ) Register Teacher
    3 ) Register Book
    4 ) Register Class
    5 ) RSB (Relation Student Book)
    6 ) RSC (Relation Student Class)
    7 ) RTB (Relation Teacher Book)
    8 ) RTC (Relation Teacher Class)
    9 ) Show RSB
   10 ) Show RSC
   11 ) Show RTB
   12 )Show RTC
   13 ) Exit
    Plaese Select Number 1 Until The 13 :
    
    '''
    while True:
        option = int(input(string_menu))
        if option == 1:
            if DataEntryStudentCSV(RgisterStudent()):
                print("\n",100*"=")
                print("Success Register Info ... ")
            else:
                print("Someting went wrong ...")    
        
        

        elif option == 2:
            if DataEntryTeacherCSV(RgisterTeacher()):
                print("\n",100*"=")
                print("Success Register Info ... ")
            else:
                print("Someting went wrong ...")        



        elif option == 3:
            if DataEntryBookCSV(RgisterBook()):
                print("\n",100*"=")
                print("Success Register Info ... ")
            else:
                print("Someting went wrong ...")
                
        elif option == 4:
            if DataEntryCLassCSV(RgisterClass()):
                print("Success Register Info ... ")
            else:
                print("Someting went wrong ...")         
                
        elif option == 5:
            if RegisterRSB_csv(Register_Rsb()):
                print("Success Register Info ... ")
            else:
                print("Someting went wrong ...")
                   
        elif option == 6:
            if RegisterRSC_csv(Register_RSC()):
                print("Success Register Info ... ")
            else:
                print("Someting went wrong ...")
        
        
        
        
        elif option == 7:
            if RegisterRTB_csv(Register_Rtb()):
                print("Success Register Info ... ")
            else:
                print("Someting went wrong ...")
        
        elif option == 8:
            if RegisterRTC_csv(Register_RTC()):
                print("Success Register Info ... ")
            else:
                print("Someting went wrong ...")
        
        
       
        elif option == 9:
            if show_list_student_book():
                print("Success Register Info ... ")
            else:
                print("Someting went wrong ...")
                
        elif option == 10:
            if show_list_student_class():
                print("Success Register Info ... ")
            else:
                print("Someting went wrong ...")
                
        elif option == 11:
            if show_list_teacher_Book():
                print("Success Register Info ... ")
            else:
                print("Someting went wrong ...")
        elif option == 12:
            if show_list_teacher_class():
                print("Success Register Info ... ")
            else:
                print("Someting went wrong ...")
                
        elif option == 13:
            break
                
                
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    