COLOR_SPACE = {
    'dark': {
        'main': '#003153',
        'text': '#ffffff',
        'hexagon': {
            'text': 'white',
            'hover': '#03dfaa',
            'active': '#ffffff',
            'inactive': '#aaaaaa',
        },
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
        },
        'buttons': {
            'bg': 'red',
            'fg': 'white',
            'hover-bg': 'black',
            'hover-text': 'white',
            'dot': 'black',
        }
    },
    'light': {
        'main': '#f5f5dc',
        'text': '#222222',
        'hexagon': {
            'active':   'white',
            'inactive': '#ffdab9',
            'outline':  '#ff4500',
            'hover':    '#ffe4e1',
            'text': '#222222',
        },
        'cells': {
            'correct-flag': '#ccff00',
            'incorrect-flag': ' #e6e6fa',
            'empty': 'white',
            'bomb': '#ff4500',
            '1': '#fef7a7',
            '2': '#eee8aa',
            '3': '#ffd800',
            '4': '#ffbf00',
            '5': '#ff7518',
            '6': '#ff033e',
            '7': '#ffffff',
            '8': '#ffffff',
        },
        'buttons': {
            'bg': 'red',
            'fg': 'white',
            'hover-bg': 'cyan',
            'hover-text': 'white',
            'dot': 'white',
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

