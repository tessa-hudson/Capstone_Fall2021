from api.Conns.connection import ServerConn
import pandas as pd

class PointlogConn(ServerConn):
    def __init__(self):
        super().__init__()
    
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

    def add_pointlog(self, temp_pointlog_id, temp_event_id, temp_attendee_id, temp_group_id, temp_log_date, temp_point_type, temp_point_change,temp_comment, temp_status, temp_username):
        qt = "INSERT INTO dbo.pointlog ([pointlog_id],[event_id],[attendee_id],[group_id],[log_date], [point_type], [point_change], [comment], [point_status], [user_name]) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        data = (temp_pointlog_id, temp_event_id, temp_attendee_id, temp_group_id, temp_log_date, temp_point_type, temp_point_change,temp_comment, temp_status, temp_username)
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

    def update_pointlog(self, temp_pointlog_id, temp_event_id, temp_attendee_id, temp_group_id, temp_log_date, temp_point_type, temp_point_change,temp_comment, temp_status, temp_username):
        qt = "UPDATE pointlog SET event_id = ?, attendee_id = ?, group_id = ?, log_date = ?, point_type, point_change = ?, comment = ?, point_status = ?, user_name = ?, WHERE pointlog_id = ?"
        data = (temp_event_id, temp_attendee_id, temp_group_id, temp_log_date, temp_point_type, temp_point_change, temp_comment, temp_status, temp_username, str(temp_pointlog_id))
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
            self.update_group_points(group, int(points))
        else:
            qt1 = "SELECT point_change, attendee_id FROM pointlog WHERE pointlog_id = ?"
            qt2 = "SELECT total_points FROM attendee_group_link WHERE attendee_id = ?"
            df1 = pd.read_sql(qt1, self.conn, params={str(temp_pointlog_id)})
            attendee = df1.loc[0].at["attendee_id"]
            df2 = pd.read_sql(qt2, self.conn, params={str(attendee)})
            points = df1.loc[0].at["point_change"]
            points += df2.loc[0].at["total_points"]
            self.accept_pointlog_status(temp_pointlog_id)
            self.update_pointlog_AGLext(attendee, int(points))

    #End of Pointlog fn

pc = PointlogConn()