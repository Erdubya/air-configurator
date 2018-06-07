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

    input('Theme changed to {}.  Press enter to continue...'.format(new_theme))


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

    input('Color changed to {}.  Press enter to continue...'.format(new_color))


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

        input('Chat font size changed to {}.  Press enter to continue...'.format(new_size))
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

        input('Chat font size reset.  Press enter to continue...')


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

    input('Notification position changed to {}.  Press enter to continue...'.format(options[choice][0]))


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

        input('Notification stack size changed to {}.  Press enter to continue...'.format(new_size))


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

    input('Display order saved.  Press enter to continue...')


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

    input('Fade value changed to {}.  Press enter to continue...'.format(new_alpha))


def friends_list_shorcut(skin: Path):
    options = [
        'Enable shortcut',
        'Disable shortcut'
    ]

    # display options
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

    with (skin / 'Resource' / 'layout' / 'steamrootdialog.layout').open() as file:
        layout = file.readlines()

    idx1 = [layout.index(s) for s in layout if 'control=online_friends' in s][0] + 1
    idx2 = [layout.index(s) for s in layout if 'control=view_friends' in s][0] + 1

    if choice == 0:
        height = '30'
        status = 'enabled'
    else:
        height = '0'
        status = 'disabled'

    layout[idx1] = layout[idx1][:layout[idx1].find('=') + 1] + height + '\n'
    layout[idx2] = layout[idx2][:layout[idx2].find('=') + 1] + height + '\n'

    with (skin / 'Resource' / 'layout' / 'steamrootdialog.layout').open('w') as file:
        file.writelines(layout)

    input('Friends list shortcut {}.  Press enter to continue...'.format(status))


def game_filters(skin: Path):
    options = [
        'Enable filters',
        'Disable filters'
    ]

    # display options
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

    with (skin / 'Resource' / 'layout' / 'uinavigatorpanel.layout').open() as file:
        layout = file.readlines()

    idx = [layout.index(s) for s in layout if 'control=label_store,label_library' in s][0]

    if choice == 0:
        if layout[idx] != "      control=label_store,label_library\n":
            # update code
            layout[idx] = "      control=label_store,label_library\n"
            idx += 4

            # insert new code
            layout[idx] = "    place {\n"
            layout.insert(idx + 1, "      control=library_filters\n")
            layout.insert(idx + 2, "      region=nav start=label_library height=30 width=15 x=0 y=7\n")
            layout.insert(idx + 3, "    }\n")
            layout.insert(idx + 4, '\n')
            layout.insert(idx + 5, "    place {\n")
            layout.insert(idx + 6, "      control=label_community,label_me\n")
            layout.insert(idx + 7,
                          "      region=nav start=library_filters height=44 spacing=16 x=10 y=0 margin-top=-7\n")
            layout.insert(idx + 8, "    }\n")

        status = 'enabled'
    else:
        if layout[idx] != "      control=label_store,label_library,label_community,label_me\n":
            # update code
            layout[idx] = "      control=label_store,label_library,label_community,label_me\n"
            idx += 4
            layout[idx] = "    place { control=library_filters height=0 width=0 margin-left=-9999 }\n"

            # remove display code
            for n in range(8):
                layout.pop(idx + 1)

        status = 'disabled'

    with(skin / 'Resource' / 'layout' / 'uinavigatorpanel.layout').open('w') as file:
        file.writelines(layout)

    input('Game filters dropdown {}.  Press enter to continue...'.format(status))


def wallet_balance(skin: Path):
    options = [
        'Show wallet balance',
        'Hide wallet balance'
    ]

    # display options
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

    if choice == 0:
        height = '30'
        status = 'shown'
    else:
        height = '0'
        status = 'hidden'

    with (skin / 'Resource' / 'layout' / 'steamrootdialog.layout').open() as file:
        layout = file.readlines()

    idx = [layout.index(s) for s in layout if 'control=account_balance' in s][0]

    param_start = layout[idx].find('height=') + len('height=')
    param_end = layout[idx].find(' margin-right')

    layout[idx] = layout[idx][:param_start] + height + layout[idx][param_end:]

    with (skin / 'Resource' / 'layout' / 'steamrootdialog.layout').open('w') as file:
        file.writelines(layout)

    input('Wallet balance {}.  Press enter to continue...'.format(status))


def inbox_icon(skin: Path):
    options = [
        'Show inbox icon',
        'Hide inbox icon'
    ]

    with (skin / 'Resource' / 'layout' / 'steamrootdialog.layout').open() as file:
        layout = file.readlines()

    idx = [layout.index(s) for s in layout if 'inbox_button {' in s][0] + 2

    # display options
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

    if choice == 0:
        if "render_bg" not in layout[idx]:
            layout.insert(idx + 0, "      render_bg {\n")
            layout.insert(idx + 1, "        0=\"image( x0 + 6, y0 + 6, x1, y1, graphics/onfocus/inbox )\"\n")
            layout.insert(idx + 2, "      }\n")

            while "inbox_button:selected {" not in layout[idx]:
                idx += 1
            idx += 2

            layout.insert(idx + 0, "      render_bg {\n")
            layout.insert(idx + 1, "        0=\"image( x0, y0, x1, y1, graphics/onfocus/active_circle )\"\n")
            layout.insert(idx + 2, "        1=\"image( x0 + 6, y0 + 6, x1, y1, graphics/onfocus/inbox )\"\n")
            layout.insert(idx + 3, "      }\n")

        status = "enabled"
    else:
        if "render_bg" in layout[idx]:
            while "}" not in layout[idx]:
                layout.pop(idx)
            layout.pop(idx)

            while "render_bg" not in layout[idx]:
                idx += 1

            while "}" not in layout[idx]:
                layout.pop(idx)
            layout.pop(idx)

        status = "disabled"

    with (skin / 'Resource' / 'layout' / 'steamrootdialog.layout').open('w') as file:
        file.writelines(layout)

    input('Inbox icon {}.  Press enter to continue...'.format(status))


def square_avatars(skin: Path):
    options = [
        'Enable square avatars',
        'Disable square avatars'
    ]

    # display options
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

    avatars = skin / "+Extras" / "Square Avatars"
    graphics = skin / "Graphics"

    if choice == 0:
        # get current theme
        with (skin / 'config.ini').open() as file:
            config = file.readlines()
        idxs = [config.index(s) for s in config if 'resource/themes' in s]
        theme = ""
        for i in idxs:
            if not config[i].startswith('//', 4):
                start = config[i].find("_") + 1
                end = config[i].find(".", start)
                theme = config[i][start:end]

        theme = theme[:1].upper() + theme[1:]

        shutil.move(str(graphics / "avatarBorderInGame.tga"), str(graphics / "avatarBorderInGame.tga.orig"))
        shutil.move(str(graphics / "avatarBorderOffline.tga"), str(graphics / "avatarBorderOffline.tga.orig"))
        shutil.move(str(graphics / "avatarBorderOnline.tga"), str(graphics / "avatarBorderOnline.tga.orig"))
        shutil.move(str(graphics / "avatarBorderOverlay.tga"), str(graphics / "avatarBorderOverlay.tga.orig"))
        if (graphics / "avatarBorderNotificationDesktop.tga").exists():
            shutil.move(str(graphics / "avatarBorderNotificationDesktop.tga"),
                        str(graphics / "avatarBorderNotificationDesktop.tga.orig"))
            shutil.move(str(graphics / "avatarBorderNotificationOverlay.tga"),
                        str(graphics / "avatarBorderNotificationOverlay.tga.orig"))
        if (graphics / "avatarBorderNotification.tga").exists():
            shutil.move(str(graphics / "avatarBorderNotification.tga"),
                        str(graphics / "avatarBorderNotification.tga.orig"))

        copy_dir(str(avatars / theme), str(graphics))
        status = "enabled"
    else:
        if (graphics / "avatarBorderNotificationDesktop.tga.orig").exists():
            shutil.move(str(graphics / "avatarBorderNotificationDesktop.tga.orig"),
                        str(graphics / "avatarBorderNotificationDesktop.tga"))
            shutil.move(str(graphics / "avatarBorderNotificationOverlay.tga.orig"),
                        str(graphics / "avatarBorderNotificationOverlay.tga"))
            shutil.move(str(graphics / "avatarBorderInGame.tga.orig"),str(graphics / "avatarBorderInGame.tga"))
            shutil.move(str(graphics / "avatarBorderOffline.tga.orig"), str(graphics / "avatarBorderOffline.tga"))
            shutil.move(str(graphics / "avatarBorderOnline.tga.orig"), str(graphics / "avatarBorderOnline.tga"))
            shutil.move(str(graphics / "avatarBorderOverlay.tga.orig"), str(graphics / "avatarBorderOverlay.tga"))
            os.remove(str(graphics / "avatarBorderNotification.tga"))
        status = "disabled"

    input('Square avatars {}.  Press enter to continue...'.format(status))


def friends_hover(skin: Path):
    options = [
        "Enable hover effect"
        "Disable hover effect"
    ]


def configure_skin(skin):
    options = [
        ('Change theme', change_theme),
        ('Change color', change_color),
        ('Change chat font size', chat_font_size),
        ('Change notification position', notify_pos),
        ('Change notification stack count', notify_stack),
        ('Reorganize sections in details mode', detail_reorg),
        ('Change fade of uninstalled games in grid mode', grid_fade),
        ('Friends list shortcut', friends_list_shorcut),
        ('Game filters dropdown', game_filters),
        ('Wallet balance', wallet_balance),
        ('Show inbox icon when no messages', inbox_icon),
        ('Friends list square avatars', square_avatars),
        ('Friends list hover effect', friends_hover),
        'Friends list status on three lines',
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
