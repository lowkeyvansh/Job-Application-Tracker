from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///applications.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    date_applied = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    notes = db.Column(db.Text, nullable=True)

class ApplicationForm(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired()])
    job_title = StringField('Job Title', validators=[DataRequired()])
    date_applied = StringField('Date Applied', validators=[DataRequired()])
    status = SelectField('Status', choices=[('Applied', 'Applied'), ('Interviewing', 'Interviewing'), ('Offer', 'Offer'), ('Rejected', 'Rejected')], validators=[DataRequired()])
    notes = TextAreaField('Notes')
    submit = SubmitField('Add Application')

db.create_all()

@app.route('/')
def home():
    applications = Application.query.all()
    return render_template('index.html', applications=applications)

@app.route('/add_application', methods=['GET', 'POST'])
def add_application():
    form = ApplicationForm()
    if form.validate_on_submit():
        new_application = Application(
            company_name=form.company_name.data,
            job_title=form.job_title.data,
            date_applied=form.date_applied.data,
            status=form.status.data,
            notes=form.notes.data
        )
        db.session.add(new_application)
        db.session.commit()
        flash('Application added successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('add_application.html', form=form)

@app.route('/update_application/<int:application_id>', methods=['GET', 'POST'])
def update_application(application_id):
    application = Application.query.get_or_404(application_id)
    form = ApplicationForm(obj=application)
    if form.validate_on_submit():
        application.company_name = form.company_name.data
        application.job_title = form.job_title.data
        application.date_applied = form.date_applied.data
        application.status = form.status.data
        application.notes = form.notes.data
        db.session.commit()
        flash('Application updated successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('add_application.html', form=form)

@app.route('/delete_application/<int:application_id>')
def delete_application(application_id):
    application = Application.query.get_or_404(application_id)
    db.session.delete(application)
    db.session.commit()
    flash('Application deleted successfully!', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
