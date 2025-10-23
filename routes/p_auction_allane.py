from flask import Blueprint, render_template, session
from programs.Auction_Allane_Scrape import auction_scrape

auction_allane_bp = Blueprint('auction_allane',
                        __name__,
                        template_folder='templates')

@auction_allane_bp.route("/allane_auction",methods=["GET","POST"])
def auction_allane():
    return render_template('allane_auction.html')