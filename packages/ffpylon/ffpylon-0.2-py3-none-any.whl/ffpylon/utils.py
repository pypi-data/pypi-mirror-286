#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author  : nickdecodes
@Email   : nickdecodes@163.com
@Usage   :
@FileName: utils.py
@DateTime: 2024/7/2 14:09
@SoftWare: 
"""

import re
import json
import datetime


class AutoGenerator:
    @classmethod
    def build_header_content(cls, file_name):
        header_content = ''
        header_content += '#!/usr/bin/env python\n'
        header_content += '# -*- coding: utf-8 -*-\n'
        header_content += '\n'
        header_content += '"""\n'
        header_content += '@Author  : nickdecodes\n'
        header_content += '@Email   : nickdecodes@163.com\n'
        header_content += '@Usage   :\n'
        header_content += f'@FileName: {file_name}\n'
        header_content += f'@DateTime: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}\n'
        header_content += f'@SoftWare: \n'
        header_content += '"""\n'
        header_content += '\n'
        header_content += '\n'
        header_content += 'from .meta import OptionMeta\n'
        header_content += 'from .exec import CommandExecutor\n'
        header_content += '\n'
        header_content += '\n'
        return header_content

    @classmethod
    def build_options_content(cls, indent, options_list):
        """
        options_list = [
            {'option': option, 'description': description},
            ......
        ]
        """
        options_content = f'{indent}options = [\n'
        for option in options_list:
            _option = option.get('option', '')
            _description = option.get('description', '')
            if '?' in _option:
                continue
            options_content += f"{indent}{indent}'{_option}',  # {_description}\n"
        options_content += f'{indent}]\n'
        options_content += f'\n'
        return options_content

    @classmethod
    def build_method_content(cls, indent, method_list):
        """
        method_list = [
            {
                'method_name': method_name,
                'comments': description,
                'other_comments': [other_comments],
            },
        ]
        """
        method_content = ''
        for method in method_list:
            method_name = method['method_name']
            comments = method['comments']
            other_comments = method['other_comments']
            if '?' in method_name:
                continue
            method_content += f'{indent}def {method_name}(self, *args, **kwargs):\n'
            method_content += f'{indent}{indent}"""\n'
            method_content += f'{indent}{indent}{comments}\n'
            method_content += f'{indent}{indent}\n'
            for comment in other_comments:
                method_content += f'{indent}{indent}{comment}\n'
            method_content += f'{indent}{indent}"""\n'
            method_content += f'{indent}{indent}\n'
            method_content += f'{indent}{indent}raise NotImplementedError\n'
            method_content += f'{indent}{indent}\n'

        return method_content

    @classmethod
    def get_ffmpeg_options(cls):
        from exec import CommandExecutor
        ret, out, err = CommandExecutor().run(command=['ffmpeg', '-h', 'full', '-hide_banner'], alone=True)
        lines = out.splitlines()
        options_dict = {}
        section = None
        option = None

        for line in lines:
            content = line.strip()
            print(content)
            if len(content) <= 0:
                continue
            if content.endswith(':'):
                section = content[:-1]
                option = None
                options_dict.setdefault(section, [])
            elif content.startswith('-') and not content.startswith('--help'):
                pattern = re.compile(r"(-\w+)(.*)")
                match = pattern.match(content)
                if match:
                    option = match.group(1)
                    parts = match.group(2)
                else:
                    option = content
                    parts = ""
                description = ' '.join([part for part in parts.split() if part])
                options_dict.setdefault(section, []).append([option, description, []])
            elif section and option:
                options_dict.setdefault(section, [])[-1][-1].append(content)

        adjust_option_dict = {key: val for key, val in options_dict.items() if len(val) > 1}
        with open('ffmpeg_options.json', 'w', encoding='utf-8') as f:
            json.dump(adjust_option_dict, f, ensure_ascii=False, indent=4)

        return adjust_option_dict

    @classmethod
    def gen_ffmpeg_options_meta_class(cls):
        ffmpeg_options_info = cls.get_ffmpeg_options()
        content_header = cls.build_header_content('ffmpeg_options.py')

        special_options = ['pass', 'async', '8x8dct']
        indent = ' ' * 4
        class_code = f'class FFmpegOptions(CommandExecutor, metaclass=OptionMeta):\n'
        class_code += f'{indent}"""\n'
        class_code += f'{indent}https://ffmpeg.org/ffmpeg.html\n'
        class_code += f'{indent}"""\n'

        options_list = []
        options_set = set()
        method_list = []
        for section, values in ffmpeg_options_info.items():
            for option, description, option_meta in values:
                if option.startswith('-'):
                    adjust_option = option.lstrip('-').replace('-', '_')
                    if adjust_option in special_options:
                        continue
                    adjust_option = f'-{adjust_option}'
                else:
                    adjust_option = option.replace('-', '_')
                if adjust_option in options_set:
                    continue
                else:
                    options_set.add(adjust_option)
                options_list.append({'option': adjust_option, 'description': description})
                method_list.append({
                    'method_name': adjust_option.lstrip('-') if adjust_option.startswith('-') else adjust_option,
                    'comments': description,
                    'other_comments': option_meta,
                })

        options_content = cls.build_options_content(indent, options_list)
        method_content = cls.build_method_content(indent, method_list)
        class_code += options_content
        class_code += method_content
        class_code += '\n'
        with open('ffmpeg_options.py', 'w', encoding='utf-8') as f:
            f.write(content_header)
            f.write(class_code)

    @classmethod
    def get_ffprobe_options(cls):
        from exec import CommandExecutor
        ret, out, err = CommandExecutor().run(command=['ffprobe', '-h', 'long', '-hide_banner'], alone=True)
        lines = out.splitlines()
        options_dict = {}
        section = None
        option = None

        for line in lines:
            content = line.strip()
            print(content)
            if len(content) <= 0:
                continue
            if content.endswith(':'):
                section = content[:-1]
                option = None
                options_dict.setdefault(section, [])
            elif content.startswith('-'):
                option, parts = content.split(maxsplit=1)
                description = ' '.join([part for part in parts.split() if part])
                options_dict.setdefault(section, []).append([option, description, []])
            elif section and option:
                options_dict.setdefault(section, [])[-1][-1].append(content)

        adjust_option_dict = {key: val for key, val in options_dict.items() if len(val) > 1}
        with open('ffprobe_options.json', 'w', encoding='utf-8') as f:
            json.dump(adjust_option_dict, f, ensure_ascii=False, indent=4)

        return adjust_option_dict

    @classmethod
    def gen_ffprobe_options_meta_class(cls):
        ffprobe_options_info = cls.get_ffprobe_options()
        content_header = cls.build_header_content('ffprobe_options.py')

        indent = ' ' * 4
        class_code = f'class FFProbeOptions(CommandExecutor, metaclass=OptionMeta):\n'
        class_code += f'{indent}"""\n'
        class_code += f'{indent}https://ffmpeg.org/ffprobe.html\n'
        class_code += f'{indent}"""\n'

        options_list = []
        options_set = set()
        method_list = []
        for section, values in ffprobe_options_info.items():
            for option, description, option_meta in values:
                if option.startswith('-'):
                    adjust_option = option.lstrip('-').replace('-', '_')
                    adjust_option = f'-{adjust_option}'
                else:
                    adjust_option = option.replace('-', '_')
                if adjust_option in options_set:
                    continue
                else:
                    options_set.add(adjust_option)
                options_list.append({'option': adjust_option, 'description': description})
                method_list.append({
                    'method_name': adjust_option.lstrip('-') if adjust_option.startswith('-') else adjust_option,
                    'comments': description,
                    'other_comments': option_meta,
                })

        options_content = cls.build_options_content(indent, options_list)
        method_content = cls.build_method_content(indent, method_list)
        class_code += options_content
        class_code += method_content
        class_code += '\n'
        with open('ffprobe_options.py', 'w', encoding='utf-8') as f:
            f.write(content_header)
            f.write(class_code)


if __name__ == '__main__':
    AutoGenerator.gen_ffmpeg_options_meta_class()
