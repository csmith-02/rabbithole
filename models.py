from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):

    __tablename__='users' # This line is necessary because we cannot create table called 'user' as 'user' is a reserved word in postgres
                          # We create a table called 'users' instead
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255), nullable=False)
    user_email = db.Column(db.String(255), nullable=False)
    user_hashpw = db.Column(db.String(255), nullable=False) # Probably going to change this later as we should 
                                                            # Will have to hash password later

    def __repr__(self) -> str:
        return f'User {self.id}: {self.user_name}, {self.user_email}'