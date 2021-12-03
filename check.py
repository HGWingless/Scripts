# Written by Wingless 20211203
# Checks omocat every 30 seconds to see if it doesn't redirect to the maint page.
# I'm assuming that the home page is NOT /password, because that wouldn't make sense based on its use
# Can be repurposed by changing the below variables
import requests
import time
website = 'https://www.omocat-shop.com'
fail_page = 'https://www.omocat-shop.com/password'

x = requests.get(website)
while x.url == fail_page:
    print(f'Trying {website}, Got {x.url}, Still down...')
    time.sleep(30)
    x = requests.get(website)