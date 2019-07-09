from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
#from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:root@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'zyxwvutsrqp2'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    post = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #pub_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, title, post, owner):
        self.title = title
        self.post = post
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'register', 'blog', 'add_user', 'index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')
def get_users():
    return User.query.all()

@app.route('/')
def index():

    return render_template('index.html', title="Blogz",users=get_users())

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    post_id = request.args.get('id')
    single_user_id = request.args.get('owner_id')


    if single_user_id:
        #indiv_post = Blog.query.get(post_id)
        owner = Owner_id.query.filter_by(username=single_user_id).first()
        blogs = Blog.query.filter_by(owner_id=owner_id).order_by.desc()
        return render_template('blog.html', title="Blogs " + blog_user, username=blog_user)
    #else:
        #if (single_user_id):
            #indiv_user = Blog.query.filter_by(owner_id=owner_id).all()
            #return render_template('blog.html', title="Blogs Your Uncle", blogs=blogs)
    #else:    
        #blogs = Blog.query.order_by(Blog.id).all()
        #return render_template('blog.html', title='Blogz', blog=blog)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/newpost')
        else:
            flash('You seem to be missing some information or info is incorrect', 'error') 
            
    return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def register():
    username_error = ""
    email_address_error = ""
    password_error = ""
    validate_password_error = ""

    if request.method == 'POST':
        username = request.form['username']
        #email = request.form['email']
        password = request.form['password']
        validate_password = request.form['verify_password']


        if not username.isalpha():
            username_error = "Not a valid user name!"
            username = ""
            return render_template('signup.html')

        if len(username) < 3 or len(username) > 20:
            flash('Invalid character count. Username must be more than 3 letters and less than 20.', 'error')
            username = ""
            return render_template('signup.html')
    
        if len(password) < 3 or len(password) > 20:
            flash('Password does not match requirements!', 'error')
            password = ""
            return render_template('signup.html')           

        if not password.isalpha():
            flash('Password does not match requirements!', 'error')
            password = ""
            return render_template('signup.html')

        if validate_password != password:
            flash('Passwords do not match!', 'error')
            password = ""
            validate_password = ""
            return render_template('signup.html')

        existing_user = User.query.filter_by(username=username).first()

        if not existing_user and not username_error and not password_error and not validate_password_error and not email_address_error:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            #session['username'] = username
            #flash('New user created. Happy blogging!')
            return redirect('/newpost')
        else:
            flash('There is already a user with this information')
            return render_template('signup.html')
    else:
        return render_template('signup.html')


def val_empty(x):
    if x:
        return True
    else:
        return False

@app.route('/newpost', methods=['POST', 'GET'])
def add_entry():
    if request.method == 'POST':
        title_error = ""
        entry_error = ""

        post_title = request.form['blog_title']
        post_entry = request.form['your_thoughts']
        owner = User.query.filter_by(username=session['username']).first()
        post_new = Blog(post_title, post_entry, owner)

        
        #blog = request.form['blog']
        #blog.append(blog)
        #db.session.add(blog)
        #db.session.commit()

        #blog = Blog.query.filter_by(owner=owner).all
        #return render_template('blog.html', title='build-a-blog', blog=blog)

        if val_empty(post_title) and val_empty(post_entry):
            db.session.add(post_new)
            db.session.commit()
            link = "/blog?id=" + str(post_new.id)
            return redirect(link)

        else:
            if not val_empty(post_title) and not val_empty(post_entry):
                title_error = "You have to give your thought a title!"
                entry_error = "You forgot to write down your thoughts!"
                return render_template('addnewpost.html', title_error=title_error, entry_error=entry_error)
            elif not val_empty(post_title):
                title_error  = "You have to give your thought a title!"
                return render_template('addnewpost.html', title_error=title_error)
            elif not val_empty(post_entry):
                entry_error = "You forgot to write down your thoughts!"
                return render_template('addnewpost.html', post_entry=post_entry)
    else:
        return render_template('addnewpost.html')

@app.route('/logout')
def logout():
    del session['username']
    flash('You have been logged out. Come back soon')
    return redirect('/blog')

if __name__ == '__main__':
    app.run()