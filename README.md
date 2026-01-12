Fitness and nutrition tracker
The purpose of this project was to help to learn how to create a fullstack application, back and front end.
For backend I used Python as that is what I am most comfortable with
For frontend I used React.

The goal was to create something that was simple where I could log my weight and create a custom template of the exercises that I do
I wanted to create something that had an authenticator for register and login as well.
A chart of the weight logged is created and can be viewed.
There is also a macro tracker for those that use it (I do not). I thought it would be a nice design challenge to create something like this.
Goals are also available to be tracked

app.py/ Main flask app and main backend
auth.py/ Authenticator, enables registration and logging in
goals.py/ Create and manage goals
templates.py/ Create, edit, and delete templates
workouts.py/ Log workouts. Workouts can be made into templates that can be reused on the day of so that they 
can be logged
weight.py/ Log weight into the website, creates graph of weight
models.py/ Database using SQLAlchemy

Next steps are to deploy onto Cloudflare and to make the Frontend look nicer.
I also want to make this on Android one day.
