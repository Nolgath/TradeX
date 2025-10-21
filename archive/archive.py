# def scheduler_task():
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(download_excel_stock, 'cron', hour=6, minute=0)  # runs every day at 06:00
#     scheduler.add_job(download_excel_sales, 'cron', hour=6, minute=5)  # runs every day at 06:00
#     scheduler.start()
# scheduler_task()