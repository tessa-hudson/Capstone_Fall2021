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
    
    #Attendee fn
    def get_attendees(self):
        df = pd.read_sql("SELECT * FROM attendee", self.conn)
        return df.to_dict(orient = 'index')
        

    def get_attendee_by_id(self, attendee_id):
        qt = "SELECT * FROM attendee WHERE attendee_id = ?"
        df = pd.read_sql(qt, self.conn, params={str(attendee_id)})
        return df.to_dict(orient = 'index')

    def get_attendee_by_name(self, first_name, last_initial):
        qt = "SELECT * FROM attendee WHERE firstname = ? AND lastname = ?"
        df = pd.read_sql(qt, self.conn,params={first_name,last_initial})
        return df.to_dict(orient = 'index')

    def get_attendees_by_group_id(self, group_id):
        qt = "SELECT attendee.attendee_id, firstname, lastname FROM attendee FULL JOIN attendee_group_link ON attendee.attendee_id = attendee_group_link.attendee_id WHERE group_id = ?"
        df = pd.read_sql(qt, self.conn, params={str(group_id)})
        return df.to_dict(orient = 'index')

    def get_attendees_by_event_id(self, event_id):
        qt = "SELECT attendee.attendee_id, firstname, lastname FROM attendee FULL JOIN attendee_group_link ON attendee.attendee_id = attendee_group_link.attendee_id WHERE group_id = ?"
        df = pd.read_sql(qt, self.conn, params={str(event_id)})
        return df.to_dict(orient = 'index')

    def get_attendee_total_points(self, attendee_id):
        qt = "SELECT firstname, lastname, total_points FROM attendee FULL JOIN attendee_group_link ON attendee.attendee_id = attendee_group_link.attendee_id WHERE attendee_id = ?"
        df = pd.read_sql(qt, self.conn, params={str(attendee_id)})
        return df.to_dict(orient = 'index')
    
    def add_attendee(self, temp_id, temp_first, temp_last):
        qt = "INSERT INTO dbo.attendee ([attendee_id],[firstname],[lastname]) VALUES (?, ?, ?)"
        data = (temp_id, temp_first, temp_last)
        try:
            self.cursor.execute(qt, data)
            self.conn.commit()
        except Exception as err:
            print(err)
    
    #Deleting by just id or by other fields?
    #Just id
    def delete_attendee(self, temp_id):
        qt = "DELETE FROM dbo.attendee WHERE attendee_id in (?)"
        try:
            self.delete_attendee_group_link_by_attendee(temp_id)
            self.cursor.execute(qt, temp_id)
            self.conn.commit()
        except Exception as err:
            print(err)

    def update_attendee(self, temp_id, first_name, last_name):
        qt = "UPDATE attendee SET firstname = ?, lastname = ? WHERE attendee_id = ?"
        data = (first_name, last_name, str(temp_id))
        try:
            self.cursor.execute(qt, data)
        except Exception as err:
            print(err)    
        finally:
            self.conn.commit()
    
    def add_attendee_to_group(self, temp_link_id, temp_attendee_id, temp_group_id):
        qt = "SELECT event_id FROM groups WHERE group_id = ?"
        df = pd.read_sql(qt, self.conn, params={str(temp_group_id)})
        self.add_attendee_group_link(0, temp_link_id, temp_attendee_id, df.loc[0].at["event_id"], temp_group_id)
    
    def update_attendee_points(self, temp_id, temp_points):
        qt = "UPDATE attendee_group_link SET total_points = ? WHERE attendee_id = ?"
        data = (temp_points, str(temp_id))
        try:
            self.cursor.execute(qt, data)
        except Exception as err:
            print(err)    
        finally:
            self.conn.commit()
    #End of Attendee fn

    #Event fn
    def get_events(self):
        df = pd.read_sql("SELECT * FROM events", self.conn)
        return df.to_dict(orient = 'index')

    def get_event_by_id(self, event_id):
        qt = "SELECT * FROM events WHERE event_id = ?"
        df = pd.read_sql(qt, self.conn, params={str(event_id)})
        return df.to_dict(orient = 'index')

    def get_event_by_name(self, event_name):
        qt = "SELECT * FROM events WHERE event_name = ?"
        df = pd.read_sql(qt, self.conn, params={event_name})
        return df.to_dict(orient = 'index')

    def add_event(self, temp_id, temp_name, temp_start, temp_end, temp_type):
        qt = "INSERT INTO dbo.events ([event_id],[event_name],[start_date],[end_date],[event_type]) VALUES (?, ?, ?, ?, ?)"
        data = (temp_id, temp_name, temp_start, temp_end, temp_type)
        try:
            self.cursor.execute(qt, data)
            self.conn.commit()
        except Exception as err:
            print(err)

    #Deleting by just id or by other fields?
    def delete_event(self, temp_id):
        qt = "DELETE FROM dbo.events WHERE event_id in (?)"
        try:
            self.delete_group_by_event(temp_id)
            self.cursor.execute(qt, temp_id)
            self.conn.commit()
        except Exception as err:
            print(err)
    
    def update_event(self, temp_id, temp_name, temp_start, temp_end, temp_type):
        qt = "UPDATE events SET event_name = ?, start_date = ?, end_date = ?, event_type = ? WHERE event_id = ?"
        data = (temp_name, temp_start, temp_end, temp_type, str(temp_id))
        try:
            self.cursor.execute(qt, data)
        except Exception as err:
            print(err)    
        finally:
            self.conn.commit()
    #End Event fn

    #Groups fn
    def get_groups(self):
        df = pd.read_sql("SELECT * FROM groups", self.conn)
        return df.to_dict(orient = 'index')

    def get_group_by_id(self, group_id):
        qt = "SELECT * FROM groups WHERE group_id = ?"
        df = pd.read_sql(qt, self.conn,params={str(group_id)})
        return df.to_dict(orient = 'index')
    
    def get_group_by_name(self, group_name):
        qt = "SELECT * FROM groups WHERE group_name = ?"
        df = pd.read_sql(qt, self.conn, params={group_name})
        return df.to_dict(orient = 'index')

    def get_groups_by_event_id(self, event_id):
        qt = "SELECT * FROM groups WHERE event_id = ?"
        df = pd.read_sql(qt, self.conn,params={str(event_id)})
        return df.to_dict(orient = 'index')

    def add_group(self, temp_group_id, temp_event_id, temp_name, temp_total_points):
        qt = "INSERT INTO dbo.groups ([group_id],[event_id],[group_name],[total_points]) VALUES (?, ?, ?, ?)"
        data = (temp_group_id, temp_event_id, temp_name, temp_total_points)
        try:
            self.cursor.execute(qt, data)
            self.conn.commit()
        except Exception as err:
            print(err)

    #Deleting by just id or by other fields?
    def delete_group(self, temp_id):
        qt = "DELETE FROM dbo.groups WHERE group_id in (?)"
        try:
            self.delete_attendee_group_link_by_group(temp_id)
            self.cursor.execute(qt, temp_id)
            self.conn.commit()
        except Exception as err:
            print(err) 
    #Only used when delete_event is called for cascading delete
    def delete_group_by_event(self, temp_id):
        qt = "DELETE FROM dbo.groups WHERE event_id in (?)"
        try:
            self.delete_attendee_group_link_by_group(temp_id)
            self.cursor.execute(qt, temp_id)
            self.conn.commit()
        except Exception as err:
            print(err) 
    #With Points, add without
    def update_group_with_points(self, temp_group_id, temp_event_id, temp_name, temp_total_points = None):
        if temp_total_points is None:
            qt = "UPDATE groups SET event_id = ?, group_name = ? WHERE group_id = ?"
            data = (temp_event_id, temp_name, str(temp_group_id))
            try:
                self.cursor.execute(qt, data)
            except Exception as err:
                print(err)    
            finally:
                self.conn.commit()
        else:
            qt = "UPDATE groups SET event_id = ?, group_name = ?, total_points = ? WHERE group_id = ?"
            data = (temp_event_id, temp_name, temp_total_points, str(temp_group_id))
            try:
                self.cursor.execute(qt, data)
            except Exception as err:
                print(err)    
            finally:
                self.conn.commit()

    def update_group_points(self, temp_id, temp_points):
        qt = "UPDATE groups SET total_points = ? WHERE group_id = ?"
        data = (temp_points, str(temp_id))
        try:
            self.cursor.execute(qt, data)
        except Exception as err:
            print(err)    
        finally:
            self.conn.commit()


    #def update_group_without_points(self, temp_group_id, temp_event_id, temp_name):
    #   data = (temp_event_id, temp_name, str(temp_group_id))
    #    try:
    #        self.cursor.execute(qt, data)
     #   except Exception as err:
      #      print(err)    
       # finally:
        #    self.conn.commit()
    #End of Groups fn

    #Users fn
    def get_user(self):
        df = pd.read_sql("SELECT * FROM users", self.conn)
        return df.to_dict(orient = 'index')

    def get_user_by_id(self, user_id):
        qt = "SELECT * FROM users WHERE user_id = ?"
        df = pd.read_sql(qt, self.conn, params={str(user_id)})
        return df.to_dict(orient = 'index')

    def add_user(self, temp_user_id, temp_login_name, temp_user_password, temp_email, temp_firstname, temp_lastname, temp_access_id):
        qt = "INSERT INTO dbo.users ([user_id],[login_name],[user_password],[email],[firstname],[lastname], [access_id]) VALUES (?, ?, ?, ?, ?, ?, ?)"
        data = (temp_user_id, temp_login_name, temp_user_password, temp_email, temp_firstname, temp_lastname, temp_access_id)
        try:
            self.cursor.execute(qt, data)
            self.conn.commit()
        except Exception as err:
            print(err)

    def delete_user(self, temp_id):
        qt = "DELETE FROM dbo.users WHERE user_id in (?)"
        try:
            self.cursor.execute(qt, temp_id)
            self.conn.commit()
        except Exception as err:
            print(err)

    def update_user(self, temp_user_id, temp_login_name, temp_user_password, temp_email, temp_firstname, temp_lastname, temp_access_id):
        qt = "UPDATE users SET login_name = ?, user_password = ?, email = ?, firstname = ?, lastname = ?, access_id = ? WHERE user_id = ?"
        data = (temp_login_name, temp_user_password, temp_email, temp_firstname, temp_lastname, temp_access_id, str(temp_user_id))
        try:
            self.cursor.execute(qt, data)
        except Exception as err:
            print(err)    
        finally:
            self.conn.commit()
    #End of Users fn

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

    #Pointlog fn
    def get_pointlog(self):
        df = pd.read_sql("SELECT * FROM pointlog", self.conn)
        return df.to_dict(orient = 'index')

    def get_pointlog_by_user_id(self, user_id):
        qt = "SELECT * FROM pointlog WHERE user_id = ?"
        df = pd.read_sql(qt, self.conn, params={str(user_id)})
        return df.to_dict(orient = 'index')

    def get_pointlog_for_event(self, event_id):
        qt = "SELECT * FROM pointlog WHERE event_id = ?"
        df = pd.read_sql(qt, self.conn,params={str(event_id)})
        return df.to_dict(orient = 'index')

    def get_pointlog_for_group(self, group_id):
        qt = "SELECT * FROM pointlog WHERE group_id = ?"
        df = pd.read_sql(qt, self.conn,params={str(group_id)})
        return df.to_dict(orient = 'index')

    def add_pointlog(self, temp_pointlog_id, temp_user_id, temp_event_id, temp_attendee_id, temp_group_id, temp_log_date, temp_point_type, temp_point_change,temp_comment, temp_status):
        qt = "INSERT INTO dbo.pointlog ([pointlog_id],[user_id],[event_id],[attendee_id],[group_id],[log_date], [point_type], [point_change], [comment], [point_status]) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        data = (temp_pointlog_id, temp_user_id, temp_event_id, temp_attendee_id, temp_group_id, temp_log_date, temp_point_type, temp_point_change,temp_comment, temp_status)
        try:
            self.cursor.execute(qt, data)
            self.conn.commit()
        except Exception as err:
            print(err)
    
    def delete_pointlog(self, temp_id):
        qt = "DELETE FROM dbo.pointlog WHERE pointlog_id in (?)"
        try:
            self.cursor.execute(qt, temp_id)
            self.conn.commit()
        except Exception as err:
            print(err)

    def update_pointlog(self, temp_pointlog_id, temp_user_id, temp_event_id, temp_attendee_id, temp_group_id, temp_log_date, temp_point_type, temp_point_change,temp_comment, temp_status):
        qt = "UPDATE pointlog SET user_id = ?, event_id = ?, attendee_id = ?, group_id = ?, log_date = ?, point_type, point_change = ?, comment = ?, point_status = ?, WHERE pointlog_id = ?"
        data = (temp_user_id, temp_event_id, temp_attendee_id, temp_group_id, temp_log_date, temp_point_type, temp_point_change, temp_comment, temp_status, str(temp_pointlog_id))
        try:
            self.cursor.execute(qt, data)
        except Exception as err:
            print(err)    
        finally:
            self.conn.commit()

    def decline_pointlog(self, temp_id):
        self.delete_pointlog(temp_id)

    def accept_pointlog_status(self, temp_pointlog_id):
        qt = "UPDATE pointlog SET point_status = 1 WHERE pointlog_id = ?"
        data = (str(temp_pointlog_id))
        try:
            self.cursor.execute(qt, data)
        except Exception as err:
            print(err)    
        finally:
            self.conn.commit()

    def accept_pointlog(self, temp_pointlog_id, temp_attendee_id = None):
        if temp_attendee_id is None:
            qt1 = "SELECT point_change, group_id FROM pointlog WHERE pointlog_id = ?"
            qt2 = "SELECT total_points FROM groups WHERE group_id = ?"
            df1 = pd.read_sql(qt1, self.conn, params={str(temp_pointlog_id)})
            group = df1.loc[0].at["group_id"]
            df2 = pd.read_sql(qt2, self.conn, params={str(group)})
            points = df1.loc[0].at["point_change"]
            points += df2.loc[0].at["total_points"]
            self.accept_pointlog_status(temp_pointlog_id)
            qt3 = "UPDATE groups SET total_points = ? where group_id = ?"
            data = (points, str(group))
            try:
                self.cursor.execute(qt3, data)
            except Exception as err:
                print(err)    
            finally:
                self.conn.commit()
        else:
            print()

    #End of Pointlog fn

    #Attendee_Group_Link fn
    def get_attendee_group_link(self):
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

conn = ServerConn()

    
