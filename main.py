from flask import Flask, Blueprint
from routes.main_page import main_page_bp
from routes.p_auction_allane import auction_allane_bp
from routes.p_condition_report import condition_bp
from routes.p_equipment_export import equipment_export_bp
from routes.p_transport_prices import transport_price_bp
from routes.p_openlane import openlane_bp
from routes.p_partslink import partslink_bp


app = Flask(__name__) #This creates our web app

app.config['SECRET_KEY'] = 'mysecretkey'

logs_bp = Blueprint("logs", __name__)

@logs_bp.get("/logs")
def get_logs():
    with open("logs.txt") as f:
        return {"logs": f.read()}

app.register_blueprint(logs_bp)
app.register_blueprint(main_page_bp)
app.register_blueprint(auction_allane_bp)
app.register_blueprint(condition_bp)
app.register_blueprint(equipment_export_bp)
app.register_blueprint(transport_price_bp)
app.register_blueprint(openlane_bp)
app.register_blueprint(partslink_bp)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)