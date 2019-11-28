from datetime import datetime, timedelta ,date
import re
import time
import vlc
import threading

class alarm():
    time_diff=None
    
    
    def __init__(self,alarm_time,day,music_path):
        self.alarm_time=alarm_time
        self.day=day  # today=0,tommorow =1, 2days =2 # put 0 if you want default
        self.music_path=music_path
        self.cancel_alarm=False # if you want to cancel alarm set it name.cancel_alarm =True
        self.player=None
        self.diff_sec=self.time_diff_sec()
        
    def time_diff(self):
        self.alarm_time=self.alarm_time.strip()
        zero=timedelta(days=0,hours=0,minutes=0,seconds=0)
        
        def time_calc(d,t): # time formate 00:00:00 am
            date_today=str(date.today()+timedelta(days=d))
            time_format = datetime.strptime(date_today+' '+t,"%Y-%m-%d %I:%M:%S %p")
            diff=time_format-datetime.now()
            return diff
        form1=re.match('^\d{0,2}:\d{0,2}:\d{0,2}\s\w{2}$',self.alarm_time) #form 00:00:00 am
        form2=re.match('^\d{0,2}:\d{0,2}:\d{0,2}$',self.alarm_time)        #form 00:00:00
        
        if form1:
            dif= time_calc(self.day,self.alarm_time)
            if dif > zero:
                time_diff=dif
            else:
                time_diff=time_calc(self.day+1,self.alarm_time)
        elif form2:
            dif1=time_calc(self.day,self.alarm_time+' am')
            dif2=time_calc(self.day,self.alarm_time+' pm')
            if dif1 > zero:
                time_diff=dif1
            elif dif2 > zero:
                time_diff=dif2
            else:
                time_diff= time_calc(self.day+1,self.alarm_time+' am')
                
        return time_diff
    
    def time_diff_sec(self):
        differ=self.time_diff()
        differ_sec=differ.days*24*60*60+differ.seconds
        return differ_sec
    
    def cancel(self):
        self.cancel_alarm=True
        print('successfully cancelled')
    
    def start(self):
        def starting(time_sleep,path):
            time.sleep(time_sleep)
            if not self.cancel_alarm:
                self.player = vlc.MediaPlayer(path)
                self.player.play()
                print('alarm playing , wake up')
        th=threading.Thread(target=starting, args=(self.diff_sec,self.music_path))
        th.start()
        print('alarm successfully start after',self.time_diff())
    
    def stop(self): #stop playing music
        if self.player:
            self.player.stop()
            
    def pause(self): #pause playing music double pausing= play
        if self.player:
            self.player.pause()
            
    def snooz(self,timer_sec): # have snooth time in seconds
        self.stop()
        self.diff_sec=timer_sec
        self.start()
        print('snooz successfully after',timer_sec,'second')
        
            
            
        
                
        
         
                
# alarm(time,day,music_path)
al=alarm('9:23:00 pm',0,'/home/pi/Downloads/Alan-Walker-Faded.mp3')
al.start()
print('hi python lovers')       
     