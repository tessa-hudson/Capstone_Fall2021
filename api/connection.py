from datetime import datetime
import pyodbc
import pandas as pd

class ServerConn:
    server = 'hbda.database.windows.net'
    database = 'hbda_tracking'
    username = 'cethorne'
    password = 'Thorne123!'

    def __init__(self):
        try:
            self.conn = pyodbc.connect('DRIVER={SQL Server};SERVER='+self.server+';DATABASE='+self.database+';UID='+self.username+';PWD='+ self.password)
            self.cursor = self.conn.cursor()
        except:
            try:
                self.conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+self.server+';DATABASE='+self.database+';UID='+self.username+';PWD='+ self.password)
                self.cursor = self.conn.cursor()
            except pyodbc.OperationalError as err:
                print(err)
    
    def query(self, q):
        return pd.read_sql(q, self.conn)

    def close_conn(self):
        self.cursor.close()
        self.conn.close()
    
    #Attendee fn
    def get_attendees(self):
        df = pd.read_sql("SELECT * FROM attendee", self.conn)
        return df.to_dict(orient = 'index')
    
    def add_attendee(self, temp_id, temp_first, temp_last):
        qt = "INSERT INTO dbo.attendee ([attendee_id],[firstname],[lastname]) VALUES (?, ?, ?)"
        data = (temp_id, temp_first, temp_last)
        self.cursor.execute(qt, data)
        self.conn.commit()
    
    #Deleting by just id or by other fields?
    #Just id
    def delete_attendee(self, temp_id):
        qt = "DELETE FROM dbo.attendee WHERE attendee_id in (?)"
        self.cursor.execute(qt, temp_id)
        self.conn.commit()
    
    #End of Attendee fn

    #Event fn
    def get_events(self):
        df = pd.read_sql("SELECT * FROM event", self.conn)
        return df.to_dict(orient = 'index')

    def add_event(self, temp_id, temp_name, temp_start, temp_end, temp_type):
        qt = "INSERT INTO dbo.event ([event_id],[name],[start_date],[end_date],[type]) VALUES (?, ?, ?, ?, ?)"
        data = (temp_id, temp_name, temp_start, temp_end, temp_type)
        self.cursor.execute(qt, data)
        self.conn.commit()

    #Deleting by just id or by other fields?
    def delete_event(self, temp_id):
        qt = "DELETE FROM dbo.event WHERE event_id in (?)"
        self.cursor.execute(qt, temp_id)
        self.conn.commit()
    #End Event fn

    #Groups fn
    def get_group(self):
        df = pd.read_sql("SELECT * FROM groups", self.conn)
        return df.to_dict(orient = 'index')

    def add_group(self, temp_group_id, temp_event_id, temp_name, temp_total_points):
        qt = "INSERT INTO dbo.groups ([group_id],[event_id],[group_name], [total_points]) VALUES (?, ?, ?, ?)"
        data = (temp_group_id, temp_event_id, temp_name, temp_total_points)
        self.cursor.execute(qt, data)
        self.conn.commit()
    
    #Deleting by just id or by other fields?
    def delete_group(self, temp_id):
        qt = "DELETE FROM dbo.groups WHERE group_id in (?)"
        self.cursor.execute(qt, temp_id)
        self.conn.commit()
    #End of Groups fn

    #Users fn
    def get_user(self):
        df = pd.read_sql("SELECT * FROM users", self.conn)
        return df.to_dict(orient = 'index')

    def add_user(self, temp_event_id, temp_login_name, temp_user_password, temp_email, temp_firstname, temp_lastname, temp_access_id):
        qt = "INSERT INTO dbo.users ([user_id],[login_name],[user_password],[email],[firstname],[lastname], [access_id]) VALUES (?, ?, ?, ?, ?, ?, ?)"
        data = (temp_event_id, temp_login_name, temp_user_password, temp_email, temp_firstname, temp_lastname, temp_access_id)
        self.cursor.execute(qt, data)
        self.conn.commit()

    def delete_user(self, temp_id):
        qt = "DELETE FROM dbo.users WHERE user_id in (?)"
        self.cursor.execute(qt, temp_id)
        self.conn.commit()
    #End of Users fn

    #Access fn
    def get_access(self):
        df = pd.read_sql("SELECT * FROM access", self.conn)
        return df.to_dict(orient = 'index')

    def add_access(self, temp_id, temp_desc, temp_admin_access):
        qt = "INSERT INTO dbo.access ([access_id],[access_desc],[admin_access]) VALUES (?, ?, ?)"
        data = (temp_id, temp_desc, temp_admin_access)
        self.cursor.execute(qt, data)
        self.conn.commit()

    def delete_access(self, temp_id):
        qt = "DELETE FROM dbo.access WHERE access_id in (?)"
        self.cursor.execute(qt, temp_id)
        self.conn.commit()
    #End of Access fn

    #Pointlog fn
    def get_pointlog(self):
        df = pd.read_sql("SELECT * FROM pointlog", self.conn)
        return df.to_dict(orient = 'index')

    def add_pointlog(self, temp_pointlog_id, temp_user_id, temp_event_id, temp_attendee_id, temp_group_id, temp_date, temp_point_change,temp_comment, temp_status):
        qt = "INSERT INTO dbo.pointlog ([pointlog_id],[user_id],[event_id],[attendee_id],[group_id],[date], [point_change], [comment], [status]) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        data = (temp_pointlog_id, temp_user_id, temp_event_id, temp_attendee_id, temp_group_id, temp_date, temp_point_change,temp_comment, temp_status)
        self.cursor.execute(qt, data)
        self.conn.commit()
    
    def delete_pointlog(self, temp_id):
        qt = "DELETE FROM dbo.pointlog WHERE pointlog_id in (?)"
        self.cursor.execute(qt, temp_id)
        self.conn.commit()

    #End of Pointlog fn

    #Attendee_Group_Link fn
    def get_attendee_group_link(self):
        df = pd.read_sql("SELECT * FROM attendee_group_link", self.conn)
        return df.to_dict(orient = 'index')
    
    def add_attendee_group_link(self, temp_id, temp_attendee_id, temp_event_id, temp_group_id, temp_total_points):
        qt = "INSERT INTO dbo.attendee_group_link ([link_id],[attendee_id],[event_id],[group_id],[total_points]) VALUES (?, ?, ?, ?, ?)"
        data = (temp_id, temp_attendee_id, temp_event_id, temp_group_id, temp_total_points)
        self.cursor.execute(qt, data)
        self.conn.commit()

    def delete_attendee_group_link(self, temp_id):
        qt = "DELETE FROM dbo.attendee_group_link WHERE link_id in (?)"
        self.cursor.execute(qt, temp_id)
        self.conn.commit()
    #End of Attendee_Group_Link fn

conn = ServerConn()

    