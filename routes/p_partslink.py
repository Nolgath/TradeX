from flask import Blueprint, render_template, request,session, send_file, send_from_directory
from modules.partslink import partslink
import pandas as pd
import os

partslink_bp = Blueprint('partslink',
                        __name__,
                        template_folder='templates')

@partslink_bp.route("/partslink",methods=["GET","POST"])
def partslink_bp_page():
    selected_country = None

    if "country" in request.form:
        session["country"] = request.form["country"]
        selected_country = request.form["country"]

    elif request.form.get("action") == "Extract":
        file = request.files['file']
        selected_country = session.get("country")
        if not file:
            return "No file uploaded", 400

        df = pd.read_excel(file)
        output = partslink(df,selected_country)

        return send_file(
            output,
            as_attachment=True,
            download_name=f"partslink_result.xlsx",
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    return render_template('partslink.html',
                           selected_country=selected_country)
