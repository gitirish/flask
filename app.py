from flask import Flask ,url_for, render_template , request,redirect
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db=SQLAlchemy(app)
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content=db.Column(db.String(200),nullable=False)
    completed=db.Column(db.Integer,default=0)
    date_time=db.Column(db.Integer,default=datetime.utcnow)

    def __repr__(self):
        return '< Task %r >' % self.id

@app.route('/', methods=['POST','GET'])

def index():
    if request.method =='POST':
        task_content=request.form['content']
        new_task=Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except: 
            return "there is an issue"
    else:
      tasks=Todo.query.order_by(Todo.date_time).all()
      return render_template('index.html', title='Home Page', message='Hello, Flask!',tasks=tasks)

@app.route('/delete/<int:id>')  
def delete(id):
    task_to_delete=Todo.query.get_or_404(id) 
    try:
            db.session.delete(task_to_delete)
            db.session.commit()
            return redirect('/')
    except: 
            return "there is an issue" 
@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
     task=Todo.query.get_or_404(id)
     if request.method=='POST':
        task.content=request.form['content']
     
        try:
            db.session.commit()
            return redirect('/')
        except: 
            return "there is an issue"
     else:
          return render_template('update.html',task=task)     
if __name__=="__main__":
   
    app.run(debug=True)