import subprocess,keyboard,os,sys,ctypes,time

GAME_PATH = r"C:\Riot Games\League of Legends\Game\League of Legends.exe"
VERSION = 1.0

def main():

    if not(is_admin()):
        print("Please run the script as administrator. Powershell cannot add firewall rules without it.")
        print("Closing in 3s.."); time.sleep(3); sys.exit()

    if not(checkPath(GAME_PATH)): 
        print("Game not found in default location."); # will later add OS directory selection.
        print("Closing in 3s.."); time.sleep(3); sys.exit()

    # selected location
    print(GAME_PATH + " exists.\n")

    # Make firewall rule (disabled by default, till the user selects the block option)
    createRule()
    
    print("Welcome to the League Loading Pauser!\n\nPlease select an option: \n")
    print("Shift + F1: Block loading\nShift + F2: Unblock loading\nShift + F3. Exit\n")


    keyboard.add_hotkey('shift+F1', block)
    keyboard.add_hotkey('shift+F2', unblock)
    keyboard.add_hotkey('shift+F3', close)
    
    keyboard.wait()




def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except AttributeError:
        # any OS other than windows
        return False

def run(cmd):
    completed = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
    return completed

def block():
    result = run(f'Enable-NetFirewallRule -Name \"League Loading Pauser\"')
    if result.returncode == 0:
        print("Blocked \"League of Legends.exe\" Successfully!\n")
    
def unblock():
    result = run(f'Disable-NetFirewallRule -Name \"League Loading Pauser\"')
    if result.returncode == 0:
        print("Unblocked \"League of Legends.exe\" Successfully!\n")
    
def close():
        print("Goodbye!"); sys.exit()
        
def checkPath(game_path):
    return os.path.exists(game_path)

def createRule():
    # check if rule already exists.
    check = run(f'Get-NetFirewallRule -Name "League Loading Pauser"')    
    if check.returncode != 0: #doesn't exist, create one
        print("Doing first time setup..")
        run(f'New-NetFirewallRule -Name "League Loading Pauser" -DisplayName "League Loading Pauser" -Direction Outbound -Program "{GAME_PATH}" -Action Block -Enabled False')
        print("Firewall rule created! \\^-^/\n")



if __name__ == "__main__":
    main()
