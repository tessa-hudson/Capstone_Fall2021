from api.Conns.connection import ServerConn
import pandas as pd
import itertools

class AttendeeConn(ServerConn):
    def __init__(self):
        super().__init__()

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
            self.delete_pointlog_by_attendee(temp_id)
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

    def add_attendees(self, temp_ids, temp_firsts, temp_lasts):
        for (a, b, c) in zip(temp_ids, temp_firsts, temp_lasts):
            self.add_attendee(a, b, c)
    
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

ac = AttendeeConn()