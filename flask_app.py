from app import create_app
from app.models import db
from werkzeug.middleware.proxy_fix import ProxyFix 


app = create_app('ProductionConfig')

app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1)

# creating the tables in the database
with app.app_context():
    # db.drop_all()
    db.create_all()
    
    
