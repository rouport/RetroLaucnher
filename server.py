from flask import Flask
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode
import os, fnmatch
import subprocess

app = Flask(__name__)
ask = Ask(app, "/")

def get_headlines():
    return "foo" 

@app.route('/')
def homepage():
    return "Nimesh is a bitch"

@ask.launch
def start_skill():
    welcome_message = 'Welcome to retro launcher, which game would you like to launch?'
    return question(welcome_message)

@ask.intent("YesIntent")
def share_headlines():
    headlines = 'Mike Hawk Burns'
    headline_msg = 'The current world news headlines are {}'.format(headlines)
    return statement(headline_msg)

@ask.intent("NoIntent")
def no_intent():
    bye_text = 'ok, let me know when you do'
    return statement(bye_text)

@ask.intent("LaunchIntent", mapping={'game': 'game'})
def launch_game(game):
    games = find(game,'/home/pi/RetroPie/roms')
    if len(games) == 1:
        command = launchBuilder(games[0][0],games[0][2])
        os.system(command)
        return statement('Launching {}.'.format(games[1]))
    elif len(games) > 1:
        session.attributes['games'] = games
        responsegames = ''
        count = 1
        for elem in games:
            responsegames += 'number ' + str(count) + ' ' + elem[1] + ' for the ' + elem[2] + ' '
            count += 1
        return question('I found multiple games of that name. Would you like to play {}?'.format(responsegames))
    else:
        return statement('I did not find any games of the name {}'.format(game))

@ask.intent("NumberIntent", mapping={'number': 'number'})
def launch_number(number):
    games = session.attributes.get('games')
    gameInfo = games[number - 1]
    command = launchBuilder(gameInfo[0],gameInfo[2])
    subprocess.call(command)
    

def launchBuilder(path, console):
    command = '/opt/retropie/supplementary/runcommand/runcommand.sh 0 _SYS_ ' + console +' \'' + path + '\''
    print(command)
    return command



def find(pattern, path):
    result = []
    pattern = pattern.replace(" ","*")
    pattern = '*' + pattern + '*'
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name.lower(), pattern.lower()):
                path = os.path.join(root, name)
                parent = os.path.basename(os.path.dirname(path))
                result.append((path,name,parent))
    return result
    
if __name__ == '__main__':
    app.run(debug=True)