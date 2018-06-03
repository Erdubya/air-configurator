import sys
from pathlib import Path


def get_default_dir() -> Path:
    if sys.platform == 'linux':
        skins_dir = Path.expanduser(Path('~/.local/share/Steam/skins/'))
    elif sys.platform == 'posix':
        skins_dir = Path.expanduser(
            Path('~/Library/Application Support/Steam/Steam.AppBundle/Steam/Contents/MacOS/skins/'))
    elif sys.platform == 'win32':
        skins_dir = Path('%ProgramFiles(x86)%\\Steam\\Skins')
    else:
        skins_dir = None

    return skins_dir


def choose_skin(skins: list) -> int:
    print('\n')
    for x in range(len(skins)):
        print("{:4} --> {}".format(x, skins[x].name))

    while True:
        choice = int(input("Choose skin to configure: "))
        if choice in range(len(skins)):
            return choice
        else:
            print('Invalid choice')


def is_air_skin(skin: Path) -> bool:
    return "Air-for-Steam" in (skin / 'Changelog.url').read_text()


def change_theme(skin: Path):
    pass


def change_color(skin: Path):
    colors = [x.stem for x in (skin / 'Resource' / 'colors').iterdir() if x.is_file()]
    colors += [x.stem for x in (skin / 'Resource' / 'colors' / 'user').iterdir() if x.is_file()]

    print('\n')
    for x in range(len(colors)):
        print("{:4} --> {}".format(x, colors[x]))

    while True:
        choice = int(input("Choose color: "))
        if choice in range(len(colors)):
            break
        else:
            print('Invalid choice')



    new_color = colors[choice]
    with (skin / 'config.ini').open() as file:
        config = file.readlines()

    idx = [config.index(s) for s in config if new_color in s]
    print(config[idx[0]])

def chat_font_size(skin: Path):
    pass


def notify_pos(skin: Path):
    pass


def configure_skin(skin):
    def choose_configuration_option(options: list):
        print('\n')
        for x in range(len(options)):
            print("{:4} --> {}".format(x, options[x][0]))

        while True:
            choice = int(input("Choose option: "))
            if choice in range(len(options)):
                return choice
            else:
                print('Invalid choice')

    options = [
        ('Change theme', change_theme),
        ('Change color', change_color),
        ('Change chat font size', chat_font_size),
        ('Change notification position', notify_pos),
        'Change notification stack count',
        'Reorganize sections in details mode',
        'Change fade of uninstalled games in grid mode',
        'Friends list shortcut',
        'Game filters dropdown',
        'Wallet balance',
        'Unread inbox icon invisiblity',
        'Friends list square avatars',
        'Friends list hover effect',
        'Three line friends list status',
        'Always visible downloads icon',
        'Exit'
    ]

    while True:
        choice = choose_configuration_option(options)

        if options[choice] == 'Exit':
            break

        options[choice][1](skin)


print("air-configurator")
print(sys.platform)

skins_dir = get_default_dir()
print('Skin path: ' + str(skins_dir))

skins = [x for x in skins_dir.iterdir() if x.is_dir()]

skin = skins[choose_skin(skins)]

if not is_air_skin(skin):
    print('Invalid skin - not Air')
    exit(1)

configure_skin(skin)
