from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

user_community = db.Table(
  'user_community',
  db.Column('uc_id', db.Integer, primary_key=True),
  db.Column('user_id', db.Integer, db.ForeignKey('users.user_id')),
  db.Column('community_id', db.Integer, db.ForeignKey('community.community_id')),
)

class User(db.Model):

    __tablename__='users' # This line is necessary because we cannot create table called 'user' as 'user' is a reserved word in postgres
                          # We create a table called 'users' instead
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String, unique=True, nullable=False)
    user_email = db.Column(db.String, unique=True, nullable=False)
    user_pfpic = db.Column(db.String, nullable=True)
    user_hashpw = db.Column(db.String, nullable=False) # Probably going to change this later as we should 
                                                            # Will have to hash password later

    communities = db.relationship('Community', secondary=user_community, backref='users')

    def __repr__(self) -> str:
        return f'<User {self.id}, {self.user_name}, {self.user_email}>'
    
class Community(db.Model):
    community_id = db.Column(db.Integer, primary_key=True)
    community_name = db.Column(db.String, nullable=False)
    pfpic = db.Column(db.String, nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    def __repr__(self) -> str:
        return f'<Community {self.community_id} {self.community_name}, {self.owner_id}>'

class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_time_created = db.Column(db.DateTime, nullable=False)
    post_title = db.Column(db.String, nullable=False)
    post_image = db.Column(db.String, nullable=True)
    post_content = db.Column(db.Text, nullable=False)
    uc_id = db.Column(db.Integer, db.ForeignKey('user_community.uc_id'))

    def __repr__(self) -> str:
        return f'<Post {self.post_id}, {self.post_title}, {self.community_id}, {self.user_id}>'