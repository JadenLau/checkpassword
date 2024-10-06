import time
import sys
import os
from tqdm.rich import tqdm
import hashlib as hash
passwd1 = None
passwd2 = None
passwd_hide_char = "\033[8m"
key = []
data = []

def load(sb,start=None,end=None):
    os.chdir("resources")
    lines = open(sb,"r",encoding="utf-8").readlines() # open(sb,"r",encoding="utf-8")
    os.chdir("..")
    barp = tqdm(total=len(lines))
    if end is None: barp.set_description(f"loading {sb}")
    else: barp.set_description(f"Loading {sb} ({start} of {end})")
    k = []
    for i in lines:
        k += [str(i).strip()]
        barp.update(1)
    barp.close()
    # data = k
    return k


# BEGIN PASSWORD LOAD
resources = os.listdir("resources")
current = 1
fails = 0
begin = 0
end = 0
for a in resources:
    try: key += load(a,current,len(resources))
    except: fails += 1
    current += 1
print(f'Skipped {fails} resources.')
# END PASSWORD LOAD


print(f"Password key length: {len(key)}")
passwd = None

if "-h" in sys.argv or "--help" in sys.argv:
    print("\033[0mHelp:\n-c [md5_hash] or --crack [md5_hash]:\n\tcrack password with md5 hash\n-e [password] or --equations [password]:\n\tcompare password with the list ")
    sys.exit(0)

print('\033[0mPassword safety test')
if "-c" in sys.argv or "--crack" in sys.argv:
    mode = "c"
    passwd = sys.argv[2]

elif "-e" in sys.argv or "--equations" in sys.argv:
    mode = "e"
    passwd = sys.argv[2]
else:
    mode = input("Select mode:\n[c] crack: crack it with md5 hash\n[e] equations: give a password and compare it with password list\n\noption [c/e]: ")
    if str(mode) != "e"and str(mode) != "c":
        print(f"failed: {mode} ({type(mode)})")
        sys.exit(1)

if mode == "e":
    if passwd is None:
        passwd1 = input(f"\033[0mEnter password: {passwd_hide_char}")
        passwd2 = input(f"\033[0mConfirm password: {passwd_hide_char}")
        if not passwd1 == passwd2:
            print("Passwords did not match!")
            sys.exit(2)
        passwd = passwd2
    begin = time.time()
    end = 0
    result = None
    print('\033[0mBegin check.')
    with tqdm(total=len(key)) as bar:
        for i in range(len(key)):
            bar.set_description(f"checking '{str(key[i])}'")
            if str(key[i]) == str(passwd):
                result = str(key[i])
                end = time.time()
                break
            bar.update(1)
elif mode == "c":
    if passwd is None: 
        passwd = ""
        passwd = input("\033[0mEnter MD5 hash or type nothing to convert password to MD5: ")
        if passwd == "":
            passwd1 = input(f"\033[0mEnter password: {passwd_hide_char}")
            passwd2 = input(f"\033[0mConfirm password: {passwd_hide_char}")
            if passwd1 == passwd2:
                passwd = passwd1
                passwd = str(hash.md5(str(passwd).encode()).hexdigest())
                print(f"\033[0mMD5 of pssword is {passwd}.")
            else:
                print("\033[0mPasswords did not match!")
                sys.exit(2)
    begin = time.time()
    result = None
    print('\033[0mBegin check.')
    with tqdm(total=len(key)) as bar:
        for i in range(len(key)):
            bar.set_description(f"checking md5 {str(hash.md5(str(key[i]).encode()).hexdigest())}")
            if str(hash.md5(str(key[i]).encode()).hexdigest()) == str(passwd):
                result = str(key[i])
                end = time.time()
                break
            bar.update(1)
print(f"\n\nUsed {round(end-begin,2)}s")
if result is None:
    print("Failed to crack password!")