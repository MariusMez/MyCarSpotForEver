# MyCarSpot For Ever
Automatically confirm that you need your car spot (https://mycarspot.fr)

## How to use it

Require ```python3 --version```  >= 3.6.x

Install dependencies with: ```pip3 install -r requirements.txt```

Run with: ```python3 mycarspotforever --logins "login1:password1,login2:password2, ..."```

## How to change webdriver
*(included version is for MacOsX)*

For chrome get the webdriver for your platform here: http://chromedriver.chromium.org

For Firefox, get it here: https://github.com/mozilla/geckodriver/releases

You can use change de executed driver with: ```python3 mycarspotforever --driver "firefox" --driver_path "path/to/geckodriver" --logins "login1:password1,login2:password2, ..."```

And debug with GUI using the `--debug` argument

## Cron

Tous les lundi matin à 11h30: ```11 30 * * 1 python3 mycarspotforever --logins "login1:password1,login2:password2, ..."```
