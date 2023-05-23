from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SelectMultipleField, FileField,  SelectField
from wtforms.validators import InputRequired

class CSVUploads(FlaskForm):
    student_reg_file = FileField('Student Registration', validators=[FileRequired(), FileAllowed(['csv', 'xlsx'], 'CSV or Excel Files Only!')])
    lect_pref_file = FileField('Lecturer Preferences', validators=[FileRequired(), FileAllowed(['csv', 'xlsx'], 'CSV or Excel Files Only!')])

class CourseForm(FlaskForm):
    course_title = StringField('Course Title', validators=[InputRequired()])
    course_code = StringField('Course Code', validators=[InputRequired()])
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    time_preferences = SelectMultipleField('Time Preferences', choices=[('1', '01:00'),('2', '02:00'),('3', '03:00'),('4', '04:00'),('5', '05:00'),('6', '06:00'),('7', '07:00'),('8', '08:00'),('9', '09:00'), ('10', '10:00'), ('11', '11:00'), ('12', '12:00'), ('13', '13:00'), ('14', '14:00'), ('15', '15:00'), ('16', '16:00'), ('17', '17:00'), ('18', '18:00'), ('19', '19:00'), ('20', '20:00'), ('21', '21:00'), ('22', '22:00'), ('23', '23:00'), ('24', '24:00')], validators=[InputRequired()])
    

class ParameterForm(FlaskForm):
    population_size = SelectField('Population Size', choices=[('1', '1'),('2', '2'),('3', '3'),('4', '4'),('5', '5'),('6', '6'),('7', '7'),('8', '8'),('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20')], validators=[InputRequired()])
    p_crossover = StringField('Crossover')
    p_mutation = StringField('Mutation')
    max_generations = SelectField('Max Generations', choices=[('10', '10'),('11', '11'),('12', '12'),('13', '13'),('14', '14'),('15', '15'),('16', '16'),('17', '17'),('18', '18'), ('19', '19'), ('20', '20')], validators=[InputRequired()])
    optimal_fitness_score = SelectField('Optimal Fitness Score', choices=[('1000', 'Very Low Threshold'),('2000', 'Low Threshold'),('3000', 'Medium Threshold'),('4000', 'High Threshold'),('5000', 'Very High Threshold')], validators=[InputRequired()])
    max_runtime = SelectField('Max Runtime', choices=[('1', '1 hour'),('2', '2 hours'),('3', '3 hours'),('4', '4 hours'),('5', '5 hours'),('6', '6 hours'),('7', '7 hours'),('8', '8 hours'),('9', '9 hours'), ('10', '10 hours'), ('11', '11 hours'), ('12', '12 hours'), ('13', '13 hours'), ('14', '14 hours'), ('15', '15 hours'), ('16', '16 hours'), ('17', '17 hours'), ('18', '18 hours'), ('19', '19 hours'), ('20', '20 hours')], validators=[InputRequired()])
    
