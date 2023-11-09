from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

user_community = db.Table('user_community', 
    db.column('user_id', db.Integer, db.ForeignKey('users.user_id')),
    db.column('community_id', db.Integer, db.ForeignKey('community.community_id')),
    db.Column('is_owner', db.bool)
)

class User(db.Model):

    __tablename__='users' # This line is necessary because we cannot create table called 'user' as 'user' is a reserved word in postgres
                          # We create a table called 'users' instead
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255), unique=True, nullable=False)
    user_email = db.Column(db.String(255), unique=True, nullable=False)
    user_pfpic = db.Column(db.String(255), nullable=True)
    user_hashpw = db.Column(db.String(255), nullable=False) # Probably going to change this later as we should 
                                                            # Will have to hash password later
    db.relationship('Community', secondary=user_community, backref='communities')

    def __repr__(self) -> str:
        return f'User {self.id}: {self.user_name}, {self.user_email}'
    
class Community(db.Model):
    community_id = db.Column(db.Integer, primary_key=True)
    community_name = db.Column(db.String(255), nullable=False)
    picture = db.Column(db.String(255), nullable=True)

    db.relationship('User', secondary=user_community, backref='users')

class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    post_time_created = db.Column(db.DateTime, nullable=False)
    post_title = db.Column(db.String(255), nullable=True)
    post_image = db.Column(db.String(255), nullable=True)
    post_content = db.Column(db.Text, nullable=True)
    community_id = db.Column(db.Integer, db.ForeignKey('user_community.community_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user_community.user_id'))
    