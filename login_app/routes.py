from . import app
from .api import RegisterView, LoginView

app.add_url_rule('/register',
                 view_func=RegisterView.as_view('register_user'))
app.add_url_rule('/login', view_func=LoginView.as_view('login_user'))
app.add_url_rule('/create', view_func=RegisterView.as_view('create'))
