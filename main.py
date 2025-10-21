from flask import Flask
from routes.p_condition_report import condition_bp
from routes.p_equipment_export import equipment_export_bp
from routes.p_index import index_bp
from routes.p_model_section import model_bp
from routes.p_analysis import analysis_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

app.register_blueprint(condition_bp)                #CONDITION REPORT PAGE
app.register_blueprint(equipment_export_bp)         #EQUIPMENT EXPORT PAGE
app.register_blueprint(index_bp)                    #INDEX (FIRST PAGE)
app.register_blueprint(model_bp)                    #MODEL (BRAND ANALYSIS LEVEL & SELECT MODEL TO GO FURTHER)
app.register_blueprint(analysis_bp)                 #ANALYSIS PAGE

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)