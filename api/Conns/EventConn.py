from api.Conns.connection import ServerConn
import pandas as pd

class EventConn(ServerConn):
    def __init__(self):
        super().__init__()
    
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
            self.delete_pointlog_by_event(temp_id)
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

ec = EventConn()