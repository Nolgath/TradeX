from flask import Flask #This is the library that we will use to create our web app
from routes.main_page import main_page_bp
from routes.p_auction_allane import auction_allane_bp
from routes.p_condition_report import condition_bp
from routes.p_equipment_export import equipment_export_bp

app = Flask(__name__) #This creates our web app

app.config['SECRET_KEY'] = 'mysecretkey'

app.register_blueprint(main_page_bp)
app.register_blueprint(auction_allane_bp)
app.register_blueprint(condition_bp)
app.register_blueprint(equipment_export_bp)

if __name__ == '__main__':
    app.run(debug=True)