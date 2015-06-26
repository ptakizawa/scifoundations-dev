from datetime import datetime
from flask import render_template, session, redirect, url_for, flash, current_app, request
from flask.ext.login import current_user, login_required
from . import main
from .. import auth
from .forms import NameForm, ThreadGoalForm, EditThreadGoalForm, SessionForm, EditSessionForm, VerbForm, LearningObjectiveForm, AddObjectiveToSessionForm
from .. import db
from ..models import User, ThreadGoal, Session, Verb, LearningObjective
from ..decorators import admin_required, thread_leader_required
import json
from json import dumps

@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.name.data).first()
        if user is None:
            user = User(username = form.name.data)
            db.session.add(user)
            session['known'] = False
            if current_app.config['FLASKY_ADMIN']:
				send_email(current_app.config['FLASKY_ADMIN'], 'New User', 'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('.index'))
    return render_template('index.html',
                            form=form,
                            name=session.get('name'),
                            known=session.get('known', False),
                            current_time=datetime.utcnow())

@main.route('/user/<username>')
def user(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		abort(404)
	return render_template('user.html', user=user)
	
@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	form = EditProfileForm()
	if form.validate_on_submit():
		current_user.name = form.name.data
		current_user.location = form.location.data
		current_user.about_me = form.about_me.data
		db.session.add(user)
		flash("Your profile has been updated")
		return redirect(url_for('.user', username=current_user.username))
	form.name.data = current_user.name
	form.location.data = current_user.location
	form.about_me.data = current_user.about_me
	return render_template('edit_profile.html', form=form)
	
@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
	user = User.query.get_or_404(id)
	form = EditProfileAdminForm(user=user)
	if form.validate_on_submit():
		user.email = form.email.data
		user.username = form.username.data
		user.confirmed = form.confirmed.data
		user.role = Role.query.get(form.role.data)
		user.name = form.name.data
		user.location = form.location.data
		db.session.add(user)
		flash('The profile has been updated')
		return redirect(url_for('.user', username=user.username))
	form.email.data = user.email
	form.username.data = user.username
	form.confirmed.data = user.confirmed
	form.role.data = user.role_id
	form.name.data = user.name
	form.location.data = user.location
	form.about_me.data = user.about_me
	return render_template('edit_profile.html', form=form, user=user)
	
@main.route('/enter-thread-goal', methods=['GET', 'POST'])
@login_required
@thread_leader_required
def enter_thread_goal():
	form = ThreadGoalForm()
	if form.validate_on_submit():
		thread_goal = ThreadGoal.query.filter_by(goal=form.goal.data).first()
		if thread_goal is None:
			thread_goal = ThreadGoal(goal=form.goal.data, thread=form.thread.data)
			db.session.add(thread_goal)
		flash('The thread goal has been added.')
		return redirect(url_for('.enter_thread_goal'))
	return render_template('enter_thread_goal.html', form=form)
	
		
@main.route('/thread-goals')
def thread_goals():
	return render_template('thread_goals.html')
	
@main.route('/edit-thread-goals', methods=['GET', 'POST'])
@login_required
@thread_leader_required
def edit_thread_goals():
	if request.method == 'GET':
		return render_template('edit_thread_goals.html')
	if request.method == 'POST':
		f = request.form
		for key, value in f.iteritems():
			if key != 'csrf_token':
				thread_goal = ThreadGoal.query.filter_by(id=int(key)).first()
				if thread_goal.goal != value:
					thread_goal.goal = value
					db.session.add(thread_goal)
		flash('The thread goals have been updated.')
		return render_template('edit_thread_goals.html')
	
@main.route('/thread-goals-data')
def thread_goals_data():
	threads = ThreadGoal.goal_dict()
	return json.dumps(threads)
	
@main.route('/enter-session', methods=['GET', 'POST'])
@login_required
def enter_session():
	form = SessionForm()
	if request.method == 'GET':
		return render_template('enter_session.html', form=form)	
	if request.method == 'POST':
		title = form.title.data
		session = Session.query.filter_by(title=title).first()
		if session is None:
			session = Session()
			session.title = title
			session.pedagogy = form.pedagogy.data
			session.thread = form.thread.data
			session.theme = form.theme.data
			form_date = form.date.data
			time = form.time.data
			date_string = str(form_date).replace('-', ' ')
			session.date_time = datetime.strptime(date_string + " " + time, '%Y %m %d %H')
			session.integrated_course = "Scientific Foundations"
			db.session.add(session)
		flash('The session has been added.')
		return redirect(url_for('.enter_session'))
		
@main.route('/sessions')
def sessions():
	return render_template('sessions.html')
	
@main.route('/session-data')
def session_data():
	sessions = Session.sessions_dict()
	return json.dumps(sessions)
	
@main.route('/edit-session', methods=['GET', 'POST'])
def edit_session():
	form = EditSessionForm()
	if request.method == 'GET':
		return render_template('edit_session.html', form=form)
	if request.method == 'POST':
		session_id = form.session_id.data
		session = Session.query.filter_by(id=int(session_id)).first()
		if session is not None:
			session.title = form.title.data
			session.pedagogy = form.pedagogy.data
			session.thread = form.thread.data
			session.theme = form.theme.data
			form_date = form.date.data
			time = form.time.data
			date_string = str(form_date).replace('-', ' ')
			session.date_time = datetime.strptime(date_string + ' ' + time, '%Y %m %d %H')
			session.integrated_course = 'Scientific Foundations'
			db.session.add(session)
		flash('The session has been updated')
		return redirect(url_for('.edit_session'))
		
@main.route('/enter-verb', methods=['GET', 'POST'])
def enter_verb():
	form = VerbForm()
	if form.validate_on_submit():
		term = form.term.data
		verb = Verb.query.filter_by(term=term).first()
		if verb is None:
			verb = Verb()
			verb.term = form.term.data
			verb.definition = form.definition.data
			verb.taxonomy = form.taxonomy.data
			db.session.add(verb)
		else:
			verb.definition = form.definition.data
			verb.taxonomy = form.taxonomy.data
			db.session.add(verb)
		flash('Verb has been added')
		return redirect(url_for('.enter_verb'))
	return render_template('enter_verb.html', form=form)
	
@main.route('/enter-learning-objective', methods=['POST', 'GET'])
def enter_learning_objective():
	form = LearningObjectiveForm()
	if request.method == 'GET':
		return render_template('enter_learning_objective.html', form=form)
	if request.method == 'POST':
		objective = LearningObjective()
		objective.who = form.who.data
		selected_verb = Verb.query.filter_by(id=int(form.verb.data)).first()
		objective.verb = selected_verb.term
		objective.taxonomy = form.taxonomy.data
		objective.content = form.content.data
		objective.conditions = form.conditions.data
		objective.author_id = current_user.id
		db.session.add(objective)
		db.session.flush()
		print objective.id
		return redirect(url_for('.added_learning_objective', id=objective.id))
		
@main.route('/guide-to-writing-learning-objectives')
def guide_to_writing_learning_objectives():
	return render_template('guide_to_writing_learning_objectives.html')
		
@main.route('/added-learning-objective/<int:id>', methods=['POST', 'GET'])
def added_learning_objective(id):
	form = AddObjectiveToSessionForm()
	if request.method == 'GET':	
		objective = LearningObjective.query.filter_by(id=id).first()		
		form.objective_id.data = objective.id
		return render_template('added_learning_objective.html', form=form, objective=objective)
	if request.method == 'POST':
		objective = LearningObjective.query.filter_by(id=int(form.objective_id.data)).first()
		objective.session_id = int(form.session.data)
		db.session.add(objective)
		return redirect(url_for('.enter_learning_objective'))
		
@main.route('/diagram-of-a-learning-objective')
def diagram_of_a_learning_objective():
	return render_template('diagram_of_a_learning_objective.html')
		
				
		
@main.route('/verb-data')
def verb_data():
	verbs = Verb.verbs_dict()
	return json.dumps(verbs)
	
		
			
	
		


		
		