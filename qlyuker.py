import os
import sys
import time
import random
import requests
from colorama import *
from datetime import datetime


import json



init(autoreset=True)

red = Fore.LIGHTRED_EX
yellow = Fore.LIGHTYELLOW_EX
green = Fore.LIGHTGREEN_EX
black = Fore.LIGHTBLACK_EX
blue = Fore.LIGHTBLUE_EX
white = Fore.LIGHTWHITE_EX
reset = Style.RESET_ALL

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.realpath(__file__))

# Construct the full paths to the files
data_file = os.path.join(script_dir, "data.txt")


class Qlyuker:
    
    def __init__(self):
        self.line = white + "~" * 50

        self.banner = f"""
        {blue}Secretniy {white}Qlyuker Auto Bot
        t.me/secretniy
        
        """

    # Clear the terminal
    def clear_terminal(self):
        # For Windows
        if os.name == "nt":
            _ = os.system("cls")
        # For macOS and Linux
        else:
            _ = os.system("clear")



    def log(self, msg):
        now = datetime.now().isoformat(" ").split(".")[0]
        print(f"{black}[{now}]{reset} {msg}{reset}")
    

    def main(self):
        def counter(start=0):
                    count = start

                    def increment():
                        nonlocal count
                        count += 1
                        return count

                    def reset(new_start=0):
                        nonlocal count
                        count = new_start

                    return increment, reset
        counter_instance = counter(0)  # 
        increment_func, reset_func = counter_instance
        while True:
            url_balance = 'https://qlyuker.io/api/auth/start'  # get
            url_sync = 'https://qlyuker.io/api/game/sync'
            url_daily = 'https://qlyuker.io/api/tasks/daily'
            url_buy = 'https://qlyuker.io/api/upgrades/buy'
            sesion1 = requests.Session()
            

            
            
            headers = {
    'Content-Length': '',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json; charset=UTF-8',
    'Sec-Ch-Ua-Platform': 'Android',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36'
    
}
            self.clear_terminal()
            print(self.banner)
            data = open(data_file, "r").read().splitlines()
            num_acc = len(data)
            self.log(self.line)
            self.log(f"{green}Numer of account: {white}{num_acc}")
            txt = increment_func()
            txt2 = txt
            
            for no, data in enumerate(data):
                self.log(self.line)
                self.log(f"{green}Account number: {white}{no+1}/{num_acc}")

                # Start bot
                try:
                    ######1 login to session
                    payload = {'startData':data}
                    get_info = sesion1.post(url_balance, headers=headers, json=payload)
                    if get_info.status_code == 200:
                        dataa = get_info.json()
                        username = dataa['user']['username']
                        currentCoins = dataa['user']['currentCoins']
                        currentEnergy = dataa['user']['currentEnergy']
                        maxEnergy = dataa['user']['maxEnergy']
                        coinsPerTap = dataa['user']['coinsPerTap']
                        minePerHour = dataa['user']['minePerHour']
                        dailystatus = dataa['user']['dailyReward']['claimed']

                        self.log(
                        f"{green}username: {white}{username}  {green}maxEnergy: {white}{maxEnergy} {green}Balance: {white}{currentCoins} {green}MinePerHour: {white}{minePerHour}"
                    )
                    else:
                        self.log(f"{red}Failed to get balance. Status code:{get_info.status_code}") 
                    
                    #####2
                    wait_time = 5
                    self.log(f"{yellow}Wait for {int(wait_time)} sec!")
                    time.sleep(wait_time)


                    #######3 tap all energy
                    self.log(f"{yellow}Trying to claim...")
                    if maxEnergy >= 50:
                        tap = currentEnergy / coinsPerTap
                        energy = tap * coinsPerTap   
                        timestamp_full = time.time()
                        timestamp = int(timestamp_full)
                        payload = {"currentEnergy":energy,"clientTime":timestamp,"taps":tap}
                        tapall = sesion1.post(url_sync, headers=headers, json=payload)
                        #print()
                        if tapall.status_code == 200:
                            data2 = tapall.json()
                            currentCoins2 = data2['currentCoins']
                            currentEnergy2 = data2['currentEnergy']
                            self.log(f"{white}Claim Mining: {green}Success")
                            self.log(
                                f"{green}Balance: {white}{currentCoins2}  {green}Mining Balance: +{white}{currentEnergy} {green}Energy: {white}{currentEnergy2}"
                            )
                        else:
                            self.log(f"{red}Claim Mining: Status code: {tapall.status_code}")
                    else:
                        self.log(f"{red}Claim Mining: {red}Error. Current energy {currentEnergy}")              
                    #####4 timer 5 sec
                    wait_time = 5
                    self.log(f"{yellow}Wait for {int(wait_time)} sec!")
                    time.sleep(wait_time)
                    ####5 sync +0 
                    self.log(f"{yellow}Trying to connect...")
                    timestamp_full = time.time()
                    timestamp = int(timestamp_full)
                    payload = {"currentEnergy":energy,"clientTime":timestamp,"taps":0}
                    connect = sesion1.post(url_sync, headers=headers, json=payload)
                    if connect.status_code == 200:
                            data3 = connect.json()
                            currentCoins3 = data3['currentCoins']
                            currentEnergy3 = data3['currentEnergy']
                            league = data3['league']
                            self.log(f"{white}Connect: {green}Success {green}Balance: {white}{currentCoins3} {green}Energy: {white}{currentEnergy3} {green}League: {white}{league}")
                    else:
                        self.log(f"{red}Connect Status code: {connect.status_code}")
                    
                    
                    ####6 daily
                    self.log(f"{yellow}Trying claim daily...")
                    if dailystatus == False:
                        daily = sesion1.post(url_daily, headers=headers)
                        if daily.status_code == 200:
                            data4 = daily.json()
                            claimed = data4['claimed']
                            reward = data4['reward']
    
                            self.log(f"{white}Claim Daily: {green}Success {green}Reward: {white}{reward}{green}Claimed: {white}{claimed} ")
                        else:
                            self.log(f"{red}Already climed: code: {daily.status_code}")
                    else:
                        self.log(f"{green}Daily already climed!!")
                        

                    
                    ######7
                    wait_time = 3
                    self.log(f"{yellow}Wait for {int(wait_time)} sec!")
                    time.sleep(wait_time)

                    #####9 buy
                    self.log(f"{yellow}Checing to buy BOOST...")
                    if txt2 >= 11 :
                        self.log(f"{yellow}Trying to buy BOOST...")
                        if currentCoins3 >= 500:
                            upgradesid = ['maxEnergy','coinsPerTap','promo1','special1','u1', 'u2', 'u3', 'u4', 'u5','u6', 'u7', 'u8','u9', 'u10', 'u11', 'u12', 'u13', 'u14', 'u15', 'u16', 'u17', 'u18', 'u19', 'u20', 'u21', 'u22', 'u23', 'u24', 'u25', 'u26', 'u27','u28']
                            rannge = random.randrange(11, 17)
                            for i in range(rannge):        
                                random_id = random.choice(upgradesid)
                                payload4 = {'upgradeId':random_id}
                                upgrade = sesion1.post(url_buy, headers=headers, json=payload4)
                                
                                if upgrade.status_code == 200:
                                    data5 = upgrade.json()
                                    price = data5['next']['next']['price']
                                    pribil = data5['next']['next']['increment']
                                    idupgrade = data5['upgrade']['id']
                                    currentCoinsafterbuy = data5['currentCoins']
                                    minePerHourafterbuy = data5['minePerHour']                            
                                    self.log(f"{white}Boost buy: {green}Success {white}ID boost: {green}{idupgrade} {white}Per hour: +{green}{pribil} {white}Price boost: {green}{price} {white}Balance: {green}{currentCoinsafterbuy}") 
                                    self.log(f"{white}ALL mine per hour: {green}{minePerHourafterbuy}")
                                    wait_time = 1
                                    self.log(f"{yellow}Wait for {int(wait_time)} sec!")
                                    time.sleep(wait_time)
                                    reset_func()
                                    
                                
                                else:
                                    if txt2 >= 11 :
                                        self.log(f"{white}Boost buy: {yellow}trying to buy..")
                                        wait_time = 2
                                        time.sleep(wait_time)
                                        reset_func()
                                    
                                        
                                    else:
                                        self.log(f"{white}Iteration: {green}{txt2} / 10{white} to try buy boost")   
                                        wait_time = 2
                                        self.log(f"{yellow}Wait for {int(wait_time)} sec!")
                                        time.sleep(wait_time)
                        else:
                            self.log(f"{yellow}Boost buy: {red}Error. Balance: {currentCoins3}")  
                            wait_time = 2
                            time.sleep(wait_time)
                    else:
                        self.log(f"{white}Iteration: {green}{txt2} / 10{white} to try buy boost")   
                        wait_time = 2
                        self.log(f"{yellow}Wait for {int(wait_time)} sec!")
                        time.sleep(wait_time)
                    print(self.banner)  
                except Exception as e:
                    self.log(f"{red}Error {e}")

            print()
            wait_time = 5 * 60
            self.log(f"{yellow}Wait for {int(wait_time/60)} minutes!")
            time.sleep(wait_time)


if __name__ == "__main__":
    try:
        qlyuker = Qlyuker()
        qlyuker.main()
    except KeyboardInterrupt:
        sys.exit()
