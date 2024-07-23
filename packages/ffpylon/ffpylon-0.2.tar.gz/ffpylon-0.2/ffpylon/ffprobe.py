#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author  : nickdecodes
@Email   : nickdecodes@163.com
@Usage   :
@FileName: ffprobe.py
@DateTime: 2024/7/2 14:09
@SoftWare: 
"""

import re
import os
import json
from typing import Tuple, List, Union, Iterable, Dict
from .ffprobe_options import FFProbeOptions


class FFprobe(FFProbeOptions):
    def __init__(self, bin_path='ffprobe', logger=None):
        super(FFprobe).__init__(bin_path=bin_path, logger=logger)
        self.commands = []
    # audio
    def get_audio_codec_name(
            self,
            input_file: str,
            timeout: int = None,
            retries: int = 0,
            delay: int = 1,
    ):
        self.i(input_file)
        self.v('panic')
        self.select_streams('A:0')
        self.show_entries('stream=codec_name')
        self.of('csv=p=0:nk=1')
        self.run()
        command = f'-v panic -select_streams A:0 -show_entries stream=codec_name -of csv=p=0:nk=1 {input_file}'
        ret, out, err = self.run(command=command, timeout=timeout, retries=retries, delay=delay)
        return out.strip()

    def get_audio_bitrate(
            self,
            input_file: str,
            timeout: int = None,
            retries: int = 0,
            delay: int = 1,
    ):
        command = f"-v panic -select_streams a:0 -show_entries stream=bit_rate -of default=nw=1:nk=1 '{input_file}'"
        ret, out, err = self.run(command=command, timeout=timeout, retries=retries, delay=delay)
        return out.strip()

    def get_audio_language(
            self,
            input_file: str,
            audio_index: int=None,
            timeout: int = None,
            retries: int = 0,
            delay: int = 1
    ):
        command = f'-v panic -select_streams a:{audio_index} -show_entries stream_tags=language -of json {input_file}'
        ret, out, err = self.run(command=command, timeout=timeout, retries=retries, delay=delay)
        if ret != 0:
            raise Exception('get audio language error')
        tags_to_lower = {i.lower(): j for i, j in list(json.loads(out)['streams'][0].get('tags', {}).items())}
        return tags_to_lower.get('language', 'undefined')

    def is_default_audio(
            self,
            input_file: str,
            audio_index: int=None,
            timeout: int = None,
            retries: int = 0,
            delay: int = 1
    ):
        command = (f'-v panic -select_streams {audio_index} '
                   f'-show_entries stream_disposition=default -of json {input_file}')
        ret, out, err = self.run(command=command, timeout=timeout, retries=retries, delay=delay)
        if ret != 0 or not out:
            raise Exception('is_default_audio error')

        return int(json.loads(out)['streams'][0].get('disposition', {}).get('default', 0))

    def get_audio_stream_info(
            self,
            input_file: str,
            timeout: int = None,
            retries: int = 0,
            delay: int = 1,
    ):
        if not os.path.exists(input_file):
            raise Exception('file {} not exists'.format(input_file))
        command = f'-v panic -select_streams a -show_streams -of json {input_file}'
        ret, out, err = self.run(command=command, timeout=timeout, retries=retries, delay=delay)
        if ret != 0:
            raise Exception('capture error {} when run {}'.format(out, command))

        return json.loads(out)['streams']

    def get_audio_sequence(
            self,
            input_file: str,
            timeout: int = None,
            retries: int = 0,
            delay: int = 1,
    ):
        command = f'-v panic -show_entries stream=index -select_streams a -of json "{input_file}"'
        ret, out, err = self.run(command=command, timeout=timeout, retries=retries, delay=delay)
        streams = json.loads(out)['streams']
        return [str(x['index']) for x in streams]

    # video
    def get_video_codec_name(
            self,
            input_file: str,
            timeout: int = None,
            retries: int = 0,
            delay: int = 1,
    ):
        command = f'-v panic -select_streams V:0 -show_entries stream=codec_name -of csv=p=0:nk=1 {input_file}'
        ret, out, err = self.run(command=command, timeout=timeout, retries=retries, delay=delay)
        return out.strip()

    def get_video_bitrate(
            self,
            input_file: str,
            timeout: int = None,
            retries: int = 0,
            delay: int = 1,
    ):
        command = f"-v panic -select_streams V:0 -show_entries stream=bit_rate -of default=nw=1:nk=1 '{input_file}'"
        try:
            ret, out, err = self.run(command=command, timeout=timeout, retries=retries, delay=delay)
            if out == 'N/A':
                raise Exception("retry for find format=bit_rate")
        except Exception as ex:
            cmd = f"-v panic -select_streams V:0 -show_entries format=bit_rate -of default=nw=1:nk=1 '{input_file}'"
            ret, out, err = self.run(command=cmd, timeout=timeout)
        return out.strip()

    def get_video_size(
            self,
            input_file: str,
            timeout: int = None,
            retries: int = 0,
            delay: int = 1,
    ):
        command = f"-v panic -show_entries format=size -of default=nw=1:nk=1 '{input_file}'"
        ret, out, err = self.run(command=command, timeout=timeout, retries=retries, delay=delay)
        try:
            return int(out.strip().split()[-1])  # avoid pthread_create failed: Resource temporarily unavailable
        except ValueError:
            return -1

    def get_video_start_time(
            self,
            input_file: str,
            timeout: int = None,
            retries: int = 0,
            delay: int = 1,
    ):
        command = f'-v panic -select_streams v:0 -show_entries stream=start_time -of json {input_file}'
        ret, out, err = self.run(command=command, timeout=timeout, retries=retries, delay=delay)
        if ret != 0:
            raise Exception('get video start time fail')

        return float(json.loads(out)['streams'][0]['start_time'])

    # subtitle
    def get_subtitles(
            self,
            input_file: str,
            timeout: int = None,
            retries: int = 0,
            delay: int = 1,
    ) -> List[Dict]:
        command = [
            'ffprobe',
            '-v', 'quiet',  # Only show error messages
            '-select_streams', 's',  # Select only subtitle streams
            '-show_entries', 'stream=index:stream_tags=language,handler_name:codec_name:codec_type',
            # Stream index, tags and codecs
            '-of', 'json',  # Output format as JSON
            f'"{input_file}"'  # Input file path
        ]
        ret, out, err = self.run(command=command, timeout=timeout, retries=retries, delay=delay)
        if ret != 0:
            raise Exception(f'get subtitles error: {err}')
        try:
            streams = json.loads(out).get('streams', [])
        except json.JSONDecodeError as ex:
            raise Exception(f'JSON decode error: {str(ex)}')

        video_subtitle_list = []
        for stream in streams:
            if stream.get('codec_type') == 'subtitle':
                tags_to_lower = {i.lower(): j for i, j in stream.get("tags", {}).items()}
                video_subtitle_list.append({
                    "index": stream["index"],
                    "language": tags_to_lower.get("language", "und"),
                    "handler_name": tags_to_lower.get("handler_name", ""),
                    "codec_name": stream.get("codec_name", ""),
                    "codec_type": stream.get("codec_type", "")
                })
        return video_subtitle_list

    def get_subtitle_sequences(
            self,
            input_file,
            timeout: int = None,
            retries: int = 0,
            delay: int = 1
    ):
        command = [
            'ffprobe',
            '-v', 'panic',  # Only show error messages
            '-select_streams', 's',  # Select only subtitle streams
            '-show_entries', 'stream=index',  # Stream index
            '-of', 'json',  # Output format as JSON
            f'"{input_file}"'  # Input file path
        ]
        ret, out, err = self.run(command=command, timeout=timeout, retries=retries, delay=delay)
        if ret != 0:
            raise Exception(f'get subtitle sequence error: {err}')
        try:
            streams = json.loads(out).get('streams', [])
        except json.JSONDecodeError as ex:
            raise Exception(f'JSON decode error: {str(ex)}')
        return [str(x['index']) for x in streams]

    def get_subtitle_languages(
            self, input_file,
            timeout: int = None,
            retries: int = 0,
            delay: int = 1
    ):
        command = [
            'ffprobe',
            '-v', 'panic',  # Only show error messages
            '-select_streams', 's',  # Select only subtitle streams
            '-show_entries', 'stream=index:stream_tags=language',  # Stream index stream_tags language
            '-of', 'json',  # Output format as JSON
            f'"{input_file}"'  # Input file path
        ]
        ret, out, err = self.run(command=command, timeout=timeout, retries=retries, delay=delay)
        if ret != 0:
            raise Exception(f'get subtitle language error: {err}')
        try:
            streams = json.loads(out).get('streams', [])
        except json.JSONDecodeError as ex:
            raise Exception(f'JSON decode error: {str(ex)}')

        subtitle_list = []
        for stream in streams:
            tags_to_lower = {i.lower(): j for i, j in stream.get("tags", {}).items()}
            subtitle_list.append({"index": stream["index"], "language": tags_to_lower.get("language", "und")})
        return subtitle_list

    # metadata
    def file_is_broken(
            self,
            input_file: str,
            timeout: int = None,
            retries: int = 0,
            delay: int = 1,
    ):
        cmd = f"'{input_file}'"
        ret, out, err = self.run(command=cmd, timeout=timeout)
        return ret != 0

    def get_meta_info(
            self,
            input_file: str,
            timeout: int = None,
            retries: int = 0,
            delay: int = 1,
    ):
        cmd = f"-hide_banner '{input_file}'"
        ret, out, err = self.run(command=cmd, timeout=timeout)
        return out

    def get_origin_height(
            self,
            input_file: str,
            timeout: int = None,
            retries: int = 0,
            delay: int = 1,
    ):
        cmd = (f"-v panic -of flat=s=_ -select_streams v:0 -show_entries "
               f"stream=height -of default=noprint_wrappers=1:nokey=1 '{input_file}'")
        ret, out, err = self.run(command=cmd, timeout=timeout)
        try:
            return int(float(out.strip().split()[-1]))  # avoid pthread_create failed: Resource temporarily unavailable
        except Exception as ex:
            # 对于mov格式的容错性处理
            pattern = re.compile(r'(^\d+$)', re.M)
            m = pattern.search(out)
            if m:
                return int(float(m.group(0)))

            raise Exception("get video height error", str(ex))

    def get_origin_width(
            self,
            input_file: str,
            timeout: int = None,
            retries: int = 0,
            delay: int = 1,
    ):
        cmd = (f"-v panic -of flat=s=_ -select_streams v:0 -show_entries stream=width "
               f"-of default=noprint_wrappers=1:nokey=1 '{input_file}'")
        ret, out, err = self.run(command=cmd, timeout=timeout)
        if ret != 0:
            raise Exception("get video width error", None, ret, out)
        try:
            return int(float(out.strip().split()[-1]))  # avoid pthread_create failed: Resource temporarily unavailable
        except Exception as ex:
            raise Exception("get video width error", str(ex))

    def get_origin_proportion(
            self,
            input_file: str,
            timeout: int = None,
            retries: int = 0,
            delay: int = 1,
    ):
        try:
            height = self.get_origin_height(input_file, timeout=timeout)
            width = self.get_origin_width(input_file, timeout=timeout)
            return width * 1.0 / height
        except ValueError:
            return -1

    def get_audio_sample_rate(
            self,
            input_file: str,
            audio_index: int = None,
            timeout: int = None,
            retries: int = 0,
            delay: int = 1,
    ):
        cmd = f'-v panic -select_streams {audio_index} -show_entries stream=sample_rate -of json {input_file}'
        ret, out, err = self.run(command=cmd, timeout=timeout)
        if ret != 0:
            raise Exception('get audio language error')
        return int(json.loads(out)['streams'][0].get('sample_rate', 48000))

    def get_channel_count(
            self,
            input_file: str,
            audio_index: int = None,
            timeout: int = None,
            retries: int = 0,
            delay: int = 1,
    ):
        cmd = f'-v panic -show_entries stream=channels -select_streams {audio_index} -of json {input_file}'
        ret, out, err = self.run(command=cmd, timeout=timeout)
        if ret != 0 or not out:
            raise Exception('get audio channel count error')

        return json.loads(out)['streams'][0]['channels']

    def get_max_bitrate_video_stream(
            self,
            input_file: str,
            timeout: int = None,
            retries: int = 0,
            delay: int = 1,
    ):
        cmd = f'-v panic -show_entries stream=index,bit_rate -select_streams v -of csv=p=0:nk=1 {input_file}'
        ret, out, err = self.run(command=cmd, timeout=timeout)
        if ret != 0:
            raise Exception('get max bitrate video stream error')

        try:
            items = out.split('\n')
            items.sort(key=lambda x: int(x.split(',')[1]))
            return int(items[-1].split(',')[0])
        except Exception as e:
            codec_name = self.get_video_codec_name(input_file, timeout=timeout)
            if codec_name.startswith('vp'):
                return 0
            else:
                raise e

    def generate_duration(
            self,
            input_file: str,
            timeout: int = None,
            retries: int = 0,
            delay: int = 1,
    ):
        cmd = f"-v panic -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 '{input_file}'"
        ret, out, err = self.run(command=cmd, timeout=timeout)
        if ret != 0:
            errmsg = "generating duration error, generate duration failed!"
            raise Exception(errmsg, None, ret, out)
        try:
            message = out.strip().split()[-1]  # avoid pthread_create failed: Resource temporarily unavailable
            duration = int(float(message))
        except Exception as e:
            if 'webm' in input_file:
                cmd = f'-v panic -select_streams V -show_entries frame=pkt_pts_time -of csv=p=0:nk=1 {input_file}'
                ret, out, err = self.run(command=cmd, timeout=timeout)
                if ret != 0:
                    raise e
                lines = out.split('\n')
                line = ''
                count = len(lines) - 1
                while not line:
                    line = lines[count]
                    count -= 1
                if line:
                    return int(float(line))
                else:
                    raise e
            else:
                raise e

        return duration

    def get_framerate(
            self,
            input_file: str,
            timeout: int = None,
            retries: int = 0,
            delay: int = 1,
    ):
        cmd = (f"-v panic -select_streams v:0 -show_entries stream=avg_frame_rate "
               f"-of default=noprint_wrappers=1:nokey=1 {input_file}")
        ret, out, err = self.run(command=cmd, timeout=timeout)
        if ret != 0:
            raise Exception('get framerate error')
        message = out.strip().split()[-1]  # avoid pthread_create failed: Resource temporarily unavailable
        v1, v2 = message.split('/')
        if v1 == '0' or v2 == '0':
            return 0
        return int(round(float(v1) / float(v2), 0))

    def generate_framerate(
            self,
            input_file: str,
            timeout: int = None,
            retries: int = 0,
            delay: int = 1,
    ):
        cmd = (f"-v panic -select_streams v:0 -show_entries stream=avg_frame_rate "
               f"-of default=noprint_wrappers=1:nokey=1 {input_file}")
        ret, out, err = self.run(command=cmd, timeout=timeout)
        if ret != 0:
            raise Exception('generating framerate error')
        message = out.strip().split()[-1]  # avoid pthread_create failed: Resource temporarily unavailable
        if message not in self.framerate_mapping:
            v1, v2 = message.split('/')
            framerate_value = round(float(v1) / float(v2), 3)
            # 获取最接近的framerate
            max_value = 9999.9
            for k, v in self.framerate_mapping.items():
                if abs(framerate_value - float(v)) < max_value:
                    max_value = abs(framerate_value - float(v))
                    message = k

        return int(round(float(self.framerate_mapping[message]), 0))

    def get_src_video_info(
            self,
            input_file: str,
            timeout: int = None,
            retries: int = 0,
            delay: int = 1,
    ):
        if not os.path.isfile(input_file):
            raise Exception(f'{input_file} is not a file')
        cmd = f'-v panic -show_streams -of json "{input_file}"'
        ret, out, err = self.run(command=cmd, timeout=timeout)
        if ret != 0:
            raise Exception('get video src info fail')
        video_metadata = json.loads(out)
        audio_track = 0
        src_video_info = dict()
        for stream in video_metadata['streams']:
            if stream['codec_type'] == 'audio':
                audio_track += 1
            elif stream['codec_type'] == 'video' and stream.get('disposition', {}).get('attached_pic',
                                                                                       0) == 0 and not src_video_info:
                src_video_info['width'] = stream['width']
                src_video_info['height'] = stream['height']
                src_video_info['codec'] = stream.get('codec_name', '')
                src_video_info['profile'] = stream.get('profile', '')
                src_video_info['bitrate'] = stream.get('bit_rate', '')
                src_video_info['avg_frame_rate'] = stream.get('avg_frame_rate', '')
                src_video_info['sar'] = stream.get('sample_aspect_ratio', '1:1')

        src_video_info['audio_track'] = audio_track
        return src_video_info

    def get_video_stream_info(
            self,
            input_file: str,
            timeout: int = None,
            retries: int = 0,
            delay: int = 1,
    ):
        if not os.path.exists(input_file):
            raise Exception(f'file {input_file} not exists')

        cmd = f'v panic -select_streams v -show_streams -of json {input_file}'
        ret, out, err = self.run(command=cmd, timeout=10)
        if ret != 0:
            raise Exception('capture error {} when run {}'.format(out, cmd))

        return json.loads(out)['streams']

    def has_corrupt_frame(
            self,
            input_file: str,
            timeout: int = None,
            retries: int = 0,
            delay: int = 1,
    ):
        cmd = f'-v error -select_streams v -show_entries frame=pkt_pts_time -of csv=p=0:nk=1 {input_file}'
        ret, out, err = self.run(command=cmd, timeout=timeout)
        if ret != 0:
            return True
        if 'Corrupt frame detected' in out:
            return True

        return False

    def get_frame_count(
            self,
            input_file: str,
            timeout: int = None,
            retries: int = 0,
            delay: int = 1,
    ):
        cmd = f'-v panic -threads 1 -select_streams v -show_entries packet=pts_time,flags -of csv=p=0:nk=1 {input_file}'
        ret, out, err = self.run(command=cmd, timeout=timeout)
        if ret != 0:
            raise Exception('capture error {} when run {}'.format(out, cmd))

        return len(out.split('\n'))

    def is_video_file(
            self,
            input_file: str,
            timeout: int = None,
            retries: int = 0,
            delay: int = 1,
    ):
        try:
            cmd = f'-show_format -show_streams -select_streams V:0 -v panic -of json {input_file}'
            ret, out, err = self.run(command=cmd, timeout=timeout)
            if ret != 0:
                return False
            info = json.loads(out)
            if not info.get('format', {}).get('duration'):
                return False
            if not info.get('streams'):
                return False
            return True
        except Exception as e:
            print('detect file type failed, e={}'.format(e))
        return False

    def get_video_metadata(
            self,
            input_file: str,
            timeout: int = None,
            retries: int = 0,
            delay: int = 1,
    ):
        cmd = f"-v panic -of json -show_streams -show_format '{input_file}'"
        ret, out, err = self.run(command=cmd, timeout=timeout)
        if ret != 0:
            raise Exception(out)
        video_info = json.loads(out)
        return video_info

    def check_lack_pts(
            self,
            input_file: str,
            timeout: int = None,
            retries: int = 0,
            delay: int = 1,
    ):
        opt = ''
        video_bitrate, _ = self.get_origin_bitrate(input_file, timeout=timeout)
        if video_bitrate > 5600000:
            opt = '-read_intervals %10:00'
        template = (f"{opt} -v panic -of default=noprint_wrappers=1 -hide_banner -select_streams V:0 "
                    f"-show_packets -show_entries packet=pts '{input_file}'| grep 'pts=N/A' ")
        try:
            ret, out, err = self.run(template, timeout=timeout)
            if ret != 0:
                if out:
                    print("check_lack_pts error!", ret, out)
                return False
            else:
                if 'pts=N/A' in out:
                    return True
                return False
        except Exception as err:
            print("check_lack_pts error! {}".format(err))
            return False
