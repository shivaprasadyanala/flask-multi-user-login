from . import app
from .api import RegisterView, LoginView, AdminView, AgentView

app.add_url_rule('/register',
                 view_func=RegisterView.as_view('register_user'))
app.add_url_rule('/login', view_func=LoginView.as_view('login_user'))
app.add_url_rule('/admin', view_func=AdminView.as_view('get_admin'))
app.add_url_rule('/agent', view_func=AgentView.as_view('get_agent'))
