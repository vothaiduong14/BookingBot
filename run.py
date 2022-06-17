from booking.booking import Booking

with Booking() as bot:
    bot.land_first_page()
    bot.change_currency(currency='VND')
    # bot.change_language(language='vi')
    bot.select_place_to_go(place_to_go = 'Phu Quoc')

    bot.select_dates(
        check_in_date = '2022-04-04', \
        check_out_date = '2022-04-11' \
    )
    bot.select_adults(2)
    bot.submit()
    bot.apply_filtration()
    bot.refresh() # A workaround to let our bot to grab data properly
    bot.report_results()
    # print("Exiting...")

    
