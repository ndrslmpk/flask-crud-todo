#!/bin/bash
printf "\n"
printf ">>>>>   START THE APP:\n"
printf "\n"
printf ">>>>>   SETS THE DEFAULT ENTRYPOINT OF THE FLASK APP TO app.py :\n"
printf "\n"
export FLASK_APP=app.py
printf ">>>>>   activates DEBUG MODE :\n"
printf "\n"
export FLASK_DEBUG=true
printf ">>>>>   starts server :\n"
printf "\n"
flask run