COLOR_SPACE = {
    'light': {
        'main':     '#003153',
        'active':   '#ffffff',
        'inactive': '#aaaaaa',
        'outline':  '#003153',
        'hover':    '#03dfaa',
        'cells': {
            'correct-flag': 'green',
            'incorrect-flag': 'yellow',
            'empty': '#ffffff',
            'bomb': '#AA0000',
            '1': '#59DF9F',
            '2': '#9BE382',
            '3': '#D0DA62',
            '4': '#DEBB60',
            '5': '#F0923C',
            '6': '#E46666',
            '7': '#ffffff',
            '8': '#ffffff',
        }
    },
    'dark': {
        'main':     'black',
        'active':   'white',
        'inactive': 'grey',
        'outline':  'yellow',
        'hover':    'cyan',
        'cells': {
            'correct-flag': 'green',
            'incorrect-flag': 'yellow',
            'empty': '#222222',
            'bomb': '#AA0000',
            '1': '#59DF9F',
            '2': '#9BE382',
            '3': '#D0DA62',
            '4': '#DEBB60',
            '5': '#F0923C',
            '6': '#E46666',
            '7': '#ffffff',
            '8': '#ffffff',
        }
    }
}


class COLORS:
    scheme = COLOR_SPACE['light']

    @staticmethod
    def scheme():
        return COLORS.scheme

    def setTheme(themeName):
        COLORS.scheme = COLOR_SPACE[themeName]

    def __class_getitem__(cls, colorName):
        stack = COLORS.scheme
        for categ in colorName.split('.'):
            if categ not in stack:
                raise ValueError(f'No color named {colorName}')
            stack = stack[categ]
        return stack

# COLORS = {
    # 'active': '#0081a3',
    # 'inactive': '#ffffff',
    # 'outline': '#003153',
    # 'hover': '#03dfaa',
    # '0': "#ffffff",
    # '1': '#59DF9F',
    # '2': '#9BE382',
    # '3': '#D0DA62',
    # '4': '#DEBB60',
    # '5': '#F0923C',
    # '6': '#E46666',
    # '7': '#ffffff',
    # '8': '#ffffff',
    # 'bomb': '#AA0000',
# }
