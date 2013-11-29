#Import libraries 
import os
import re
import random
import hashlib
import hmac
import logging
import json
from string import letters

import webapp2
import jinja2

from google.appengine.ext import db

#Defines a directory for template files
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
#Creates a  environment. 
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

#the secret is used for hashing passwords. 
#Should usually not be store in the code. 
secret = 'python'

#This function fetches a template and renders it with params and its parameters. 
def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

#takes a value, and the of that val. 
#and the hashed version of the secret word
def make_secure_val(val):
    return '%s|%s' % (val, hmac.new(secret, val).hexdigest())

#Making sure the value is valid. 
def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val

#The main handler of this blog. 
class BlogHandler(webapp2.RequestHandler):
    def write(self, *a, **kw): #Cover function to make tings more legible and faster.
        self.response.out.write(*a, **kw)
		
		#Renders templates. 
    def render_str(self, template, **params):
        params['user'] = self.user
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
	
	#Out write json text, uses json library. 
    def render_json(self, d):
        json_txt = json.dumps(d)
        self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
        self.write(json_txt)
	
	#Sets a cookie
    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))
	
	#Reads the cookie
    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))
	
	#Sets a cookie for
    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')
	
	#Check for user cookie, if exist store the user object. Is user logged in?
    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))

        if self.request.url.endswith('.json'): 
        #If user request url with .json return.
            self.format = 'json'  
        #Else return regular html. 
        else:
            self.format = 'html' 

#The root handler of my blogg. Renders a frontpage.html
class MainPage(BlogHandler):
  def get(self):
      self.render('frontpage.html')


#Makes salt
def make_salt(length = 5):
    return ''.join(random.choice(letters) for x in xrange(length))

#Make a password hash
def make_pw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)

#Verifies password
def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)

#Storing users. 
def users_key(group = 'default'):
    return db.Key.from_path('users', group)

#User objects.  
class User(db.Model):
    name = db.StringProperty(required = True)
    pw_hash = db.StringProperty(required = True)
    email = db.StringProperty()
	
	#decorator looks up a user by id
    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid, parent = users_key())
	
	#looks up user by name
    @classmethod
    def by_name(cls, name):
        u = User.all().filter('name =', name).get()
        return u
	
	#Creates password hash, and user object.  
    @classmethod
    def register(cls, name, pw, email = None):
        pw_hash = make_pw_hash(name, pw)
        return User(parent = users_key(),
                    name = name,
                    pw_hash = pw_hash,
                    email = email)

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.pw_hash):
            return u



# Defines the blog key for google datastore. 
def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)

#List of a properties for blog post. 
class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True) 

	#render blog entry, replaces new lines of input text into html line breaks. 
    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("post.html", p = self)

    def as_dict(self): #Dictionary representation of blogg post object. , for json.
        time_fmt = '%c'
        d = {'subject': self.subject,
             'content': self.content,
             'created': self.created.strftime(time_fmt),
             'last_modified': self.last_modified.strftime(time_fmt)}
        return d



class BlogFront(BlogHandler):
	#Gets post from googles datastore, listed after when the post was created. 
    def get(self):
        posts = greetings = Post.all().order('-created')
        #if the format is html, render front.html.
        if self.format == 'html': 
            self.render('front.html', posts = posts)
        #Else render Json, list of each object with as_dict function above. 
        else: 
            return self.render_json([p.as_dict() for p in posts])

class PostPage(BlogHandler):
	#looks up a particular post. 
    def get(self, post_id): 
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)
		
		#If post doesnt excist 404. 
        if not post: 
            self.error(404)
            return
        #if format html render html.     
        if self.format == 'html': 
            self.render("permalink.html", post = post)
       #elser render json. 
        else: 
            self.render_json(post.as_dict())
            
#Handler for new posts. 
class NewPost(BlogHandler):
    def get(self):
        if self.user:
            self.render("newpost.html")#if user is loged inn, render new-post.html
        else:
            self.redirect("/login")#else redirect user to login page. 

    def post(self):
        if not self.user:
            self.redirect('/blog')
		
		 #Gets subject from  newpost.html 
        subject = self.request.get('subject')
        #Gets content from newpost.html  
        content = self.request.get('content') 

        if subject and content:
            p = Post(parent = blog_key(), subject = subject, content = content)
            p.put()
            self.redirect('/blog')  #If content and subjects is present, post, 
            						#and redirect user to blog. 
        else:
        	 #Else show error, render newpost again. 
            error = "Emne og innhold, takk."
            self.render("newpost.html", subject=subject, content=content, error=error)

class Rot13(BlogHandler):
    def get(self):
    #Gets input string from rot13-form.html
        self.render('rot13-form.html') 

    def post(self):  
        rot13 = ''
        text = self.request.get('text')
        if text:
            rot13 = text.encode('rot13') 
		# If valid string, return rot13 result.
        self.render('rot13-form.html', text = rot13)
        
#Sets requirements for username. 
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$") 
def valid_username(username):
	#Checks if requirements is fulfilled. 
    return username and USER_RE.match(username) 

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class Signup(BlogHandler):
    #Renders signup-form.html when /signup is called.
    def get(self):
        self.render("signup-form.html") 
	#Takes in all user input. 
    def post(self): 
        have_error = False 
        #Gets user info from form. 
        self.username = self.request.get('username') 
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')

        params = dict(username = self.username,
                      email = self.email)
		#Checks if user info is valid, if not return error. 
        if not valid_username(self.username): 
            params['error_username'] = "Brukernavnet er ikke godkjent"
            have_error = True

        if not valid_password(self.password):
            params['error_password'] = "Passordet er ikke godkjent."
            have_error = True
        elif self.password != self.verify:
            params['error_verify'] = "Passordene matcher ikke"
            have_error = True

        if not valid_email(self.email):
            params['error_email'] = "E-posten er ikke godkjent"
            have_error = True

        if have_error:
            self.render('signup-form.html', **params)
        else:
            self.done()#This method is defined in Register Class. 

    def done(self, *a, **kw):
        raise NotImplementedError


class Register(Signup):
    def done(self):
        #make sure the user doesn't already exist
        u = User.by_name(self.username)
        if u:
            msg = 'Brukernavnet eksisterer, velg et annet'
            self.render('signup-form.html', error_username = msg)
        else:
            u = User.register(self.username, self.password, self.email)
            u.put()
			#Redirects user to / when a registration is complete. 
            self.login(u)
            self.redirect("/") 
            
#Called when a user submit a login. #renders login-form.   
#gets username, checks it with db. 
class Login(BlogHandler):
    
    def get(self):
        self.render('login-form.html'

      def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/blog')
        else:
            msg = 'Invalid logg inn'
            self.render('login-form.html', error = msg)


#Called when a user log out. The user gets re-directed to /.  
class Logout(BlogHandler):
    def get(self):
        self.logout()
        self.redirect('/')


#list to handle page requests. 
app = webapp2.WSGIApplication([('/', MainPage),
							   ('/rot13', Rot13),
                               ('/blog/?(?:.json)?', BlogFront), #optional ending i json
                               ('/blog/([0-9]+)(?:.json)?', PostPage), 
                               ('/blog/newpost', NewPost),
                               ('/signup', Register),
                               ('/login', Login),
                               ('/logout', Logout),
                               ],
                              debug=True)
