from flask import Blueprint, render_template, request, send_file, session, send_from_directory
import os
from modules.Transport_Price_Input import transport_price_input
import pandas as pd

transport_price_bp = Blueprint(
    'transport_price',
    __name__,
    template_folder='../templates'
)

@transport_price_bp.route('/transport_price', methods=['GET', 'POST'])
def transport_price():
    df = None
    open("logs.txt", "w", encoding='utf-8').close()
    logs = []

    if request.method == 'POST':
        if 'user' in request.form and 'password' in request.form:
            session['user'] = request.form['user']
            session['password'] = request.form['password']
            session['user_done'] = True

        elif 'file' in request.files:
            f = request.files['file']
            df = pd.read_excel(f)
            # retrieve credentials from session
            user = session.get('user')
            password = session.get('password')

            if user and password:
                logs = transport_price_input(df, user, password)
            else:
                print("User or password missing in session")

    return render_template('transport_prices.html', df=df, logs=logs)

@transport_price_bp.route('/download_template')
def download_template():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_dir = os.path.join(base_dir, '../files_templates')
    file_name = 'template_prices_transport.xlsx'
    return send_from_directory(file_dir, file_name, as_attachment=True)
