from flask import Blueprint, render_template, request, send_file
from modules.Auction_Allane_Scrape import auction_scrape

auction_allane_bp = Blueprint('auction_allane',
                        __name__,
                        template_folder='templates')

@auction_allane_bp.route("/allane_auction",methods=["GET","POST"])
def auction_allane():
    if request.method == "POST":
        excel_file = auction_scrape()
        return send_file(
            excel_file,
            as_attachment=True,
            download_name="allane_auction.xlsx",
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    return render_template('allane_export.html')