import os
import glob
import platform
import re
import subprocess

PATH_DATA = '../data/'
DIR_TRANSLATION = glob.glob(PATH_DATA + "*.json")

def main():

    print("\n==== TRANSLATION FILE LIST ====\n")
    for file in DIR_TRANSLATION:
        if (os.path.isfile(file) and re.search(r'(.+?)\.json', file)):
            if file == PATH_DATA + "en.json":
                print("English OK")
            elif file == PATH_DATA + "nl.json":
                print("Dutch OK")
            elif file == PATH_DATA + "tr.json":
                print("Turkey OK")
        else:
            print('NO FILE FOUND')

    print("\n==== TOOL LIST ====\n")

    # print(os.name)
    if platform.system() == 'Linux':
        print('OS: Linux')
    elif platform.system() == 'Darwin':
        print('OS: MacOS')
    elif platform.system() == 'Windows':
        print('OS: Windows')

    list_cmd = ['chromedriver', 'geckodriver']

    for cmd in list_cmd:
        exist = subprocess.call('command -v ' + cmd + '>> /dev/null', shell=True)
        if exist == 0:
            print(cmd + " OK")
        else:
            print(cmd + " NOT FOUND")


if __name__ == "__main__":
    main()
