#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author  : nickdecodes
@Email   : nickdecodes@163.com
@Usage   :
@FileName: ffmpeg.py
@DateTime: 2024/7/2 14:09
@SoftWare: 
"""

from .ffmpeg_options import FFmpegOptions
from .exec import CommandExecutor


class FFmpeg(CommandExecutor, FFmpegOptions):
    def __init__(self, bin_path='ffmpeg', logger=None):
        super().__init__(bin_path=bin_path, logger=logger)
        self.commands = []

    # audio

    # video

    # subtitle

    # metadata
