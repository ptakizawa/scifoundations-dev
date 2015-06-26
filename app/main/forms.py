from flask.ext.wtf import Form
from datetime import date
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField, SubmitField, FieldList, HiddenField, DateField
from wtforms_components import DateRange, TimeField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from ..models import Role, User, ThreadGoal


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

class EditProfileForm(Form):
	name = StringField('Real name', validators=[Length(0, 64)])
	location = StringField('Location', validators=[Length(0, 64)])
	abount_me = TextAreaField('About me')
	submit = SubmitField('Submit')
	
class EditProfileAdminForm(Form):
	email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
	username = StringField('Username', validators=[Required(), Length(1,64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Usernames must have only letters, numbers, dots or underscores')])
	confirmed = BooleanField('Confirmed')
	role = SelectField('Role', coerce=int)
	name = StringField('Real name', validators=[Length(0, 64)])
	location = StringField('Location', validators=[Length(0, 64)])
	about_me = TextAreaField('About me')
	submit = SubmitField('Submit')
	
	def __init__(self, user, *args, **kwargs):
		super(EditProfileAdminForm, self).__init__(*args, **kwargs)
		self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
		self.user = user
		
	def validate_email(self, field):
		if field.data != self.user.email and User.query.filter_by(email=field.data).first():
			raise ValidationError('Email already registered')
			
	def validate_username(self, field):
		if field.data != self.user.username and User.query.filter_by(username=field.data).first():
			raise ValidationError('Username already in use')
			
class SessionForm(Form):
	title = StringField('Session Title: ', validators=[Required(), Length(128)])
	pedagogy = SelectField('Pedagogy: ', choices=[('lecture', 'Lecture'),
												('lab', 'Lab'),
												('workshop', 'Workshop'),
												('team-based', 'Team-Based Learning')])
	thread = SelectField('Longitudinal Thread: ', choices=[('biochemistry', 'Biochemistry'),
														('cell-biology', 'Cell Biology'),
														('epidemiology-and-public-health', 'EPH'),
														('genetics', 'Genetics'),
														('pathology', 'Pathology'),
														('pharmacology', 'Pharmacology'),
														('physiology', 'Physiology'),
														('embryology', 'Embryology')])
	theme = SelectField('Theme: ', choices=[('building-a-body', 'Building a Body'),
											('cell-communication', 'Cell Communication'),
											('cell-energy', 'Cell Energy'),
											('epidemiology-and-public-health', 'Epidemiology and Public Health'),
											('fluids-and-gradients', 'Fluids and Gradients'),
											('gene-expression', 'Gene Expression'),
											('life-and-death-of-a-cell', 'Life and Death of a Cell')])
	date = DateField('Date: ', format='%m/%d/%Y')
	time = SelectField('Start Time: ', choices=[('8', '8 AM'),
												('9', '9 AM'),
												('10', '10 AM'),
												('11', '11 AM')])
	submit = SubmitField('Submit')
	
class ThreadGoalForm(Form):
	goal = TextAreaField('Thread Goal', validators = [Required()])
	thread = SelectField('Longitudinal Thread', choices=[('biochemistry', 'Biochemistry'),
														('cell-biology', 'Cell Biology'),
														('epidemiology-and-public-health', 'EPH'),
														('genetics', 'Genetics'),
														('pathology', 'Pathology'),
														('pharmacology', 'Pharmacology'),
														('physiology', 'Physiology'),
														('embryology', 'Embryology')])
	submit = SubmitField('Submit')
	
class EditThreadGoalForm(Form):
	goals = FieldList(TextAreaField('Thread Goal'), HiddenField('ID'))
	
class EditSessionForm(Form):
	session_id = HiddenField('ID')
	title = StringField('Session Title: ', validators=[Required(), Length(128)])
	pedagogy = SelectField('Pedagogy: ', choices=[('lecture', 'Lecture'),
												('lab', 'Lab'),
												('workshop', 'Workshop'),
												('team-based', 'Team-Based Learning')])
	thread = SelectField('Longitudinal Thread: ', choices=[('biochemistry', 'Biochemistry'),
														('cell-biology', 'Cell Biology'),
														('epidemiology-and-public-health', 'EPH'),
														('genetics', 'Genetics'),
														('pathology', 'Pathology'),
														('pharmacology', 'Pharmacology'),
														('physiology', 'Physiology'),
														('embryology', 'Embryology')])
	theme = SelectField('Theme: ', choices=[('building-a-body', 'Building a Body'),
											('cell-communication', 'Cell Communication'),
											('cell-energy', 'Cell Energy'),
											('epidemiology-and-public-health', 'Epidemiology and Public Health'),
											('fluids-and-gradients', 'Fluids and Gradients'),
											('gene-expression', 'Gene Expression'),
											('life-and-death-of-a-cell', 'Life and Death of a Cell')])
	date = DateField('Date: ', format='%m/%d/%Y')
	time = SelectField('Start Time: ', choices=[('8', '8 AM'),
												('9', '9 AM'),
												('10', '10 AM'),
												('11', '11 AM')])
	submit = SubmitField('Submit')
	
class VerbForm(Form):
	term = StringField('Verb: ', validators=[Required()])
	definition = TextAreaField('Definition: ')
	taxonomy = SelectField("Bloom's Level: ", choices=[('knowledge', 'Knowledge'),
														('comprehension', 'Comprehension'),
														('application', 'Application'),
														('analysis', 'Analysis'),
														('synthesis', 'Synthesis'),
														('evaluation', 'Evaluation')], default='knowledge')
	submit = SubmitField('Submit')
	
class LearningObjectiveForm(Form):
	who = SelectField('Select for whom is the learning objective: ', choices=[("", ""),
										('students', 'Students'),
										('residents', 'Residents'),
										('faculty', 'Faculty')])
	taxonomy = SelectField("Select the Bloom's level of the learning objective: ", choices=[("", ""),
														('knowledge', 'Knowledge'),
														('comprehension', 'Comprehension'),
														('application', 'Application'),
														('analysis', 'Analysis'),
														('synthesis', 'Synthesis'),
														('evaluation', 'Evaluation')])
	verb = SelectField("Select a verb at that Bloom's level: ", choices=[("", "")])
	content = TextAreaField('Do what: ')
	conditions = TextAreaField('Under what conditions: ')
	session_id = HiddenField('ID')
	submit = SubmitField('Submit')
	
class AddObjectiveToSessionForm(Form):
	objective_id = HiddenField('ID')
	theme = SelectField('Select a Theme', choices=[("","")])
	thread = SelectField('Or Select a Thread', choices=[("","")])
	session = SelectField("Select a session for the learning objective", choices=[("","First, select a theme or thread")])
	submit = SubmitField('Submit')
														 

