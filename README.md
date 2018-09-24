# MyCarSpot For Ever

## How to use it

Require ``python3 --version```  >= 3.6.x

Install dependencies with: ```pip3 install -r requirements.txt```

Run with: ```python3 mycarspotforever --logins "login1:password1,login2:password2, ..."```

## How to change webdriver

For chrome get the webdriver for your platform here: http://chromedriver.chromium.org

For Firefox, get it here: https://github.com/mozilla/geckodriver/releases

You can use change de executed driver with: ```python3 mycarspotforever --driver "firefox" --driver_path "path/to/geckodriver" --logins "login1:password1,login2:password2, ..."```

And debug with GUI using the `--debu`g argument