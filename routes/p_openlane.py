from flask import Blueprint, render_template

openlane_bp = Blueprint('openlane',
                        __name__,
                        template_folder='templates')

@openlane_bp.route("/openlane",methods=["GET","POST"])
def openlane_bp_page():
    return render_template('openlane.html')