
# __          _______  _____ _____ 
# \ \        / / ____|/ ____|_   _|
#  \ \  /\  / / (___ | |  __  | |  
#   \ \/  \/ / \___ \| | |_ | | |  
#    \  /\  /  ____) | |__| |_| |_ 
#     \/  \/  |_____/ \_____|_____|
#
# This is the file Web Server Gateway Interface It will forward all requests
# from the web server (Guicorn recommended) to the Python Flask framework which
# will handle the data exchange.
#
# Written by Team CCC
#
# Remember to set-up the systemctl file to auto-start the web server when the
# system boots
# For a Guicorn server:
# 
'''
    [Unit]
    Description=Gunicorn instance to serve a Flask Framework
    After=network.target
    
    [Service]
    User=<systemuser>
    Group=<systemgroup>
    WorkingDirectory=<Path to working directory>
    ExecStart=<Path to gunicorn>/gunicorn --workers 3 --log-file <Path to logs> --log-level DEBUG --bind localhost:5000 wsgi:app
    
    [Install]
    WantedBy=multi-user.target
'''


from server import app

if __name__ == "__main__":
    app.run()
