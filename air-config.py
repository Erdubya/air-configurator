import os
import shutil
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


def get_int(num: str):
    if num.isdigit():
        return int(num)
    return -1


def print_header():
    print("air-configurator")
    print(sys.platform)
    print('Skin path: ' + str(skin_dir))


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def copy_dir(root_src_dir, root_dst_dir):
    for src_dir, dirs, files in os.walk(root_src_dir):
        dst_dir = src_dir.replace(root_src_dir, root_dst_dir, 1)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                os.remove(dst_file)
            shutil.copy(src_file, dst_dir)


def choose_skin(skin_list: list) -> int:
    cls()
    print_header()
    for x in range(len(skin_list)):
        print("{:4} --> {}".format(x, skin_list[x].name))

    while True:
        choice = get_int(input("Choose skin to configure: "))
        if choice in range(len(skin_list)):
            return choice
        else:
            print('Invalid choice')


def is_air_skin(skin: Path) -> bool:
    return "Air-for-Steam" in (skin / 'Changelog.url').read_text()


def change_theme(skin: Path):
    # get theme list
    themes = [x.name for x in (skin / '+Extras' / 'Themes').iterdir() if x.is_dir()]

    cls()
    print_header()
    for x in range(len(themes)):
        print("{:4} --> {}".format(x, themes[x]))

    # get user choice of theme
    while True:
        choice = get_int(input("Choose theme: "))
        if choice in range(len(themes)):
            break
        else:
            print('Invalid choice')
    new_theme = themes[choice]

    # copy theme directory
    copy_dir(str(skin / '+Extras' / 'Themes' / new_theme), str(skin))

    # set theme in config
    # read in current config
    with (skin / 'config.ini').open() as file:
        config = file.readlines()

    # get color specific lines
    idxs = [config.index(s) for s in config if 'resource/themes' in s]

    # set new color
    for i in idxs:
        if not config[i].startswith('//', 4):
            config[i] = config[i][:4] + '//' + config[i][4:]

        if new_theme.lower() in config[i]:
            config[i] = config[i].replace('//', '', 1)

    # write out config
    with (skin / 'config.ini').open('w') as file:
        file.writelines(config)

    input('Theme changed to {}.  Press any key to continue...'.format(new_theme))


def change_color(skin: Path):
    # get list of available colors
    colors = [x.stem for x in (skin / 'Resource' / 'colors').iterdir() if x.is_file()]
    colors += [x.stem for x in (skin / 'Resource' / 'colors' / 'user').iterdir() if x.is_file()]

    # display list of colors
    cls()
    print_header()
    for x in range(len(colors)):
        print("{:4} --> {}".format(x, colors[x]))

    # get user choice of color
    while True:
        choice = get_int(input("Choose color: "))
        if choice in range(len(colors)):
            break
        else:
            print('Invalid choice')
    new_color = colors[choice]

    # read in current config
    with (skin / 'config.ini').open() as file:
        config = file.readlines()

    # get color specific lines
    idxs = [config.index(s) for s in config if 'resource/colors' in s]

    # set new color
    for i in idxs:
        if '//' not in config[i]:
            config[i] = config[i][:4] + '//' + config[i][4:]

        if new_color in config[i]:
            config[i] = config[i].replace('//', '')

    # write out config
    with (skin / 'config.ini').open('w') as file:
        file.writelines(config)

    input('Color changed to {}.  Press any key to continue...'.format(new_color))


def chat_font_size(skin: Path):
    options = [
        'Enter new font size',
        'Reset to default',
        'Cancel'
    ]

    # print options
    cls()
    print_header()
    for x in range(len(options)):
        print("{:4} --> {}".format(x, options[x]))

    # get user choice
    while True:
        choice = get_int(input("Choose option: "))
        if choice in range(len(options)):
            break
        else:
            print('Invalid choice')

    # change font size
    if choice == 0:
        while True:
            new_size = get_int(input('Enter new font size: '))
            if new_size > 0:
                break

        # read file
        with (skin / 'Resource' / 'styles' / '_fonts.styles').open() as file:
            fonts = file.readlines()

        # get correct line
        idx = [fonts.index(s) for s in fonts if 'ChatListPanel RichText' in s][0]

        # uncomment line
        if fonts[idx].startswith('//'):
            fonts[idx] = fonts[idx][2:]

        # add font size
        fonts[idx] = fonts[idx][:fonts[idx].find('{') + 1] + ' font-size={} '.format(new_size) + fonts[idx][
                                                                                                 fonts[idx].find('}'):]

        # write file
        with (skin / 'Resource' / 'styles' / '_fonts.styles').open('w') as file:
            file.writelines(fonts)

        input('Chat font size changed to {}.  Press any button to continue...'.format(new_size))
    elif choice == 1:
        # read file
        with (skin / 'Resource' / 'styles' / '_fonts.styles').open() as file:
            fonts = file.readlines()

        # get correct line
        idx = [fonts.index(s) for s in fonts if 'ChatListPanel RichText' in s][0]

        # comment line
        if not fonts[idx].startswith('//'):
            fonts[idx] = '//' + fonts[idx]

        # write file
        with (skin / 'Resource' / 'styles' / '_fonts.styles').open('w') as file:
            file.writelines(fonts)

        input('Chat font size reset.  Press any button to continue...')


def notify_pos(skin: Path):
    options = [
        ('Bottom right', 'BottomRight'),
        ('Bottom left', 'BottomLeft'),
        ('Top right', 'TopRight'),
        ('Top left', 'TopLeft'),
    ]

    # print options
    cls()
    print_header()
    for x in range(len(options)):
        print("{:4} --> {}".format(x, options[x][0]))

    # get user choice
    while True:
        choice = get_int(input("Choose position: "))
        if choice in range(len(options)):
            break
        else:
            print('Invalid choice')

    # read file
    with (skin / 'Resource' / 'styles' / 'steam.styles').open() as file:
        styles = file.readlines()

    # get correct line
    idxs = [styles.index(s) for s in styles if 'Notifications.PanelPosition' in s]

    for idx in idxs:
        qopen = styles[idx].find('"') + 1
        styles[idx] = styles[idx][:qopen] + options[choice][1] + styles[idx][styles[idx].find('"', qopen):]

    # write file
    with (skin / 'Resource' / 'styles' / 'steam.styles').open('w') as file:
        file.writelines(styles)

    input('Notification position changed to {}.  Press any button to continue...'.format(options[choice][0]))


def notify_stack(skin: Path):
    options = [
        'Change stack size',
        'Cancel'
    ]

    # print options
    cls()
    print_header()
    for x in range(len(options)):
        print("{:4} --> {}".format(x, options[x][0]))

    # get user choice
    while True:
        choice = get_int(input("Choose option: "))
        if choice in range(len(options)):
            break
        else:
            print('Invalid choice')

    if choice == 0:
        while True:
            new_size = get_int(input("Enter new stack size: "))
            if new_size > 0:
                break
            else:
                print('Invalid choice')

        # read file
        with (skin / 'Resource' / 'styles' / 'steam.styles').open() as file:
            styles = file.readlines()

        # get correct line
        idx = [styles.index(s) for s in styles if 'Notifications.StackSize' in s][0]

        qopen = styles[idx].find('"') + 1
        styles[idx] = styles[idx][:qopen] + str(new_size) + styles[idx][styles[idx].find('"', qopen):]

        # write file
        with (skin / 'Resource' / 'styles' / 'steam.styles').open('w') as file:
            file.writelines(styles)

        input('Notification stack size changed to {}.  Press any button to continue...'.format(new_size))


def detail_reorg(skin: Path):
    with (skin / 'Resource' / 'layout' / 'steamrootdialog_gamespage_details.layout').open() as file:
        layout = file.readlines()

    idx = [layout.index(s) for s in layout if 'welcomedetails' in s][0]

    param_start = layout[idx].find('=') + 1
    items = layout[idx][param_start:-1].split(',')

    items.append('Save Order')

    while True:
        # print options
        cls()
        print_header()
        for x in range(len(items)):
            print("{:4} --> {}".format(x, items[x]))

        # get user choice
        while True:
            swap_dst = get_int(input("Choose position to change: "))
            if swap_dst in range(len(items)):
                break
            else:
                print('Invalid choice')

        # cancel out of loop
        if swap_dst is len(items) - 1:
            break

        # print options
        cls()
        print_header()
        for x in range(len(items) - 1):
            print("{:4} --> {}".format(x, items[x]))

        # get user choice
        while True:
            swap_src = get_int(input("Replace with: "))
            if swap_src in range(len(items) - 1):
                break
            else:
                print('Invalid choice')

        # swap items
        items[swap_src], items[swap_dst] = items[swap_dst], items[swap_src]

    layout[idx] = layout[idx][:param_start] + ','.join(items[:-1]) + '\n'

    with (skin / 'Resource' / 'layout' / 'steamrootdialog_gamespage_details.layout').open('w') as file:
        file.writelines(layout)

    input('Display order saved.  Press any button to continue...')


def grid_fade(skin: Path):
    with (skin / 'Resource' / 'styles' / 'steam.styles').open() as file:
        styles = file.readlines()

    idx = [styles.index(s) for s in styles if 'GameItem_Uninstalled GamesGridImage' in s][0] + 1

    cur_alpha = styles[idx].strip(' \t\nalpha')

    cls()
    print_header()
    print('\nCurrent fade value: {}'.format(cur_alpha))

    while True:
        new_alpha = get_int(input("Enter new fade value: "))
        if new_alpha in range(256):
            break
        else:
            print("Invalid value")

    styles[idx] = "      {} {:10}\n".format('alpha', new_alpha)

    with (skin / 'Resource' / 'styles' / 'steam.styles').open('w') as file:
        file.writelines(styles)

    input('Fade value changed to {}.  Press any button to continue...'.format(new_alpha))


def configure_skin(skin):
    options = [
        ('Change theme', change_theme),
        ('Change color', change_color),
        ('Change chat font size', chat_font_size),
        ('Change notification position', notify_pos),
        ('Change notification stack count', notify_stack),
        ('Reorganize sections in details mode', detail_reorg),
        ('Change fade of uninstalled games in grid mode', grid_fade),
        'Friends list shortcut',
        'Game filters dropdown',
        'Wallet balance',
        'Unread inbox icon invisiblity',
        'Friends list square avatars',
        'Friends list hover effect',
        'Three line friends list status',
        'Always visible downloads icon',
        ('Exit', 0)
    ]

    while True:
        cls()
        print_header()
        for x in range(len(options)):
            print("{:4} --> {}".format(x, options[x][0]))

        while True:
            choice = get_int(input("Choose option: "))
            if choice in range(len(options)):
                break
            else:
                print('Invalid choice')

        if options[choice][0] == 'Exit':
            break

        options[choice][1](skin)


skin_dir = get_default_dir()

print_header()

skins = [x for x in skin_dir.iterdir() if x.is_dir()]

skin_dir = skins[choose_skin(skins)]

if not is_air_skin(skin_dir):
    print('Invalid skin - not Air')
    exit(1)

configure_skin(skin_dir)
