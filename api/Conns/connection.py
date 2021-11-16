from datetime import datetime
import pyodbc
import pandas as pd

class ServerConn:
    server = 'tcp:hbda.database.windows.net'
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
            except:
                try:
                    self.conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};Server=tcp:hbda.database.windows.net,1433;Database=hbda_tracking;Uid=trblair;Pwd=Linkedlist4788;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')
                    self.cursor = self.conn.cursor()
                except pyodbc.OperationalError as err:
                    print(err)
    
    def query(self, q, data = None):
        if data is None:
          return pd.read_sql(q, self.conn)
        else:
            return pd.read_sql(q, self.conn, params={data})

    def close_conn(self):
        self.cursor.close()
        self.conn.close()

    #Login fn

    #End of Login fn

    #Access fn
    def get_access(self):
        df = pd.read_sql("SELECT * FROM access", self.conn)
        return df.to_dict(orient = 'index')

    def get_access_by_id(self, access_id):
        qt = "SELECT * FROM access WHERE access_id = ?"
        df = pd.read_sql(qt, self.conn,params={str(access_id)})
        return df.to_dict(orient = 'index')
    
    def get_access_by_desc(self, access_desc):
        qt = "SELECT * FROM access WHERE access_desc = ?"
        df = pd.read_sql(qt, self.conn,params={access_desc})
        return df.to_dict(orient = 'index')

    def add_access(self, temp_id, temp_desc, temp_admin_access):
        qt = "INSERT INTO dbo.access ([access_id],[access_desc],[admin_access]) VALUES (?, ?, ?)"
        data = (temp_id, temp_desc, temp_admin_access)
        try:
            self.cursor.execute(qt, data)
            self.conn.commit()
        except Exception as err:
            print(err)

    def delete_access(self, temp_id):
        qt = "DELETE FROM dbo.access WHERE access_id in (?)"
        try:
            self.cursor.execute(qt, temp_id)
            self.conn.commit()
        except Exception as err:
            print(err)

    def update_access(self, temp_id, temp_desc, temp_admin_access):
        qt = "UPDATE users SET access_desc = ?, admin_access = ? WHERE access_id = ?"
        data = (temp_desc, temp_admin_access, str(temp_id))
        try:
            self.cursor.execute(qt, data)
        except Exception as err:
            print(err)    
        finally:
            self.conn.commit()
    
    #End of Access fn

    

    #Attendee_Group_Link fn
    def get_attendee_group_links(self):
        df = pd.read_sql("SELECT * FROM attendee_group_link", self.conn)
        return df.to_dict(orient = 'index')

    def get_attendee_group_link_by_id(self, link_id):
        qt = "SELECT * FROM attendee_group_link WHERE link_id = ?"
        df = pd.read_sql(qt, self.conn, params={str(link_id)})
        return df.to_dict(orient = 'index')
    
    def add_attendee_group_link(self, temp_total_points, temp_id, temp_attendee_id, temp_event_id, temp_group_id):
        qt = "INSERT INTO dbo.attendee_group_link ([total_points],[link_id],[attendee_id],[event_id],[group_id]) VALUES (?, ?, ?, ?, ?)"
        data = (temp_total_points, str(temp_id), str(temp_attendee_id), str(temp_event_id), str(temp_group_id))
        try:
            self.cursor.execute(qt, data)
            self.conn.commit()
        except Exception as err:
            print(err)

    def delete_attendee_group_link(self, temp_id):
        qt = "DELETE FROM dbo.attendee_group_link WHERE link_id in (?)"
        try:
            self.cursor.execute(qt, temp_id)
            self.conn.commit()
        except Exception as err:
            print(err)

    def delete_attendee_group_link_by_attendee(self, temp_id):
        qt = "DELETE FROM dbo.attendee_group_link WHERE attendee_id in (?)"
        try:
            self.cursor.execute(qt, temp_id)
            self.conn.commit()
        except Exception as err:
            print(err)

    

    def update_attendee_group_link(self, temp_id, temp_attendee_id, temp_event_id, temp_group_id, temp_total_points = None):
        if temp_total_points is None:
            qt = "UPDATE attendee_group_link SET attendee_id = ?, event_id = ?, group_id = ? WHERE link_id = ?"
            data = (temp_total_points, temp_attendee_id, temp_event_id, temp_group_id, str(temp_id))
            try:
                self.cursor.execute(qt, data)
            except Exception as err:
                print(err)    
            finally:
                self.conn.commit()
        else:
            qt = "UPDATE attendee_group_link SET total_points = ?, attendee_id = ?, event_id = ?, group_id = ? WHERE link_id = ?"
            data = (temp_total_points, temp_attendee_id, temp_event_id, temp_group_id, str(temp_id))
            try:
                self.cursor.execute(qt, data)
            except Exception as err:
                print(err)    
            finally:
                self.conn.commit()

    def change_attendee_group(self, temp_attendee_id, temp_group_id):
        qt = "UPDATE attendee_group_link SET group_id = ? WHERE attendee_id = ?"
        data = (str(temp_group_id), str(temp_attendee_id))
        try:
            self.cursor.execute(qt, data)
        except Exception as err:
            print(err)    
        finally:
            self.conn.commit()

    def update_pointlog_AGLext(self, temp_id, temp_total_points):
        qt = "UPDATE attendee_group_link SET total_points = ? WHERE attendee_id = ?"
        data = (temp_total_points, str(temp_id))
        try:
            self.cursor.execute(qt, data)
        except Exception as err:
            print(err)    
        finally:
            self.conn.commit()
    #End of Attendee_Group_Link fn

    #Cascading Deletion functions
    def delete_group_by_event(self, temp_id):
        qt = "DELETE FROM dbo.groups WHERE event_id in (?)"
        try:
            self.delete_attendee_group_link_by_event(temp_id)
            self.cursor.execute(qt, temp_id)
            self.conn.commit()
        except Exception as err:
            print(err)

    def delete_attendee_group_link_by_group(self, temp_id):
        qt = "DELETE FROM dbo.attendee_group_link WHERE group_id in (?)"
        try:
            self.cursor.execute(qt, temp_id)
            self.conn.commit()
        except Exception as err:
            print(err)

    def delete_attendee_group_link_by_event(self, temp_id):
        qt = "DELETE FROM dbo.attendee_group_link WHERE event_id in (?)"
        try:
            self.cursor.execute(qt, temp_id)
            self.conn.commit()
        except Exception as err:
            print(err)

    def delete_pointlog_by_attendee(self, temp_id):
        qt = "DELETE FROM dbo.pointlog WHERE attendee_id in (?)"
        try:
            self.cursor.execute(qt, temp_id)
            self.conn.commit()
        except Exception as err:
            print(err)
    
    def delete_pointlog_by_group(self, temp_id):
        qt = "DELETE FROM dbo.pointlog WHERE group_id in (?)"
        try:
            self.cursor.execute(qt, temp_id)
            self.conn.commit()
        except Exception as err:
            print(err)

    
    def delete_pointlog_by_event(self, temp_id):
        qt = "DELETE FROM dbo.pointlog WHERE event_id in (?)"
        try:
            self.cursor.execute(qt, temp_id)
            self.conn.commit()
        except Exception as err:
            print(err)
    

    #End of Cascading Deletion functions


conn = ServerConn()

    
