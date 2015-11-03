from time import gmtime, strftime, time
import datetime
import sqlite3 as sql
import plugins.pluginapi


class Plugin(plugins.pluginapi.BasicPlugin):
    def __init__(self, bot, config):
        name = 'logs'
        desc = 'Saves logs'
        plugins.pluginapi.BasicPlugin.__init__(self, name, desc, config, bot.connection)
        
        self.db = sql.connect('logs.db')
        with self.db: self.db.row_factory = sql.Row
        
        self.register_command('lastmessage', self.get_lastmessage)
        self.register_command('lastjoined', self.get_lastjoined)
        
    
    def on_message(self, msg, usr):
        try:
            # Insert logs into database
            with self.db:
                cur = self.db.cursor()
                cur.execute("INSERT INTO Logs (user, message, time) VALUES (?, ?, ?)", (usr, msg, int(time())))
            
            print(strftime("[%Y-%m-%d %H:%M:%S]", gmtime()) + " <%s> %s" % (usr, msg))
        except:
            print("Woops! %s" % ("[%s] <%s> %s" % (datetime.fromtimestamp(time()), usr, msg)))
    
    def on_userjoin(self, usr):
        # Insert logs into database
        with self.db:
            cur = self.db.cursor()
            cur.execute("INSERT INTO JoinMessages (user, time) VALUES ('%s', %s)" % (usr, int(time())))
        
        print(strftime("[%Y-%m-%d %H:%M:%S]", gmtime()) + " %s has joined." % (usr))
    
    def on_userquit(self, usr):
        # Insert logs into database
        with self.db:
            cur = self.db.cursor()
            cur.execute("INSERT INTO LeaveMessages (user, time) VALUES ('%s', %s)" % (usr, int(time())))
        
        print(strftime("[%Y-%m-%d %H:%M:%S]", gmtime()) + " <%s> has quit." % (usr))
    
    def get_lastmessage(self, usr, cmd):
        try:
            if len(cmd) > 1:
                user = cmd[1]
                print("Getting last message of %s." % user)
                
                with self.db:
                    cur = self.db.cursor()
                    cur.execute("SELECT * FROM Logs WHERE `user` = \"%s\"" % user)
                    
                    rows = cur.fetchall()
                    
                    highest_row = {"id": 0, "user": "user", "message": " ", "time": 0}
                    
                    for row in rows:
                        #print("[%s] <%s> %s" % (row["time"], row["user"], row["message"]))
                        if row["time"] > highest_row["time"]:
                            highest_row = row
                    
                    if highest_row["id"] != 0:
                        self.send_notice("[%s] <%s> %s" % (datetime.datetime.fromtimestamp(highest_row["time"]), highest_row["user"],
                                                        highest_row["message"]), usr)
                    else:
                        self.send_notice("%s never spoke on this channel!" % user, usr)
                else:
                    print("Getting last message.")
            
                    with self.db:
                        cur = self.db.cursor()
                        cur.execute("SELECT * FROM Logs")
                        
                        rows = cur.fetchall()
                        
                        highest_row = {"id": 0, "user": "user", "message": " ", "time": 0}
                        
                        for row in rows:
                            #print("[%s] <%s> %s" % (row["time"], row["user"], row["message"]))
                            if row["time"] > highest_row["time"]:
                                highest_row = row
                        
                        if highest_row["id"] != 0:
                            self.send_msg("[%s] <%s> %s" % (datetime.datetime.fromtimestamp(highest_row["time"]), highest_row["user"],
                                                            highest_row["message"]), self.channel)
                        else:
                            self.send_msg("There are no logs on this channel!", self.channel)
        except:
            self.send_msg("Sorry, an error occurred.", self.channel)
                    
    
    def get_lastjoined(self, usr, cmd):
        try:
            if len(cmd) > 1:
                user = cmd[1]
                print("Getting last joining time of %s." % user)
                
                with self.db:
                    cur = self.db.cursor()
                    cur.execute("SELECT * FROM JoinMessages WHERE `user` = ?", [user])
                    
                    rows = cur.fetchall()
                    
                    highest_row = {"id": 0, "user": "user", "time": 0}
                    
                    for row in rows:
                        #print("[%s] <%s> %s" % (row["time"], row["user"], row["message"]))
                        if row["time"] > highest_row["time"]:
                            highest_row = row
                    
                    if highest_row["id"] != 0:
                        self.send_msg("%s joined on: %s" % (highest_row["user"], datetime.datetime.fromtimestamp(highest_row["time"])),
                                      self.channel)
                    else:
                        self.send_msg("%s never joined this channel!" % user, self.channel)
                        
            else:
                print("Getting last user joined")
                
                with self.db:
                    cur = self.db.cursor()
                    cur.execute("SELECT * FROM JoinMessages")
                    
                    rows = cur.fetchall()
                    
                    highest_row = {"id": 0, "user": "user", "message": " ", "time": 0}
                    
                    for row in rows:
                        #print("[%s] <%s> %s" % (row["time"], row["user"], row["message"]))
                        if row["time"] > highest_row["time"]:
                            highest_row = row
                    
                    if highest_row["id"] != 0:
                        self.send_msg("%s joined on: %s" % (highest_row["user"], datetime.datetime.fromtimestamp(highest_row["time"])),
                                      self.channel)
                    else:
                        self.send_msg("There are no join logs on this channel!", self.channel)
        except:
            self.send_msg("Sorry, an error occurred.", self.channel)