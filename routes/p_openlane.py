from flask import Blueprint, render_template, send_file, request
from modules.openlane import openlane_scrape

openlane_bp = Blueprint('openlane',
                        __name__,
                        template_folder='templates')

@openlane_bp.route("/openlane",methods=["GET","POST"])
def openlane_bp_page():
    if request.method == "POST":
        excel_file = openlane_scrape()
        return send_file(
            excel_file,
            as_attachment=True,
            download_name="equipment_export.xlsx",
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    return render_template('openlane.html')