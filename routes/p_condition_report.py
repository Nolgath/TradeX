from flask import Blueprint, render_template, request, send_file
import os
from modules.ConditionReports import conditionreports

condition_bp = Blueprint(
    'condition_report',
    __name__,
    template_folder='../templates'
)

@condition_bp.route('/condition_report', methods=['GET', 'POST'])
def condition_report():
    if request.method == 'POST':
        user_input = request.form.get("user_input", "")
        vins = [v.strip() for v in user_input.splitlines() if v.strip()]
        conditionreports(vins)
        zip_path = 'ConditionReports.zip'
        if os.path.exists(zip_path):
            return send_file(
                zip_path,
                as_attachment=True,
                download_name="ConditionReports.zip",
                mimetype="application/zip"
            )
    return render_template('condition_reports.html')