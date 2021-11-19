from api.Conns.connection import ServerConn
import pandas as pd

class GroupConn(ServerConn):
    def __init__(self):
        super().__init__()

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
            self.delete_pointlog_by_group(temp_id)
            self.cursor.execute(qt, temp_id)
            self.conn.commit()
        except Exception as err:
            print(err) 
    #Only used when delete_event is called for cascading delete
     
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

    


    #def update_group_without_points(self, temp_group_id, temp_event_id, temp_name):
    #   data = (temp_event_id, temp_name, str(temp_group_id))
    #    try:
    #        self.cursor.execute(qt, data)
     #   except Exception as err:
      #      print(err)    
       # finally:
        #    self.conn.commit()
    #End of Groups fn

gc = GroupConn()