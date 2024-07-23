import sys
import argparse
from colorama import Fore, Style

class ColorFore:
    @classmethod
    def color_text(cls, color, text):
        return f'{color}{text}{Style.RESET_ALL}'
    
    @classmethod
    def bold_color_text(cls, color, text):
        return f'{Style.BRIGHT}{color}{text}{Style.RESET_ALL}'

    @classmethod
    def _add_color_methods(cls):
        colors = {
            'BLACK': Fore.BLACK,
            'RED': Fore.RED,
            'GREEN': Fore.GREEN,
            'YELLOW': Fore.YELLOW,
            'BLUE': Fore.BLUE,
            'MAGENTA': Fore.MAGENTA,
            'CYAN': Fore.CYAN,
            'WHITE': Fore.WHITE,
            'RESET': Fore.RESET,
            'BRIGHT_RED': Fore.LIGHTRED_EX,
            'BRIGHT_GREEN': Fore.LIGHTGREEN_EX,
            'BRIGHT_YELLOW': Fore.LIGHTYELLOW_EX,
            'BRIGHT_BLUE': Fore.LIGHTBLUE_EX,
            'BRIGHT_MAGENTA': Fore.LIGHTMAGENTA_EX,
            'BRIGHT_CYAN': Fore.LIGHTCYAN_EX,
            'BRIGHT_WHITE': Fore.LIGHTWHITE_EX,
            'BACKGROUND_RED': Fore.LIGHTRED_EX,
            'BACKGROUND_GREEN': Fore.LIGHTGREEN_EX,
            'BACKGROUND_YELLOW': Fore.LIGHTYELLOW_EX,
            'BACKGROUND_BLUE': Fore.LIGHTBLUE_EX,
            'BACKGROUND_MAGENTA': Fore.LIGHTMAGENTA_EX,
            'BACKGROUND_CYAN': Fore.LIGHTCYAN_EX,
            'BACKGROUND_WHITE': Fore.LIGHTWHITE_EX,
        }
        for color_name, color_value in colors.items():
            setattr(cls, f"{color_name}", classmethod(lambda cls, text, color=color_value: cls.color_text(color, text)))
            setattr(cls, f"BOLD_{color_name}", classmethod(lambda cls, text, color=color_value: cls.bold_color_text(color, text)))
            
# Add the color methods to the ColorFore class
ColorFore._add_color_methods()

class ColorFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter):
    def _get_help_string(self, action):
        help_str = action.help
        if isinstance(action, argparse._HelpAction):
            help_str = "显示帮助信息"
        help_str = ColorFore.YELLOW(help_str)
        if not action.required and action.default != "==SUPPRESS==":
            help_str = help_str + ColorFore.RED(f' (默认值: {action.default})')
        return help_str + '\n\n'

    def format_help(self):
        help_text = super().format_help()
        help_text = help_text.replace('usage:', ColorFore.BOLD_GREEN("基本用法：\n\n "))
        help_text = help_text.replace('options:', ColorFore.BOLD_GREEN("参数选项：\n"))
        return '\n' + help_text + '\n\n'

class ColorArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        # Pass custom formatter class to the ArgumentParser constructor
        kwargs['formatter_class'] = ColorFormatter
        # Set a custom description
        lines = kwargs['description'].split('\n')
        description = '\n'.join(['  ' + line for line in lines])
        kwargs['description'] = ColorFore.BOLD_GREEN("\n命令简介：\n\n") + description
        super().__init__(*args, **kwargs)

    def error(self, message):
        # Custom error messages in Chinese
        error_messages = {
            'the following arguments are required:': '缺少必需参数:',
            'unrecognized arguments': '无法识别的参数',
            'invalid choice:': '无效选择:',
            'not allowed': '不允许',
            'expected one argument': '需要一个参数'
        }

        # Determine the appropriate error message
        for key, value in error_messages.items():
            if key in message:
                formatted_message = '\n' + ColorFore.BOLD_RED(f'错误: \n\n') + ColorFore.YELLOW(value) + f'{message.split(key, 1)[1].strip()}' + '\n\n'
                print(formatted_message, file=sys.stderr)
                self.exit(2)
                return
         # If no custom message matched, use the default behavior
        print(ColorFore.color_text(ColorFore.RED, f'错误: {message}'), file=sys.stderr)
        self.exit(2)
