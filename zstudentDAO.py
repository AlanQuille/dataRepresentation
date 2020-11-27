import mysql.connector
class StudentDAO:
    db=""
    def __init__(self):
        self.db=mysql.connector.connect(
            host="localhost",
            user="root",
            password="callous1.",
            #user="datarep",#thisistheusernameonmymac#passwd="password"#formymac
            database="datarepresentation",
            auth_plugin='mysql_native_password')
    def create(self,values):
        cursor=self.db.cursor(buffered=True)
        # rewrite this code to make it clearer
        # make values into readable form
        sql="insert into student (Name,Age) values(%s,%s)"
        cursor.execute(sql,values)
        #sql = "select * from student"
        #cursor.execute(sql)
        self.db.commit()
        return cursor.lastrowid
    def getAll(self):
        cursor=self.db.cursor()
        sql="select *from student"
        cursor.execute(sql)
        result=cursor.fetchall()
        return result
    def findByID(self,id):
        cursor=self.db.cursor()
        sql="select * from student where id=%s"
        values=(id,)
        cursor.execute(sql,values)
        result=cursor.fetchone()
        return result
    def update(self,values):
        cursor=self.db.cursor()
        sql="update student set name=%s, age=%s where id=%s"
        cursor.execute(sql,values)
        self.db.commit()
        
    def delete(self,id):
        cursor=self.db.cursor()
        sql="delete from student where id=%s"
        values=(id,)
        
        cursor.execute(sql,values)
        
        self.db.commit()
        print("delete done")
        
studentDAO=StudentDAO()
