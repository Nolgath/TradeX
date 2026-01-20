from flask import Blueprint, render_template, request, send_file
import os
import pandas as pd
from modules.EquipmentExport import equipment_export

equipment_export_bp = Blueprint(
    'equipment_export',
    __name__,
    template_folder='../templates'
)
@equipment_export_bp.route("/equipment_export", methods=["GET", "POST"])            #EQUIPMENT EXPORT
def equipment_export_route():
    if request.method == "POST":
        user_input = request.form.get("user_input", "")
        vins = [v.strip() for v in user_input.splitlines() if v.strip()]
        # Call function and get Excel file
        excel_file = equipment_export(vins)
        # Send it to the user for download
        return send_file(
            excel_file,
            as_attachment=True,
            download_name="equipment_export.xlsx",
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    return render_template("equipment_export.html")