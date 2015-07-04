from datetime import datetime
import time
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from . import db
from . import login_manager



@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	default = db.Column(db.Boolean, default=False, index=True)
	permissions = db.Column(db.Integer)
	users = db.relationship('User', backref='role', lazy='dynamic')

	@staticmethod
	def insert_roles():
		roles = {
			'Student': (Permission.FOLLOW |
						Permission.COMMENT, True),
			'Faculty': (Permission.FOLLOW |
						Permission.COMMENT |
						Permission.WRITE_ARTICLES |
						Permission.WRITE_QUESTIONS_AND_OBJECTIVES, False),
			'Thread_Leader': (Permission.FOLLOW |
								Permission.COMMENT |
								Permission.WRITE_ARTICLES |
								Permission.WRITE_QUESTIONS_AND_OBJECTIVES |
								Permission.WRITE_GOALS, False),
			'Course_Director': (Permission.FOLLOW |
								Permission.COMMENT |
								Permission.WRITE_ARTICLES |
								Permission.WRITE_QUESTIONS_AND_OBJECTIVES |
								Permission.WRITE_GOALS, False),
			'Administrator': (0xff, False)
			
		}
		
		for r in roles:
			role = Role.query.filter_by(name=r).first()
			if role is None:
				role = Role(name=r)
			role.permissions = roles[r][0]
			role.default = roles[r][1]
			db.session.add(role)
		db.session.commit()
		
	def __repr__(self):
		return '<Role %r>' % self.name

class User(UserMixin, db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(64), unique=True, index=True)
	username = db.Column(db.String(64), unique=True, index=True)
	password_hash = db.Column(db.String(128))
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	password_hash = db.Column(db.String(128))
	confirmed = db.Column(db.Boolean, default=False)
	name = db.Column(db.String(64))
	location = db.Column(db.String(64))
	about_me = db.Column(db.Text())
	member_since = db.Column(db.DateTime(), default=datetime.utcnow)
	last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
	objectives = db.relationship('LearningObjective', backref='author', lazy='dynamic')
	
	
	def __init__(self, **kwargs):
		super(User, self).__init__(**kwargs)
		if self.role is None:
			if self.email == current_app.config['SF_ADMIN']:
				self.role = Role.query.filter_by(permissions=0xff).first()
			if self.role is None:
				self.role = Role.query.filter_by(default=True).first()
	
	def can(self, permissions):
		return self.role is not None and (self.role.permissions & permissions) == permissions
		
	def is_administer(self):
		return self.can(Permission.ADMINISTER)
				
	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')
		
	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)
	
	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)
		
	def generate_confirmation_token(self, expiration=3600):
		s = Serializer(current_app.config['SECRET_KEY'], expiration)
		return s.dumps({'confirm': self.id})

	def confirm(self, token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except:
			return False
		if data.get('confirm') != self.id:
			return False
		self.confirmed = True
		db.session.add(self)
		return True
		
	def generate_reset_token(self, expiration=3600):
		s = Serializer(current_app.config['SECRET_KEY'], expiration)
		return s.dumps({'reset': self.id})
		
	def reset_password(self, token, new_password):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except:
			return False
		if data.get('reset') != self.id:
			return False
		self.password = new_password
		db.session.add(self)
		return True
		
	def generate_email_change_token(self, new_email, expiration=3600):
		s = Serializer(current_app.config['SECRET_KEY'], expiration)
		return s.dumps({'change_email': self.id, 'new_email': new_email})

	def change_email(self, token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except:
			return False
		if data.get('change_email') != self.id:
		    return False
		new_email = data.get('new_email')
		if new_email is None:
		    return False
		if self.query.filter_by(email=new_email).first() is not None:
		    return False
		self.email = new_email
		db.session.add(self)
		return True
		
	def ping(self):
		self.last_seen = datetime.utcnow()
		db.session.add(self)
		
	def __repr__(self):
		return '<User %r>' % self.username

class AnonymousUser(AnonymousUserMixin):
	def can(self, permissions):
		return False
		
	def is_administer(self):
		return False
		
	def is_authenticated(self):
	    return False
		
class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    WRITE_QUESTIONS_AND_OBJECTIVES = 0x08
    WRITE_GOALS = 0x10
    ADMINISTER = 0x80
	
class ThreadGoal(db.Model):
	__tablename__ = 'thread_goals'
	id = db.Column(db.Integer, primary_key=True)
	goal = db.Column(db.Text())
	thread = db.Column(db.String(64))
	objectives = db.relationship('LearningObjective', backref='thread_goal', lazy='dynamic')
	
	@classmethod
	def goal_dict(cls_obj):
		goal_dict = {}
		for thread in current_app.config['THREADS']:
			thread_goals = ThreadGoal.query.filter_by(thread=thread).all()
			goals = []
			for thread_goal in thread_goals:
				goal = {}
				goal['id'] = thread_goal.id
				goal['goal'] = thread_goal.goal
				goals.append(goal)
			goal_dict[thread] = goals
		return goal_dict
		
class ThemeGoal(db.Model):
	__tablename__ = 'theme_goals'
	id = db.Column(db.Integer, primary_key=True)
	goal = db.Column(db.Text())
	theme = db.Column(db.String(64))
	objectives = db.relationship('LearningObjective', backref='threme_goal', lazy='dynamic')

	@classmethod
	def goal_dict(cls_obj):
		goal_dict = {}
		for theme in current_app.config['THEMES']:
			theme_goals = ThemeGoal.query.filter_by(theme=theme).all()
			goals = []
			for theme_goal in theme_goals:
				goal = {}
				goal['id'] = theme_goal.id
				goal['goal'] = theme_goal.goal
				goals.append(goal)
			goal_dict[thread] = goals
		return goal_dict
				
class Session(db.Model):
	__tablename__ = 'sessions'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(128))
	pedagogy = db.Column(db.String(64))
	date_time = db.Column(db.DateTime)
	objectives = db.relationship('LearningObjective', backref='session', lazy='dynamic')
	questions = db.relationship('Question', backref='session', lazy='dynamic')
	thread = db.Column(db.String(64))
	theme = db.Column(db.String(64))
	integrated_course = db.Column(db.String(64))
	summary = db.Column(db.Text())
	
	@classmethod
	def sessions_dict(cls_obj):
		sessions_dict = {}
		session_list = []
		sessions = Session.query.all()
		for session in sessions:
			session_dict = {}
			session_dict['id'] = session.id
			session_dict['title'] = session.title
			session_dict['pedagogy'] = session.pedagogy
			session_dict['date-time'] = session.date_time.isoformat(' ')
			session_dict['thread'] = session.thread
			session_dict['theme'] = session.theme
			session_dict['integrated_course'] = session.integrated_course
			session_dict['summary'] = session.summary
			session_list.append(session_dict)
		sessions_dict['sessions'] = session_list
		sessions_dict['themes'] = current_app.config['THEMES']
		sessions_dict['threads'] = current_app.config['THREADS']
		return sessions_dict
		
	
class LearningObjective(db.Model):
	__tablename__ = 'learning_objectives'
	id = db.Column(db.Integer, primary_key=True)
	who = db.Column(db.String(64))
	verb = db.Column(db.String(32))
	content = db.Column(db.Text())
	conditions = db.Column(db.Text())
	free_form_version = db.Column(db.Text())
	taxonomy = db.Column(db.String(64))
	integrated_course = db.Column(db.String(64))
	session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'))	
	author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	thread_id = db.Column(db.Integer, db.ForeignKey('thread_goals.id'))
	theme_id = db.Column(db.Integer, db.ForeignKey('theme_goals.id'))
	questions = db.relationship('Question', backref='learning_objective', lazy='dynamic') 
	
class Question(db.Model):
	__tablename__ = 'questions'
	id = db.Column(db.Integer, primary_key=True)
        narrative = db.Column(db.Text())
	stem = db.Column(db.Text())
	correct_response = db.Column(db.String(128))
        distractor_1 = db.Column(db.String(128))
        distractor_2 = db.Column(db.String(128))
        distractor_3 = db.Column(db.String(128))
        image_url = db.Column(db.String(128))
	learning_objective_id = db.Column(db.Integer, db.ForeignKey('learning_objectives.id'))
	session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'))
	integrated_course = db.Column(db.String(64))
	
class Verb(db.Model):
	__tablename__ = 'verbs'
	id = db.Column(db.Integer, primary_key=True)
	term = db.Column(db.String(32))
	definition = db.Column(db.Text())
	taxonomy = db.Column(db.String(64))
	
	@classmethod
	def verbs_dict(cls_obj):
		verbs_dict = {}
		for taxonomy in current_app.config['BLOOMS_TAXONOMY']:
			verbs = Verb.query.filter_by(taxonomy=taxonomy).all()
			verb_list = []
			for verb in verbs:
				verb_dict = {}
				verb_dict['id'] = verb.id
				verb_dict['term'] = verb.term
				verb_dict['definition'] = verb.definition
				verb_dict['taxonomy'] = verb.taxonomy
				verb_list.append(verb_dict)
			verbs_dict[taxonomy] = verb_list
		return verbs_dict
	
login_manager.anonymous_user = AnonymousUser

		
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))
