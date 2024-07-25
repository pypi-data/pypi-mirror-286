**Selenium-google-signin** helps to automate google signin via selenium.  
  
Once logged in, it saves the logged in information in a cache directory, which can be  
utilized the next time you need to log in to avoid typing.  
Don't worry, it doesn't save the username and password used to log in.

# Installation
`pip install selenium-google-signin`

# What it can do:
### You can use it as follows
```
# ./main.py 

from selenium_google_signin import launch_selenium
from selenium_google_signin import login_to_google

if __name__ == '__main__':
    driver = launch_selenium('/path/where/chromedriver')
    login_to_google(driver)
    driver.quit()
```

### You can store the ID and password in the environment beforehand.
```
$export GOOGLE_ID='Your ID'
$export GOOGLE_PWD='Your Password'

python ./main.py
```
or
```
cat >> .env << EOF
GOOGLE_ID='Your ID'
GOOGLE_PWD='Your Password'
EOF

python ./main.py
```
