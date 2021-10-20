## Starting the Servers
- To start the backend server, run the startup script by entering `./startserver.sh`
  - You may need to give the script permission to run by entering the command `chmod +x startserver.sh`
  
  - Alternatively, you can run the commands in the script individually:
  
  ```
  python -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  flask run
  
  ```
- To start the front end cd into `/score-tracker-frontend` and enter the
command `yarn dev`
