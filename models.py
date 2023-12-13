from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import TIMESTAMP

db = SQLAlchemy()

user_community = db.Table(
  'user_community',
  db.Column('uc_id', db.Integer, primary_key=True),
  db.Column('user_id', db.Integer, db.ForeignKey('users.id'), unique=True),
  db.Column('community_id', db.Integer, db.ForeignKey('community.id'), unique=True),
)

class User(db.Model):

    __tablename__='users' 

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    pfpic = db.Column(db.String, nullable=True)
    hashpw = db.Column(db.String, nullable=False)

    communities = db.relationship('Community', secondary=user_community, backref='users')

    def __repr__(self) -> str:
        return f'<User {self.user_id}, {self.user_name}, {self.user_email}>'
    
class Community(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    subject = db.Column(db.String, nullable=False)
    pfpic = db.Column(db.String, nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self) -> str:
        return f'<Community {self.community_id}, {self.community_name}, {self.owner_id}>'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time_created = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=True)
    content = db.Column(db.Text, nullable=False)
    uc_id = db.Column(db.Integer, db.ForeignKey('user_community.uc_id'))
    owner = db.Column(db.String, db.ForeignKey('users.username'))
    community = db.Column(db.String, db.ForeignKey('community.name'), unique=True)

    def __repr__(self) -> str:
        return f'<Post {self.id}, {self.title}'
    
class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time_created = db.Column(TIMESTAMP, nullable=False)
    content = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('reply.parent_id'), nullable=True)
    __table_args__ = (db.UniqueConstraint('parent_id'),)