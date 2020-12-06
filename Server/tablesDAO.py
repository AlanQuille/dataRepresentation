import mysql.connector
class StudentDAO:
    db=""
    def __init__(self):
        self.db=mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            #user="datarep",#thisistheusernameonmymac#passwd="password"#formymac
            database="datarepresentation")
    def create(self,values):
        try:
            cursor=self.db.cursor()
            sql="insert into student (Name,Age) values(%s,%s)"
            cursor.execute(sql,values)
            self.db.commit()
            return cursor.lastrowid
        except mysql.connector.Error as err:
            return "Error: {}".format(err)
            
    def getAll(self):
        try:
            cursor=self.db.cursor()
            sql="select *from student"
            cursor.execute(sql)
            result=cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            return "Error: {}".format(err)

    def findByID(self,id):
        try:
            cursor=self.db.cursor()
            sql="select * from student where id=%s"
            values=(id,)
            cursor.execute(sql, values)
            result = cursor.fetchone()
            return result
        except mysql.connector.Error as err:
            return "Error: {}".format(err)
    def update(self,values):
        try:
            cursor=self.db.cursor()
            sql="update student set name=%s, age=%s where id=%s"
            cursor.execute(sql,values)
            self.db.commit()
            return "Success"
        except mysql.connector.Error as err:
            return "Error: {}".format(err)
        
    def delete(self,id):
        try:
            cursor=self.db.cursor()
            sql="delete from student where id=%s"
            values=(id,)
            cursor.execute(sql,values)
            self.db.commit()
            if(self.findByID(id)=="Success"):
                return "Success"
            else:
                return self.findByID(id)
        except mysql.connector.Error as err:
            return "Error: {}".format(err)

        
studentDAO=StudentDAO()

class LecturerDAO:
    db=""
    def __init__(self):
        self.db=mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            #user="datarep",#thisistheusernameonmymac#passwd="password"#formymac
            database="datarepresentation")
    def create(self,values):
        try:
          cursor=self.db.cursor()
          sql="insert into lecturer (Name,Age) values(%s,%s)"
          cursor.execute(sql,values)
          self.db.commit()
          return cursor.lastrowid
        except mysql.connector.Error as err:
            return "Error: {}".format(err)

    def getAll(self):
        try:
            cursor=self.db.cursor()
            sql="select *from lecturer"
            cursor.execute(sql)
            result=cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            return "Error: {}".format(err)
    def findByID(self,id):
        try:
            cursor=self.db.cursor()
            sql="select * from lecturer where id=%s"
            values=(id,)
            cursor.execute(sql, values)
            result = cursor.fetchone()
            return result
        except mysql.connector.Error as err:
            return "Error: {}".format(err)

    def update(self,values):
        try:
            cursor=self.db.cursor()
            sql="update lecturer set name=%s, age=%s where id=%s"
            cursor.execute(sql,values)
            self.db.commit()
            return "Success"
        except mysql.connector.Error as err:
            return "Error: {}".format(err)

        
    def delete(self,id):
        try:
            cursor=self.db.cursor()
            sql="delete from lecturer where id=%s"
            values=(id,)
            cursor.execute(sql,values)
            self.db.commit()
            return "Success"
        except mysql.connector.Error as err:
            return "Error: {}".format(err)


lecturerDAO=LecturerDAO()


class Create_and_Delete_Tables:
    db=""
    def __init__(self):
        self.db=mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            #user="datarep",#thisistheusernameonmymac#passwd="password"#formymac
            database="datarepresentation")

    def create_student(self):
        try:
            cursor=self.db.cursor()
            sql="CREATE TABLE student (ID int auto_increment,Name varchar(255),Age int,PRIMARY KEY(ID));"
            cursor.execute(sql)
            return "Success"
        except mysql.connector.Error as err:
            return "Error: {}".format(err)
    
    def delete_student(self):
        try:
            cursor=self.db.cursor()
            sql="DROP TABLE student;"
            cursor.execute(sql)
            return "Success"
        except mysql.connector.Error as err:
            return "Error: {}".format(err)

    def create_lecturer(self):
        try:
            cursor=self.db.cursor()
            sql="CREATE TABLE lecturer (ID int auto_increment,Name varchar(255),Age int,PRIMARY KEY(ID));"
            cursor.execute(sql)
            return "Success"
        except mysql.connector.Error as err:
            return "Error: {}".format(err)
    
    def delete_lecturer(self):
        try:
            cursor=self.db.cursor()
            sql="DROP TABLE lecturer;"
            cursor.execute(sql)
            return "Success"
        except mysql.connector.Error as err:
            return "Error: {}".format(err)

cadt =Create_and_Delete_Tables()


class Join_Table:
    db=""
    def __init__(self):
        self.db=mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            #user="datarep",#thisistheusernameonmymac#passwd="password"#formymac
            database="datarepresentation")

    def inner_join(self):
        try:
            cursor=self.db.cursor()
            sql="select s.name, l.name from student s inner join lecturer l on l.ID = s.ID;"
            cursor.execute(sql)
            result=cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            return "Error: {}".format(err)

jointable = Join_Table()