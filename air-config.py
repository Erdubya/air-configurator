import sys


def get_default_dir():
    if sys.platform is 'linux':
        skins_dir = '~/.local/share/Steam/skins/'
    elif sys.platform is 'posix':
        skins_dir = '~/Library/Application Support/Steam/Steam.AppBundle/Steam/Contents/MacOS/skins/'
    elif sys.platform is 'win32':
        skins_dir = '%ProgramFiles(x86)%\\Steam\\Skins'
    else:
        skins_dir = None

    return skins_dir


path = input("Enter path to ")
