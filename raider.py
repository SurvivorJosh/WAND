import aiohttp, asyncio, os, sys, threading, requests, time, aiohttp, asyncio

try: 
    import tasksio
except:
    os.system('pip install tasksio')

os.system('cls')


def mainHeader(token):
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Accept': '*/*',
        'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json',
        'X-Context-Properties': 'eyJsb2NhdGlvbiI6IkpvaW4gR3VpbGQiLCJsb2NhdGlvbl9ndWlsZF9pZCI6Ijk4OTkxOTY0NTY4MTE4ODk1NCIsImxvY2F0aW9uX2NoYW5uZWxfaWQiOiI5OTAzMTc0ODgxNzg4NjgyMjQiLCJsb2NhdGlvbl9jaGFubmVsX3R5cGUiOjB9',
        'Authorization': token,
        'X-Super-Properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRmlyZWZveCIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJmciIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQ7IHJ2OjEwMi4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94LzEwMi4wIiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTAyLjAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTM2MjQwLCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==',
        'X-Discord-Locale': 'en-US',
        'X-Debug-Options': 'bugReporterEnabled',
        'Origin': 'https://discord.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://discord.com',
        'Cookie': '__dcfduid=21183630021f11edb7e89582009dfd5e; __sdcfduid=21183631021f11edb7e89582009dfd5ee4936758ec8c8a248427f80a1732a58e4e71502891b76ca0584dc6fafa653638; locale=en-US',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'TE': 'trailers',
    }
    
    
async def token_joiner(token, inv):
        
    headers = mainHeader(token)
    async with aiohttp.ClientSession() as s:
        async with s.post(f"https://canary.discord.com/api/v9/invites/{inv}", headers=headers, json={}) as res:
            if res.status in [200, 201, 204]:
                print(f"Successfully joined server")
            elif res.status == 429:
                f = await res.json()
                print(f'Ratelimited, retrying in {f["retry_after"]}')
            elif res.status == 403:
                print(f'Error, token was locked') 
            else:
                print(f"Error couldn't join lol")
                    
async def mass_join():
    print("Make sure you have valid tokens in tokens.txt")
    inv = input("server invite link -> ")
    try:
        ins = inv.split(".gg/")
        invite = ins[1]
    except:
        invite = inv
    tokens = open("tokens.txt", "r").readlines()
    async with tasksio.TaskPool(10_000) as pool:
        for token in tokens:
            tok = token.strip()
            await pool.put(token_joiner(tok, invite))
    
def spam(token, channel, message):
    url = 'https://discord.com/api/v9/channels/' + channel + '/messages'
    json = {"content": message, "tts": False}
    header = mainHeader(token)
    while True:
        try:
            r = requests.post(url, headers=header, json=json)
            

            if r.status_code == 429:
                print(f"Ratlimit")
                time.sleep(float(ratelimit['retry_after']))
            elif r.status_code == 200:
                print(f'Sent: {message}')

            elif r.status_code == 401:
                print(f'Invalid Token')
            elif r.status_code == 404:
                print('Not Found')
            elif r.status_code == 403:
                print(f'Token Doesnt Have Perms For This Channel!')
                
        except:
            pass
        
        
        
async def main():
    os.system('cls')
    print("""
    
                                                ___  
                                           (   ) 
     ___  ___  ___   .---.   ___ .-.     .-.| |  
    (   )(   )(   ) / .-, \ (   )   \   /   \ |  
     | |  | |  | | (__) ; |  |  .-. .  |  .-. |  
     | |  | |  | |   .'`  |  | |  | |  | |  | |  
     | |  | |  | |  / .'| |  | |  | |  | |  | |  
     | |  | |  | | | /  | |  | |  | |  | |  | |  
     | |  ; '  | | ; |  ; |  | |  | |  | '  | |  
     ' `-'   `-' ' ' `-'  |  | |  | |  ' `-'  /  
      '.__.'.__.'  `.__.'_. (___)(___)  `.__,'   
                                             
    
            [1] Token Joiner
            [2] Server Raider
            [x] Exit           
    """)
    choice = input("   >  ")
    
    if choice == "1":
        await mass_join()
        await asyncio.sleep(2)
        await main()
        
    elif choice == "2":
        print()
        print("Make sure you have tokens in tokens.txt for this to work")
        print()
        tokens = open("tokens.txt").read().split('\n')
        channel_id = input("channel id: ")
        message = input("message: ")
    
        def thread():
            for token in tokens:
                threading.Thread(target=spam, args=(token, channel_id, message,)).start()
                
        start = input("Press ENTER to start: ")
        start = thread()        
            
        await asyncio.sleep(2)
        await main()
        
    elif choice == "x" or choice == "X":
        print("Exiting....")
        await asyncio.sleep(1)
        os._exit(0)
    
    else:
        os._exit(0)    

    


if __name__ == "__main__":
    asyncio.run(main())            
        