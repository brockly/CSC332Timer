import time
from aiy.board import Board, Led
#would have to pass in values from user before the function is called
def pomodoro(study_session_time, break_time):
    study_session_time = int(study_session_time) * 60
    break_time = int(break_time)
    
    tts.say("Press Google Home button to start. Press Google Home button to stop")
    mins = 0
    
    #FIXME if statement to say if button on google home pressed, run the pomodoro timer
    while input != 'stop' or input != 'STOP':   #FIXME modify to button pressed.
        # Loop until we reach specified session time 
        while mins != study_session_time:
            print(">>>>>>>>>>>>>>>>>>>>>", mins)
            #FIXME HERE: RECORD SOUNDS IN SESSION
            
            time.sleep(60)
            mins += 1
            
            #FIXME if statement to say if button pressed again, stop/break
        
        time.sleep(break_time)
        #FIXME SOUND BREAK ALARM!
        #FIXME Mention amount of high volume sounds made
        #FIXME RECORD SOUNDS IN SESSION
        #FIXME if statement to say if button pressed again, stop/break