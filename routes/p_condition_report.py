from flask import Blueprint, render_template, request, send_file
import os, time
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

        # run normally, but safer for long tasks
        try:
            conditionreports(vins)
        except Exception as e:
            return f"Error during processing: {e}", 500

        zip_path = 'ConditionReports.zip'

        # wait a few seconds in case of file system delay
        for _ in range(10):
            if os.path.exists(zip_path):
                break
            time.sleep(0.5)

        if os.path.exists(zip_path):
            return send_file(
                zip_path,
                as_attachment=True,
                download_name="ConditionReports.zip",
                mimetype="application/zip"
            )
        else:
            return "File not found after processing.", 404

    return render_template('condition_reports.html')
