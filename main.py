from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy


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


    def __init__(self, title, post):
        self.title = title
        self.post = post


@app.route('/blog', methods=['POST', 'GET'])
def blog():

    post_id = request.args.get('id')
 
    if post_id:
        indiv_post = Blog.query.get(post_id)

        return render_template('indiv_post.html', indiv_post=indiv_post)
    else:    
        blogs = Blog.query.all()
        
        return render_template('blog.html', blogs=blogs )



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

        post_new = Blog(post_title, post_entry)


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


if __name__ == '__main__':
    app.run()