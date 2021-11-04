from api.Conns.connection import ServerConn
import pandas as pd

class UserConn(ServerConn):
    def __init__(self):
        super().__init__()

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