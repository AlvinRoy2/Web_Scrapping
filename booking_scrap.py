from playwright.sync_api import sync_playwright
import pandas as pd


def main():
    
    with sync_playwright() as p:
        
        # IMPORTANT: Change dates to future dates, otherwise it won't work
        checkin_date = '2024-04-13'
        checkout_date = '2024-04-14'
        
        page_url = f'https://www.booking.com/searchresults.en-us.html?checkin={checkin_date}&checkout={checkout_date}&selected_currency=USD&ss=Paris&ssne=Paris&ssne_untouched=Paris&lang=en-us&sb=1&src_elem=sb&src=searchresults&dest_type=city&group_adults=1&no_rooms=1&group_children=0&sb_travel_purpose=leisure'
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto('https://www.booking.com')

        # page.goto(page_url, timeout=60000)
        page.locator('//*[@id=":re:"]').fill('Paris')    
            # Click search button
        page.locator('#indexsearch > div.hero-banner-searchbox > div > form > div.ffb9c3d6a3.c9a7790c31.e691439f9a > div.e22b782521.d12ff5f5bf > button').click()


            # Wait for search results page to load
        page.wait_for_load_state()

        hotels = page.locator('//div[@data-testid="property-card"]').all()
        print(f'There are: {len(hotels)} hotels.')

        hotels_list = []
        for hotel in hotels:
            hotel_dict = {}
            hotel_dict['hotel'] = hotel.locator('//div[@data-testid="title"]').inner_text()
            hotel_dict['price'] = hotel.locator('//*[@id="bodyconstraint-inner"]/div[2]/div/div[2]/div[3]/div[2]/div[2]/div[3]/div[3]/div[1]/div[2]/div/div[3]/div[2]/div/div[1]/span/div/div/span[1]')
            hotel_dict['score'] = hotel.locator('//div[@data-testid="review-score"]/div[1]').inner_text()
            hotel_dict['avg review'] = hotel.locator('//div[@data-testid="review-score"]/div[2]/div[1]').inner_text()
            hotel_dict['reviews count'] = hotel.locator('//div[@data-testid="review-score"]/div[2]/div[2]').inner_text().split()[0]

            hotels_list.append(hotel_dict)
        
        df = pd.DataFrame(hotels_list)
        df.to_excel('hotels_list.xlsx', index=False) 
        df.to_csv('hotels_list.csv', index=False) 
        browser.close()

if __name__ == '__main__':
    main()
