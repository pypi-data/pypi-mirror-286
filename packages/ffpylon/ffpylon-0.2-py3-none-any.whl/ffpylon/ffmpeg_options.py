#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author  : nickdecodes
@Email   : nickdecodes@163.com
@Usage   :
@FileName: ffmpeg_options.py
@DateTime: 2024-07-22 17:58
@SoftWare: 
"""


from .meta import OptionMeta
from .exec import CommandExecutor


class FFmpegOptions(CommandExecutor, metaclass=OptionMeta):
    """
    https://ffmpeg.org/ffmpeg.html
    """
    options = [
        '-h',  # -- print basic options
        '-L',  # show license
        '-version',  # show version
        '-muxers',  # show available muxers
        '-demuxers',  # show available demuxers
        '-devices',  # show available devices
        '-decoders',  # show available decoders
        '-encoders',  # show available encoders
        '-filters',  # show available filters
        '-pix_fmts',  # show available pixel formats
        '-layouts',  # show standard channel layouts
        '-sample_fmts',  # show available audio sample formats
        '-help',  # <topic> show help
        '-buildconf',  # show build configuration
        '-formats',  # show available formats
        '-codecs',  # show available codecs
        '-bsfs',  # show available bit stream filters
        '-protocols',  # show available protocols
        '-dispositions',  # show available stream dispositions
        '-colors',  # show available color names
        '-sources',  # <device> list sources of the input device
        '-sinks',  # <device> list sinks of the output device
        '-hwaccels',  # show available HW acceleration methods
        '-v',  # <loglevel> set logging level
        '-y',  # overwrite output files
        '-n',  # never overwrite output files
        '-stats',  # print progress report during encoding
        '-loglevel',  # <loglevel> set logging level
        '-report',  # generate a report
        '-max_alloc',  # <bytes> set maximum size of a single allocated block
        '-cpuflags',  # <flags> force specific cpu flags
        '-cpucount',  # <count> force specific cpu count
        '-hide_banner',  # <hide_banner> do not show program banner
        '-ignore_unknown',  # Ignore unknown stream types
        '-copy_unknown',  # Copy unknown stream types
        '-recast_media',  # allow recasting stream type in order to force a decoder of different media type
        '-benchmark',  # add timings for benchmarking
        '-benchmark_all',  # add timings for each task
        '-progress',  # <url> write program-readable progress information
        '-stdin',  # enable or disable interaction on standard input
        '-timelimit',  # <limit> set max runtime in seconds in CPU user time
        '-dump',  # dump each input packet
        '-hex',  # when dumping packets, also dump the payload
        '-frame_drop_threshold',  # <> frame drop threshold
        '-copyts',  # copy timestamps
        '-start_at_zero',  # shift input timestamps to start at 0 when using copyts
        '-copytb',  # <mode> copy input stream time base when stream copying
        '-dts_delta_threshold',  # <threshold> timestamp discontinuity delta threshold
        '-dts_error_threshold',  # <threshold> timestamp error delta threshold
        '-xerror',  # <error> exit on error
        '-abort_on',  # <flags> abort on the specified condition flags
        '-filter_threads',  # number of non-complex filter threads
        '-filter_complex',  # <graph_description> create a complex filtergraph
        '-filter_complex_threads',  # number of threads for -filter_complex
        '-lavfi',  # <graph_description> create a complex filtergraph
        '-filter_complex_script',  # <filename> deprecated, use -/filter_complex instead
        '-auto_conversion_filters',  # enable automatic conversion filters globally
        '-stats_period',  # <time> set the period at which ffmpeg updates stats and -progress output
        '-debug_ts',  # print timestamp debugging info
        '-max_error_rate',  # <maximum error rate> ratio of decoding errors (0.0: no errors, 1.0: 100% errors) above which ffmpeg returns an error instead of success.
        '-vstats',  # dump video coding statistics to file
        '-vstats_file',  # <file> dump video coding statistics to file
        '-vstats_version',  # Version of the vstats format to use.
        '-sdp_file',  # <file> specify a file in which to print sdp information
        '-init_hw_device',  # <args> initialise hardware device
        '-filter_hw_device',  # <device> set hardware device used when filtering
        '-adrift_threshold',  # <threshold> deprecated, does nothing
        '-qphist',  # deprecated, does nothing
        '-vsync',  # <> set video sync method globally; deprecated, use -fps_mode
        '-f',  # <fmt> force container format (auto-detected otherwise)
        '-t',  # <duration> stop transcoding after specified duration
        '-to',  # <time_stop> stop transcoding after specified time is reached
        '-ss',  # <time_off> start transcoding at specified time
        '-bitexact',  # bitexact mode
        '-thread_queue_size',  # set the maximum number of queued packets from the demuxer
        '-sseof',  # <time_off> set the start time offset relative to EOF
        '-seek_timestamp',  # enable/disable seeking by timestamp with -ss
        '-accurate_seek',  # enable/disable accurate seeking with -ss
        '-isync',  # <sync ref> Indicate the input index for sync reference
        '-itsoffset',  # <time_off> set the input ts offset
        '-re',  # <> read input at native frame rate; equivalent to -readrate 1
        '-readrate',  # <speed> read input at specified rate
        '-readrate_initial_burst',  # <seconds> The initial amount of input to burst read before imposing any readrate
        '-dump_attachment',  # [:<spec>] <filename> extract an attachment into a file
        '-stream_loop',  # <loop count> set number of times input stream shall be looped
        '-find_stream_info',  # read and decode the streams to fill missing information with heuristics
        '-map',  # <[-]input_file_id[:stream_specifier][,sync_file_id[:stream_specifier]]> set input stream mapping
        '-map_metadata',  # [:<spec>] <outfile[,metadata]:infile[,metadata]> set metadata information of outfile from infile
        '-map_chapters',  # <input_file_index> set chapters mapping
        '-fs',  # <limit_size> set the limit file size in bytes
        '-timestamp',  # <time> set the recording timestamp ('now' to set the current time)
        '-program',  # [:<spec>] <title=string:st=number...> add program with specified streams
        '-stream_group',  # [:<spec>] <id=number:st=number...> add stream group with specified streams and group type-specific arguments
        '-dframes',  # <number> set the number of data frames to output
        '-target',  # <type> specify target file type ("vcd", "svcd", "dvd", "dv" or "dv50" with optional prefixes "pal-", "ntsc-" or "film-")
        '-shortest',  # finish encoding within shortest input
        '-shortest_buf_duration',  # maximum buffering duration (in seconds) for the -shortest option
        '-qscale',  # <q> use fixed quality scale (VBR)
        '-profile',  # <profile> set profile
        '-attach',  # <filename> add an attachment to the output file
        '-muxdelay',  # <seconds> set the maximum demux-decode delay
        '-muxpreload',  # <seconds> set the initial demux-decode delay
        '-fpre',  # <filename> set options from indicated preset file
        '-c',  # [:<stream_spec>] <codec> select encoder/decoder ('copy' to copy stream without reencoding)
        '-filter',  # [:<stream_spec>] <filter_graph> apply specified filters to audio/video
        '-codec',  # [:<stream_spec>] <codec> alias for -c (select encoder/decoder)
        '-pre',  # [:<stream_spec>] <preset> preset name
        '-itsscale',  # [:<stream_spec>] <scale> set the input ts scale
        '-apad',  # [:<stream_spec>] <> audio pad
        '-copyinkf',  # [:<stream_spec>] copy initial non-keyframes
        '-copypriorss',  # [:<stream_spec>] copy or discard frames before start time
        '-frames',  # [:<stream_spec>] <number> set the number of frames to output
        '-tag',  # [:<stream_spec>] <fourcc/tag> force codec tag/fourcc
        '-q',  # [:<stream_spec>] <q> use fixed quality scale (VBR)
        '-filter_script',  # [:<stream_spec>] <filename> deprecated, use -/filter
        '-reinit_filter',  # [:<stream_spec>] <> reinit filtergraph on input parameter changes
        '-discard',  # [:<stream_spec>] <> discard
        '-disposition',  # [:<stream_spec>] <> disposition
        '-bits_per_raw_sample',  # [:<stream_spec>] <number> set the number of bits per raw sample
        '-stats_enc_pre',  # [:<stream_spec>] write encoding stats before encoding
        '-stats_enc_post',  # [:<stream_spec>] write encoding stats after encoding
        '-stats_mux_pre',  # [:<stream_spec>] write packets stats before muxing
        '-stats_enc_pre_fmt',  # [:<stream_spec>] format of the stats written with -stats_enc_pre
        '-stats_enc_post_fmt',  # [:<stream_spec>] format of the stats written with -stats_enc_post
        '-stats_mux_pre_fmt',  # [:<stream_spec>] format of the stats written with -stats_mux_pre
        '-autorotate',  # [:<stream_spec>] automatically insert correct rotate filters
        '-autoscale',  # [:<stream_spec>] automatically insert a scale filter at the end of the filter graph
        '-time_base',  # [:<stream_spec>] <ratio> set the desired time base hint for output stream (1:24, 1:48000 or 0.04166, 2.0833e-5)
        '-enc_time_base',  # [:<stream_spec>] <ratio> set the desired time base for the encoder (1:24, 1:48000 or 0.04166, 2.0833e-5). two special values are defined - 0 = use frame rate (video) or sample rate (audio),-1 = match source time base
        '-bsf',  # [:<stream_spec>] <bitstream_filters> A comma-separated list of bitstream filters
        '-max_muxing_queue_size',  # [:<stream_spec>] <packets> maximum number of packets that can be buffered while waiting for all streams to initialize
        '-muxing_queue_data_threshold',  # [:<stream_spec>] <bytes> set the threshold after which max_muxing_queue_size is taken into account
        '-r',  # [:<stream_spec>] <rate> override input framerate/convert to given output framerate (Hz value, fraction or abbreviation)
        '-aspect',  # [:<stream_spec>] <aspect> set aspect ratio (4:3, 16:9 or 1.3333, 1.7777)
        '-vn',  # disable video
        '-vcodec',  # <codec> alias for -c:v (select encoder/decoder for video streams)
        '-vf',  # <filter_graph> alias for -filter:v (apply filters to video streams)
        '-b',  # <bitrate> video bitrate (please use -b:v)
        '-vframes',  # <number> set the number of video frames to output
        '-fpsmax',  # [:<stream_spec>] <rate> set max frame rate (Hz value, fraction or abbreviation)
        '-pix_fmt',  # [:<stream_spec>] <format> set pixel format
        '-display_rotation',  # [:<stream_spec>] <angle> set pure counter-clockwise rotation in degrees for stream(s)
        '-display_hflip',  # [:<stream_spec>] set display horizontal flip for stream(s) (overrides any display rotation if it is not set)
        '-display_vflip',  # [:<stream_spec>] set display vertical flip for stream(s) (overrides any display rotation if it is not set)
        '-rc_override',  # [:<stream_spec>] <override> rate control override for specific intervals
        '-timecode',  # <hh:mm:ss[:;.]ff> set initial TimeCode value.
        '-passlogfile',  # [:<stream_spec>] <prefix> select two pass log file name prefix
        '-intra_matrix',  # [:<stream_spec>] <matrix> specify intra matrix coeffs
        '-inter_matrix',  # [:<stream_spec>] <matrix> specify inter matrix coeffs
        '-chroma_intra_matrix',  # [:<stream_spec>] <matrix> specify intra matrix coeffs
        '-vtag',  # <fourcc/tag> force video tag/fourcc
        '-fps_mode',  # [:<stream_spec>] set framerate mode for matching video streams; overrides vsync
        '-force_fps',  # [:<stream_spec>] force the selected framerate, disable the best supported framerate selection
        '-streamid',  # <streamIndex:value> set the value of an outfile streamid
        '-force_key_frames',  # [:<stream_spec>] <timestamps> force key frames at specified timestamps
        '-hwaccel',  # [:<stream_spec>] <hwaccel name> use HW accelerated decoding
        '-hwaccel_device',  # [:<stream_spec>] <devicename> select a device for HW acceleration
        '-hwaccel_output_format',  # [:<stream_spec>] <format> select output format used with HW accelerated decoding
        '-fix_sub_duration_heartbeat',  # [:<stream_spec>] set this video output stream to be a heartbeat stream for fix_sub_duration, according to which subtitles should be split at random access points
        '-vpre',  # <preset> set the video options to the indicated preset
        '-top',  # [:<stream_spec>] <> deprecated, use the setfield video filter
        '-aq',  # <quality> set audio quality (codec-specific)
        '-ar',  # [:<stream_spec>] <rate> set audio sampling rate (in Hz)
        '-ac',  # [:<stream_spec>] <channels> set number of audio channels
        '-an',  # disable audio
        '-acodec',  # <codec> alias for -c:a (select encoder/decoder for audio streams)
        '-ab',  # <bitrate> alias for -b:a (select bitrate for audio streams)
        '-af',  # <filter_graph> alias for -filter:a (apply filters to audio streams)
        '-aframes',  # <number> set the number of audio frames to output
        '-atag',  # <fourcc/tag> force audio tag/fourcc
        '-sample_fmt',  # [:<stream_spec>] <format> set sample format
        '-channel_layout',  # [:<stream_spec>] <layout> set channel layout
        '-ch_layout',  # [:<stream_spec>] <layout> set channel layout
        '-guess_layout_max',  # [:<stream_spec>] set the maximum number of channels to try to guess the channel layout
        '-apre',  # <preset> set the audio options to the indicated preset
        '-sn',  # disable subtitle
        '-scodec',  # <codec> alias for -c:s (select encoder/decoder for subtitle streams)
        '-stag',  # <fourcc/tag> force subtitle tag/fourcc
        '-fix_sub_duration',  # [:<stream_spec>] fix subtitles duration
        '-canvas_size',  # [:<stream_spec>] <size> set canvas size (WxH or abbreviation)
        '-spre',  # <preset> set the subtitle options to the indicated preset
        '-dcodec',  # <codec> alias for -c:d (select encoder/decoder for data streams)
        '-dn',  # disable data
        '-bt',  # <int> E..VA...... Set video bitrate tolerance (in bits/s). In 1-pass mode, bitrate tolerance specifies how far ratecontrol is willing to deviate from the target average bitrate value. This is not related to minimum/maximum bitrate. Lowering tolerance too much has an adverse effect on quality. (from 0 to INT_MAX) (default 4000000)
        '-flags',  # <flags> ED.VAS..... (default 0)
        '-flags2',  # <flags> ED.VAS..... (default 0)
        '-export_side_data',  # <flags> ED.VAS..... Export metadata as side data (default 0)
        '-g',  # <int> E..V....... set the group of picture (GOP) size (from INT_MIN to INT_MAX) (default 12)
        '-cutoff',  # <int> E...A...... set cutoff bandwidth (from INT_MIN to INT_MAX) (default 0)
        '-frame_size',  # <int> E...A...... (from 0 to INT_MAX) (default 0)
        '-qcomp',  # <float> E..V....... video quantizer scale compression (VBR). Constant of ratecontrol equation. Recommended range for default rc_eq: 0.0-1.0 (from -FLT_MAX to FLT_MAX) (default 0.5)
        '-qblur',  # <float> E..V....... video quantizer scale blur (VBR) (from -1 to FLT_MAX) (default 0.5)
        '-qmin',  # <int> E..V....... minimum video quantizer scale (VBR) (from -1 to 69) (default 2)
        '-qmax',  # <int> E..V....... maximum video quantizer scale (VBR) (from -1 to 1024) (default 31)
        '-qdiff',  # <int> E..V....... maximum difference between the quantizer scales (VBR) (from INT_MIN to INT_MAX) (default 3)
        '-bf',  # <int> E..V....... set maximum number of B-frames between non-B-frames (from -1 to INT_MAX) (default 0)
        '-b_qfactor',  # <float> E..V....... QP factor between P- and B-frames (from -FLT_MAX to FLT_MAX) (default 1.25)
        '-bug',  # <flags> .D.V....... work around not autodetected encoder bugs (default autodetect)
        '-strict',  # <int> ED.VA...... how strictly to follow the standards (from INT_MIN to INT_MAX) (default normal)
        '-b_qoffset',  # <float> E..V....... QP offset between P- and B-frames (from -FLT_MAX to FLT_MAX) (default 1.25)
        '-err_detect',  # <flags> ED.VAS..... set error detection flags (default 0)
        '-maxrate',  # <int64> E..VA...... maximum bitrate (in bits/s). Used for VBV together with bufsize. (from 0 to INT_MAX) (default 0)
        '-minrate',  # <int64> E..VA...... minimum bitrate (in bits/s). Most useful in setting up a CBR encode. It is of little use otherwise. (from INT_MIN to INT_MAX) (default 0)
        '-bufsize',  # <int> E..VA...... set ratecontrol buffer size (in bits) (from INT_MIN to INT_MAX) (default 0)
        '-i_qfactor',  # <float> E..V....... QP factor between P- and I-frames (from -FLT_MAX to FLT_MAX) (default -0.8)
        '-i_qoffset',  # <float> E..V....... QP offset between P- and I-frames (from -FLT_MAX to FLT_MAX) (default 0)
        '-dct',  # <int> E..V....... DCT algorithm (from 0 to INT_MAX) (default auto)
        '-lumi_mask',  # <float> E..V....... compresses bright areas stronger than medium ones (from -FLT_MAX to FLT_MAX) (default 0)
        '-tcplx_mask',  # <float> E..V....... temporal complexity masking (from -FLT_MAX to FLT_MAX) (default 0)
        '-scplx_mask',  # <float> E..V....... spatial complexity masking (from -FLT_MAX to FLT_MAX) (default 0)
        '-p_mask',  # <float> E..V....... inter masking (from -FLT_MAX to FLT_MAX) (default 0)
        '-dark_mask',  # <float> E..V....... compresses dark areas stronger than medium ones (from -FLT_MAX to FLT_MAX) (default 0)
        '-idct',  # <int> ED.V....... select IDCT implementation (from 0 to INT_MAX) (default auto)
        '-ec',  # <flags> .D.V....... set error concealment strategy (default guess_mvs+deblock)
        '-sar',  # <rational> E..V....... sample aspect ratio (from 0 to 10) (default 0/1)
        '-debug',  # <flags> ED.VAS..... print specific debug info (default 0)
        '-dia_size',  # <int> E..V....... diamond type & size for motion estimation (from INT_MIN to INT_MAX) (default 0)
        '-last_pred',  # <int> E..V....... amount of motion predictors from the previous frame (from INT_MIN to INT_MAX) (default 0)
        '-pre_dia_size',  # <int> E..V....... diamond type & size for motion estimation pre-pass (from INT_MIN to INT_MAX) (default 0)
        '-subq',  # <int> E..V....... sub-pel motion estimation quality (from INT_MIN to INT_MAX) (default 8)
        '-me_range',  # <int> E..V....... limit motion vectors range (1023 for DivX player) (from INT_MIN to INT_MAX) (default 0)
        '-global_quality',  # <int> E..VA...... (from INT_MIN to INT_MAX) (default 0)
        '-mbd',  # <int> E..V....... macroblock decision algorithm (high quality mode) (from 0 to 2) (default simple)
        '-rc_init_occupancy',  # <int> E..V....... number of bits which should be loaded into the rc buffer before decoding starts (from INT_MIN to INT_MAX) (default 0)
        '-threads',  # <int> ED.VA...... set the number of threads (from 0 to INT_MAX) (default 1)
        '-dc',  # <int> E..V....... intra_dc_precision (from -8 to 16) (default 0)
        '-nssew',  # <int> E..V....... nsse weight (from INT_MIN to INT_MAX) (default 8)
        '-skip_top',  # <int> .D.V....... number of macroblock rows at the top which are skipped (from INT_MIN to INT_MAX) (default 0)
        '-skip_bottom',  # <int> .D.V....... number of macroblock rows at the bottom which are skipped (from INT_MIN to INT_MAX) (default 0)
        '-level',  # <int> E..VA...... encoding level, usually corresponding to the profile level, codec-specific (from INT_MIN to INT_MAX) (default unknown)
        '-lowres',  # <int> .D.VA...... decode at 1= 1/2, 2=1/4, 3=1/8 resolutions (from 0 to INT_MAX) (default 0)
        '-cmp',  # <int> E..V....... full-pel ME compare function (from INT_MIN to INT_MAX) (default sad)
        '-subcmp',  # <int> E..V....... sub-pel ME compare function (from INT_MIN to INT_MAX) (default sad)
        '-mbcmp',  # <int> E..V....... macroblock compare function (from INT_MIN to INT_MAX) (default sad)
        '-ildctcmp',  # <int> E..V....... interlaced DCT compare function (from INT_MIN to INT_MAX) (default vsad)
        '-precmp',  # <int> E..V....... pre motion estimation compare function (from INT_MIN to INT_MAX) (default sad)
        '-mblmin',  # <int> E..V....... minimum macroblock Lagrange factor (VBR) (from 1 to 32767) (default 236)
        '-mblmax',  # <int> E..V....... maximum macroblock Lagrange factor (VBR) (from 1 to 32767) (default 3658)
        '-skip_loop_filter',  # <int> .D.V....... skip loop filtering process for the selected frames (from INT_MIN to INT_MAX) (default default)
        '-skip_idct',  # <int> .D.V....... skip IDCT/dequantization for the selected frames (from INT_MIN to INT_MAX) (default default)
        '-skip_frame',  # <int> .D.V....... skip decoding for the selected frames (from INT_MIN to INT_MAX) (default default)
        '-bidir_refine',  # <int> E..V....... refine the two motion vectors used in bidirectional macroblocks (from 0 to 4) (default 1)
        '-keyint_min',  # <int> E..V....... minimum interval between IDR-frames (from INT_MIN to INT_MAX) (default 25)
        '-refs',  # <int> E..V....... reference frames to consider for motion compensation (from INT_MIN to INT_MAX) (default 1)
        '-trellis',  # <int> E..VA...... rate-distortion optimal quantization (from INT_MIN to INT_MAX) (default 0)
        '-mv0_threshold',  # <int> E..V....... (from 0 to INT_MAX) (default 256)
        '-compression_level',  # <int> E..VA...... (from INT_MIN to INT_MAX) (default -1)
        '-rc_max_vbv_use',  # <float> E..V....... (from 0 to FLT_MAX) (default 0)
        '-rc_min_vbv_use',  # <float> E..V....... (from 0 to FLT_MAX) (default 3)
        '-ticks_per_frame',  # <int> ED.VA...... (from 1 to INT_MAX) (default 1)
        '-color_primaries',  # <int> ED.V....... color primaries (from 1 to INT_MAX) (default unknown)
        '-color_trc',  # <int> ED.V....... color transfer characteristics (from 1 to INT_MAX) (default unknown)
        '-colorspace',  # <int> ED.V....... color space (from 0 to INT_MAX) (default unknown)
        '-color_range',  # <int> ED.V....... color range (from 0 to INT_MAX) (default unknown)
        '-chroma_sample_location',  # <int> ED.V....... chroma sample location (from 0 to INT_MAX) (default unknown)
        '-slices',  # <int> E..V....... set the number of slices, used in parallelized encoding (from 0 to INT_MAX) (default 0)
        '-thread_type',  # <flags> ED.VA...... select multithreading type (default slice+frame)
        '-audio_service_type',  # <int> E...A...... audio service type (from 0 to 8) (default ma)
        '-request_sample_fmt',  # <sample_fmt> .D..A...... sample format audio decoders should prefer (default none)
        '-sub_charenc',  # <string> .D...S..... set input text subtitles character encoding
        '-sub_charenc_mode',  # <flags> .D...S..... set input text subtitles character encoding mode (default 0)
        '-apply_cropping',  # <boolean> .D.V....... (default true)
        '-skip_alpha',  # <boolean> .D.V....... Skip processing alpha (default false)
        '-field_order',  # <int> ED.V....... Field order (from 0 to 5) (default 0)
        '-dump_separator',  # <string> ED.VAS..... set information dump field separator
        '-codec_whitelist',  # <string> .D.VAS..... List of decoders that are allowed to be used
        '-max_pixels',  # <int64> ED.VAS..... Maximum number of pixels (from 0 to INT_MAX) (default INT_MAX)
        '-max_samples',  # <int64> ED..A...... Maximum number of samples (from 0 to INT_MAX) (default INT_MAX)
        '-hwaccel_flags',  # <flags> .D.V....... (default ignore_level)
        '-extra_hw_frames',  # <int> .D.V....... Number of extra hardware frames to allocate for the user (from -1 to INT_MAX) (default -1)
        '-discard_damaged_percentage',  # <int> .D.V....... Percentage of damaged samples to discard a frame (from 0 to 100) (default 95)
        '-side_data_prefer_packet',  # [<int> ].D.VAS..... Comma-separated list of side data types for which user-supplied (container) data is preferred over coded bytestream
        '-mpv_flags',  # <flags> E..V....... Flags common for all mpegvideo-based encoders. (default 0)
        '-luma_elim_threshold',  # <int> E..V....... single coefficient elimination threshold for luminance (negative values also consider dc coefficient) (from INT_MIN to INT_MAX) (default 0)
        '-chroma_elim_threshold',  # <int> E..V....... single coefficient elimination threshold for chrominance (negative values also consider dc coefficient) (from INT_MIN to INT_MAX) (default 0)
        '-quantizer_noise_shaping',  # <int> E..V....... (from 0 to INT_MAX) (default 0)
        '-error_rate',  # <int> E..V....... Simulate errors in the bitstream to test error concealment. (from 0 to INT_MAX) (default 0)
        '-qsquish',  # <float> E..V....... how to keep quantizer between qmin and qmax (0 = clip, 1 = use differentiable function) (from 0 to 99) (default 0)
        '-rc_qmod_amp',  # <float> E..V....... experimental quantizer modulation (from -FLT_MAX to FLT_MAX) (default 0)
        '-rc_qmod_freq',  # <int> E..V....... experimental quantizer modulation (from INT_MIN to INT_MAX) (default 0)
        '-rc_eq',  # <string> E..V....... Set rate control equation. When computing the expression, besides the standard functions defined in the section 'Expression Evaluation', the following functions are available: bits2qp(bits), qp2bits(qp). Also the following constants are available: iTex pTex tex mv fCode iCount mcVar var isI isP isB avgQP qComp avgIITex avgPITex avgPPTex avgBPTex avgTex.
        '-rc_init_cplx',  # <float> E..V....... initial complexity for 1-pass encoding (from -FLT_MAX to FLT_MAX) (default 0)
        '-rc_buf_aggressivity',  # <float> E..V....... currently useless (from -FLT_MAX to FLT_MAX) (default 1)
        '-border_mask',  # <float> E..V....... increase the quantizer for macroblocks close to borders (from -FLT_MAX to FLT_MAX) (default 0)
        '-lmin',  # <int> E..V....... minimum Lagrange factor (VBR) (from 0 to INT_MAX) (default 236)
        '-lmax',  # <int> E..V....... maximum Lagrange factor (VBR) (from 0 to INT_MAX) (default 3658)
        '-skip_threshold',  # <int> E..V....... Frame skip threshold (from INT_MIN to INT_MAX) (default 0)
        '-skip_factor',  # <int> E..V....... Frame skip factor (from INT_MIN to INT_MAX) (default 0)
        '-skip_exp',  # <int> E..V....... Frame skip exponent (from INT_MIN to INT_MAX) (default 0)
        '-skip_cmp',  # <int> E..V....... Frame skip compare function (from INT_MIN to INT_MAX) (default dctmax)
        '-sc_threshold',  # <int> E..V....... Scene change threshold (from INT_MIN to INT_MAX) (default 0)
        '-noise_reduction',  # <int> E..V....... Noise reduction (from INT_MIN to INT_MAX) (default 0)
        '-ps',  # <int> E..V....... RTP payload size in bytes (from INT_MIN to INT_MAX) (default 0)
        '-huffman',  # <int> E..V....... Huffman table strategy (from 0 to 1) (default optimal)
        '-force_duplicated_matrix',  # <boolean> E..V....... Always write luma and chroma matrix for mjpeg, useful for rtp streaming. (default false)
        '-dpi',  # <int> E..V....... Set image resolution (in dots per inch) (from 0 to 65536) (default 0)
        '-dpm',  # <int> E..V....... Set image resolution (in dots per meter) (from 0 to 65536) (default 0)
        '-pred',  # <int> E..V....... Prediction method (from 0 to 5) (default none)
        '-max_extra_cb_iterations',  # <int> E..V....... Max extra codebook recalculation passes, more is better and slower (from 0 to INT_MAX) (default 2)
        '-skip_empty_cb',  # <boolean> E..V....... Avoid wasting bytes, ignore vintage MacOS decoder (default false)
        '-max_strips',  # <int> E..V....... Limit strips/frame, vintage compatible is 1..3, otherwise the more the better (from 1 to 32) (default 3)
        '-min_strips',  # <int> E..V....... Enforce min strips/frame, more is worse and faster, must be <= max_strips (from 1 to 32) (default 1)
        '-strip_number_adaptivity',  # <int> E..V....... How fast the strip number adapts, more is slightly better, much slower (from 0 to 31) (default 0)
        '-nitris_compat',  # <boolean> E..V....... encode with Avid Nitris compatibility (default false)
        '-ibias',  # <int> E..V....... intra quant bias (from INT_MIN to INT_MAX) (default 0)
        '-compression',  # <int> E..V....... set compression type (from 0 to 3) (default none)
        '-format',  # <int> E..V....... set pixel type (from 1 to 2) (default float)
        '-gamma',  # <float> E..V....... set gamma (from 0.001 to FLT_MAX) (default 1)
        '-slicecrc',  # <boolean> E..V....... Protect slices with CRCs (default auto)
        '-coder',  # <int> E..V....... Coder type (from -2 to 2) (default rice)
        '-context',  # <int> E..V....... Context model (from 0 to 1) (default 0)
        '-non_deterministic',  # <boolean> E..V....... Allow multithreading for e.g. context=1 at the expense of determinism (default false)
        '-motion_est',  # <int> E..V....... motion estimation algorithm (from 0 to 2) (default epzs)
        '-mepc',  # <int> E..V....... Motion estimation bitrate penalty compensation (1.0 = 256) (from INT_MIN to INT_MAX) (default 256)
        '-mepre',  # <int> E..V....... pre motion estimation (from INT_MIN to INT_MAX) (default 0)
        '-intra_penalty',  # <int> E..V....... Penalty for intra blocks in block decision (from 0 to 1.07374e+09) (default 0)
        '-gifflags',  # <flags> E..V....... set GIF flags (default offsetting+transdiff)
        '-gifimage',  # <boolean> E..V....... enable encoding only images per frame (default false)
        '-global_palette',  # <boolean> E..V....... write a palette to the global gif header where feasible (default true)
        '-obmc',  # <boolean> E..V....... use overlapped block motion compensation. (default false)
        '-mb_info',  # <int> E..V....... emit macroblock info for RFC 2190 packetization, the parameter value is the maximum payload size (from 0 to INT_MAX) (default 0)
        '-umv',  # <boolean> E..V....... Use unlimited motion vectors. (default false)
        '-aiv',  # <boolean> E..V....... Use alternative inter VLC. (default false)
        '-structured_slices',  # <boolean> E..V....... Write slice start position at every GOB header instead of just GOB number. (default false)
        '-chunks',  # <int> E..V....... chunk count (from 1 to 64) (default 1)
        '-compressor',  # <int> E..V....... second-stage compressor (from 160 to 176) (default snappy)
        '-tile_width',  # <int> E..V....... Tile Width (from 1 to 1.07374e+09) (default 256)
        '-tile_height',  # <int> E..V....... Tile Height (from 1 to 1.07374e+09) (default 256)
        '-sop',  # <int> E..V....... SOP marker (from 0 to 1) (default 0)
        '-eph',  # <int> E..V....... EPH marker (from 0 to 1) (default 0)
        '-prog',  # <int> E..V....... Progression Order (from 0 to 4) (default lrcp)
        '-layer_rates',  # <string> E..V....... Layer Rates
        '-gop_timecode',  # <string> E..V....... MPEG GOP Timecode in hh:mm:ss[:;.]ff format. Overrides timecode_frame_start.
        '-drop_frame_timecode',  # <boolean> E..V....... Timecode is in drop frame format. (default false)
        '-scan_offset',  # <boolean> E..V....... Reserve space for SVCD scan offset user data. (default false)
        '-timecode_frame_start',  # <int64> E..V....... GOP timecode frame start number, in non-drop-frame format (from -1 to I64_MAX) (default -1)
        '-b_strategy',  # <int> E..V....... Strategy to choose between I/P/B-frames (from 0 to 2) (default 0)
        '-b_sensitivity',  # <int> E..V....... Adjust sensitivity of b_frame_strategy 1 (from 1 to INT_MAX) (default 40)
        '-brd_scale',  # <int> E..V....... Downscale frames for dynamic B-frame decision (from 0 to 3) (default 0)
        '-intra_vlc',  # <boolean> E..V....... Use MPEG-2 intra VLC table. (default false)
        '-non_linear_quant',  # <boolean> E..V....... Use nonlinear quantizer. (default false)
        '-alternate_scan',  # <boolean> E..V....... Enable alternate scantable. (default false)
        '-a53cc',  # <boolean> E..V....... Use A53 Closed Captions (if available) (default true)
        '-seq_disp_ext',  # <int> E..V....... Write sequence_display_extension blocks. (from -1 to 1) (default auto)
        '-video_format',  # <int> E..V....... Video_format in the sequence_display_extension indicating the source of the video. (from 0 to 7) (default unspecified)
        '-data_partitioning',  # <boolean> E..V....... Use data partitioning. (default false)
        '-mpeg_quant',  # <int> E..V....... Use MPEG quantizers instead of H.263 (from 0 to 1) (default 0)
        '-vendor',  # <string> E..V....... vendor ID (default "fmpg")
        '-mbs_per_slice',  # <int> E..V....... macroblocks per slice (from 1 to 8) (default 8)
        '-bits_per_mb',  # <int> E..V....... desired bits per macroblock (from 0 to 8192) (default 0)
        '-quant_mat',  # <int> E..V....... quantiser matrix (from -1 to 6) (default auto)
        '-alpha_bits',  # <int> E..V....... bits for alpha plane (from 0 to 16) (default 16)
        '-skip_frame_thresh',  # <int> E..V....... (from 0 to 24) (default 1)
        '-start_one_color_thresh',  # <int> E..V....... (from 0 to 24) (default 1)
        '-continue_one_color_thresh',  # <int> E..V....... (from 0 to 24) (default 0)
        '-sixteen_color_thresh',  # <int> E..V....... (from 0 to 24) (default 1)
        '-memc_only',  # <boolean> E..V....... Only do ME/MC (I frames -> ref, P frame -> ME+MC). (default false)
        '-no_bitstream',  # <boolean> E..V....... Skip final bitstream writeout. (default false)
        '-iterative_dia_size',  # <int> E..V....... Dia size for the iterative ME (from 0 to INT_MAX) (default 0)
        '-compression_algo',  # <int> E..V....... (from 1 to 32946) (default packbits)
        '-tolerance',  # <double> E..V....... Max undershoot in percent (from 0 to 45) (default 5)
        '-slice_width',  # <int> E..V....... Slice width (from 32 to 1024) (default 32)
        '-slice_height',  # <int> E..V....... Slice height (from 8 to 1024) (default 16)
        '-wavelet_depth',  # <int> E..V....... Transform depth (from 1 to 5) (default 4)
        '-wavelet_type',  # <int> E..V....... Transform type (from 0 to 7) (default 9_7)
        '-qm',  # <int> E..V....... Custom quantization matrix (from 0 to 3) (default default)
        '-aac_coder',  # <int> E...A...... Coding algorithm (from 0 to 2) (default twoloop)
        '-aac_ms',  # <boolean> E...A...... Force M/S stereo coding (default auto)
        '-aac_is',  # <boolean> E...A...... Intensity stereo coding (default true)
        '-aac_pns',  # <boolean> E...A...... Perceptual noise substitution (default true)
        '-aac_tns',  # <boolean> E...A...... Temporal noise shaping (default true)
        '-aac_ltp',  # <boolean> E...A...... Long term prediction (default false)
        '-aac_pred',  # <boolean> E...A...... AAC-Main prediction (default false)
        '-aac_pce',  # <boolean> E...A...... Forces the use of PCEs (default false)
        '-center_mixlev',  # <float> E...A...... Center Mix Level (from 0 to 1) (default 0.594604)
        '-surround_mixlev',  # <float> E...A...... Surround Mix Level (from 0 to 1) (default 0.5)
        '-mixing_level',  # <int> E...A...... Mixing Level (from -1 to 111) (default -1)
        '-room_type',  # <int> E...A...... Room Type (from -1 to 2) (default -1)
        '-per_frame_metadata',  # <boolean> E...A...... Allow Changing Metadata Per-Frame (default false)
        '-copyright',  # <int> E...A...... Copyright Bit (from -1 to 1) (default -1)
        '-dialnorm',  # <int> E...A...... Dialogue Level (dB) (from -31 to -1) (default -31)
        '-dsur_mode',  # <int> E...A...... Dolby Surround Mode (from -1 to 2) (default -1)
        '-original',  # <int> E...A...... Original Bit Stream (from -1 to 1) (default -1)
        '-dmix_mode',  # <int> E...A...... Preferred Stereo Downmix Mode (from -1 to 3) (default -1)
        '-ltrt_cmixlev',  # <float> E...A...... Lt/Rt Center Mix Level (from -1 to 2) (default -1)
        '-ltrt_surmixlev',  # <float> E...A...... Lt/Rt Surround Mix Level (from -1 to 2) (default -1)
        '-loro_cmixlev',  # <float> E...A...... Lo/Ro Center Mix Level (from -1 to 2) (default -1)
        '-loro_surmixlev',  # <float> E...A...... Lo/Ro Surround Mix Level (from -1 to 2) (default -1)
        '-dsurex_mode',  # <int> E...A...... Dolby Surround EX Mode (from -1 to 3) (default -1)
        '-dheadphone_mode',  # <int> E...A...... Dolby Headphone Mode (from -1 to 2) (default -1)
        '-ad_conv_type',  # <int> E...A...... A/D Converter Type (from -1 to 1) (default -1)
        '-stereo_rematrixing',  # <boolean> E...A...... Stereo Rematrixing (default true)
        '-channel_coupling',  # <int> E...A...... Channel Coupling (from -1 to 1) (default auto)
        '-cpl_start_band',  # <int> E...A...... Coupling Start Band (from -1 to 15) (default auto)
        '-min_prediction_order',  # <int> E...A...... (from 1 to 30) (default 4)
        '-max_prediction_order',  # <int> E...A...... (from 1 to 30) (default 6)
        '-lpc_coeff_precision',  # <int> E...A...... LPC coefficient precision (from 0 to 15) (default 15)
        '-lpc_type',  # <int> E...A...... LPC algorithm (from -1 to 3) (default -1)
        '-lpc_passes',  # <int> E...A...... Number of passes to use for Cholesky factorization during LPC analysis (from 1 to INT_MAX) (default 2)
        '-min_partition_order',  # <int> E...A...... (from -1 to 8) (default -1)
        '-max_partition_order',  # <int> E...A...... (from -1 to 8) (default -1)
        '-prediction_order_method',  # <int> E...A...... Search method for selecting prediction order (from -1 to 5) (default -1)
        '-ch_mode',  # <int> E...A...... Stereo decorrelation mode (from -1 to 3) (default auto)
        '-exact_rice_parameters',  # <boolean> E...A...... Calculate rice parameters exactly (default false)
        '-multi_dim_quant',  # <boolean> E...A...... Multi-dimensional quantization (default false)
        '-max_interval',  # <int> E...A...... Max number of frames between each new header (from 8 to 128) (default 16)
        '-codebook_search',  # <int> E...A...... Max number of codebook searches (from 1 to 100) (default 3)
        '-prediction_order',  # <int> E...A...... Search method for selecting prediction order (from 0 to 4) (default estimation)
        '-rematrix_precision',  # <int> E...A...... Rematrix coefficient precision (from 0 to 14) (default 1)
        '-opus_delay',  # <float> E...A...... Maximum delay in milliseconds (from 2.5 to 360) (default 360)
        '-apply_phase_inv',  # <boolean> E...A...... Apply intensity stereo phase inversion (default true)
        '-sbc_delay',  # <duration> E...A...... set maximum algorithmic latency (default 0.013)
        '-msbc',  # <boolean> E...A...... use mSBC mode (wideband speech mono SBC) (default false)
        '-joint_stereo',  # <boolean> E...A...... (default auto)
        '-optimize_mono',  # <boolean> E...A...... (default false)
        '-block_size',  # <int> E...A...... set the block size (from 32 to 8192) (default 1024)
        '-code_size',  # <int> E...A...... Bits per code (from 2 to 5) (default 4)
        '-palette',  # <string> E....S..... set the global palette
        '-even_rows_fix',  # <boolean> E....S..... Make number of rows even (workaround for some players) (default false)
        '-aac_at_mode',  # <int> E...A...... ratecontrol mode (from -1 to 3) (default auto)
        '-aac_at_quality',  # <int> E...A...... quality vs speed control (from 0 to 2) (default 0)
        '-cpu',  # -used <int> E..V....... Quality/Speed ratio modifier (from 0 to 8) (default 1)
        '-auto',  # -alt-ref <int> E..V....... Enable use of alternate reference frames (2-pass only) (from -1 to 2) (default -1)
        '-lag',  # -in-frames <int> E..V....... Number of frames to look ahead at for alternate reference frame selection (from -1 to INT_MAX) (default -1)
        '-arnr',  # -max-frames <int> E..V....... altref noise reduction max frame count (from -1 to INT_MAX) (default -1)
        '-error',  # -resilience <flags> E..V....... Error resilience configuration (default 0)
        '-crf',  # <int> E..V....... Select the quality for constant quality mode (from -1 to 63) (default -1)
        '-static',  # -thresh <int> E..V....... A change threshold on blocks below which they will be skipped by the encoder (from 0 to INT_MAX) (default 0)
        '-drop',  # -threshold <int> E..V....... Frame drop threshold (from INT_MIN to INT_MAX) (default 0)
        '-denoise',  # -noise-level <int> E..V....... Amount of noise to be removed (from -1 to INT_MAX) (default -1)
        '-undershoot',  # -pct <int> E..V....... Datarate undershoot (min) target (%) (from -1 to 100) (default -1)
        '-overshoot',  # -pct <int> E..V....... Datarate overshoot (max) target (%) (from -1 to 1000) (default -1)
        '-minsection',  # -pct <int> E..V....... GOP min bitrate (% of target) (from -1 to 100) (default -1)
        '-maxsection',  # -pct <int> E..V....... GOP max bitrate (% of target) (from -1 to 5000) (default -1)
        '-frame',  # -parallel <boolean> E..V....... Enable frame parallel decodability features (default auto)
        '-tiles',  # <image_size> E..V....... Tile columns x rows
        '-tile',  # -columns <int> E..V....... Log2 of number of tile columns to use (from -1 to 6) (default -1)
        '-row',  # -mt <boolean> E..V....... Enable row based multi-threading (default auto)
        '-enable',  # -cdef <boolean> E..V....... Enable CDEF filtering (default auto)
        '-usage',  # <int> E..V....... Quality and compression efficiency vs speed trade-off (from 0 to INT_MAX) (default good)
        '-tune',  # <int> E..V....... The metric that the encoder tunes for. Automatically chosen by the encoder by default (from -1 to 1) (default -1)
        '-still',  # -picture <boolean> E..V....... Encode in single frame mode (typically used for still AVIF images). (default false)
        '-reduced',  # -tx-type-set <boolean> E..V....... Use reduced set of transform types (default auto)
        '-use',  # -intra-dct-only <boolean> E..V....... Use DCT only for INTRA modes (default auto)
        '-aom',  # -params <dictionary> E..V....... Set libaom options using a :-separated list of key=value pairs
        '-effort',  # <int> E..V....... Encoding effort (from 1 to 9) (default 7)
        '-distance',  # <float> E..V....... Maximum Butteraugli distance (quality setting, lower = better, zero = lossless, default 1.0) (from -1 to 15) (default -1)
        '-modular',  # <int> E..V....... Force modular mode (from 0 to 1) (default 0)
        '-xyb',  # <int> E..V....... Use XYB-encoding for lossy images (from 0 to 1) (default 1)
        '-reservoir',  # <boolean> E...A...... use bit reservoir (default true)
        '-abr',  # <boolean> E...A...... use ABR (default false)
        '-cinema_mode',  # <int> E..V....... Digital Cinema (from 0 to 3) (default off)
        '-prog_order',  # <int> E..V....... Progression Order (from 0 to 4) (default lrcp)
        '-numresolution',  # <int> E..V....... (from 0 to 33) (default 6)
        '-irreversible',  # <int> E..V....... (from 0 to 1) (default 0)
        '-disto_alloc',  # <int> E..V....... (from 0 to 1) (default 1)
        '-fixed_quality',  # <int> E..V....... (from 0 to 1) (default 0)
        '-application',  # <int> E...A...... Intended application type (from 2048 to 2051) (default audio)
        '-frame_duration',  # <float> E...A...... Duration of a frame in milliseconds (from 2.5 to 120) (default 20)
        '-packet_loss',  # <int> E...A...... Expected packet loss percentage (from 0 to 100) (default 0)
        '-fec',  # <boolean> E...A...... Enable inband FEC. Expected packet loss must be non-zero (default false)
        '-vbr',  # <int> E...A...... Variable bit rate mode (from 0 to 2) (default on)
        '-mapping_family',  # <int> E...A...... Channel Mapping Family (from -1 to 255) (default -1)
        '-qp',  # <int> E..V....... use constant quantizer mode (from -1 to 255) (default -1)
        '-speed',  # <int> E..V....... what speed preset to use (from -1 to 10) (default -1)
        '-rav1e',  # -params <dictionary> E..V....... set the rav1e configuration using a :-separated list of key=value parameters
        '-cbr_quality',  # <int> E...A...... Set quality value (0 to 10) for CBR (from 0 to 10) (default 8)
        '-frames_per_packet',  # <int> E...A...... Number of frames to encode in each packet (from 1 to 8) (default 1)
        '-vad',  # <int> E...A...... Voice Activity Detection (from 0 to 1) (default 0)
        '-dtx',  # <int> E...A...... Discontinuous Transmission (from 0 to 1) (default 0)
        '-preset',  # <int> E..V....... Encoding preset (from -2 to 13) (default -2)
        '-svtav1',  # -params <dictionary> E..V....... Set the SVT-AV1 configuration using a :-separated list of key=value parameters
        '-deadline',  # <int> E..V....... Time to spend encoding, in microseconds. (from INT_MIN to INT_MAX) (default good)
        '-max',  # -intra-rate <int> E..V....... Maximum I-frame bitrate (pct) 0=unlimited (from -1 to INT_MAX) (default -1)
        '-noise',  # -sensitivity <int> E..V....... Noise sensitivity (from 0 to 4) (default 0)
        '-ts',  # -parameters <dictionary> E..V....... Temporal scaling configuration using a :-separated list of key=value parameters
        '-screen',  # -content-mode <int> E..V....... Encoder screen content mode (from -1 to 2) (default -1)
        '-quality',  # <int> E..V....... (from INT_MIN to INT_MAX) (default good)
        '-vp8flags',  # <flags> E..V....... (default 0)
        '-arnr_max_frames',  # <int> E..V....... altref noise reduction max frame count (from 0 to 15) (default 0)
        '-arnr_strength',  # <int> E..V....... altref noise reduction filter strength (from 0 to 6) (default 3)
        '-arnr_type',  # <int> E..V....... altref noise reduction filter type (from 1 to 3) (default 3)
        '-rc_lookahead',  # <int> E..V....... Number of frames to look ahead for alternate reference frame selection (from 0 to 25) (default 25)
        '-sharpness',  # <int> E..V....... Increase sharpness at the expense of lower PSNR (from -1 to 7) (default -1)
        '-lossless',  # <int> E..V....... Lossless mode (from -1 to 1) (default -1)
        '-corpus',  # -complexity <int> E..V....... corpus vbr complexity midpoint (from -1 to 10000) (default -1)
        '-min',  # -gf-interval <int> E..V....... Minimum golden/alternate reference frame interval (from -1 to INT_MAX) (default -1)
        '-cr_threshold',  # <int> E..V....... Conditional replenishment threshold (from 0 to INT_MAX) (default 0)
        '-cr_size',  # <int> E..V....... Conditional replenishment block size (from 0 to 256) (default 16)
        '-fastfirstpass',  # <boolean> E..V....... Use fast settings when encoding first pass (default true)
        '-wpredp',  # <string> E..V....... Weighted prediction for P-frames
        '-x264opts',  # <string> E..V....... x264 options
        '-crf_max',  # <float> E..V....... In CRF mode, prevents VBV from lowering quality beyond this point. (from -1 to FLT_MAX) (default -1)
        '-psy',  # <boolean> E..V....... Use psychovisual optimizations. (default auto)
        '-rc',  # -lookahead <int> E..V....... Number of frames to look ahead for frametype and ratecontrol (from -1 to INT_MAX) (default -1)
        '-weightb',  # <boolean> E..V....... Weighted prediction for B-frames. (default auto)
        '-weightp',  # <int> E..V....... Weighted prediction analysis method. (from -1 to INT_MAX) (default -1)
        '-ssim',  # <boolean> E..V....... Calculate and print SSIM stats. (default auto)
        '-intra',  # -refresh <boolean> E..V....... Use Periodic Intra Refresh instead of IDR frames. (default auto)
        '-bluray',  # -compat <boolean> E..V....... Bluray compatibility workarounds. (default auto)
        '-mixed',  # -refs <boolean> E..V....... One reference per partition, as opposed to one reference per macroblock (default auto)
        '-fast',  # -pskip <boolean> E..V....... (default auto)
        '-aud',  # <boolean> E..V....... Use access unit delimiters. (default auto)
        '-mbtree',  # <boolean> E..V....... Use macroblock tree ratecontrol. (default auto)
        '-deblock',  # <string> E..V....... Loop filter parameters, in <alpha:beta> form.
        '-cplxblur',  # <float> E..V....... Reduce fluctuations in QP (before curve compression) (from -1 to FLT_MAX) (default -1)
        '-partitions',  # <string> E..V....... A comma-separated list of partitions to consider. Possible values: p8x8, p4x4, b8x8, i8x8, i4x4, none, all
        '-direct',  # -pred <int> E..V....... Direct MV prediction mode (from -1 to INT_MAX) (default -1)
        '-slice',  # -max-size <int> E..V....... Limit the size of each slice in bytes (from -1 to INT_MAX) (default -1)
        '-nal',  # -hrd <int> E..V....... Signal HRD information (requires vbv-bufsize; cbr not allowed in .mp4) (from -1 to INT_MAX) (default -1)
        '-avcintra',  # -class <int> E..V....... AVC-Intra class 50/100/200/300/480 (from -1 to 480) (default -1)
        '-me_method',  # <int> E..V....... Set motion estimation method (from -1 to 4) (default -1)
        '-motion',  # -est <int> E..V....... Set motion estimation method (from -1 to 4) (default -1)
        '-forced',  # -idr <boolean> E..V....... If forcing keyframes, force them as IDR frames. (default false)
        '-chromaoffset',  # <int> E..V....... QP difference between chroma and luma (from INT_MIN to INT_MAX) (default 0)
        '-udu_sei',  # <boolean> E..V....... Use user data unregistered SEI if available (default false)
        '-x264',  # -params <dictionary> E..V....... Override the x264 configuration using a :-separated list of key=value parameters
        '-x265',  # -params <dictionary> E..V....... set the x265 configuration using a :-separated list of key=value parameters
        '-lumi_aq',  # <int> E..V....... Luminance masking AQ (from 0 to 1) (default 0)
        '-variance_aq',  # <int> E..V....... Variance AQ (from 0 to 1) (default 0)
        '-ssim_acc',  # <int> E..V....... SSIM accuracy (from 0 to 4) (default 2)
        '-gmc',  # <int> E..V....... use GMC (from 0 to 1) (default 0)
        '-me_quality',  # <int> E..V....... Motion estimation quality (from 0 to 6) (default 4)
        '-constant_bit_rate',  # <boolean> E..V....... Require constant bit rate (macOS 13 or newer) (default false)
        '-max_slice_bytes',  # <int> E..V....... Set the maximum number of bytes in an H.264 slice. (from -1 to INT_MAX) (default -1)
        '-allow_sw',  # <boolean> E..V....... Allow software encoding (default false)
        '-require_sw',  # <boolean> E..V....... Require software encoding (default false)
        '-realtime',  # <boolean> E..V....... Hint that encoding should happen in real-time if not faster (e.g. capturing from camera). (default false)
        '-frames_before',  # <boolean> E..V....... Other frames will come before the frames in this session. This helps smooth concatenation issues. (default false)
        '-frames_after',  # <boolean> E..V....... Other frames will come after the frames in this session. This helps smooth concatenation issues. (default false)
        '-prio_speed',  # <boolean> E..V....... prioritize encoding speed (default auto)
        '-power_efficient',  # <int> E..V....... Set to 1 to enable more power-efficient encoding if supported. (from -1 to 1) (default -1)
        '-max_ref_frames',  # <int> E..V....... Sets the maximum number of reference frames. This only has an effect when the value is less than the maximum allowed by the profile/level. (from 0 to INT_MAX) (default 0)
        '-alpha_quality',  # <double> E..V....... Compression quality for the alpha channel (from 0 to 1) (default 0)
        '-layer',  # <string> .D.V....... Set the decoding layer (default "")
        '-part',  # <int> .D.V....... Set the decoding part (from 0 to INT_MAX) (default 0)
        '-apply_trc',  # <int> .D.V....... color transfer characteristics to apply to EXR linear input (from 1 to 18) (default gamma)
        '-is_avc',  # <boolean> .D.V..X.... is avc (default false)
        '-nal_length_size',  # <int> .D.V..X.... nal_length_size (from 0 to 4) (default 0)
        '-enable_er',  # <boolean> .D.V....... Enable error resilience on damaged frames (unsafe) (default auto)
        '-x264_build',  # <int> .D.V....... Assume this x264 version if no x264 version found in any SEI (from -1 to INT_MAX) (default -1)
        '-skip_gray',  # <boolean> .D.V....... Do not return gray gap frames (default false)
        '-noref_gray',  # <boolean> .D.V....... Avoid using gray gap frames as references (default true)
        '-apply_defdispwin',  # <boolean> .D.V....... Apply default display window from VUI (default false)
        '-subimage',  # <boolean> .D.V....... decode subimage instead if available (default false)
        '-thumbnail',  # <boolean> .D.V....... decode embedded thumbnail subimage instead if available (default false)
        '-page',  # <int> .D.V....... page number of multi-page image to decode (starting from 1) (from 0 to 65535) (default 0)
        '-dual_mono_mode',  # <int> .D..A...... Select the channel to decode for dual mono (from -1 to 2) (default auto)
        '-channel_order',  # <int> .D..A...... Order in which the channels are to be exported (from 0 to 1) (default default)
        '-cons_noisegen',  # <boolean> .D..A...... enable consistent noise generation (default false)
        '-drc_scale',  # <float> .D..A...... percentage of dynamic range compression to apply (from 0 to 6) (default 1)
        '-heavy_compr',  # <boolean> .D..A...... enable heavy dynamic range compression (default false)
        '-target_level',  # <int> .D..A...... target level in -dBFS (0 not applied) (from -31 to 0) (default 0)
        '-downmix',  # <channel_layout> .D..A...... Request a specific channel layout from the decoder
        '-core_only',  # <boolean> .D..A...... Decode core only without extensions (default false)
        '-real_time',  # <boolean> .D...S..... emit subtitle events as they are decoded for real-time display (default false)
        '-real_time_latency_msec',  # <int> .D...S..... minimum elapsed time between emitting real-time subtitle events (from 0 to 500) (default 200)
        '-data_field',  # <int> .D...S..... select data field (from -1 to 1) (default auto)
        '-compute_edt',  # <boolean> .D...S..... compute end of time using pts or timeout (default false)
        '-compute_clut',  # <boolean> .D...S..... compute clut when not available(-1) or only once (-2) or always(1) or never(0) (default auto)
        '-dvb_substream',  # <int> .D...S..... (from -1 to 63) (default -1)
        '-ifo_palette',  # <string> .D...S..... obtain the global palette from .IFO file
        '-forced_subs_only',  # <boolean> .D...S..... Only show forced subtitles (default false)
        '-width',  # <int> .D...S..... Frame width, usually video width (from 0 to INT_MAX) (default 0)
        '-height',  # <int> .D...S..... Frame height, usually video height (from 0 to INT_MAX) (default 0)
        '-keep_ass_markup',  # <boolean> .D...S..... Set if ASS tags must be escaped (default false)
        '-aribb24',  # -base-path <string> .D...S..... set the base path for the libaribb24 library
        '-default_profile',  # <int> .D...S..... default profile to use if not specified in the stream parameters (from -99 to 1) (default -99)
        '-tilethreads',  # <int> .D.V......P Tile threads (from 0 to 256) (default 0)
        '-framethreads',  # <int> .D.V......P Frame threads (from 0 to 256) (default 0)
        '-max_frame_delay',  # <int> .D.V....... Max frame delay (from 0 to 256) (default 0)
        '-filmgrain',  # <boolean> .D.V......P Apply Film Grain (default auto)
        '-oppoint',  # <int> .D.V....... Select an operating point of the scalable bitstream (from -1 to 31) (default -1)
        '-alllayers',  # <boolean> .D.V....... Output all spatial layers (default false)
        '-avioflags',  # <flags> ED......... (default 0)
        '-probesize',  # <int64> .D......... set probing size (from 32 to I64_MAX) (default 5000000)
        '-formatprobesize',  # <int> .D......... number of bytes to probe file format (from 0 to 2.14748e+09) (default 1048576)
        '-packetsize',  # <int> E.......... set packet size (from 0 to INT_MAX) (default 0)
        '-fflags',  # <flags> ED......... (default autobsf)
        '-seek2any',  # <boolean> .D......... allow seeking to non-keyframes on demuxer level when supported (default false)
        '-analyzeduration',  # <int64> .D......... specify how many microseconds are analyzed to probe the input (from 0 to I64_MAX) (default 0)
        '-cryptokey',  # <binary> .D......... decryption key
        '-indexmem',  # <int> .D......... max memory used for timestamp index (per stream) (from 0 to INT_MAX) (default 1048576)
        '-rtbufsize',  # <int> .D......... max memory used for buffering real-time frames (from 0 to INT_MAX) (default 3041280)
        '-fdebug',  # <flags> ED......... print specific debug info (default 0)
        '-max_delay',  # <int> ED......... maximum muxing or demuxing delay in microseconds (from -1 to INT_MAX) (default -1)
        '-start_time_realtime',  # <int64> E.......... wall-clock time when stream begins (PTS==0) (from I64_MIN to I64_MAX) (default I64_MIN)
        '-fpsprobesize',  # <int> .D......... number of frames used to probe fps (from -1 to 2.14748e+09) (default -1)
        '-audio_preload',  # <int> E.......... microseconds by which audio packets should be interleaved earlier (from 0 to 2.14748e+09) (default 0)
        '-chunk_duration',  # <int> E.......... microseconds for each chunk (from 0 to 2.14748e+09) (default 0)
        '-chunk_size',  # <int> E.......... size in bytes for each chunk (from 0 to 2.14748e+09) (default 0)
        '-f_err_detect',  # <flags> .D......... set error detection flags (deprecated; use err_detect, save via avconv) (default crccheck)
        '-use_wallclock_as_timestamps',  # <boolean> .D......... use wallclock as timestamps (default false)
        '-skip_initial_bytes',  # <int64> .D......... set number of bytes to skip before reading header and frames (from 0 to I64_MAX) (default 0)
        '-correct_ts_overflow',  # <boolean> .D......... correct single timestamp overflows (default true)
        '-flush_packets',  # <int> E.......... enable flushing of the I/O context after each packet (from -1 to 1) (default -1)
        '-metadata_header_padding',  # <int> E.......... set number of bytes to be written as padding in a metadata header (from -1 to INT_MAX) (default -1)
        '-output_ts_offset',  # <duration> E.......... set output timestamp offset (default 0)
        '-max_interleave_delta',  # <int64> E.......... maximum buffering duration for interleaving (from 0 to I64_MAX) (default 10000000)
        '-f_strict',  # <int> ED......... how strictly to follow the standards (deprecated; use strict, save via avconv) (from INT_MIN to INT_MAX) (default normal)
        '-max_ts_probe',  # <int> .D......... maximum number of packets to read while waiting for the first timestamp (from 0 to INT_MAX) (default 50)
        '-avoid_negative_ts',  # <int> E.......... shift timestamps so they start at 0 (from -1 to 2) (default auto)
        '-format_whitelist',  # <string> .D......... List of demuxers that are allowed to be used
        '-protocol_whitelist',  # <string> .D......... List of protocols that are allowed to be used
        '-protocol_blacklist',  # <string> .D......... List of protocols that are not allowed to be used
        '-max_streams',  # <int> .D......... maximum number of streams (from 0 to INT_MAX) (default 1000)
        '-skip_estimate_duration_from_pts',  # <boolean> .D......... skip duration calculation in estimate_timings_from_pts (default false)
        '-max_probe_packets',  # <int> .D......... Maximum number of packets to probe a codec (from 0 to INT_MAX) (default 2500)
        '-rw_timeout',  # <int64> ED......... Timeout for IO operations (in microseconds) (from 0 to I64_MAX) (default 0)
        '-playlist',  # <int> .D......... (from -1 to 99999) (default -1)
        '-angle',  # <int> .D......... (from 0 to 254) (default 0)
        '-chapter',  # <int> .D......... (from 1 to 65534) (default 1)
        '-key',  # <binary> ED......... AES encryption/decryption key
        '-iv',  # <binary> ED......... AES encryption/decryption initialization vector
        '-decryption_key',  # <binary> .D......... AES decryption key
        '-decryption_iv',  # <binary> .D......... AES decryption initialization vector
        '-encryption_key',  # <binary> E.......... AES encryption key
        '-encryption_iv',  # <binary> E.......... AES encryption initialization vector
        '-blocksize',  # <int> E.......... set I/O operation maximum block size (from 1 to INT_MAX) (default INT_MAX)
        '-fd',  # <int> E.......... set file descriptor (from -1 to INT_MAX) (default -1)
        '-truncate',  # <boolean> E.......... truncate existing files on write (default true)
        '-follow',  # <int> .D......... Follow a file as it is being written (from 0 to 1) (default 0)
        '-seekable',  # <int> ED......... Sets if the file is seekable (from -1 to 0) (default -1)
        '-timeout',  # <int> ED......... set timeout of socket I/O operations (from -1 to INT_MAX) (default -1)
        '-ftp',  # -write-seekable <boolean> E.......... control seekability of connection during encoding (default false)
        '-chunked_post',  # <boolean> E.......... use chunked transfer-encoding for posts (default true)
        '-http_proxy',  # <string> ED......... set HTTP proxy to tunnel through
        '-headers',  # <string> ED......... set custom HTTP headers, can override built in default headers
        '-content_type',  # <string> ED......... set a specific content type for the POST messages
        '-user_agent',  # <string> .D......... override User-Agent header (default "Lavf/61.1.100")
        '-referer',  # <string> .D......... override referer header
        '-multiple_requests',  # <boolean> ED......... use persistent connections (default false)
        '-post_data',  # <binary> ED......... set custom HTTP post data
        '-cookies',  # <string> .D......... set cookies to be sent in applicable future requests, use newline delimited Set-Cookie HTTP field value syntax
        '-icy',  # <boolean> .D......... request ICY metadata (default true)
        '-auth_type',  # <int> ED......... HTTP authentication type (from 0 to 1) (default none)
        '-send_expect_100',  # <boolean> E.......... Force sending an Expect: 100-continue header for POST (default auto)
        '-location',  # <string> ED......... The actual location of the data received
        '-offset',  # <int64> .D......... initial byte offset (from 0 to I64_MAX) (default 0)
        '-end_offset',  # <int64> .D......... try to limit the request to bytes preceding this offset (from 0 to I64_MAX) (default 0)
        '-method',  # <string> ED......... Override the HTTP method or set the expected HTTP method from a client
        '-reconnect',  # <boolean> .D......... auto reconnect after disconnect before EOF (default false)
        '-reconnect_at_eof',  # <boolean> .D......... auto reconnect at EOF (default false)
        '-reconnect_on_network_error',  # <boolean> .D......... auto reconnect in case of tcp/tls error during connect (default false)
        '-reconnect_on_http_error',  # <string> .D......... list of http status codes to reconnect on
        '-reconnect_streamed',  # <boolean> .D......... auto reconnect streamed / non seekable streams (default false)
        '-reconnect_delay_max',  # <int> .D......... max reconnect delay in seconds after which to give up (from 0 to 4294) (default 120)
        '-listen',  # <int> ED......... listen on HTTP (from 0 to 2) (default 0)
        '-resource',  # <string> E.......... The resource requested by a client
        '-reply_code',  # <int> E.......... The http status code to return to a client (from INT_MIN to 599) (default 200)
        '-short_seek_size',  # <int> .D......... Threshold to favor readahead over seek. (from 0 to INT_MAX) (default 0)
        '-ice_genre',  # <string> E.......... set stream genre
        '-ice_name',  # <string> E.......... set stream description
        '-ice_description',  # <string> E.......... set stream description
        '-ice_url',  # <string> E.......... set stream website
        '-ice_public',  # <boolean> E.......... set if stream is public (default false)
        '-password',  # <string> E.......... set password
        '-legacy_icecast',  # <boolean> E.......... use legacy SOURCE method, for Icecast < v2.4 (default false)
        '-tls',  # <boolean> E.......... use a TLS connection (default false)
        '-ttl',  # <int> E.......... Time to live (in milliseconds, multicast only) (from -1 to INT_MAX) (default -1)
        '-l',  # <int> E.......... FEC L (from 4 to 20) (default 5)
        '-d',  # <int> E.......... FEC D (from 4 to 20) (default 5)
        '-rtmp_app',  # <string> ED......... Name of application to connect to on the RTMP server
        '-rtmp_buffer',  # <int> ED......... Set buffer time in milliseconds. The default is 3000. (from 0 to INT_MAX) (default 3000)
        '-rtmp_conn',  # <string> ED......... Append arbitrary AMF data to the Connect message
        '-rtmp_flashver',  # <string> ED......... Version of the Flash plugin used to run the SWF player.
        '-rtmp_flush_interval',  # <int> E.......... Number of packets flushed in the same request (RTMPT only). (from 0 to INT_MAX) (default 10)
        '-rtmp_enhanced_codecs',  # <string> E.......... Specify the codec(s) to use in an enhanced rtmp live stream
        '-rtmp_live',  # <int> .D......... Specify that the media is a live stream. (from INT_MIN to INT_MAX) (default any)
        '-rtmp_pageurl',  # <string> .D......... URL of the web page in which the media was embedded. By default no value will be sent.
        '-rtmp_playpath',  # <string> ED......... Stream identifier to play or to publish
        '-rtmp_subscribe',  # <string> .D......... Name of live stream to subscribe to. Defaults to rtmp_playpath.
        '-rtmp_swfhash',  # <binary> .D......... SHA256 hash of the decompressed SWF file (32 bytes).
        '-rtmp_swfsize',  # <int> .D......... Size of the decompressed SWF file, required for SWFVerification. (from 0 to INT_MAX) (default 0)
        '-rtmp_swfurl',  # <string> ED......... URL of the SWF player. By default no value will be sent
        '-rtmp_swfverify',  # <string> .D......... URL to player swf file, compute hash/size automatically.
        '-rtmp_tcurl',  # <string> ED......... URL of the target stream. Defaults to proto://host[:port]/app.
        '-rtmp_listen',  # <int> .D......... Listen for incoming rtmp connections (from INT_MIN to INT_MAX) (default 0)
        '-tcp_nodelay',  # <int> ED......... Use TCP_NODELAY to disable Nagle's algorithm (from 0 to 1) (default 0)
        '-buffer_size',  # <int> ED......... Send/Receive buffer size (in bytes) (from -1 to INT_MAX) (default -1)
        '-rtcp_port',  # <int> ED......... Custom rtcp port (from -1 to INT_MAX) (default -1)
        '-local_rtpport',  # <int> ED......... Local rtp port (from -1 to INT_MAX) (default -1)
        '-local_rtcpport',  # <int> ED......... Local rtcp port (from -1 to INT_MAX) (default -1)
        '-connect',  # <boolean> ED......... Connect socket (default false)
        '-write_to_source',  # <boolean> ED......... Send packets to the source address of the latest received packet (default false)
        '-pkt_size',  # <int> ED......... Maximum packet size (from -1 to INT_MAX) (default -1)
        '-dscp',  # <int> ED......... DSCP class (from -1 to INT_MAX) (default -1)
        '-block',  # <string> ED......... Block list
        '-localaddr',  # <string> ED......... Local address
        '-srtp_out_suite',  # <string> E..........
        '-srtp_out_params',  # <string> E..........
        '-srtp_in_suite',  # <string> .D.........
        '-srtp_in_params',  # <string> .D.........
        '-start',  # <int64> .D......... start offset (from 0 to I64_MAX) (default 0)
        '-end',  # <int64> .D......... end offset (from 0 to I64_MAX) (default 0)
        '-local_port',  # <string> ED......... Local port
        '-local_addr',  # <string> ED......... Local address
        '-listen_timeout',  # <int> ED......... Connection awaiting timeout (in milliseconds) (from -1 to INT_MAX) (default -1)
        '-send_buffer_size',  # <int> ED......... Socket send buffer size (in bytes) (from -1 to INT_MAX) (default -1)
        '-recv_buffer_size',  # <int> ED......... Socket receive buffer size (in bytes) (from -1 to INT_MAX) (default -1)
        '-tcp_mss',  # <int> ED......... Maximum segment size for outgoing TCP packets (from -1 to INT_MAX) (default -1)
        '-ca_file',  # <string> ED......... Certificate Authority database file
        '-cafile',  # <string> ED......... Certificate Authority database file
        '-tls_verify',  # <int> ED......... Verify the peer certificate (from 0 to 1) (default 0)
        '-cert_file',  # <string> ED......... Certificate file
        '-key_file',  # <string> ED......... Private key file
        '-verifyhost',  # <string> ED......... Verify against a specific hostname
        '-bitrate',  # <int64> E.......... Bits to send per second (from 0 to I64_MAX) (default 0)
        '-burst_bits',  # <int64> E.......... Max length of bursts in bits (when using bitrate) (from 0 to I64_MAX) (default 0)
        '-localport',  # <int> ED......... Local port (from -1 to INT_MAX) (default -1)
        '-udplite_coverage',  # <int> ED......... choose UDPLite head size which should be validated by checksum (from 0 to INT_MAX) (default 0)
        '-reuse',  # <boolean> ED......... explicitly allow reusing UDP sockets (default auto)
        '-reuse_socket',  # <boolean> ED......... explicitly allow reusing UDP sockets (default auto)
        '-broadcast',  # <boolean> E.......... explicitly allow or disallow broadcast destination (default false)
        '-fifo_size',  # <int> .D......... set the UDP receiving circular buffer size, expressed as a number of packets with size of 188 bytes (from 0 to INT_MAX) (default 28672)
        '-overrun_nonfatal',  # <boolean> .D......... survive in case of UDP receiving circular buffer overrun (default false)
        '-type',  # <int> ED......... Socket type (from INT_MIN to INT_MAX) (default stream)
        '-rist_profile',  # <int> ED......... set profile (from 0 to 2) (default main)
        '-log_level',  # <int> ED......... set loglevel (from -1 to INT_MAX) (default 6)
        '-secret',  # <string> ED......... set encryption secret
        '-encryption',  # <int> ED......... set encryption type (from 0 to INT_MAX) (default 0)
        '-payload_size',  # <int> ED......... Maximum SRT packet size (from -1 to 1456) (default -1)
        '-maxbw',  # <int64> ED......... Maximum bandwidth (bytes per second) that the connection can use (from -1 to I64_MAX) (default -1)
        '-pbkeylen',  # <int> ED......... Crypto key len in bytes {16,24,32} Default: 16 (128-bit) (from -1 to 32) (default -1)
        '-passphrase',  # <string> ED......... Crypto PBKDF2 Passphrase size[0,10..64] 0:disable crypto
        '-enforced_encryption',  # <boolean> ED......... Enforces that both connection parties have the same passphrase set (default auto)
        '-kmrefreshrate',  # <int> ED......... The number of packets to be transmitted after which the encryption key is switched to a new key (from -1 to INT_MAX) (default -1)
        '-kmpreannounce',  # <int> ED......... The interval between when a new encryption key is sent and when switchover occurs (from -1 to INT_MAX) (default -1)
        '-snddropdelay',  # <int64> ED......... The sender's extra delay(in microseconds) before dropping packets (from -2 to I64_MAX) (default -2)
        '-mss',  # <int> ED......... The Maximum Segment Size (from -1 to 1500) (default -1)
        '-ffs',  # <int> ED......... Flight flag size (window size) (in bytes) (from -1 to INT_MAX) (default -1)
        '-ipttl',  # <int> ED......... IP Time To Live (from -1 to 255) (default -1)
        '-iptos',  # <int> ED......... IP Type of Service (from -1 to 255) (default -1)
        '-inputbw',  # <int64> ED......... Estimated input stream rate (from -1 to I64_MAX) (default -1)
        '-oheadbw',  # <int> ED......... MaxBW ceiling based on % over input stream rate (from -1 to 100) (default -1)
        '-latency',  # <int64> ED......... receiver delay (in microseconds) to absorb bursts of missed packet retransmissions (from -1 to I64_MAX) (default -1)
        '-tsbpddelay',  # <int64> ED......... deprecated, same effect as latency option (from -1 to I64_MAX) (default -1)
        '-rcvlatency',  # <int64> ED......... receive latency (in microseconds) (from -1 to I64_MAX) (default -1)
        '-peerlatency',  # <int64> ED......... peer latency (in microseconds) (from -1 to I64_MAX) (default -1)
        '-tlpktdrop',  # <boolean> ED......... Enable too-late pkt drop (default auto)
        '-nakreport',  # <boolean> ED......... Enable receiver to send periodic NAK reports (default auto)
        '-connect_timeout',  # <int64> ED......... Connect timeout(in milliseconds). Caller default: 3000, rendezvous (x 10) (from -1 to I64_MAX) (default -1)
        '-mode',  # <int> ED......... Connection mode (caller, listener, rendezvous) (from 0 to 2) (default caller)
        '-sndbuf',  # <int> ED......... Send buffer size (in bytes) (from -1 to INT_MAX) (default -1)
        '-rcvbuf',  # <int> ED......... Receive buffer size (in bytes) (from -1 to INT_MAX) (default -1)
        '-lossmaxttl',  # <int> ED......... Maximum possible packet reorder tolerance (from -1 to INT_MAX) (default -1)
        '-minversion',  # <int> ED......... The minimum SRT version that is required from the peer (from -1 to INT_MAX) (default -1)
        '-srt_streamid',  # <string> ED......... A string of up to 512 characters that an Initiator can pass to a Responder
        '-smoother',  # <string> ED......... The type of Smoother used for the transmission for that socket
        '-messageapi',  # <boolean> ED......... Enable message API (default auto)
        '-transtype',  # <int> ED......... The transmission type for the socket (from 0 to 2) (default 2)
        '-linger',  # <int> ED......... Number of seconds that the socket waits for unsent data when closing (from -1 to INT_MAX) (default -1)
        '-tsbpd',  # <boolean> ED......... Timestamp-based packet delivery (default auto)
        '-private_key',  # <string> ED......... set path to private key
        '-gateway',  # <string> .D......... The gateway to ask for IPFS data.
        '-write_id3v2',  # <boolean> E.......... Enable ID3v2 tag writing (default false)
        '-write_apetag',  # <boolean> E.......... Enable APE tag writing (default false)
        '-write_mpeg2',  # <boolean> E.......... Set MPEG version to MPEG-2 (default false)
        '-id3v2_version',  # <int> E.......... Select ID3v2 version to write. Currently 3 and 4 are supported. (from 3 to 4) (default 4)
        '-plays',  # <int> E.......... Number of times to play the output: 0 - infinite loop, 1 - no loop (from 0 to 65535) (default 1)
        '-final_delay',  # <rational> E.......... Force delay after the last frame (from 0 to 65535) (default 0/1)
        '-version_major',  # <int> E.......... override file major version (from 0 to 65535) (default 2)
        '-version_minor',  # <int> E.......... override file minor version (from 0 to 65535) (default 1)
        '-name',  # <string> E.......... embedded file name (max 8 characters)
        '-skip_rate_check',  # <boolean> E.......... skip sample rate check (default false)
        '-loop',  # <boolean> E.......... set loop flag (default false)
        '-reverb',  # <boolean> E.......... set reverb flag (default true)
        '-packet_size',  # <int> E.......... Packet size (from 100 to 65536) (default 3200)
        '-loopstart',  # <int64> E.......... Loopstart position in milliseconds. (from -1 to INT_MAX) (default -1)
        '-loopend',  # <int64> E.......... Loopend position in milliseconds. (from 0 to INT_MAX) (default 0)
        '-reserve_index_space',  # <int> E.......... reserve space (in bytes) at the beginning of the file for each stream index (from 0 to INT_MAX) (default 0)
        '-write_channel_mask',  # <boolean> E.......... write channel mask into wave format header (default true)
        '-flipped_raw_rgb',  # <boolean> E.......... Raw RGB bitmaps are stored bottom-up (default false)
        '-movie_timescale',  # <int> E.......... set movie timescale (from 1 to INT_MAX) (default 1000)
        '-adaptation_sets',  # <string> E.......... Adaptation sets. Syntax: id=0,streams=0,1,2 id=1,streams=3,4 and so on
        '-dash_segment_type',  # <int> E.......... set dash segment files type (from 0 to 2) (default auto)
        '-extra_window_size',  # <int> E.......... number of segments kept outside of the manifest before removing from disk (from 0 to INT_MAX) (default 5)
        '-format_options',  # <dictionary> E.......... set list of options for the container format (mp4/webm) used for dash
        '-frag_duration',  # <duration> E.......... fragment duration (in seconds, fractional value can be set) (default 0)
        '-frag_type',  # <int> E.......... set type of interval for fragments (from 0 to 3) (default none)
        '-global_sidx',  # <boolean> E.......... Write global SIDX atom. Applicable only for single file, mp4 output, non-streaming mode (default false)
        '-hls_master_name',  # <string> E.......... HLS master playlist name (default "master.m3u8")
        '-hls_playlist',  # <boolean> E.......... Generate HLS playlist files(master.m3u8, media_%d.m3u8) (default false)
        '-http_opts',  # <dictionary> E.......... HTTP protocol options
        '-http_persistent',  # <boolean> E.......... Use persistent HTTP connections (default false)
        '-http_user_agent',  # <string> E.......... override User-Agent field in HTTP header
        '-ignore_io_errors',  # <boolean> E.......... Ignore IO errors during open and write. Useful for long-duration runs with network output (default false)
        '-index_correction',  # <boolean> E.......... Enable/Disable segment index correction logic (default false)
        '-init_seg_name',  # <string> E.......... DASH-templated name to used for the initialization segment (default "init-stream$RepresentationID$.$ext$")
        '-ldash',  # <boolean> E.......... Enable Low-latency dash. Constrains the value of a few elements (default false)
        '-lhls',  # <boolean> E.......... Enable Low-latency HLS(Experimental). Adds #EXT-X-PREFETCH tag with current segment's URI (default false)
        '-master_m3u8_publish_rate',  # <int> E.......... Publish master playlist every after this many segment intervals (from 0 to UINT32_MAX) (default 0)
        '-max_playback_rate',  # <rational> E.......... Set desired maximum playback rate (from 0.5 to 1.5) (default 1/1)
        '-media_seg_name',  # <string> E.......... DASH-templated name to used for the media segments (default "chunk-stream$RepresentationID$-$Number%05d$.$ext$")
        '-min_playback_rate',  # <rational> E.......... Set desired minimum playback rate (from 0.5 to 1.5) (default 1/1)
        '-mpd_profile',  # <flags> E.......... Set profiles. Elements and values used in the manifest may be constrained by them (default dash)
        '-remove_at_exit',  # <boolean> E.......... remove all segments when finished (default false)
        '-seg_duration',  # <duration> E.......... segment duration (in seconds, fractional value can be set) (default 5)
        '-single_file',  # <boolean> E.......... Store all segments in one file, accessed using byte ranges (default false)
        '-single_file_name',  # <string> E.......... DASH-templated name to be used for baseURL. Implies storing all segments in one file, accessed using byte ranges
        '-streaming',  # <boolean> E.......... Enable/Disable streaming mode of output. Each frame will be moof fragment (default false)
        '-target_latency',  # <duration> E.......... Set desired target latency for Low-latency dash (default 0)
        '-update_period',  # <int64> E.......... Set the mpd update interval (from 0 to I64_MAX) (default 0)
        '-use_template',  # <boolean> E.......... Use SegmentTemplate instead of SegmentList (default true)
        '-use_timeline',  # <boolean> E.......... Use SegmentTimeline in SegmentTemplate (default true)
        '-utc_timing_url',  # <string> E.......... URL of the page that will return the UTC timestamp in ISO format
        '-window_size',  # <int> E.......... number of segments kept in the manifest (from 0 to INT_MAX) (default 0)
        '-write_prft',  # <boolean> E.......... Write producer reference time element (default auto)
        '-brand',  # <string> E.......... Override major brand
        '-empty_hdlr_name',  # <boolean> E.......... write zero-length name string in hdlr atoms within mdia and minf atoms (default false)
        '-encryption_kid',  # <binary> E.......... The media encryption key identifier (hex)
        '-encryption_scheme',  # <string> E.......... Configures the encryption scheme, allowed values are none, cenc-aes-ctr
        '-frag_interleave',  # <int> E.......... Interleave samples within fragments (max number of consecutive samples, lower is tighter interleaving, but with more overhead) (from 0 to INT_MAX) (default 0)
        '-frag_size',  # <int> E.......... Maximum fragment size (from 0 to INT_MAX) (default 0)
        '-fragment_index',  # <int> E.......... Fragment number of the next fragment (from 1 to INT_MAX) (default 1)
        '-iods_audio_profile',  # <int> E.......... iods audio profile atom. (from -1 to 255) (default -1)
        '-iods_video_profile',  # <int> E.......... iods video profile atom. (from -1 to 255) (default -1)
        '-ism_lookahead',  # <int> E.......... Number of lookahead entries for ISM files (from 0 to 255) (default 0)
        '-movflags',  # <flags> E.......... MOV muxer flags (default 0)
        '-moov_size',  # <int> E.......... maximum moov size so it can be placed at the begin (from 0 to INT_MAX) (default 0)
        '-min_frag_duration',  # <int> E.......... Minimum fragment duration (from 0 to INT_MAX) (default 0)
        '-mov_gamma',  # <float> E.......... gamma value for gama atom (from 0 to 10) (default 0)
        '-rtpflags',  # <flags> E.......... RTP muxer flags (default 0)
        '-skip_iods',  # <boolean> E.......... Skip writing iods atom. (default true)
        '-use_editlist',  # <boolean> E.......... use edit list (default auto)
        '-use_stream_ids_as_track_ids',  # <boolean> E.......... use stream ids as track ids (default false)
        '-video_track_timescale',  # <int> E.......... set timescale of all video tracks (from 0 to INT_MAX) (default 0)
        '-write_btrt',  # <boolean> E.......... force or disable writing btrt (default auto)
        '-write_tmcd',  # <boolean> E.......... force or disable writing tmcd (default auto)
        '-attempt_recovery',  # <boolean> E.......... Attempt recovery in case of failure (default false)
        '-drop_pkts_on_overflow',  # <boolean> E.......... Drop packets on fifo queue overflow not to block encoder (default false)
        '-fifo_format',  # <string> E.......... Target muxer
        '-format_opts',  # <dictionary> E.......... Options to be passed to underlying muxer
        '-max_recovery_attempts',  # <int> E.......... Maximal number of recovery attempts (from 0 to INT_MAX) (default 0)
        '-queue_size',  # <int> E.......... Size of fifo queue (from 1 to INT_MAX) (default 60)
        '-recovery_wait_streamtime',  # <boolean> E.......... Use stream time instead of real time while waiting for recovery (default false)
        '-recovery_wait_time',  # <duration> E.......... Waiting time between recovery attempts (default 5)
        '-recover_any_error',  # <boolean> E.......... Attempt recovery regardless of type of the error (default false)
        '-restart_with_keyframe',  # <boolean> E.......... Wait for keyframe when restarting output (default false)
        '-timeshift',  # <duration> E.......... Delay fifo output (default 0)
        '-hash',  # <string> E.......... set hash to use (default "sha256")
        '-format_version',  # <int> E.......... file format version (from 1 to 2) (default 2)
        '-start_number',  # <int64> E.......... set first number in the sequence (from 0 to I64_MAX) (default 0)
        '-hls_time',  # <duration> E.......... set segment length (default 2)
        '-hls_init_time',  # <duration> E.......... set segment length at init list (default 0)
        '-hls_list_size',  # <int> E.......... set maximum number of playlist entries (from 0 to INT_MAX) (default 5)
        '-hls_delete_threshold',  # <int> E.......... set number of unreferenced segments to keep before deleting (from 1 to INT_MAX) (default 1)
        '-hls_vtt_options',  # <string> E.......... set hls vtt list of options for the container format used for hls
        '-hls_allow_cache',  # <int> E.......... explicitly set whether the client MAY (1) or MUST NOT (0) cache media segments (from INT_MIN to INT_MAX) (default -1)
        '-hls_base_url',  # <string> E.......... url to prepend to each playlist entry
        '-hls_segment_filename',  # <string> E.......... filename template for segment files
        '-hls_segment_options',  # <dictionary> E.......... set segments files format options of hls
        '-hls_segment_size',  # <int> E.......... maximum size per segment file, (in bytes) (from 0 to INT_MAX) (default 0)
        '-hls_key_info_file',  # <string> E.......... file with key URI and key file path
        '-hls_enc',  # <boolean> E.......... enable AES128 encryption support (default false)
        '-hls_enc_key',  # <string> E.......... hex-coded 16 byte key to encrypt the segments
        '-hls_enc_key_url',  # <string> E.......... url to access the key to decrypt the segments
        '-hls_enc_iv',  # <string> E.......... hex-coded 16 byte initialization vector
        '-hls_subtitle_path',  # <string> E.......... set path of hls subtitles
        '-hls_segment_type',  # <int> E.......... set hls segment files type (from 0 to 1) (default mpegts)
        '-hls_fmp4_init_filename',  # <string> E.......... set fragment mp4 file init filename (default "init.mp4")
        '-hls_fmp4_init_resend',  # <boolean> E.......... resend fragment mp4 init file after refresh m3u8 every time (default false)
        '-hls_flags',  # <flags> E.......... set flags affecting HLS playlist and media file generation (default 0)
        '-strftime',  # <boolean> E.......... set filename expansion with strftime at segment creation (default false)
        '-strftime_mkdir',  # <boolean> E.......... create last directory component in strftime-generated filename (default false)
        '-hls_playlist_type',  # <int> E.......... set the HLS playlist type (from 0 to 2) (default 0)
        '-hls_start_number_source',  # <int> E.......... set source of first number in sequence (from 0 to 3) (default generic)
        '-var_stream_map',  # <string> E.......... Variant stream map string
        '-cc_stream_map',  # <string> E.......... Closed captions stream map string
        '-master_pl_name',  # <string> E.......... Create HLS master playlist with this name
        '-master_pl_publish_rate',  # <int> E.......... Publish master play list every after this many segment intervals (from 0 to UINT32_MAX) (default 0)
        '-update',  # <boolean> E.......... continuously overwrite one file (default false)
        '-frame_pts',  # <boolean> E.......... use current frame pts for filename (default false)
        '-atomic_writing',  # <boolean> E.......... write files atomically (using temporary files and renames) (default false)
        '-protocol_opts',  # <dictionary> E.......... specify protocol options for the opened files
        '-cues_to_front',  # <boolean> E.......... Move Cues (the index) to the front by shifting data if necessary (default false)
        '-cluster_size_limit',  # <int> E.......... Store at most the provided amount of bytes in a cluster. (from -1 to INT_MAX) (default -1)
        '-cluster_time_limit',  # <int64> E.......... Store at most the provided number of milliseconds in a cluster. (from -1 to I64_MAX) (default -1)
        '-dash',  # <boolean> E.......... Create a WebM file conforming to WebM DASH specification (default false)
        '-dash_track_number',  # <int> E.......... Track number for the DASH stream (from 1 to INT_MAX) (default 1)
        '-live',  # <boolean> E.......... Write files assuming it is a live stream. (default false)
        '-allow_raw_vfw',  # <boolean> E.......... allow RAW VFW mode (default false)
        '-write_crc32',  # <boolean> E.......... write a CRC32 element inside every Level 1 element (default true)
        '-default_mode',  # <int> E.......... Controls how a track's FlagDefault is inferred (from 0 to 2) (default passthrough)
        '-write_id3v1',  # <boolean> E.......... Enable ID3v1 writing. ID3v1 tags are written in UTF-8 which may not be supported by most software. (default false)
        '-write_xing',  # <boolean> E.......... Write the Xing header containing file duration. (default true)
        '-muxrate',  # <int> E.......... mux rate as bits/s (from 0 to 1.67772e+09) (default 0)
        '-preload',  # <int> E.......... initial demux-decode delay in microseconds (from 0 to INT_MAX) (default 500000)
        '-mpegts_transport_stream_id',  # <int> E.......... Set transport_stream_id field. (from 1 to 65535) (default 1)
        '-mpegts_original_network_id',  # <int> E.......... Set original_network_id field. (from 1 to 65535) (default 65281)
        '-mpegts_service_id',  # <int> E.......... Set service_id field. (from 1 to 65535) (default 1)
        '-mpegts_service_type',  # <int> E.......... Set service_type field. (from 1 to 255) (default digital_tv)
        '-mpegts_pmt_start_pid',  # <int> E.......... Set the first pid of the PMT. (from 32 to 8186) (default 4096)
        '-mpegts_start_pid',  # <int> E.......... Set the first pid. (from 32 to 8186) (default 256)
        '-mpegts_m2ts_mode',  # <boolean> E.......... Enable m2ts mode. (default auto)
        '-pes_payload_size',  # <int> E.......... Minimum PES packet payload in bytes (from 0 to INT_MAX) (default 2930)
        '-mpegts_flags',  # <flags> E.......... MPEG-TS muxing flags (default 0)
        '-mpegts_copyts',  # <boolean> E.......... don't offset dts/pts (default auto)
        '-tables_version',  # <int> E.......... set PAT, PMT, SDT and NIT version (from 0 to 31) (default 0)
        '-omit_video_pes_length',  # <boolean> E.......... Omit the PES packet length for video packets (default true)
        '-pcr_period',  # <int> E.......... PCR retransmission time in milliseconds (from -1 to INT_MAX) (default -1)
        '-pat_period',  # <duration> E.......... PAT/PMT retransmission time limit in seconds (default 0.1)
        '-sdt_period',  # <duration> E.......... SDT retransmission time limit in seconds (default 0.5)
        '-nit_period',  # <duration> E.......... NIT retransmission time limit in seconds (default 0.5)
        '-signal_standard',  # <int> E.......... Force/set Signal Standard (from -1 to 7) (default -1)
        '-store_user_comments',  # <boolean> E.......... (default true)
        '-d10_channelcount',  # <int> E.......... Force/set channelcount in generic sound essence descriptor (from -1 to 8) (default -1)
        '-mxf_audio_edit_rate',  # <rational> E.......... Audio edit rate for timecode (from 0 to INT_MAX) (default 25/1)
        '-syncpoints',  # <flags> E.......... NUT syncpoint behaviour (default 0)
        '-write_index',  # <boolean> E.......... Write index (default true)
        '-serial_offset',  # <int> E.......... serial number offset (from 0 to INT_MAX) (default 0)
        '-oggpagesize',  # <int> E.......... Set preferred Ogg page size. (from 0 to 65025) (default 0)
        '-pagesize',  # <int> E.......... preferred page size in bytes (deprecated) (from 0 to 65025) (default 0)
        '-page_duration',  # <int64> E.......... preferred page duration, in microseconds (from 0 to I64_MAX) (default 1000000)
        '-payload_type',  # <int> E.......... Specify RTP payload type (from -1 to 127) (default -1)
        '-ssrc',  # <int> E.......... Stream identifier (from INT_MIN to INT_MAX) (default 0)
        '-cname',  # <string> E.......... CNAME to include in RTCP SR packets
        '-seq',  # <int> E.......... Starting sequence number (from -1 to 65535) (default -1)
        '-mpegts_muxer_options',  # <dictionary> E.......... set list of options for the MPEG-TS muxer
        '-rtp_muxer_options',  # <dictionary> E.......... set list of options for the RTP muxer
        '-initial_pause',  # <boolean> .D......... do not start playing the stream immediately (default false)
        '-rtsp_transport',  # <flags> ED......... set RTSP transport protocols (default 0)
        '-rtsp_flags',  # <flags> .D......... set RTSP flags (default 0)
        '-allowed_media_types',  # <flags> .D......... set media types to accept from the server (default video+audio+data+subtitle)
        '-min_port',  # <int> ED......... set minimum local UDP port (from 0 to 65535) (default 5000)
        '-max_port',  # <int> ED......... set maximum local UDP port (from 0 to 65535) (default 65000)
        '-reorder_queue_size',  # <int> .D......... set number of packets to buffer for handling of reordered packets (from -1 to INT_MAX) (default -1)
        '-reference_stream',  # <string> E.......... set reference stream (default "auto")
        '-segment_format',  # <string> E.......... set container format used for the segments
        '-segment_format_options',  # <dictionary> E.......... set list of options for the container format used for the segments
        '-segment_list',  # <string> E.......... set the segment list filename
        '-segment_header_filename',  # <string> E.......... write a single file containing the header
        '-segment_list_flags',  # <flags> E.......... set flags affecting segment list generation (default cache)
        '-segment_list_size',  # <int> E.......... set the maximum number of playlist entries (from 0 to INT_MAX) (default 0)
        '-segment_list_type',  # <int> E.......... set the segment list type (from -1 to 4) (default -1)
        '-segment_atclocktime',  # <boolean> E.......... set segment to be cut at clocktime (default false)
        '-segment_clocktime_offset',  # <duration> E.......... set segment clocktime offset (default 0)
        '-segment_clocktime_wrap_duration',  # <duration> E.......... set segment clocktime wrapping duration (default INT64_MAX)
        '-segment_time',  # <duration> E.......... set segment duration (default 2)
        '-segment_time_delta',  # <duration> E.......... set approximation value used for the segment times (default 0)
        '-min_seg_duration',  # <duration> E.......... set minimum segment duration (default 0)
        '-segment_times',  # <string> E.......... set segment split time points
        '-segment_frames',  # <string> E.......... set segment split frame numbers
        '-segment_wrap',  # <int> E.......... set number after which the index wraps (from 0 to INT_MAX) (default 0)
        '-segment_list_entry_prefix',  # <string> E.......... set base url prefix for segments
        '-segment_start_number',  # <int> E.......... set the sequence number of the first segment (from 0 to INT_MAX) (default 0)
        '-segment_wrap_number',  # <int> E.......... set the number of wrap before the first segment (from 0 to INT_MAX) (default 0)
        '-increment_tc',  # <boolean> E.......... increment timecode between each segment (default false)
        '-break_non_keyframes',  # <boolean> E.......... allow breaking segments on non-keyframes (default false)
        '-individual_header_trailer',  # <boolean> E.......... write header/trailer to each segment (default true)
        '-write_header_trailer',  # <boolean> E.......... write a header to the first segment and a trailer to the last one (default true)
        '-reset_timestamps',  # <boolean> E.......... reset timestamps at the beginning of each segment (default false)
        '-initial_offset',  # <duration> E.......... set initial timestamp offset (default 0)
        '-write_empty_segments',  # <boolean> E.......... allow writing empty 'filler' segments (default false)
        '-lookahead_count',  # <int> E.......... number of lookahead fragments (from 0 to INT_MAX) (default 2)
        '-spdif_flags',  # <flags> E.......... IEC 61937 encapsulation flags (default 0)
        '-dtshd_rate',  # <int> E.......... mux complete DTS frames in HD mode at the specified IEC958 rate (in Hz, default 0=disabled) (from 0 to 768000) (default 0)
        '-dtshd_fallback_time',  # <int> E.......... min secs to strip HD for after an overflow (-1: till the end, default 60) (from -1 to INT_MAX) (default 60)
        '-use_fifo',  # <boolean> E.......... Use fifo pseudo-muxer to separate actual muxers from encoder (default false)
        '-fifo_options',  # <dictionary> E.......... fifo pseudo-muxer options
        '-write_bext',  # <boolean> E.......... Write BEXT chunk. (default false)
        '-write_peak',  # <int> E.......... Write Peak Envelope chunk. (from 0 to 2) (default off)
        '-rf64',  # <int> E.......... Use RF64 header rather than RIFF for large files. (from -1 to 1) (default never)
        '-peak_block_size',  # <int> E.......... Number of audio samples used to generate each peak frame. (from 0 to 65536) (default 256)
        '-peak_format',  # <int> E.......... The format of the peak envelope data (1: uint8, 2: uint16). (from 1 to 2) (default 2)
        '-peak_ppv',  # <int> E.......... Number of peak points per peak value (1 or 2). (from 1 to 2) (default 2)
        '-chunk_start_index',  # <int> E.......... start index of the chunk (from 0 to INT_MAX) (default 0)
        '-chunk_duration_ms',  # <int> E.......... duration of each chunk (in milliseconds) (from 0 to INT_MAX) (default 1000)
        '-time_shift_buffer_depth',  # <double> E.......... Smallest time (in seconds) shifting buffer for which any Representation is guaranteed to be available. (from 1 to DBL_MAX) (default 60)
        '-minimum_update_period',  # <int> E.......... Minimum Update Period (in seconds) of the manifest. (from 0 to INT_MAX) (default 0)
        '-header',  # <string> E.......... filename of the header where the initialization data will be written
        '-audio_chunk_duration',  # <int> E.......... duration of each chunk in milliseconds (from 0 to INT_MAX) (default 5000)
        '-list_devices',  # <boolean> E.......... list available audio devices (default false)
        '-audio_device_index',  # <int> E.......... select audio device by index (starts at 0) (from -1 to INT_MAX) (default -1)
        '-window_title',  # <string> E.......... set SDL window title
        '-window_x',  # <int> E.......... set SDL window x position (from INT_MIN to INT_MAX) (default 805240832)
        '-window_y',  # <int> E.......... set SDL window y position (from INT_MIN to INT_MAX) (default 805240832)
        '-window_fullscreen',  # <boolean> E.......... set SDL window fullscreen (default false)
        '-window_borderless',  # <boolean> E.......... set SDL window border off (default false)
        '-window_enable_quit',  # <int> E.......... set if quit action is available (from 0 to 1) (default 1)
        '-raw_packet_size',  # <int> .D......... (from 1 to INT_MAX) (default 1024)
        '-linespeed',  # <int> .D......... set simulated line speed (bytes per second) (from 1 to INT_MAX) (default 6000)
        '-video_size',  # <image_size> .D......... set video size, such as 640x480 or hd720.
        '-framerate',  # <video_rate> .D......... set framerate (frames per second) (default "25")
        '-ignore_loop',  # <boolean> .D......... ignore loop setting (default true)
        '-max_fps',  # <int> .D......... maximum framerate (0 is no limit) (from 0 to INT_MAX) (default 0)
        '-default_fps',  # <int> .D......... default framerate (0 is as fast as possible) (from 0 to INT_MAX) (default 15)
        '-sample_rate',  # <int> .D......... (from 0 to INT_MAX) (default 48000)
        '-no_resync_search',  # <boolean> .D......... Don't try to resynchronize by looking for a certain optional start code (default false)
        '-export_xmp',  # <boolean> .D......... Export full XMP metadata (default false)
        '-pixel_format',  # <string> .D......... set pixel format (default "yuv420p")
        '-frame_rate',  # <video_rate> .D......... (default "15")
        '-safe',  # <boolean> .D......... enable safe mode (default true)
        '-auto_convert',  # <boolean> .D......... automatically convert bitstream format (default true)
        '-segment_time_metadata',  # <boolean> .D......... output file segment start time and duration as packet metadata (default false)
        '-allowed_extensions',  # <string> .D......... List of file extensions that dash is allowed to access (default "aac,m4a,m4s,m4v,mov,mp4,webm,ts")
        '-cenc_decryption_key',  # <string> .D......... Media decryption key (hex)
        '-flv_metadata',  # <boolean> .D.V....... Allocate streams according to the onMetaData array (default false)
        '-flv_full_metadata',  # <boolean> .D.V....... Dump full metadata of the onMetadata (default false)
        '-flv_ignore_prevtag',  # <boolean> .D.V....... Ignore the Size of previous tag (default false)
        '-missing_streams',  # <int> .D.V..XR... (from 0 to 255) (default 0)
        '-min_delay',  # <int> .D......... minimum valid delay between frames (in hundredths of second) (from 0 to 6000) (default 2)
        '-max_gif_delay',  # <int> .D......... maximum valid delay between frames (in hundredths of seconds) (from 0 to 65535) (default 65535)
        '-default_delay',  # <int> .D......... default delay between frames (in hundredths of second) (from 0 to 6000) (default 10)
        '-hca_lowkey',  # <int64> .D......... Low key used for handling CRI HCA files (from 0 to UINT32_MAX) (default 0)
        '-hca_highkey',  # <int64> .D......... High key used for handling CRI HCA files (from 0 to UINT32_MAX) (default 0)
        '-hca_subkey',  # <int> .D......... Subkey used for handling CRI HCA files (from 0 to 65535) (default 0)
        '-live_start_index',  # <int> .D......... segment index to start live streams at (negative values are from the end) (from INT_MIN to INT_MAX) (default -3)
        '-prefer_x_start',  # <boolean> .D......... prefer to use #EXT-X-START if it's in playlist instead of live_start_index (default false)
        '-max_reload',  # <int> .D......... Maximum number of times a insufficient list is attempted to be reloaded (from 0 to INT_MAX) (default 3)
        '-m3u8_hold_counters',  # <int> .D......... The maximum number of times to load m3u8 when it refreshes without new segments (from 0 to INT_MAX) (default 1000)
        '-http_multiple',  # <boolean> .D......... Use multiple HTTP connections for fetching segments (default auto)
        '-http_seekable',  # <boolean> .D......... Use HTTP partial requests, 0 = disable, 1 = enable, -1 = auto (default auto)
        '-seg_format_options',  # <dictionary> .D......... Set options for segment demuxer
        '-seg_max_retry',  # <int> .D......... Maximum number of times to reload a segment on error. (from 0 to INT_MAX) (default 0)
        '-pattern_type',  # <int> .D......... set pattern type (from 0 to INT_MAX) (default 4)
        '-start_number_range',  # <int> .D......... set range for looking at the first sequence number (from 1 to INT_MAX) (default 5)
        '-ts_from_file',  # <int> .D......... set frame timestamp from file's one (from 0 to 2) (default none)
        '-export_path_metadata',  # <boolean> .D......... enable metadata containing input path information (default false)
        '-use_absolute_path',  # <boolean> .D.V....... allow using absolute path when opening alias, this is a possible security issue (default false)
        '-seek_streams_individually',  # <boolean> .D.V....... Seek each stream individually to the closest point (default true)
        '-ignore_editlist',  # <boolean> .D.V....... Ignore the edit list atom. (default false)
        '-advanced_editlist',  # <boolean> .D.V....... Modify the AVIndex according to the editlists. Use this option to decode in the order specified by the edits. (default true)
        '-ignore_chapters',  # <boolean> .D.V....... (default false)
        '-use_mfra_for',  # <int> .D.V....... use mfra for fragment timestamps (from -1 to 2) (default auto)
        '-use_tfdt',  # <boolean> .D.V....... use tfdt for fragment timestamps (default true)
        '-export_all',  # <boolean> .D.V....... Export unrecognized metadata entries (default false)
        '-activation_bytes',  # <binary> .D......... Secret bytes for Audible AAX files
        '-audible_key',  # <binary> .D......... AES-128 Key for Audible AAXC files
        '-audible_iv',  # <binary> .D......... AES-128 IV for Audible AAXC files
        '-audible_fixed_key',  # <binary> .D......... Fixed key used for handling Audible AAX files
        '-enable_drefs',  # <boolean> .D.V....... Enable external track support. (default false)
        '-max_stts_delta',  # <int> .D......... treat offsets above this value as invalid (from 0 to UINT32_MAX) (default 4294487295)
        '-interleaved_read',  # <boolean> .D......... Interleave packets from multiple tracks at demuxer level (default true)
        '-resync_size',  # <int> .D......... set size limit for looking up a new synchronization (from 0 to INT_MAX) (default 65536)
        '-fix_teletext_pts',  # <boolean> .D......... try to fix pts values of dvb teletext streams (default true)
        '-scan_all_pmts',  # <boolean> .D......... scan and combine all PMTs (default auto)
        '-skip_unknown_pmt',  # <boolean> .D......... skip PMTs for programs not advertised in the PAT (default false)
        '-merge_pmt_versions',  # <boolean> .D......... re-use streams when PMT's version/pids change (default false)
        '-max_packet_size',  # <int> .D......... maximum size of emitted packet (from 1 to 1.07374e+09) (default 204800)
        '-compute_pcr',  # <boolean> .D......... compute exact PCR for each transport stream packet (default false)
        '-rtp_flags',  # <flags> .D......... set RTP flags (default 0)
        '-max_file_size',  # <int> .D......... (from 0 to INT_MAX) (default 5000000)
        '-sdp_flags',  # <flags> .D......... SDP flags (default 0)
        '-chars_per_frame',  # <int> .D......... (from 1 to INT_MAX) (default 6000)
        '-ignore_length',  # <boolean> .D......... Ignore length (default false)
        '-max_size',  # <int> .D......... max size of single packet (from 0 to 4.1943e+06) (default 0)
        '-bandwidth',  # <int> .D......... bandwidth of this stream to be specified in the DASH manifest. (from 0 to INT_MAX) (default 0)
        '-video_device_index',  # <int> .D......... select video device by index for devices with same name (starts at 0) (from -1 to INT_MAX) (default -1)
        '-capture_cursor',  # <boolean> .D......... capture the screen cursor (default false)
        '-capture_mouse_clicks',  # <boolean> .D......... capture the screen mouse clicks (default false)
        '-capture_raw_data',  # <boolean> .D......... capture the raw data from device connection (default false)
        '-drop_late_frames',  # <boolean> .D......... drop frames that are available later than expected (default true)
        '-graph',  # <string> .D......... set libavfilter graph
        '-graph_file',  # <string> .D......... set libavfilter graph filename
        '-dumpgraph',  # <string> .D......... dump graph to stderr
        '-window_id',  # <int> .D......... Window to capture. (from 0 to UINT32_MAX) (default 0)
        '-x',  # <int> .D......... Initial x coordinate. (from 0 to INT_MAX) (default 0)
        '-grab_x',  # <int> .D......... Initial x coordinate. (from 0 to INT_MAX) (default 0)
        '-grab_y',  # <int> .D......... Initial y coordinate. (from 0 to INT_MAX) (default 0)
        '-draw_mouse',  # <int> .D......... Draw the mouse pointer. (from 0 to 1) (default 1)
        '-follow_mouse',  # <int> .D......... Move the grabbing region when the mouse pointer reaches within specified amount of pixels to the edge of region. (from -1 to INT_MAX) (default 0)
        '-show_region',  # <int> .D......... Show the grabbing region. (from 0 to 1) (default 0)
        '-region_border',  # <int> .D......... Set the region border thickness. (from 1 to 128) (default 3)
        '-select_region',  # <boolean> .D......... Select the grabbing region graphically using the pointer. (default false)
        '-sws_flags',  # <flags> E..V....... scaler flags (default bicubic)
        '-srcw',  # <int> E..V....... source width (from 1 to INT_MAX) (default 16)
        '-srch',  # <int> E..V....... source height (from 1 to INT_MAX) (default 16)
        '-dstw',  # <int> E..V....... destination width (from 1 to INT_MAX) (default 16)
        '-dsth',  # <int> E..V....... destination height (from 1 to INT_MAX) (default 16)
        '-src_format',  # <pix_fmt> E..V....... source format (default yuv420p)
        '-dst_format',  # <pix_fmt> E..V....... destination format (default yuv420p)
        '-src_range',  # <boolean> E..V....... source is full range (default false)
        '-dst_range',  # <boolean> E..V....... destination is full range (default false)
        '-param0',  # <double> E..V....... scaler param 0 (from INT_MIN to INT_MAX) (default 123456)
        '-param1',  # <double> E..V....... scaler param 1 (from INT_MIN to INT_MAX) (default 123456)
        '-src_v_chr_pos',  # <int> E..V....... source vertical chroma position in luma grid/256 (from -513 to 512) (default -513)
        '-src_h_chr_pos',  # <int> E..V....... source horizontal chroma position in luma grid/256 (from -513 to 512) (default -513)
        '-dst_v_chr_pos',  # <int> E..V....... destination vertical chroma position in luma grid/256 (from -513 to 512) (default -513)
        '-dst_h_chr_pos',  # <int> E..V....... destination horizontal chroma position in luma grid/256 (from -513 to 512) (default -513)
        '-sws_dither',  # <int> E..V....... set dithering algorithm (from 0 to 6) (default auto)
        '-alphablend',  # <int> E..V....... mode for alpha -> non alpha (from 0 to 2) (default none)
        '-isr',  # <int> ....A...... set input sample rate (from 0 to INT_MAX) (default 0)
        '-in_sample_rate',  # <int> ....A...... set input sample rate (from 0 to INT_MAX) (default 0)
        '-osr',  # <int> ....A...... set output sample rate (from 0 to INT_MAX) (default 0)
        '-out_sample_rate',  # <int> ....A...... set output sample rate (from 0 to INT_MAX) (default 0)
        '-isf',  # <sample_fmt> ....A...... set input sample format (default none)
        '-in_sample_fmt',  # <sample_fmt> ....A...... set input sample format (default none)
        '-osf',  # <sample_fmt> ....A...... set output sample format (default none)
        '-out_sample_fmt',  # <sample_fmt> ....A...... set output sample format (default none)
        '-tsf',  # <sample_fmt> ....A...... set internal sample format (default none)
        '-internal_sample_fmt',  # <sample_fmt> ....A...... set internal sample format (default none)
        '-ichl',  # <channel_layout> ....A...... set input channel layout
        '-in_chlayout',  # <channel_layout> ....A...... set input channel layout
        '-ochl',  # <channel_layout> ....A...... set output channel layout
        '-out_chlayout',  # <channel_layout> ....A...... set output channel layout
        '-uchl',  # <channel_layout> ....A...... set used channel layout
        '-used_chlayout',  # <channel_layout> ....A...... set used channel layout
        '-clev',  # <float> ....A...... set center mix level (from -32 to 32) (default 0.707107)
        '-center_mix_level',  # <float> ....A...... set center mix level (from -32 to 32) (default 0.707107)
        '-slev',  # <float> ....A...... set surround mix level (from -32 to 32) (default 0.707107)
        '-surround_mix_level',  # <float> ....A...... set surround mix Level (from -32 to 32) (default 0.707107)
        '-lfe_mix_level',  # <float> ....A...... set LFE mix level (from -32 to 32) (default 0)
        '-rmvol',  # <float> ....A...... set rematrix volume (from -1000 to 1000) (default 1)
        '-rematrix_volume',  # <float> ....A...... set rematrix volume (from -1000 to 1000) (default 1)
        '-rematrix_maxval',  # <float> ....A...... set rematrix maxval (from 0 to 1000) (default 0)
        '-swr_flags',  # <flags> ....A...... set flags (default 0)
        '-dither_scale',  # <float> ....A...... set dither scale (from 0 to INT_MAX) (default 1)
        '-dither_method',  # <int> ....A...... set dither method (from 0 to 71) (default 0)
        '-filter_size',  # <int> ....A...... set swr resampling filter size (from 0 to INT_MAX) (default 32)
        '-phase_shift',  # <int> ....A...... set swr resampling phase shift (from 0 to 24) (default 10)
        '-linear_interp',  # <boolean> ....A...... enable linear interpolation (default true)
        '-exact_rational',  # <boolean> ....A...... enable exact rational (default true)
        '-resample_cutoff',  # <double> ....A...... set cutoff frequency ratio (from 0 to 1) (default 0)
        '-resampler',  # <int> ....A...... set resampling Engine (from 0 to 1) (default swr)
        '-precision',  # <double> ....A...... set soxr resampling precision (in bits) (from 15 to 33) (default 20)
        '-cheby',  # <boolean> ....A...... enable soxr Chebyshev passband & higher-precision irrational ratio approximation (default false)
        '-min_comp',  # <float> ....A...... set minimum difference between timestamps and audio data (in seconds) below which no timestamp compensation of either kind is applied (from 0 to FLT_MAX) (default FLT_MAX)
        '-min_hard_comp',  # <float> ....A...... set minimum difference between timestamps and audio data (in seconds) to trigger padding/trimming the data. (from 0 to INT_MAX) (default 0.1)
        '-comp_duration',  # <float> ....A...... set duration (in seconds) over which data is stretched/squeezed to make it match the timestamps. (from 0 to INT_MAX) (default 1)
        '-max_soft_comp',  # <float> ....A...... set maximum factor by which data is stretched/squeezed to make it match the timestamps. (from INT_MIN to INT_MAX) (default 0)
        '-first_pts',  # <int64> ....A...... Assume the first pts should be this value (in samples). (from I64_MIN to I64_MAX) (default I64_MIN)
        '-matrix_encoding',  # <int> ....A...... set matrixed stereo encoding (from 0 to 6) (default none)
        '-filter_type',  # <int> ....A...... select swr filter type (from 0 to 2) (default kaiser)
        '-kaiser_beta',  # <double> ....A...... set swr Kaiser window beta (from 2 to 16) (default 9)
        '-output_sample_bits',  # <int> ....A...... set swr number of output sample bits (from 0 to 64) (default 0)
        '-amount',  # <string> ...VA...B..
        '-dropamount',  # <int> ...VA...B.. (from 0 to INT_MAX) (default 0)
        '-tilt',  # <int> ...V....... Tilt the video horizontally while shifting (from 0 to 1) (default 1)
        '-hold',  # <int> ...V....... Number of columns to hold at the start of the video (from 0 to INT_MAX) (default 0)
        '-pad',  # <int> ...V....... Number of columns to pad at the end of the video (from 0 to INT_MAX) (default 0)
        '-td',  # <int> ...V....B.. Temporal Delimiter OBU (from 0 to 2) (default pass)
        '-transfer_characteristics',  # <int> ...V....B.. Set transfer characteristics (section 6.4.2) (from -1 to 255) (default -1)
        '-matrix_coefficients',  # <int> ...V....B.. Set matrix coefficients (section 6.4.2) (from -1 to 255) (default -1)
        '-chroma_sample_position',  # <int> ...V....B.. Set chroma sample position (section 6.4.2) (from -1 to 3) (default -1)
        '-tick_rate',  # <rational> ...V....B.. Set display tick rate (time_scale / num_units_in_display_tick) (from 0 to UINT32_MAX) (default 0/1)
        '-num_ticks_per_picture',  # <int> ...V....B.. Set display ticks per picture for CFR streams (from -1 to INT_MAX) (default -1)
        '-delete_padding',  # <boolean> ...V....B.. Delete all Padding OBUs (default false)
        '-color',  # <color> ...V....B.. set color (default "yellow")
        '-sta',  # <flags> ...V....B.. specify which error status value to match (default Aa+Ba+Ca+erri+erru+err+Ab+Bb+Cb+A+B+C+a+b+res+notok+notres)
        '-pass_types',  # <string> ...V....B.. List of unit types to pass through the filter.
        '-remove_types',  # <string> ...V....B.. List of unit types to remove in the filter.
        '-discard_flags',  # <flags> ...V....B.. flags to control the discard frame behavior (default 0)
        '-sample_aspect_ratio',  # <rational> ...V....B.. Set sample aspect ratio (table E-1) (from 0 to 65535) (default 0/1)
        '-overscan_appropriate_flag',  # <int> ...V....B.. Set VUI overscan appropriate flag (from -1 to 1) (default -1)
        '-video_full_range_flag',  # <int> ...V....B.. Set video full range flag (from -1 to 1) (default -1)
        '-colour_primaries',  # <int> ...V....B.. Set colour primaries (table E-3) (from -1 to 255) (default -1)
        '-chroma_sample_loc_type',  # <int> ...V....B.. Set chroma sample location type (figure E-1) (from -1 to 5) (default -1)
        '-fixed_frame_rate_flag',  # <int> ...V....B.. Set VUI fixed frame rate flag (from -1 to 1) (default -1)
        '-zero_new_constraint_set_flags',  # <boolean> ...V....B.. Set constraint_set4_flag / constraint_set5_flag to zero (default false)
        '-crop_left',  # <int> ...V....B.. Set left border crop offset (from -1 to 16880) (default -1)
        '-crop_right',  # <int> ...V....B.. Set right border crop offset (from -1 to 16880) (default -1)
        '-crop_top',  # <int> ...V....B.. Set top border crop offset (from -1 to 16880) (default -1)
        '-crop_bottom',  # <int> ...V....B.. Set bottom border crop offset (from -1 to 16880) (default -1)
        '-sei_user_data',  # <string> ...V....B.. Insert SEI user data (UUID+string)
        '-delete_filler',  # <int> ...V....B.. Delete all filler (both NAL and SEI) (from 0 to 1) (default 0)
        '-display_orientation',  # <int> ...V....B.. Display orientation SEI (from 0 to 3) (default pass)
        '-rotate',  # <double> ...V....B.. Set rotation in display orientation SEI (anticlockwise angle in degrees) (from -360 to 360) (default nan)
        '-flip',  # <flags> ...V....B.. Set flip in display orientation SEI (default 0)
        '-num_ticks_poc_diff_one',  # <int> ...V....B.. Set VPS and VUI number of ticks per POC increment (from -1 to INT_MAX) (default -1)
        '-display_aspect_ratio',  # <rational> ...V....B.. Set display aspect ratio (table 6-3) (from 0 to 65535) (default 0/1)
        '-nb_out_samples',  # <int> ....A...B.. set the number of per-packet output samples (from 1 to INT_MAX) (default 1024)
        '-p',  # <boolean> ....A...B.. pad last packet with zeros (default true)
        '-pts',  # <string> ...VAS..B.. set expression for packet PTS
        '-dts',  # <string> ...VAS..B.. set expression for packet DTS
        '-duration',  # <string> ...VAS..B.. set expression for packet duration (default "DURATION")
        '-color_space',  # <int> ...V....B.. Set colour space (section 7.2.2) (from -1 to 7) (default -1)
    ]

    def h(self, *args, **kwargs):
        """
        -- print basic options
        
        """
        
        raise NotImplementedError
        
    def L(self, *args, **kwargs):
        """
        show license
        
        """
        
        raise NotImplementedError
        
    def version(self, *args, **kwargs):
        """
        show version
        
        """
        
        raise NotImplementedError
        
    def muxers(self, *args, **kwargs):
        """
        show available muxers
        
        """
        
        raise NotImplementedError
        
    def demuxers(self, *args, **kwargs):
        """
        show available demuxers
        
        """
        
        raise NotImplementedError
        
    def devices(self, *args, **kwargs):
        """
        show available devices
        
        """
        
        raise NotImplementedError
        
    def decoders(self, *args, **kwargs):
        """
        show available decoders
        
        """
        
        raise NotImplementedError
        
    def encoders(self, *args, **kwargs):
        """
        show available encoders
        
        """
        
        raise NotImplementedError
        
    def filters(self, *args, **kwargs):
        """
        show available filters
        
        """
        
        raise NotImplementedError
        
    def pix_fmts(self, *args, **kwargs):
        """
        show available pixel formats
        
        """
        
        raise NotImplementedError
        
    def layouts(self, *args, **kwargs):
        """
        show standard channel layouts
        
        """
        
        raise NotImplementedError
        
    def sample_fmts(self, *args, **kwargs):
        """
        show available audio sample formats
        
        """
        
        raise NotImplementedError
        
    def help(self, *args, **kwargs):
        """
        <topic> show help
        
        --help <topic>      show help
        """
        
        raise NotImplementedError
        
    def buildconf(self, *args, **kwargs):
        """
        show build configuration
        
        """
        
        raise NotImplementedError
        
    def formats(self, *args, **kwargs):
        """
        show available formats
        
        """
        
        raise NotImplementedError
        
    def codecs(self, *args, **kwargs):
        """
        show available codecs
        
        """
        
        raise NotImplementedError
        
    def bsfs(self, *args, **kwargs):
        """
        show available bit stream filters
        
        """
        
        raise NotImplementedError
        
    def protocols(self, *args, **kwargs):
        """
        show available protocols
        
        """
        
        raise NotImplementedError
        
    def dispositions(self, *args, **kwargs):
        """
        show available stream dispositions
        
        """
        
        raise NotImplementedError
        
    def colors(self, *args, **kwargs):
        """
        show available color names
        
        """
        
        raise NotImplementedError
        
    def sources(self, *args, **kwargs):
        """
        <device> list sources of the input device
        
        """
        
        raise NotImplementedError
        
    def sinks(self, *args, **kwargs):
        """
        <device> list sinks of the output device
        
        """
        
        raise NotImplementedError
        
    def hwaccels(self, *args, **kwargs):
        """
        show available HW acceleration methods
        
        """
        
        raise NotImplementedError
        
    def v(self, *args, **kwargs):
        """
        <loglevel> set logging level
        
        """
        
        raise NotImplementedError
        
    def y(self, *args, **kwargs):
        """
        overwrite output files
        
        """
        
        raise NotImplementedError
        
    def n(self, *args, **kwargs):
        """
        never overwrite output files
        
        """
        
        raise NotImplementedError
        
    def stats(self, *args, **kwargs):
        """
        print progress report during encoding
        
        """
        
        raise NotImplementedError
        
    def loglevel(self, *args, **kwargs):
        """
        <loglevel> set logging level
        
        """
        
        raise NotImplementedError
        
    def report(self, *args, **kwargs):
        """
        generate a report
        
        """
        
        raise NotImplementedError
        
    def max_alloc(self, *args, **kwargs):
        """
        <bytes> set maximum size of a single allocated block
        
        """
        
        raise NotImplementedError
        
    def cpuflags(self, *args, **kwargs):
        """
        <flags> force specific cpu flags
        
        """
        
        raise NotImplementedError
        
    def cpucount(self, *args, **kwargs):
        """
        <count> force specific cpu count
        
        """
        
        raise NotImplementedError
        
    def hide_banner(self, *args, **kwargs):
        """
        <hide_banner> do not show program banner
        
        """
        
        raise NotImplementedError
        
    def ignore_unknown(self, *args, **kwargs):
        """
        Ignore unknown stream types
        
        """
        
        raise NotImplementedError
        
    def copy_unknown(self, *args, **kwargs):
        """
        Copy unknown stream types
        
        """
        
        raise NotImplementedError
        
    def recast_media(self, *args, **kwargs):
        """
        allow recasting stream type in order to force a decoder of different media type
        
        """
        
        raise NotImplementedError
        
    def benchmark(self, *args, **kwargs):
        """
        add timings for benchmarking
        
        """
        
        raise NotImplementedError
        
    def benchmark_all(self, *args, **kwargs):
        """
        add timings for each task
        
        """
        
        raise NotImplementedError
        
    def progress(self, *args, **kwargs):
        """
        <url> write program-readable progress information
        
        """
        
        raise NotImplementedError
        
    def stdin(self, *args, **kwargs):
        """
        enable or disable interaction on standard input
        
        """
        
        raise NotImplementedError
        
    def timelimit(self, *args, **kwargs):
        """
        <limit> set max runtime in seconds in CPU user time
        
        """
        
        raise NotImplementedError
        
    def dump(self, *args, **kwargs):
        """
        dump each input packet
        
        """
        
        raise NotImplementedError
        
    def hex(self, *args, **kwargs):
        """
        when dumping packets, also dump the payload
        
        """
        
        raise NotImplementedError
        
    def frame_drop_threshold(self, *args, **kwargs):
        """
        <> frame drop threshold
        
        """
        
        raise NotImplementedError
        
    def copyts(self, *args, **kwargs):
        """
        copy timestamps
        
        """
        
        raise NotImplementedError
        
    def start_at_zero(self, *args, **kwargs):
        """
        shift input timestamps to start at 0 when using copyts
        
        """
        
        raise NotImplementedError
        
    def copytb(self, *args, **kwargs):
        """
        <mode> copy input stream time base when stream copying
        
        """
        
        raise NotImplementedError
        
    def dts_delta_threshold(self, *args, **kwargs):
        """
        <threshold> timestamp discontinuity delta threshold
        
        """
        
        raise NotImplementedError
        
    def dts_error_threshold(self, *args, **kwargs):
        """
        <threshold> timestamp error delta threshold
        
        """
        
        raise NotImplementedError
        
    def xerror(self, *args, **kwargs):
        """
        <error> exit on error
        
        """
        
        raise NotImplementedError
        
    def abort_on(self, *args, **kwargs):
        """
        <flags> abort on the specified condition flags
        
        """
        
        raise NotImplementedError
        
    def filter_threads(self, *args, **kwargs):
        """
        number of non-complex filter threads
        
        """
        
        raise NotImplementedError
        
    def filter_complex(self, *args, **kwargs):
        """
        <graph_description> create a complex filtergraph
        
        """
        
        raise NotImplementedError
        
    def filter_complex_threads(self, *args, **kwargs):
        """
        number of threads for -filter_complex
        
        """
        
        raise NotImplementedError
        
    def lavfi(self, *args, **kwargs):
        """
        <graph_description> create a complex filtergraph
        
        """
        
        raise NotImplementedError
        
    def filter_complex_script(self, *args, **kwargs):
        """
        <filename> deprecated, use -/filter_complex instead
        
        """
        
        raise NotImplementedError
        
    def auto_conversion_filters(self, *args, **kwargs):
        """
        enable automatic conversion filters globally
        
        """
        
        raise NotImplementedError
        
    def stats_period(self, *args, **kwargs):
        """
        <time> set the period at which ffmpeg updates stats and -progress output
        
        """
        
        raise NotImplementedError
        
    def debug_ts(self, *args, **kwargs):
        """
        print timestamp debugging info
        
        """
        
        raise NotImplementedError
        
    def max_error_rate(self, *args, **kwargs):
        """
        <maximum error rate> ratio of decoding errors (0.0: no errors, 1.0: 100% errors) above which ffmpeg returns an error instead of success.
        
        """
        
        raise NotImplementedError
        
    def vstats(self, *args, **kwargs):
        """
        dump video coding statistics to file
        
        """
        
        raise NotImplementedError
        
    def vstats_file(self, *args, **kwargs):
        """
        <file> dump video coding statistics to file
        
        """
        
        raise NotImplementedError
        
    def vstats_version(self, *args, **kwargs):
        """
        Version of the vstats format to use.
        
        """
        
        raise NotImplementedError
        
    def sdp_file(self, *args, **kwargs):
        """
        <file> specify a file in which to print sdp information
        
        """
        
        raise NotImplementedError
        
    def init_hw_device(self, *args, **kwargs):
        """
        <args> initialise hardware device
        
        """
        
        raise NotImplementedError
        
    def filter_hw_device(self, *args, **kwargs):
        """
        <device> set hardware device used when filtering
        
        """
        
        raise NotImplementedError
        
    def adrift_threshold(self, *args, **kwargs):
        """
        <threshold> deprecated, does nothing
        
        """
        
        raise NotImplementedError
        
    def qphist(self, *args, **kwargs):
        """
        deprecated, does nothing
        
        """
        
        raise NotImplementedError
        
    def vsync(self, *args, **kwargs):
        """
        <> set video sync method globally; deprecated, use -fps_mode
        
        """
        
        raise NotImplementedError
        
    def f(self, *args, **kwargs):
        """
        <fmt> force container format (auto-detected otherwise)
        
        """
        
        raise NotImplementedError
        
    def t(self, *args, **kwargs):
        """
        <duration> stop transcoding after specified duration
        
        """
        
        raise NotImplementedError
        
    def to(self, *args, **kwargs):
        """
        <time_stop> stop transcoding after specified time is reached
        
        """
        
        raise NotImplementedError
        
    def ss(self, *args, **kwargs):
        """
        <time_off> start transcoding at specified time
        
        """
        
        raise NotImplementedError
        
    def bitexact(self, *args, **kwargs):
        """
        bitexact mode
        
        """
        
        raise NotImplementedError
        
    def thread_queue_size(self, *args, **kwargs):
        """
        set the maximum number of queued packets from the demuxer
        
        """
        
        raise NotImplementedError
        
    def sseof(self, *args, **kwargs):
        """
        <time_off> set the start time offset relative to EOF
        
        """
        
        raise NotImplementedError
        
    def seek_timestamp(self, *args, **kwargs):
        """
        enable/disable seeking by timestamp with -ss
        
        """
        
        raise NotImplementedError
        
    def accurate_seek(self, *args, **kwargs):
        """
        enable/disable accurate seeking with -ss
        
        """
        
        raise NotImplementedError
        
    def isync(self, *args, **kwargs):
        """
        <sync ref> Indicate the input index for sync reference
        
        """
        
        raise NotImplementedError
        
    def itsoffset(self, *args, **kwargs):
        """
        <time_off> set the input ts offset
        
        """
        
        raise NotImplementedError
        
    def re(self, *args, **kwargs):
        """
        <> read input at native frame rate; equivalent to -readrate 1
        
        """
        
        raise NotImplementedError
        
    def readrate(self, *args, **kwargs):
        """
        <speed> read input at specified rate
        
        """
        
        raise NotImplementedError
        
    def readrate_initial_burst(self, *args, **kwargs):
        """
        <seconds> The initial amount of input to burst read before imposing any readrate
        
        """
        
        raise NotImplementedError
        
    def dump_attachment(self, *args, **kwargs):
        """
        [:<spec>] <filename> extract an attachment into a file
        
        """
        
        raise NotImplementedError
        
    def stream_loop(self, *args, **kwargs):
        """
        <loop count> set number of times input stream shall be looped
        
        """
        
        raise NotImplementedError
        
    def find_stream_info(self, *args, **kwargs):
        """
        read and decode the streams to fill missing information with heuristics
        
        """
        
        raise NotImplementedError
        
    def map(self, *args, **kwargs):
        """
        <[-]input_file_id[:stream_specifier][,sync_file_id[:stream_specifier]]> set input stream mapping
        
        """
        
        raise NotImplementedError
        
    def map_metadata(self, *args, **kwargs):
        """
        [:<spec>] <outfile[,metadata]:infile[,metadata]> set metadata information of outfile from infile
        
        """
        
        raise NotImplementedError
        
    def map_chapters(self, *args, **kwargs):
        """
        <input_file_index> set chapters mapping
        
        """
        
        raise NotImplementedError
        
    def fs(self, *args, **kwargs):
        """
        <limit_size> set the limit file size in bytes
        
        """
        
        raise NotImplementedError
        
    def timestamp(self, *args, **kwargs):
        """
        <time> set the recording timestamp ('now' to set the current time)
        
        """
        
        raise NotImplementedError
        
    def program(self, *args, **kwargs):
        """
        [:<spec>] <title=string:st=number...> add program with specified streams
        
        """
        
        raise NotImplementedError
        
    def stream_group(self, *args, **kwargs):
        """
        [:<spec>] <id=number:st=number...> add stream group with specified streams and group type-specific arguments
        
        """
        
        raise NotImplementedError
        
    def dframes(self, *args, **kwargs):
        """
        <number> set the number of data frames to output
        
        """
        
        raise NotImplementedError
        
    def target(self, *args, **kwargs):
        """
        <type> specify target file type ("vcd", "svcd", "dvd", "dv" or "dv50" with optional prefixes "pal-", "ntsc-" or "film-")
        
        """
        
        raise NotImplementedError
        
    def shortest(self, *args, **kwargs):
        """
        finish encoding within shortest input
        
        """
        
        raise NotImplementedError
        
    def shortest_buf_duration(self, *args, **kwargs):
        """
        maximum buffering duration (in seconds) for the -shortest option
        
        """
        
        raise NotImplementedError
        
    def qscale(self, *args, **kwargs):
        """
        <q> use fixed quality scale (VBR)
        
        """
        
        raise NotImplementedError
        
    def profile(self, *args, **kwargs):
        """
        <profile> set profile
        
        """
        
        raise NotImplementedError
        
    def attach(self, *args, **kwargs):
        """
        <filename> add an attachment to the output file
        
        """
        
        raise NotImplementedError
        
    def muxdelay(self, *args, **kwargs):
        """
        <seconds> set the maximum demux-decode delay
        
        """
        
        raise NotImplementedError
        
    def muxpreload(self, *args, **kwargs):
        """
        <seconds> set the initial demux-decode delay
        
        """
        
        raise NotImplementedError
        
    def fpre(self, *args, **kwargs):
        """
        <filename> set options from indicated preset file
        
        """
        
        raise NotImplementedError
        
    def c(self, *args, **kwargs):
        """
        [:<stream_spec>] <codec> select encoder/decoder ('copy' to copy stream without reencoding)
        
        """
        
        raise NotImplementedError
        
    def filter(self, *args, **kwargs):
        """
        [:<stream_spec>] <filter_graph> apply specified filters to audio/video
        
        """
        
        raise NotImplementedError
        
    def codec(self, *args, **kwargs):
        """
        [:<stream_spec>] <codec> alias for -c (select encoder/decoder)
        
        """
        
        raise NotImplementedError
        
    def pre(self, *args, **kwargs):
        """
        [:<stream_spec>] <preset> preset name
        
        """
        
        raise NotImplementedError
        
    def itsscale(self, *args, **kwargs):
        """
        [:<stream_spec>] <scale> set the input ts scale
        
        """
        
        raise NotImplementedError
        
    def apad(self, *args, **kwargs):
        """
        [:<stream_spec>] <> audio pad
        
        """
        
        raise NotImplementedError
        
    def copyinkf(self, *args, **kwargs):
        """
        [:<stream_spec>] copy initial non-keyframes
        
        """
        
        raise NotImplementedError
        
    def copypriorss(self, *args, **kwargs):
        """
        [:<stream_spec>] copy or discard frames before start time
        
        """
        
        raise NotImplementedError
        
    def frames(self, *args, **kwargs):
        """
        [:<stream_spec>] <number> set the number of frames to output
        
        """
        
        raise NotImplementedError
        
    def tag(self, *args, **kwargs):
        """
        [:<stream_spec>] <fourcc/tag> force codec tag/fourcc
        
        """
        
        raise NotImplementedError
        
    def q(self, *args, **kwargs):
        """
        [:<stream_spec>] <q> use fixed quality scale (VBR)
        
        """
        
        raise NotImplementedError
        
    def filter_script(self, *args, **kwargs):
        """
        [:<stream_spec>] <filename> deprecated, use -/filter
        
        """
        
        raise NotImplementedError
        
    def reinit_filter(self, *args, **kwargs):
        """
        [:<stream_spec>] <> reinit filtergraph on input parameter changes
        
        """
        
        raise NotImplementedError
        
    def discard(self, *args, **kwargs):
        """
        [:<stream_spec>] <> discard
        
        """
        
        raise NotImplementedError
        
    def disposition(self, *args, **kwargs):
        """
        [:<stream_spec>] <> disposition
        
        """
        
        raise NotImplementedError
        
    def bits_per_raw_sample(self, *args, **kwargs):
        """
        [:<stream_spec>] <number> set the number of bits per raw sample
        
        """
        
        raise NotImplementedError
        
    def stats_enc_pre(self, *args, **kwargs):
        """
        [:<stream_spec>] write encoding stats before encoding
        
        """
        
        raise NotImplementedError
        
    def stats_enc_post(self, *args, **kwargs):
        """
        [:<stream_spec>] write encoding stats after encoding
        
        """
        
        raise NotImplementedError
        
    def stats_mux_pre(self, *args, **kwargs):
        """
        [:<stream_spec>] write packets stats before muxing
        
        """
        
        raise NotImplementedError
        
    def stats_enc_pre_fmt(self, *args, **kwargs):
        """
        [:<stream_spec>] format of the stats written with -stats_enc_pre
        
        """
        
        raise NotImplementedError
        
    def stats_enc_post_fmt(self, *args, **kwargs):
        """
        [:<stream_spec>] format of the stats written with -stats_enc_post
        
        """
        
        raise NotImplementedError
        
    def stats_mux_pre_fmt(self, *args, **kwargs):
        """
        [:<stream_spec>] format of the stats written with -stats_mux_pre
        
        """
        
        raise NotImplementedError
        
    def autorotate(self, *args, **kwargs):
        """
        [:<stream_spec>] automatically insert correct rotate filters
        
        """
        
        raise NotImplementedError
        
    def autoscale(self, *args, **kwargs):
        """
        [:<stream_spec>] automatically insert a scale filter at the end of the filter graph
        
        """
        
        raise NotImplementedError
        
    def time_base(self, *args, **kwargs):
        """
        [:<stream_spec>] <ratio> set the desired time base hint for output stream (1:24, 1:48000 or 0.04166, 2.0833e-5)
        
        """
        
        raise NotImplementedError
        
    def enc_time_base(self, *args, **kwargs):
        """
        [:<stream_spec>] <ratio> set the desired time base for the encoder (1:24, 1:48000 or 0.04166, 2.0833e-5). two special values are defined - 0 = use frame rate (video) or sample rate (audio),-1 = match source time base
        
        """
        
        raise NotImplementedError
        
    def bsf(self, *args, **kwargs):
        """
        [:<stream_spec>] <bitstream_filters> A comma-separated list of bitstream filters
        
        """
        
        raise NotImplementedError
        
    def max_muxing_queue_size(self, *args, **kwargs):
        """
        [:<stream_spec>] <packets> maximum number of packets that can be buffered while waiting for all streams to initialize
        
        """
        
        raise NotImplementedError
        
    def muxing_queue_data_threshold(self, *args, **kwargs):
        """
        [:<stream_spec>] <bytes> set the threshold after which max_muxing_queue_size is taken into account
        
        """
        
        raise NotImplementedError
        
    def r(self, *args, **kwargs):
        """
        [:<stream_spec>] <rate> override input framerate/convert to given output framerate (Hz value, fraction or abbreviation)
        
        """
        
        raise NotImplementedError
        
    def aspect(self, *args, **kwargs):
        """
        [:<stream_spec>] <aspect> set aspect ratio (4:3, 16:9 or 1.3333, 1.7777)
        
        """
        
        raise NotImplementedError
        
    def vn(self, *args, **kwargs):
        """
        disable video
        
        """
        
        raise NotImplementedError
        
    def vcodec(self, *args, **kwargs):
        """
        <codec> alias for -c:v (select encoder/decoder for video streams)
        
        """
        
        raise NotImplementedError
        
    def vf(self, *args, **kwargs):
        """
        <filter_graph> alias for -filter:v (apply filters to video streams)
        
        """
        
        raise NotImplementedError
        
    def b(self, *args, **kwargs):
        """
        <bitrate> video bitrate (please use -b:v)
        
        """
        
        raise NotImplementedError
        
    def vframes(self, *args, **kwargs):
        """
        <number> set the number of video frames to output
        
        """
        
        raise NotImplementedError
        
    def fpsmax(self, *args, **kwargs):
        """
        [:<stream_spec>] <rate> set max frame rate (Hz value, fraction or abbreviation)
        
        """
        
        raise NotImplementedError
        
    def pix_fmt(self, *args, **kwargs):
        """
        [:<stream_spec>] <format> set pixel format
        
        """
        
        raise NotImplementedError
        
    def display_rotation(self, *args, **kwargs):
        """
        [:<stream_spec>] <angle> set pure counter-clockwise rotation in degrees for stream(s)
        
        """
        
        raise NotImplementedError
        
    def display_hflip(self, *args, **kwargs):
        """
        [:<stream_spec>] set display horizontal flip for stream(s) (overrides any display rotation if it is not set)
        
        """
        
        raise NotImplementedError
        
    def display_vflip(self, *args, **kwargs):
        """
        [:<stream_spec>] set display vertical flip for stream(s) (overrides any display rotation if it is not set)
        
        """
        
        raise NotImplementedError
        
    def rc_override(self, *args, **kwargs):
        """
        [:<stream_spec>] <override> rate control override for specific intervals
        
        """
        
        raise NotImplementedError
        
    def timecode(self, *args, **kwargs):
        """
        <hh:mm:ss[:;.]ff> set initial TimeCode value.
        
        """
        
        raise NotImplementedError
        
    def passlogfile(self, *args, **kwargs):
        """
        [:<stream_spec>] <prefix> select two pass log file name prefix
        
        """
        
        raise NotImplementedError
        
    def intra_matrix(self, *args, **kwargs):
        """
        [:<stream_spec>] <matrix> specify intra matrix coeffs
        
        """
        
        raise NotImplementedError
        
    def inter_matrix(self, *args, **kwargs):
        """
        [:<stream_spec>] <matrix> specify inter matrix coeffs
        
        """
        
        raise NotImplementedError
        
    def chroma_intra_matrix(self, *args, **kwargs):
        """
        [:<stream_spec>] <matrix> specify intra matrix coeffs
        
        """
        
        raise NotImplementedError
        
    def vtag(self, *args, **kwargs):
        """
        <fourcc/tag> force video tag/fourcc
        
        """
        
        raise NotImplementedError
        
    def fps_mode(self, *args, **kwargs):
        """
        [:<stream_spec>] set framerate mode for matching video streams; overrides vsync
        
        """
        
        raise NotImplementedError
        
    def force_fps(self, *args, **kwargs):
        """
        [:<stream_spec>] force the selected framerate, disable the best supported framerate selection
        
        """
        
        raise NotImplementedError
        
    def streamid(self, *args, **kwargs):
        """
        <streamIndex:value> set the value of an outfile streamid
        
        """
        
        raise NotImplementedError
        
    def force_key_frames(self, *args, **kwargs):
        """
        [:<stream_spec>] <timestamps> force key frames at specified timestamps
        
        """
        
        raise NotImplementedError
        
    def hwaccel(self, *args, **kwargs):
        """
        [:<stream_spec>] <hwaccel name> use HW accelerated decoding
        
        """
        
        raise NotImplementedError
        
    def hwaccel_device(self, *args, **kwargs):
        """
        [:<stream_spec>] <devicename> select a device for HW acceleration
        
        """
        
        raise NotImplementedError
        
    def hwaccel_output_format(self, *args, **kwargs):
        """
        [:<stream_spec>] <format> select output format used with HW accelerated decoding
        
        """
        
        raise NotImplementedError
        
    def fix_sub_duration_heartbeat(self, *args, **kwargs):
        """
        [:<stream_spec>] set this video output stream to be a heartbeat stream for fix_sub_duration, according to which subtitles should be split at random access points
        
        """
        
        raise NotImplementedError
        
    def vpre(self, *args, **kwargs):
        """
        <preset> set the video options to the indicated preset
        
        """
        
        raise NotImplementedError
        
    def top(self, *args, **kwargs):
        """
        [:<stream_spec>] <> deprecated, use the setfield video filter
        
        """
        
        raise NotImplementedError
        
    def aq(self, *args, **kwargs):
        """
        <quality> set audio quality (codec-specific)
        
        """
        
        raise NotImplementedError
        
    def ar(self, *args, **kwargs):
        """
        [:<stream_spec>] <rate> set audio sampling rate (in Hz)
        
        """
        
        raise NotImplementedError
        
    def ac(self, *args, **kwargs):
        """
        [:<stream_spec>] <channels> set number of audio channels
        
        """
        
        raise NotImplementedError
        
    def an(self, *args, **kwargs):
        """
        disable audio
        
        """
        
        raise NotImplementedError
        
    def acodec(self, *args, **kwargs):
        """
        <codec> alias for -c:a (select encoder/decoder for audio streams)
        
        """
        
        raise NotImplementedError
        
    def ab(self, *args, **kwargs):
        """
        <bitrate> alias for -b:a (select bitrate for audio streams)
        
        """
        
        raise NotImplementedError
        
    def af(self, *args, **kwargs):
        """
        <filter_graph> alias for -filter:a (apply filters to audio streams)
        
        """
        
        raise NotImplementedError
        
    def aframes(self, *args, **kwargs):
        """
        <number> set the number of audio frames to output
        
        """
        
        raise NotImplementedError
        
    def atag(self, *args, **kwargs):
        """
        <fourcc/tag> force audio tag/fourcc
        
        """
        
        raise NotImplementedError
        
    def sample_fmt(self, *args, **kwargs):
        """
        [:<stream_spec>] <format> set sample format
        
        """
        
        raise NotImplementedError
        
    def channel_layout(self, *args, **kwargs):
        """
        [:<stream_spec>] <layout> set channel layout
        
        """
        
        raise NotImplementedError
        
    def ch_layout(self, *args, **kwargs):
        """
        [:<stream_spec>] <layout> set channel layout
        
        """
        
        raise NotImplementedError
        
    def guess_layout_max(self, *args, **kwargs):
        """
        [:<stream_spec>] set the maximum number of channels to try to guess the channel layout
        
        """
        
        raise NotImplementedError
        
    def apre(self, *args, **kwargs):
        """
        <preset> set the audio options to the indicated preset
        
        """
        
        raise NotImplementedError
        
    def sn(self, *args, **kwargs):
        """
        disable subtitle
        
        """
        
        raise NotImplementedError
        
    def scodec(self, *args, **kwargs):
        """
        <codec> alias for -c:s (select encoder/decoder for subtitle streams)
        
        """
        
        raise NotImplementedError
        
    def stag(self, *args, **kwargs):
        """
        <fourcc/tag> force subtitle tag/fourcc
        
        """
        
        raise NotImplementedError
        
    def fix_sub_duration(self, *args, **kwargs):
        """
        [:<stream_spec>] fix subtitles duration
        
        """
        
        raise NotImplementedError
        
    def canvas_size(self, *args, **kwargs):
        """
        [:<stream_spec>] <size> set canvas size (WxH or abbreviation)
        
        """
        
        raise NotImplementedError
        
    def spre(self, *args, **kwargs):
        """
        <preset> set the subtitle options to the indicated preset
        
        """
        
        raise NotImplementedError
        
    def dcodec(self, *args, **kwargs):
        """
        <codec> alias for -c:d (select encoder/decoder for data streams)
        
        """
        
        raise NotImplementedError
        
    def dn(self, *args, **kwargs):
        """
        disable data
        
        """
        
        raise NotImplementedError
        
    def bt(self, *args, **kwargs):
        """
        <int> E..VA...... Set video bitrate tolerance (in bits/s). In 1-pass mode, bitrate tolerance specifies how far ratecontrol is willing to deviate from the target average bitrate value. This is not related to minimum/maximum bitrate. Lowering tolerance too much has an adverse effect on quality. (from 0 to INT_MAX) (default 4000000)
        
        """
        
        raise NotImplementedError
        
    def flags(self, *args, **kwargs):
        """
        <flags> ED.VAS..... (default 0)
        
        unaligned                    .D.V....... allow decoders to produce unaligned output
        mv4                          E..V....... use four motion vectors per macroblock (MPEG-4)
        qpel                         E..V....... use 1/4-pel motion compensation
        loop                         E..V....... use loop filter
        gray                         ED.V....... only decode/encode grayscale
        psnr                         E..V....... error[?] variables will be set during encoding
        ildct                        E..V....... use interlaced DCT
        low_delay                    ED.V....... force low delay
        global_header                E..VA...... place global headers in extradata instead of every keyframe
        bitexact                     ED.VAS..... use only bitexact functions (except (I)DCT)
        aic                          E..V....... H.263 advanced intra coding / MPEG-4 AC prediction
        ilme                         E..V....... interlaced motion estimation
        cgop                         E..V....... closed GOP
        output_corrupt               .D.V....... Output even potentially corrupted frames
        drop_changed                 .D.VA.....P Drop frames whose parameters differ from first decoded frame
        """
        
        raise NotImplementedError
        
    def flags2(self, *args, **kwargs):
        """
        <flags> ED.VAS..... (default 0)
        
        fast                         E..V....... allow non-spec-compliant speedup tricks
        noout                        E..V....... skip bitstream encoding
        ignorecrop                   .D.V....... ignore cropping information from sps
        local_header                 E..V....... place global headers at every keyframe instead of in extradata
        chunks                       .D.V....... Frame data might be split into multiple chunks
        showall                      .D.V....... Show all frames before the first keyframe
        export_mvs                   .D.V....... export motion vectors through frame side data
        skip_manual                  .D..A...... do not skip samples and export skip information as frame side data
        ass_ro_flush_noop              .D...S..... do not reset ASS ReadOrder field on flush
        icc_profiles                 .D...S..... generate/parse embedded ICC profiles from/to colorimetry tags
        """
        
        raise NotImplementedError
        
    def export_side_data(self, *args, **kwargs):
        """
        <flags> ED.VAS..... Export metadata as side data (default 0)
        
        mvs                          .D.V....... export motion vectors through frame side data
        prft                         E..VAS..... export Producer Reference Time through packet side data
        venc_params                  .D.V....... export video encoding parameters through frame side data
        film_grain                   .D.V....... export film grain parameters through frame side data
        """
        
        raise NotImplementedError
        
    def g(self, *args, **kwargs):
        """
        <int> E..V....... set the group of picture (GOP) size (from INT_MIN to INT_MAX) (default 12)
        
        """
        
        raise NotImplementedError
        
    def cutoff(self, *args, **kwargs):
        """
        <int> E...A...... set cutoff bandwidth (from INT_MIN to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def frame_size(self, *args, **kwargs):
        """
        <int> E...A...... (from 0 to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def qcomp(self, *args, **kwargs):
        """
        <float> E..V....... video quantizer scale compression (VBR). Constant of ratecontrol equation. Recommended range for default rc_eq: 0.0-1.0 (from -FLT_MAX to FLT_MAX) (default 0.5)
        
        """
        
        raise NotImplementedError
        
    def qblur(self, *args, **kwargs):
        """
        <float> E..V....... video quantizer scale blur (VBR) (from -1 to FLT_MAX) (default 0.5)
        
        """
        
        raise NotImplementedError
        
    def qmin(self, *args, **kwargs):
        """
        <int> E..V....... minimum video quantizer scale (VBR) (from -1 to 69) (default 2)
        
        """
        
        raise NotImplementedError
        
    def qmax(self, *args, **kwargs):
        """
        <int> E..V....... maximum video quantizer scale (VBR) (from -1 to 1024) (default 31)
        
        """
        
        raise NotImplementedError
        
    def qdiff(self, *args, **kwargs):
        """
        <int> E..V....... maximum difference between the quantizer scales (VBR) (from INT_MIN to INT_MAX) (default 3)
        
        """
        
        raise NotImplementedError
        
    def bf(self, *args, **kwargs):
        """
        <int> E..V....... set maximum number of B-frames between non-B-frames (from -1 to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def b_qfactor(self, *args, **kwargs):
        """
        <float> E..V....... QP factor between P- and B-frames (from -FLT_MAX to FLT_MAX) (default 1.25)
        
        """
        
        raise NotImplementedError
        
    def bug(self, *args, **kwargs):
        """
        <flags> .D.V....... work around not autodetected encoder bugs (default autodetect)
        
        autodetect                   .D.V.......
        xvid_ilace                   .D.V....... Xvid interlacing bug (autodetected if FOURCC == XVIX)
        ump4                         .D.V....... (autodetected if FOURCC == UMP4)
        no_padding                   .D.V....... padding bug (autodetected)
        amv                          .D.V.......
        qpel_chroma                  .D.V.......
        std_qpel                     .D.V....... old standard qpel (autodetected per FOURCC/version)
        qpel_chroma2                 .D.V.......
        direct_blocksize              .D.V....... direct-qpel-blocksize bug (autodetected per FOURCC/version)
        edge                         .D.V....... edge padding bug (autodetected per FOURCC/version)
        hpel_chroma                  .D.V.......
        dc_clip                      .D.V.......
        ms                           .D.V....... work around various bugs in Microsoft's broken decoders
        trunc                        .D.V....... truncated frames
        iedge                        .D.V.......
        """
        
        raise NotImplementedError
        
    def strict(self, *args, **kwargs):
        """
        <int> ED.VA...... how strictly to follow the standards (from INT_MIN to INT_MAX) (default normal)
        
        very            2            ED.VA...... strictly conform to a older more strict version of the spec or reference software
        strict          1            ED.VA...... strictly conform to all the things in the spec no matter what the consequences
        normal          0            ED.VA......
        unofficial      -1           ED.VA...... allow unofficial extensions
        experimental    -2           ED.VA...... allow non-standardized experimental things
        """
        
        raise NotImplementedError
        
    def b_qoffset(self, *args, **kwargs):
        """
        <float> E..V....... QP offset between P- and B-frames (from -FLT_MAX to FLT_MAX) (default 1.25)
        
        """
        
        raise NotImplementedError
        
    def err_detect(self, *args, **kwargs):
        """
        <flags> ED.VAS..... set error detection flags (default 0)
        
        crccheck                     ED.VAS..... verify embedded CRCs
        bitstream                    ED.VAS..... detect bitstream specification deviations
        buffer                       ED.VAS..... detect improper bitstream length
        explode                      ED.VAS..... abort decoding on minor error detection
        ignore_err                   ED.VAS..... ignore errors
        careful                      ED.VAS..... consider things that violate the spec, are fast to check and have not been seen in the wild as errors
        compliant                    ED.VAS..... consider all spec non compliancies as errors
        aggressive                   ED.VAS..... consider things that a sane encoder should not do as an error
        """
        
        raise NotImplementedError
        
    def maxrate(self, *args, **kwargs):
        """
        <int64> E..VA...... maximum bitrate (in bits/s). Used for VBV together with bufsize. (from 0 to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def minrate(self, *args, **kwargs):
        """
        <int64> E..VA...... minimum bitrate (in bits/s). Most useful in setting up a CBR encode. It is of little use otherwise. (from INT_MIN to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def bufsize(self, *args, **kwargs):
        """
        <int> E..VA...... set ratecontrol buffer size (in bits) (from INT_MIN to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def i_qfactor(self, *args, **kwargs):
        """
        <float> E..V....... QP factor between P- and I-frames (from -FLT_MAX to FLT_MAX) (default -0.8)
        
        """
        
        raise NotImplementedError
        
    def i_qoffset(self, *args, **kwargs):
        """
        <float> E..V....... QP offset between P- and I-frames (from -FLT_MAX to FLT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def dct(self, *args, **kwargs):
        """
        <int> E..V....... DCT algorithm (from 0 to INT_MAX) (default auto)
        
        auto            0            E..V....... autoselect a good one
        fastint         1            E..V....... fast integer
        int             2            E..V....... accurate integer
        mmx             3            E..V.......
        altivec         5            E..V.......
        faan            6            E..V....... floating point AAN DCT
        """
        
        raise NotImplementedError
        
    def lumi_mask(self, *args, **kwargs):
        """
        <float> E..V....... compresses bright areas stronger than medium ones (from -FLT_MAX to FLT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def tcplx_mask(self, *args, **kwargs):
        """
        <float> E..V....... temporal complexity masking (from -FLT_MAX to FLT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def scplx_mask(self, *args, **kwargs):
        """
        <float> E..V....... spatial complexity masking (from -FLT_MAX to FLT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def p_mask(self, *args, **kwargs):
        """
        <float> E..V....... inter masking (from -FLT_MAX to FLT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def dark_mask(self, *args, **kwargs):
        """
        <float> E..V....... compresses dark areas stronger than medium ones (from -FLT_MAX to FLT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def idct(self, *args, **kwargs):
        """
        <int> ED.V....... select IDCT implementation (from 0 to INT_MAX) (default auto)
        
        auto            0            ED.V.......
        int             1            ED.V.......
        simple          2            ED.V.......
        simplemmx       3            ED.V.......
        arm             7            ED.V.......
        altivec         8            ED.V.......
        simplearm       10           ED.V.......
        simplearmv5te   16           ED.V.......
        simplearmv6     17           ED.V.......
        simpleneon      22           ED.V.......
        xvid            14           ED.V.......
        xvidmmx         14           ED.V....... deprecated, for compatibility only
        faani           20           ED.V....... floating point AAN IDCT
        simpleauto      128          ED.V.......
        """
        
        raise NotImplementedError
        
    def ec(self, *args, **kwargs):
        """
        <flags> .D.V....... set error concealment strategy (default guess_mvs+deblock)
        
        guess_mvs                    .D.V....... iterative motion vector (MV) search (slow)
        deblock                      .D.V....... use strong deblock filter for damaged MBs
        favor_inter                  .D.V....... favor predicting from the previous frame
        """
        
        raise NotImplementedError
        
    def sar(self, *args, **kwargs):
        """
        <rational> E..V....... sample aspect ratio (from 0 to 10) (default 0/1)
        
        """
        
        raise NotImplementedError
        
    def debug(self, *args, **kwargs):
        """
        <flags> ED.VAS..... print specific debug info (default 0)
        
        pict                         .D.V....... picture info
        rc                           E..V....... rate control
        bitstream                    .D.V.......
        mb_type                      .D.V....... macroblock (MB) type
        qp                           .D.V....... per-block quantization parameter (QP)
        dct_coeff                    .D.V.......
        green_metadata               .D.V.......
        skip                         .D.V.......
        startcode                    .D.V.......
        er                           .D.V....... error recognition
        mmco                         .D.V....... memory management control operations (H.264)
        bugs                         .D.V.......
        buffers                      .D.V....... picture buffer allocations
        thread_ops                   .D.VA...... threading operations
        nomc                         .D.VA...... skip motion compensation
        """
        
        raise NotImplementedError
        
    def dia_size(self, *args, **kwargs):
        """
        <int> E..V....... diamond type & size for motion estimation (from INT_MIN to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def last_pred(self, *args, **kwargs):
        """
        <int> E..V....... amount of motion predictors from the previous frame (from INT_MIN to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def pre_dia_size(self, *args, **kwargs):
        """
        <int> E..V....... diamond type & size for motion estimation pre-pass (from INT_MIN to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def subq(self, *args, **kwargs):
        """
        <int> E..V....... sub-pel motion estimation quality (from INT_MIN to INT_MAX) (default 8)
        
        """
        
        raise NotImplementedError
        
    def me_range(self, *args, **kwargs):
        """
        <int> E..V....... limit motion vectors range (1023 for DivX player) (from INT_MIN to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def global_quality(self, *args, **kwargs):
        """
        <int> E..VA...... (from INT_MIN to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def mbd(self, *args, **kwargs):
        """
        <int> E..V....... macroblock decision algorithm (high quality mode) (from 0 to 2) (default simple)
        
        simple          0            E..V....... use mbcmp
        bits            1            E..V....... use fewest bits
        rd              2            E..V....... use best rate distortion
        """
        
        raise NotImplementedError
        
    def rc_init_occupancy(self, *args, **kwargs):
        """
        <int> E..V....... number of bits which should be loaded into the rc buffer before decoding starts (from INT_MIN to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def threads(self, *args, **kwargs):
        """
        <int> ED.VA...... set the number of threads (from 0 to INT_MAX) (default 1)
        
        auto            0            ED.V....... autodetect a suitable number of threads to use
        """
        
        raise NotImplementedError
        
    def dc(self, *args, **kwargs):
        """
        <int> E..V....... intra_dc_precision (from -8 to 16) (default 0)
        
        """
        
        raise NotImplementedError
        
    def nssew(self, *args, **kwargs):
        """
        <int> E..V....... nsse weight (from INT_MIN to INT_MAX) (default 8)
        
        """
        
        raise NotImplementedError
        
    def skip_top(self, *args, **kwargs):
        """
        <int> .D.V....... number of macroblock rows at the top which are skipped (from INT_MIN to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def skip_bottom(self, *args, **kwargs):
        """
        <int> .D.V....... number of macroblock rows at the bottom which are skipped (from INT_MIN to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def level(self, *args, **kwargs):
        """
        <int> E..VA...... encoding level, usually corresponding to the profile level, codec-specific (from INT_MIN to INT_MAX) (default unknown)
        
        unknown         -99          E..VA......
        """
        
        raise NotImplementedError
        
    def lowres(self, *args, **kwargs):
        """
        <int> .D.VA...... decode at 1= 1/2, 2=1/4, 3=1/8 resolutions (from 0 to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def cmp(self, *args, **kwargs):
        """
        <int> E..V....... full-pel ME compare function (from INT_MIN to INT_MAX) (default sad)
        
        sad             0            E..V....... sum of absolute differences, fast
        sse             1            E..V....... sum of squared errors
        satd            2            E..V....... sum of absolute Hadamard transformed differences
        dct             3            E..V....... sum of absolute DCT transformed differences
        psnr            4            E..V....... sum of squared quantization errors (avoid, low quality)
        bit             5            E..V....... number of bits needed for the block
        rd              6            E..V....... rate distortion optimal, slow
        zero            7            E..V....... 0
        vsad            8            E..V....... sum of absolute vertical differences
        vsse            9            E..V....... sum of squared vertical differences
        nsse            10           E..V....... noise preserving sum of squared differences
        w53             11           E..V....... 5/3 wavelet, only used in snow
        w97             12           E..V....... 9/7 wavelet, only used in snow
        dctmax          13           E..V.......
        chroma          256          E..V.......
        msad            15           E..V....... sum of absolute differences, median predicted
        """
        
        raise NotImplementedError
        
    def subcmp(self, *args, **kwargs):
        """
        <int> E..V....... sub-pel ME compare function (from INT_MIN to INT_MAX) (default sad)
        
        sad             0            E..V....... sum of absolute differences, fast
        sse             1            E..V....... sum of squared errors
        satd            2            E..V....... sum of absolute Hadamard transformed differences
        dct             3            E..V....... sum of absolute DCT transformed differences
        psnr            4            E..V....... sum of squared quantization errors (avoid, low quality)
        bit             5            E..V....... number of bits needed for the block
        rd              6            E..V....... rate distortion optimal, slow
        zero            7            E..V....... 0
        vsad            8            E..V....... sum of absolute vertical differences
        vsse            9            E..V....... sum of squared vertical differences
        nsse            10           E..V....... noise preserving sum of squared differences
        w53             11           E..V....... 5/3 wavelet, only used in snow
        w97             12           E..V....... 9/7 wavelet, only used in snow
        dctmax          13           E..V.......
        chroma          256          E..V.......
        msad            15           E..V....... sum of absolute differences, median predicted
        """
        
        raise NotImplementedError
        
    def mbcmp(self, *args, **kwargs):
        """
        <int> E..V....... macroblock compare function (from INT_MIN to INT_MAX) (default sad)
        
        sad             0            E..V....... sum of absolute differences, fast
        sse             1            E..V....... sum of squared errors
        satd            2            E..V....... sum of absolute Hadamard transformed differences
        dct             3            E..V....... sum of absolute DCT transformed differences
        psnr            4            E..V....... sum of squared quantization errors (avoid, low quality)
        bit             5            E..V....... number of bits needed for the block
        rd              6            E..V....... rate distortion optimal, slow
        zero            7            E..V....... 0
        vsad            8            E..V....... sum of absolute vertical differences
        vsse            9            E..V....... sum of squared vertical differences
        nsse            10           E..V....... noise preserving sum of squared differences
        w53             11           E..V....... 5/3 wavelet, only used in snow
        w97             12           E..V....... 9/7 wavelet, only used in snow
        dctmax          13           E..V.......
        chroma          256          E..V.......
        msad            15           E..V....... sum of absolute differences, median predicted
        """
        
        raise NotImplementedError
        
    def ildctcmp(self, *args, **kwargs):
        """
        <int> E..V....... interlaced DCT compare function (from INT_MIN to INT_MAX) (default vsad)
        
        sad             0            E..V....... sum of absolute differences, fast
        sse             1            E..V....... sum of squared errors
        satd            2            E..V....... sum of absolute Hadamard transformed differences
        dct             3            E..V....... sum of absolute DCT transformed differences
        psnr            4            E..V....... sum of squared quantization errors (avoid, low quality)
        bit             5            E..V....... number of bits needed for the block
        rd              6            E..V....... rate distortion optimal, slow
        zero            7            E..V....... 0
        vsad            8            E..V....... sum of absolute vertical differences
        vsse            9            E..V....... sum of squared vertical differences
        nsse            10           E..V....... noise preserving sum of squared differences
        w53             11           E..V....... 5/3 wavelet, only used in snow
        w97             12           E..V....... 9/7 wavelet, only used in snow
        dctmax          13           E..V.......
        chroma          256          E..V.......
        msad            15           E..V....... sum of absolute differences, median predicted
        """
        
        raise NotImplementedError
        
    def precmp(self, *args, **kwargs):
        """
        <int> E..V....... pre motion estimation compare function (from INT_MIN to INT_MAX) (default sad)
        
        sad             0            E..V....... sum of absolute differences, fast
        sse             1            E..V....... sum of squared errors
        satd            2            E..V....... sum of absolute Hadamard transformed differences
        dct             3            E..V....... sum of absolute DCT transformed differences
        psnr            4            E..V....... sum of squared quantization errors (avoid, low quality)
        bit             5            E..V....... number of bits needed for the block
        rd              6            E..V....... rate distortion optimal, slow
        zero            7            E..V....... 0
        vsad            8            E..V....... sum of absolute vertical differences
        vsse            9            E..V....... sum of squared vertical differences
        nsse            10           E..V....... noise preserving sum of squared differences
        w53             11           E..V....... 5/3 wavelet, only used in snow
        w97             12           E..V....... 9/7 wavelet, only used in snow
        dctmax          13           E..V.......
        chroma          256          E..V.......
        msad            15           E..V....... sum of absolute differences, median predicted
        """
        
        raise NotImplementedError
        
    def mblmin(self, *args, **kwargs):
        """
        <int> E..V....... minimum macroblock Lagrange factor (VBR) (from 1 to 32767) (default 236)
        
        """
        
        raise NotImplementedError
        
    def mblmax(self, *args, **kwargs):
        """
        <int> E..V....... maximum macroblock Lagrange factor (VBR) (from 1 to 32767) (default 3658)
        
        """
        
        raise NotImplementedError
        
    def skip_loop_filter(self, *args, **kwargs):
        """
        <int> .D.V....... skip loop filtering process for the selected frames (from INT_MIN to INT_MAX) (default default)
        
        none            -16          .D.V....... discard no frame
        default         0            .D.V....... discard useless frames
        noref           8            .D.V....... discard all non-reference frames
        bidir           16           .D.V....... discard all bidirectional frames
        nointra         24           .D.V....... discard all frames except I frames
        nokey           32           .D.V....... discard all frames except keyframes
        all             48           .D.V....... discard all frames
        """
        
        raise NotImplementedError
        
    def skip_idct(self, *args, **kwargs):
        """
        <int> .D.V....... skip IDCT/dequantization for the selected frames (from INT_MIN to INT_MAX) (default default)
        
        none            -16          .D.V....... discard no frame
        default         0            .D.V....... discard useless frames
        noref           8            .D.V....... discard all non-reference frames
        bidir           16           .D.V....... discard all bidirectional frames
        nointra         24           .D.V....... discard all frames except I frames
        nokey           32           .D.V....... discard all frames except keyframes
        all             48           .D.V....... discard all frames
        """
        
        raise NotImplementedError
        
    def skip_frame(self, *args, **kwargs):
        """
        <int> .D.V....... skip decoding for the selected frames (from INT_MIN to INT_MAX) (default default)
        
        none            -16          .D.V....... discard no frame
        default         0            .D.V....... discard useless frames
        noref           8            .D.V....... discard all non-reference frames
        bidir           16           .D.V....... discard all bidirectional frames
        nointra         24           .D.V....... discard all frames except I frames
        nokey           32           .D.V....... discard all frames except keyframes
        all             48           .D.V....... discard all frames
        """
        
        raise NotImplementedError
        
    def bidir_refine(self, *args, **kwargs):
        """
        <int> E..V....... refine the two motion vectors used in bidirectional macroblocks (from 0 to 4) (default 1)
        
        """
        
        raise NotImplementedError
        
    def keyint_min(self, *args, **kwargs):
        """
        <int> E..V....... minimum interval between IDR-frames (from INT_MIN to INT_MAX) (default 25)
        
        """
        
        raise NotImplementedError
        
    def refs(self, *args, **kwargs):
        """
        <int> E..V....... reference frames to consider for motion compensation (from INT_MIN to INT_MAX) (default 1)
        
        """
        
        raise NotImplementedError
        
    def trellis(self, *args, **kwargs):
        """
        <int> E..VA...... rate-distortion optimal quantization (from INT_MIN to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def mv0_threshold(self, *args, **kwargs):
        """
        <int> E..V....... (from 0 to INT_MAX) (default 256)
        
        """
        
        raise NotImplementedError
        
    def compression_level(self, *args, **kwargs):
        """
        <int> E..VA...... (from INT_MIN to INT_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def rc_max_vbv_use(self, *args, **kwargs):
        """
        <float> E..V....... (from 0 to FLT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def rc_min_vbv_use(self, *args, **kwargs):
        """
        <float> E..V....... (from 0 to FLT_MAX) (default 3)
        
        """
        
        raise NotImplementedError
        
    def ticks_per_frame(self, *args, **kwargs):
        """
        <int> ED.VA...... (from 1 to INT_MAX) (default 1)
        
        """
        
        raise NotImplementedError
        
    def color_primaries(self, *args, **kwargs):
        """
        <int> ED.V....... color primaries (from 1 to INT_MAX) (default unknown)
        
        bt709           1            ED.V....... BT.709
        unknown         2            ED.V....... Unspecified
        bt470m          4            ED.V....... BT.470 M
        bt470bg         5            ED.V....... BT.470 BG
        smpte170m       6            ED.V....... SMPTE 170 M
        smpte240m       7            ED.V....... SMPTE 240 M
        film            8            ED.V....... Film
        bt2020          9            ED.V....... BT.2020
        smpte428        10           ED.V....... SMPTE 428-1
        smpte428_1      10           ED.V....... SMPTE 428-1
        smpte431        11           ED.V....... SMPTE 431-2
        smpte432        12           ED.V....... SMPTE 422-1
        jedec-p22       22           ED.V....... JEDEC P22
        ebu3213         22           ED.V....... EBU 3213-E
        unspecified     2            ED.V....... Unspecified
        """
        
        raise NotImplementedError
        
    def color_trc(self, *args, **kwargs):
        """
        <int> ED.V....... color transfer characteristics (from 1 to INT_MAX) (default unknown)
        
        bt709           1            ED.V....... BT.709
        unknown         2            ED.V....... Unspecified
        gamma22         4            ED.V....... BT.470 M
        gamma28         5            ED.V....... BT.470 BG
        smpte170m       6            ED.V....... SMPTE 170 M
        smpte240m       7            ED.V....... SMPTE 240 M
        linear          8            ED.V....... Linear
        log100          9            ED.V....... Log
        log316          10           ED.V....... Log square root
        iec61966-2-4    11           ED.V....... IEC 61966-2-4
        bt1361e         12           ED.V....... BT.1361
        iec61966-2-1    13           ED.V....... IEC 61966-2-1
        bt2020-10       14           ED.V....... BT.2020 - 10 bit
        bt2020-12       15           ED.V....... BT.2020 - 12 bit
        smpte2084       16           ED.V....... SMPTE 2084
        smpte428        17           ED.V....... SMPTE 428-1
        arib-std-b67    18           ED.V....... ARIB STD-B67
        unspecified     2            ED.V....... Unspecified
        log             9            ED.V....... Log
        log_sqrt        10           ED.V....... Log square root
        iec61966_2_4    11           ED.V....... IEC 61966-2-4
        bt1361          12           ED.V....... BT.1361
        iec61966_2_1    13           ED.V....... IEC 61966-2-1
        bt2020_10bit    14           ED.V....... BT.2020 - 10 bit
        bt2020_12bit    15           ED.V....... BT.2020 - 12 bit
        smpte428_1      17           ED.V....... SMPTE 428-1
        """
        
        raise NotImplementedError
        
    def colorspace(self, *args, **kwargs):
        """
        <int> ED.V....... color space (from 0 to INT_MAX) (default unknown)
        
        rgb             0            ED.V....... RGB
        bt709           1            ED.V....... BT.709
        unknown         2            ED.V....... Unspecified
        fcc             4            ED.V....... FCC
        bt470bg         5            ED.V....... BT.470 BG
        smpte170m       6            ED.V....... SMPTE 170 M
        smpte240m       7            ED.V....... SMPTE 240 M
        ycgco           8            ED.V....... YCGCO
        bt2020nc        9            ED.V....... BT.2020 NCL
        bt2020c         10           ED.V....... BT.2020 CL
        smpte2085       11           ED.V....... SMPTE 2085
        chroma-derived-nc 12           ED.V....... Chroma-derived NCL
        chroma-derived-c 13           ED.V....... Chroma-derived CL
        ictcp           14           ED.V....... ICtCp
        unspecified     2            ED.V....... Unspecified
        ycocg           8            ED.V....... YCGCO
        bt2020_ncl      9            ED.V....... BT.2020 NCL
        bt2020_cl       10           ED.V....... BT.2020 CL
        """
        
        raise NotImplementedError
        
    def color_range(self, *args, **kwargs):
        """
        <int> ED.V....... color range (from 0 to INT_MAX) (default unknown)
        
        unknown         0            ED.V....... Unspecified
        tv              1            ED.V....... MPEG (219*2^(n-8))
        pc              2            ED.V....... JPEG (2^n-1)
        unspecified     0            ED.V....... Unspecified
        mpeg            1            ED.V....... MPEG (219*2^(n-8))
        jpeg            2            ED.V....... JPEG (2^n-1)
        limited         1            ED.V....... MPEG (219*2^(n-8))
        full            2            ED.V....... JPEG (2^n-1)
        """
        
        raise NotImplementedError
        
    def chroma_sample_location(self, *args, **kwargs):
        """
        <int> ED.V....... chroma sample location (from 0 to INT_MAX) (default unknown)
        
        unknown         0            ED.V....... Unspecified
        left            1            ED.V....... Left
        center          2            ED.V....... Center
        topleft         3            ED.V....... Top-left
        top             4            ED.V....... Top
        bottomleft      5            ED.V....... Bottom-left
        bottom          6            ED.V....... Bottom
        unspecified     0            ED.V....... Unspecified
        """
        
        raise NotImplementedError
        
    def slices(self, *args, **kwargs):
        """
        <int> E..V....... set the number of slices, used in parallelized encoding (from 0 to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def thread_type(self, *args, **kwargs):
        """
        <flags> ED.VA...... select multithreading type (default slice+frame)
        
        slice                        ED.V.......
        frame                        ED.V.......
        """
        
        raise NotImplementedError
        
    def audio_service_type(self, *args, **kwargs):
        """
        <int> E...A...... audio service type (from 0 to 8) (default ma)
        
        ma              0            E...A...... Main Audio Service
        ef              1            E...A...... Effects
        vi              2            E...A...... Visually Impaired
        hi              3            E...A...... Hearing Impaired
        di              4            E...A...... Dialogue
        co              5            E...A...... Commentary
        em              6            E...A...... Emergency
        vo              7            E...A...... Voice Over
        ka              8            E...A...... Karaoke
        """
        
        raise NotImplementedError
        
    def request_sample_fmt(self, *args, **kwargs):
        """
        <sample_fmt> .D..A...... sample format audio decoders should prefer (default none)
        
        """
        
        raise NotImplementedError
        
    def sub_charenc(self, *args, **kwargs):
        """
        <string> .D...S..... set input text subtitles character encoding
        
        """
        
        raise NotImplementedError
        
    def sub_charenc_mode(self, *args, **kwargs):
        """
        <flags> .D...S..... set input text subtitles character encoding mode (default 0)
        
        do_nothing                   .D...S.....
        auto                         .D...S.....
        pre_decoder                  .D...S.....
        ignore                       .D...S.....
        """
        
        raise NotImplementedError
        
    def apply_cropping(self, *args, **kwargs):
        """
        <boolean> .D.V....... (default true)
        
        """
        
        raise NotImplementedError
        
    def skip_alpha(self, *args, **kwargs):
        """
        <boolean> .D.V....... Skip processing alpha (default false)
        
        """
        
        raise NotImplementedError
        
    def field_order(self, *args, **kwargs):
        """
        <int> ED.V....... Field order (from 0 to 5) (default 0)
        
        progressive     1            ED.V.......
        tt              2            ED.V.......
        bb              3            ED.V.......
        tb              4            ED.V.......
        bt              5            ED.V.......
        """
        
        raise NotImplementedError
        
    def dump_separator(self, *args, **kwargs):
        """
        <string> ED.VAS..... set information dump field separator
        
        """
        
        raise NotImplementedError
        
    def codec_whitelist(self, *args, **kwargs):
        """
        <string> .D.VAS..... List of decoders that are allowed to be used
        
        """
        
        raise NotImplementedError
        
    def max_pixels(self, *args, **kwargs):
        """
        <int64> ED.VAS..... Maximum number of pixels (from 0 to INT_MAX) (default INT_MAX)
        
        """
        
        raise NotImplementedError
        
    def max_samples(self, *args, **kwargs):
        """
        <int64> ED..A...... Maximum number of samples (from 0 to INT_MAX) (default INT_MAX)
        
        """
        
        raise NotImplementedError
        
    def hwaccel_flags(self, *args, **kwargs):
        """
        <flags> .D.V....... (default ignore_level)
        
        ignore_level                 .D.V....... ignore level even if the codec level used is unknown or higher than the maximum supported level reported by the hardware driver
        allow_high_depth              .D.V....... allow to output YUV pixel formats with a different chroma sampling than 4:2:0 and/or other than 8 bits per component
        allow_profile_mismatch              .D.V....... attempt to decode anyway if HW accelerated decoder's supported profiles do not exactly match the stream
        unsafe_output                .D.V....... allow potentially unsafe hwaccel frame output that might require special care to process successfully
        """
        
        raise NotImplementedError
        
    def extra_hw_frames(self, *args, **kwargs):
        """
        <int> .D.V....... Number of extra hardware frames to allocate for the user (from -1 to INT_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def discard_damaged_percentage(self, *args, **kwargs):
        """
        <int> .D.V....... Percentage of damaged samples to discard a frame (from 0 to 100) (default 95)
        
        """
        
        raise NotImplementedError
        
    def side_data_prefer_packet(self, *args, **kwargs):
        """
        [<int> ].D.VAS..... Comma-separated list of side data types for which user-supplied (container) data is preferred over coded bytestream
        
        replaygain      4            .D..A......
        displaymatrix   5            .D..A......
        spherical       21           .D..A......
        stereo3d        6            .D..A......
        audio_service_type 7            .D..A......
        mastering_display_metadata 20           .D..A......
        content_light_level 22           .D..A......
        icc_profile     28           .D..A......
        """
        
        raise NotImplementedError
        
    def mpv_flags(self, *args, **kwargs):
        """
        <flags> E..V....... Flags common for all mpegvideo-based encoders. (default 0)
        
        skip_rd                      E..V....... RD optimal MB level residual skipping
        strict_gop                   E..V....... Strictly enforce gop size
        qp_rd                        E..V....... Use rate distortion optimization for qp selection
        cbp_rd                       E..V....... use rate distortion optimization for CBP
        naq                          E..V....... normalize adaptive quantization
        mv0                          E..V....... always try a mb with mv=<0,0>
        """
        
        raise NotImplementedError
        
    def luma_elim_threshold(self, *args, **kwargs):
        """
        <int> E..V....... single coefficient elimination threshold for luminance (negative values also consider dc coefficient) (from INT_MIN to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def chroma_elim_threshold(self, *args, **kwargs):
        """
        <int> E..V....... single coefficient elimination threshold for chrominance (negative values also consider dc coefficient) (from INT_MIN to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def quantizer_noise_shaping(self, *args, **kwargs):
        """
        <int> E..V....... (from 0 to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def error_rate(self, *args, **kwargs):
        """
        <int> E..V....... Simulate errors in the bitstream to test error concealment. (from 0 to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def qsquish(self, *args, **kwargs):
        """
        <float> E..V....... how to keep quantizer between qmin and qmax (0 = clip, 1 = use differentiable function) (from 0 to 99) (default 0)
        
        """
        
        raise NotImplementedError
        
    def rc_qmod_amp(self, *args, **kwargs):
        """
        <float> E..V....... experimental quantizer modulation (from -FLT_MAX to FLT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def rc_qmod_freq(self, *args, **kwargs):
        """
        <int> E..V....... experimental quantizer modulation (from INT_MIN to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def rc_eq(self, *args, **kwargs):
        """
        <string> E..V....... Set rate control equation. When computing the expression, besides the standard functions defined in the section 'Expression Evaluation', the following functions are available: bits2qp(bits), qp2bits(qp). Also the following constants are available: iTex pTex tex mv fCode iCount mcVar var isI isP isB avgQP qComp avgIITex avgPITex avgPPTex avgBPTex avgTex.
        
        """
        
        raise NotImplementedError
        
    def rc_init_cplx(self, *args, **kwargs):
        """
        <float> E..V....... initial complexity for 1-pass encoding (from -FLT_MAX to FLT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def rc_buf_aggressivity(self, *args, **kwargs):
        """
        <float> E..V....... currently useless (from -FLT_MAX to FLT_MAX) (default 1)
        
        """
        
        raise NotImplementedError
        
    def border_mask(self, *args, **kwargs):
        """
        <float> E..V....... increase the quantizer for macroblocks close to borders (from -FLT_MAX to FLT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def lmin(self, *args, **kwargs):
        """
        <int> E..V....... minimum Lagrange factor (VBR) (from 0 to INT_MAX) (default 236)
        
        """
        
        raise NotImplementedError
        
    def lmax(self, *args, **kwargs):
        """
        <int> E..V....... maximum Lagrange factor (VBR) (from 0 to INT_MAX) (default 3658)
        
        """
        
        raise NotImplementedError
        
    def skip_threshold(self, *args, **kwargs):
        """
        <int> E..V....... Frame skip threshold (from INT_MIN to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def skip_factor(self, *args, **kwargs):
        """
        <int> E..V....... Frame skip factor (from INT_MIN to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def skip_exp(self, *args, **kwargs):
        """
        <int> E..V....... Frame skip exponent (from INT_MIN to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def skip_cmp(self, *args, **kwargs):
        """
        <int> E..V....... Frame skip compare function (from INT_MIN to INT_MAX) (default dctmax)
        
        sad             0            E..V....... Sum of absolute differences, fast
        sse             1            E..V....... Sum of squared errors
        satd            2            E..V....... Sum of absolute Hadamard transformed differences
        dct             3            E..V....... Sum of absolute DCT transformed differences
        psnr            4            E..V....... Sum of squared quantization errors, low quality
        bit             5            E..V....... Number of bits needed for the block
        rd              6            E..V....... Rate distortion optimal, slow
        zero            7            E..V....... Zero
        vsad            8            E..V....... Sum of absolute vertical differences
        vsse            9            E..V....... Sum of squared vertical differences
        nsse            10           E..V....... Noise preserving sum of squared differences
        dct264          14           E..V.......
        dctmax          13           E..V.......
        chroma          256          E..V.......
        msad            15           E..V....... Sum of absolute differences, median predicted
        """
        
        raise NotImplementedError
        
    def sc_threshold(self, *args, **kwargs):
        """
        <int> E..V....... Scene change threshold (from INT_MIN to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def noise_reduction(self, *args, **kwargs):
        """
        <int> E..V....... Noise reduction (from INT_MIN to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def ps(self, *args, **kwargs):
        """
        <int> E..V....... RTP payload size in bytes (from INT_MIN to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def huffman(self, *args, **kwargs):
        """
        <int> E..V....... Huffman table strategy (from 0 to 1) (default optimal)
        
        default         0            E..V.......
        optimal         1            E..V.......
        """
        
        raise NotImplementedError
        
    def force_duplicated_matrix(self, *args, **kwargs):
        """
        <boolean> E..V....... Always write luma and chroma matrix for mjpeg, useful for rtp streaming. (default false)
        
        """
        
        raise NotImplementedError
        
    def dpi(self, *args, **kwargs):
        """
        <int> E..V....... Set image resolution (in dots per inch) (from 0 to 65536) (default 0)
        
        """
        
        raise NotImplementedError
        
    def dpm(self, *args, **kwargs):
        """
        <int> E..V....... Set image resolution (in dots per meter) (from 0 to 65536) (default 0)
        
        """
        
        raise NotImplementedError
        
    def pred(self, *args, **kwargs):
        """
        <int> E..V....... Prediction method (from 0 to 5) (default none)
        
        none            0            E..V.......
        sub             1            E..V.......
        up              2            E..V.......
        avg             3            E..V.......
        paeth           4            E..V.......
        mixed           5            E..V.......
        """
        
        raise NotImplementedError
        
    def max_extra_cb_iterations(self, *args, **kwargs):
        """
        <int> E..V....... Max extra codebook recalculation passes, more is better and slower (from 0 to INT_MAX) (default 2)
        
        """
        
        raise NotImplementedError
        
    def skip_empty_cb(self, *args, **kwargs):
        """
        <boolean> E..V....... Avoid wasting bytes, ignore vintage MacOS decoder (default false)
        
        """
        
        raise NotImplementedError
        
    def max_strips(self, *args, **kwargs):
        """
        <int> E..V....... Limit strips/frame, vintage compatible is 1..3, otherwise the more the better (from 1 to 32) (default 3)
        
        """
        
        raise NotImplementedError
        
    def min_strips(self, *args, **kwargs):
        """
        <int> E..V....... Enforce min strips/frame, more is worse and faster, must be <= max_strips (from 1 to 32) (default 1)
        
        """
        
        raise NotImplementedError
        
    def strip_number_adaptivity(self, *args, **kwargs):
        """
        <int> E..V....... How fast the strip number adapts, more is slightly better, much slower (from 0 to 31) (default 0)
        
        """
        
        raise NotImplementedError
        
    def nitris_compat(self, *args, **kwargs):
        """
        <boolean> E..V....... encode with Avid Nitris compatibility (default false)
        
        """
        
        raise NotImplementedError
        
    def ibias(self, *args, **kwargs):
        """
        <int> E..V....... intra quant bias (from INT_MIN to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def compression(self, *args, **kwargs):
        """
        <int> E..V....... set compression type (from 0 to 3) (default none)
        
        none            0            E..V....... none
        rle             1            E..V....... RLE
        zip1            2            E..V....... ZIP1
        zip16           3            E..V....... ZIP16
        """
        
        raise NotImplementedError
        
    def format(self, *args, **kwargs):
        """
        <int> E..V....... set pixel type (from 1 to 2) (default float)
        
        half            1            E..V.......
        float           2            E..V.......
        """
        
        raise NotImplementedError
        
    def gamma(self, *args, **kwargs):
        """
        <float> E..V....... set gamma (from 0.001 to FLT_MAX) (default 1)
        
        """
        
        raise NotImplementedError
        
    def slicecrc(self, *args, **kwargs):
        """
        <boolean> E..V....... Protect slices with CRCs (default auto)
        
        """
        
        raise NotImplementedError
        
    def coder(self, *args, **kwargs):
        """
        <int> E..V....... Coder type (from -2 to 2) (default rice)
        
        rice            0            E..V....... Golomb rice
        range_def       -2           E..V....... Range with default table
        range_tab       2            E..V....... Range with custom table
        ac              1            E..V....... Range with custom table (the ac option exists for compatibility and is deprecated)
        """
        
        raise NotImplementedError
        
    def context(self, *args, **kwargs):
        """
        <int> E..V....... Context model (from 0 to 1) (default 0)
        
        """
        
        raise NotImplementedError
        
    def non_deterministic(self, *args, **kwargs):
        """
        <boolean> E..V....... Allow multithreading for e.g. context=1 at the expense of determinism (default false)
        
        """
        
        raise NotImplementedError
        
    def motion_est(self, *args, **kwargs):
        """
        <int> E..V....... motion estimation algorithm (from 0 to 2) (default epzs)
        
        zero            0            E..V.......
        epzs            1            E..V.......
        xone            2            E..V.......
        """
        
        raise NotImplementedError
        
    def mepc(self, *args, **kwargs):
        """
        <int> E..V....... Motion estimation bitrate penalty compensation (1.0 = 256) (from INT_MIN to INT_MAX) (default 256)
        
        """
        
        raise NotImplementedError
        
    def mepre(self, *args, **kwargs):
        """
        <int> E..V....... pre motion estimation (from INT_MIN to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def intra_penalty(self, *args, **kwargs):
        """
        <int> E..V....... Penalty for intra blocks in block decision (from 0 to 1.07374e+09) (default 0)
        
        """
        
        raise NotImplementedError
        
    def gifflags(self, *args, **kwargs):
        """
        <flags> E..V....... set GIF flags (default offsetting+transdiff)
        
        offsetting                   E..V....... enable picture offsetting
        transdiff                    E..V....... enable transparency detection between frames
        """
        
        raise NotImplementedError
        
    def gifimage(self, *args, **kwargs):
        """
        <boolean> E..V....... enable encoding only images per frame (default false)
        
        """
        
        raise NotImplementedError
        
    def global_palette(self, *args, **kwargs):
        """
        <boolean> E..V....... write a palette to the global gif header where feasible (default true)
        
        """
        
        raise NotImplementedError
        
    def obmc(self, *args, **kwargs):
        """
        <boolean> E..V....... use overlapped block motion compensation. (default false)
        
        """
        
        raise NotImplementedError
        
    def mb_info(self, *args, **kwargs):
        """
        <int> E..V....... emit macroblock info for RFC 2190 packetization, the parameter value is the maximum payload size (from 0 to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def umv(self, *args, **kwargs):
        """
        <boolean> E..V....... Use unlimited motion vectors. (default false)
        
        """
        
        raise NotImplementedError
        
    def aiv(self, *args, **kwargs):
        """
        <boolean> E..V....... Use alternative inter VLC. (default false)
        
        """
        
        raise NotImplementedError
        
    def structured_slices(self, *args, **kwargs):
        """
        <boolean> E..V....... Write slice start position at every GOB header instead of just GOB number. (default false)
        
        """
        
        raise NotImplementedError
        
    def chunks(self, *args, **kwargs):
        """
        <int> E..V....... chunk count (from 1 to 64) (default 1)
        
        """
        
        raise NotImplementedError
        
    def compressor(self, *args, **kwargs):
        """
        <int> E..V....... second-stage compressor (from 160 to 176) (default snappy)
        
        none            160          E..V....... None
        snappy          176          E..V....... Snappy
        """
        
        raise NotImplementedError
        
    def tile_width(self, *args, **kwargs):
        """
        <int> E..V....... Tile Width (from 1 to 1.07374e+09) (default 256)
        
        """
        
        raise NotImplementedError
        
    def tile_height(self, *args, **kwargs):
        """
        <int> E..V....... Tile Height (from 1 to 1.07374e+09) (default 256)
        
        """
        
        raise NotImplementedError
        
    def sop(self, *args, **kwargs):
        """
        <int> E..V....... SOP marker (from 0 to 1) (default 0)
        
        """
        
        raise NotImplementedError
        
    def eph(self, *args, **kwargs):
        """
        <int> E..V....... EPH marker (from 0 to 1) (default 0)
        
        """
        
        raise NotImplementedError
        
    def prog(self, *args, **kwargs):
        """
        <int> E..V....... Progression Order (from 0 to 4) (default lrcp)
        
        lrcp            0            E..V.......
        rlcp            1            E..V.......
        rpcl            2            E..V.......
        pcrl            3            E..V.......
        cprl            4            E..V.......
        """
        
        raise NotImplementedError
        
    def layer_rates(self, *args, **kwargs):
        """
        <string> E..V....... Layer Rates
        
        """
        
        raise NotImplementedError
        
    def gop_timecode(self, *args, **kwargs):
        """
        <string> E..V....... MPEG GOP Timecode in hh:mm:ss[:;.]ff format. Overrides timecode_frame_start.
        
        """
        
        raise NotImplementedError
        
    def drop_frame_timecode(self, *args, **kwargs):
        """
        <boolean> E..V....... Timecode is in drop frame format. (default false)
        
        """
        
        raise NotImplementedError
        
    def scan_offset(self, *args, **kwargs):
        """
        <boolean> E..V....... Reserve space for SVCD scan offset user data. (default false)
        
        """
        
        raise NotImplementedError
        
    def timecode_frame_start(self, *args, **kwargs):
        """
        <int64> E..V....... GOP timecode frame start number, in non-drop-frame format (from -1 to I64_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def b_strategy(self, *args, **kwargs):
        """
        <int> E..V....... Strategy to choose between I/P/B-frames (from 0 to 2) (default 0)
        
        """
        
        raise NotImplementedError
        
    def b_sensitivity(self, *args, **kwargs):
        """
        <int> E..V....... Adjust sensitivity of b_frame_strategy 1 (from 1 to INT_MAX) (default 40)
        
        """
        
        raise NotImplementedError
        
    def brd_scale(self, *args, **kwargs):
        """
        <int> E..V....... Downscale frames for dynamic B-frame decision (from 0 to 3) (default 0)
        
        """
        
        raise NotImplementedError
        
    def intra_vlc(self, *args, **kwargs):
        """
        <boolean> E..V....... Use MPEG-2 intra VLC table. (default false)
        
        """
        
        raise NotImplementedError
        
    def non_linear_quant(self, *args, **kwargs):
        """
        <boolean> E..V....... Use nonlinear quantizer. (default false)
        
        """
        
        raise NotImplementedError
        
    def alternate_scan(self, *args, **kwargs):
        """
        <boolean> E..V....... Enable alternate scantable. (default false)
        
        """
        
        raise NotImplementedError
        
    def a53cc(self, *args, **kwargs):
        """
        <boolean> E..V....... Use A53 Closed Captions (if available) (default true)
        
        """
        
        raise NotImplementedError
        
    def seq_disp_ext(self, *args, **kwargs):
        """
        <int> E..V....... Write sequence_display_extension blocks. (from -1 to 1) (default auto)
        
        auto            -1           E..V.......
        never           0            E..V.......
        always          1            E..V.......
        """
        
        raise NotImplementedError
        
    def video_format(self, *args, **kwargs):
        """
        <int> E..V....... Video_format in the sequence_display_extension indicating the source of the video. (from 0 to 7) (default unspecified)
        
        component       0            E..V.......
        pal             1            E..V.......
        ntsc            2            E..V.......
        secam           3            E..V.......
        mac             4            E..V.......
        unspecified     5            E..V.......
        """
        
        raise NotImplementedError
        
    def data_partitioning(self, *args, **kwargs):
        """
        <boolean> E..V....... Use data partitioning. (default false)
        
        """
        
        raise NotImplementedError
        
    def mpeg_quant(self, *args, **kwargs):
        """
        <int> E..V....... Use MPEG quantizers instead of H.263 (from 0 to 1) (default 0)
        
        """
        
        raise NotImplementedError
        
    def vendor(self, *args, **kwargs):
        """
        <string> E..V....... vendor ID (default "fmpg")
        
        """
        
        raise NotImplementedError
        
    def mbs_per_slice(self, *args, **kwargs):
        """
        <int> E..V....... macroblocks per slice (from 1 to 8) (default 8)
        
        """
        
        raise NotImplementedError
        
    def bits_per_mb(self, *args, **kwargs):
        """
        <int> E..V....... desired bits per macroblock (from 0 to 8192) (default 0)
        
        """
        
        raise NotImplementedError
        
    def quant_mat(self, *args, **kwargs):
        """
        <int> E..V....... quantiser matrix (from -1 to 6) (default auto)
        
        auto            -1           E..V.......
        proxy           0            E..V.......
        lt              2            E..V.......
        standard        3            E..V.......
        hq              4            E..V.......
        default         6            E..V.......
        """
        
        raise NotImplementedError
        
    def alpha_bits(self, *args, **kwargs):
        """
        <int> E..V....... bits for alpha plane (from 0 to 16) (default 16)
        
        """
        
        raise NotImplementedError
        
    def skip_frame_thresh(self, *args, **kwargs):
        """
        <int> E..V....... (from 0 to 24) (default 1)
        
        """
        
        raise NotImplementedError
        
    def start_one_color_thresh(self, *args, **kwargs):
        """
        <int> E..V....... (from 0 to 24) (default 1)
        
        """
        
        raise NotImplementedError
        
    def continue_one_color_thresh(self, *args, **kwargs):
        """
        <int> E..V....... (from 0 to 24) (default 0)
        
        """
        
        raise NotImplementedError
        
    def sixteen_color_thresh(self, *args, **kwargs):
        """
        <int> E..V....... (from 0 to 24) (default 1)
        
        """
        
        raise NotImplementedError
        
    def memc_only(self, *args, **kwargs):
        """
        <boolean> E..V....... Only do ME/MC (I frames -> ref, P frame -> ME+MC). (default false)
        
        """
        
        raise NotImplementedError
        
    def no_bitstream(self, *args, **kwargs):
        """
        <boolean> E..V....... Skip final bitstream writeout. (default false)
        
        """
        
        raise NotImplementedError
        
    def iterative_dia_size(self, *args, **kwargs):
        """
        <int> E..V....... Dia size for the iterative ME (from 0 to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def compression_algo(self, *args, **kwargs):
        """
        <int> E..V....... (from 1 to 32946) (default packbits)
        
        packbits        32773        E..V.......
        raw             1            E..V.......
        lzw             5            E..V.......
        deflate         32946        E..V.......
        """
        
        raise NotImplementedError
        
    def tolerance(self, *args, **kwargs):
        """
        <double> E..V....... Max undershoot in percent (from 0 to 45) (default 5)
        
        """
        
        raise NotImplementedError
        
    def slice_width(self, *args, **kwargs):
        """
        <int> E..V....... Slice width (from 32 to 1024) (default 32)
        
        """
        
        raise NotImplementedError
        
    def slice_height(self, *args, **kwargs):
        """
        <int> E..V....... Slice height (from 8 to 1024) (default 16)
        
        """
        
        raise NotImplementedError
        
    def wavelet_depth(self, *args, **kwargs):
        """
        <int> E..V....... Transform depth (from 1 to 5) (default 4)
        
        """
        
        raise NotImplementedError
        
    def wavelet_type(self, *args, **kwargs):
        """
        <int> E..V....... Transform type (from 0 to 7) (default 9_7)
        
        9_7             0            E..V....... Deslauriers-Dubuc (9,7)
        5_3             1            E..V....... LeGall (5,3)
        haar            4            E..V....... Haar (with shift)
        haar_noshift    3            E..V....... Haar (without shift)
        """
        
        raise NotImplementedError
        
    def qm(self, *args, **kwargs):
        """
        <int> E..V....... Custom quantization matrix (from 0 to 3) (default default)
        
        default         0            E..V....... Default from the specifications
        color           1            E..V....... Prevents low bitrate discoloration
        flat            2            E..V....... Optimize for PSNR
        """
        
        raise NotImplementedError
        
    def aac_coder(self, *args, **kwargs):
        """
        <int> E...A...... Coding algorithm (from 0 to 2) (default twoloop)
        
        anmr            0            E...A...... ANMR method
        twoloop         1            E...A...... Two loop searching method
        fast            2            E...A...... Default fast search
        """
        
        raise NotImplementedError
        
    def aac_ms(self, *args, **kwargs):
        """
        <boolean> E...A...... Force M/S stereo coding (default auto)
        
        """
        
        raise NotImplementedError
        
    def aac_is(self, *args, **kwargs):
        """
        <boolean> E...A...... Intensity stereo coding (default true)
        
        """
        
        raise NotImplementedError
        
    def aac_pns(self, *args, **kwargs):
        """
        <boolean> E...A...... Perceptual noise substitution (default true)
        
        """
        
        raise NotImplementedError
        
    def aac_tns(self, *args, **kwargs):
        """
        <boolean> E...A...... Temporal noise shaping (default true)
        
        """
        
        raise NotImplementedError
        
    def aac_ltp(self, *args, **kwargs):
        """
        <boolean> E...A...... Long term prediction (default false)
        
        """
        
        raise NotImplementedError
        
    def aac_pred(self, *args, **kwargs):
        """
        <boolean> E...A...... AAC-Main prediction (default false)
        
        """
        
        raise NotImplementedError
        
    def aac_pce(self, *args, **kwargs):
        """
        <boolean> E...A...... Forces the use of PCEs (default false)
        
        """
        
        raise NotImplementedError
        
    def center_mixlev(self, *args, **kwargs):
        """
        <float> E...A...... Center Mix Level (from 0 to 1) (default 0.594604)
        
        """
        
        raise NotImplementedError
        
    def surround_mixlev(self, *args, **kwargs):
        """
        <float> E...A...... Surround Mix Level (from 0 to 1) (default 0.5)
        
        """
        
        raise NotImplementedError
        
    def mixing_level(self, *args, **kwargs):
        """
        <int> E...A...... Mixing Level (from -1 to 111) (default -1)
        
        """
        
        raise NotImplementedError
        
    def room_type(self, *args, **kwargs):
        """
        <int> E...A...... Room Type (from -1 to 2) (default -1)
        
        notindicated    0            E...A...... Not Indicated (default)
        large           1            E...A...... Large Room
        small           2            E...A...... Small Room
        """
        
        raise NotImplementedError
        
    def per_frame_metadata(self, *args, **kwargs):
        """
        <boolean> E...A...... Allow Changing Metadata Per-Frame (default false)
        
        """
        
        raise NotImplementedError
        
    def copyright(self, *args, **kwargs):
        """
        <int> E...A...... Copyright Bit (from -1 to 1) (default -1)
        
        """
        
        raise NotImplementedError
        
    def dialnorm(self, *args, **kwargs):
        """
        <int> E...A...... Dialogue Level (dB) (from -31 to -1) (default -31)
        
        """
        
        raise NotImplementedError
        
    def dsur_mode(self, *args, **kwargs):
        """
        <int> E...A...... Dolby Surround Mode (from -1 to 2) (default -1)
        
        notindicated    0            E...A...... Not Indicated (default)
        on              2            E...A...... Dolby Surround Encoded
        off             1            E...A...... Not Dolby Surround Encoded
        """
        
        raise NotImplementedError
        
    def original(self, *args, **kwargs):
        """
        <int> E...A...... Original Bit Stream (from -1 to 1) (default -1)
        
        """
        
        raise NotImplementedError
        
    def dmix_mode(self, *args, **kwargs):
        """
        <int> E...A...... Preferred Stereo Downmix Mode (from -1 to 3) (default -1)
        
        notindicated    0            E...A...... Not Indicated (default)
        ltrt            1            E...A...... Lt/Rt Downmix Preferred
        loro            2            E...A...... Lo/Ro Downmix Preferred
        dplii           3            E...A...... Dolby Pro Logic II Downmix Preferred
        """
        
        raise NotImplementedError
        
    def ltrt_cmixlev(self, *args, **kwargs):
        """
        <float> E...A...... Lt/Rt Center Mix Level (from -1 to 2) (default -1)
        
        """
        
        raise NotImplementedError
        
    def ltrt_surmixlev(self, *args, **kwargs):
        """
        <float> E...A...... Lt/Rt Surround Mix Level (from -1 to 2) (default -1)
        
        """
        
        raise NotImplementedError
        
    def loro_cmixlev(self, *args, **kwargs):
        """
        <float> E...A...... Lo/Ro Center Mix Level (from -1 to 2) (default -1)
        
        """
        
        raise NotImplementedError
        
    def loro_surmixlev(self, *args, **kwargs):
        """
        <float> E...A...... Lo/Ro Surround Mix Level (from -1 to 2) (default -1)
        
        """
        
        raise NotImplementedError
        
    def dsurex_mode(self, *args, **kwargs):
        """
        <int> E...A...... Dolby Surround EX Mode (from -1 to 3) (default -1)
        
        notindicated    0            E...A...... Not Indicated (default)
        on              2            E...A...... Dolby Surround EX Encoded
        off             1            E...A...... Not Dolby Surround EX Encoded
        dpliiz          3            E...A...... Dolby Pro Logic IIz-encoded
        """
        
        raise NotImplementedError
        
    def dheadphone_mode(self, *args, **kwargs):
        """
        <int> E...A...... Dolby Headphone Mode (from -1 to 2) (default -1)
        
        notindicated    0            E...A...... Not Indicated (default)
        on              2            E...A...... Dolby Headphone Encoded
        off             1            E...A...... Not Dolby Headphone Encoded
        """
        
        raise NotImplementedError
        
    def ad_conv_type(self, *args, **kwargs):
        """
        <int> E...A...... A/D Converter Type (from -1 to 1) (default -1)
        
        standard        0            E...A...... Standard (default)
        hdcd            1            E...A...... HDCD
        """
        
        raise NotImplementedError
        
    def stereo_rematrixing(self, *args, **kwargs):
        """
        <boolean> E...A...... Stereo Rematrixing (default true)
        
        """
        
        raise NotImplementedError
        
    def channel_coupling(self, *args, **kwargs):
        """
        <int> E...A...... Channel Coupling (from -1 to 1) (default auto)
        
        auto            -1           E...A...... Selected by the Encoder
        """
        
        raise NotImplementedError
        
    def cpl_start_band(self, *args, **kwargs):
        """
        <int> E...A...... Coupling Start Band (from -1 to 15) (default auto)
        
        auto            -1           E...A...... Selected by the Encoder
        """
        
        raise NotImplementedError
        
    def min_prediction_order(self, *args, **kwargs):
        """
        <int> E...A...... (from 1 to 30) (default 4)
        
        """
        
        raise NotImplementedError
        
    def max_prediction_order(self, *args, **kwargs):
        """
        <int> E...A...... (from 1 to 30) (default 6)
        
        """
        
        raise NotImplementedError
        
    def lpc_coeff_precision(self, *args, **kwargs):
        """
        <int> E...A...... LPC coefficient precision (from 0 to 15) (default 15)
        
        """
        
        raise NotImplementedError
        
    def lpc_type(self, *args, **kwargs):
        """
        <int> E...A...... LPC algorithm (from -1 to 3) (default -1)
        
        none            0            E...A......
        fixed           1            E...A......
        levinson        2            E...A......
        cholesky        3            E...A......
        """
        
        raise NotImplementedError
        
    def lpc_passes(self, *args, **kwargs):
        """
        <int> E...A...... Number of passes to use for Cholesky factorization during LPC analysis (from 1 to INT_MAX) (default 2)
        
        """
        
        raise NotImplementedError
        
    def min_partition_order(self, *args, **kwargs):
        """
        <int> E...A...... (from -1 to 8) (default -1)
        
        """
        
        raise NotImplementedError
        
    def max_partition_order(self, *args, **kwargs):
        """
        <int> E...A...... (from -1 to 8) (default -1)
        
        """
        
        raise NotImplementedError
        
    def prediction_order_method(self, *args, **kwargs):
        """
        <int> E...A...... Search method for selecting prediction order (from -1 to 5) (default -1)
        
        estimation      0            E...A......
        2level          1            E...A......
        4level          2            E...A......
        8level          3            E...A......
        search          4            E...A......
        log             5            E...A......
        """
        
        raise NotImplementedError
        
    def ch_mode(self, *args, **kwargs):
        """
        <int> E...A...... Stereo decorrelation mode (from -1 to 3) (default auto)
        
        auto            -1           E...A......
        indep           0            E...A......
        left_side       1            E...A......
        right_side      2            E...A......
        mid_side        3            E...A......
        """
        
        raise NotImplementedError
        
    def exact_rice_parameters(self, *args, **kwargs):
        """
        <boolean> E...A...... Calculate rice parameters exactly (default false)
        
        """
        
        raise NotImplementedError
        
    def multi_dim_quant(self, *args, **kwargs):
        """
        <boolean> E...A...... Multi-dimensional quantization (default false)
        
        """
        
        raise NotImplementedError
        
    def max_interval(self, *args, **kwargs):
        """
        <int> E...A...... Max number of frames between each new header (from 8 to 128) (default 16)
        
        """
        
        raise NotImplementedError
        
    def codebook_search(self, *args, **kwargs):
        """
        <int> E...A...... Max number of codebook searches (from 1 to 100) (default 3)
        
        """
        
        raise NotImplementedError
        
    def prediction_order(self, *args, **kwargs):
        """
        <int> E...A...... Search method for selecting prediction order (from 0 to 4) (default estimation)
        
        estimation      0            E...A......
        search          4            E...A......
        """
        
        raise NotImplementedError
        
    def rematrix_precision(self, *args, **kwargs):
        """
        <int> E...A...... Rematrix coefficient precision (from 0 to 14) (default 1)
        
        """
        
        raise NotImplementedError
        
    def opus_delay(self, *args, **kwargs):
        """
        <float> E...A...... Maximum delay in milliseconds (from 2.5 to 360) (default 360)
        
        """
        
        raise NotImplementedError
        
    def apply_phase_inv(self, *args, **kwargs):
        """
        <boolean> E...A...... Apply intensity stereo phase inversion (default true)
        
        """
        
        raise NotImplementedError
        
    def sbc_delay(self, *args, **kwargs):
        """
        <duration> E...A...... set maximum algorithmic latency (default 0.013)
        
        """
        
        raise NotImplementedError
        
    def msbc(self, *args, **kwargs):
        """
        <boolean> E...A...... use mSBC mode (wideband speech mono SBC) (default false)
        
        """
        
        raise NotImplementedError
        
    def joint_stereo(self, *args, **kwargs):
        """
        <boolean> E...A...... (default auto)
        
        """
        
        raise NotImplementedError
        
    def optimize_mono(self, *args, **kwargs):
        """
        <boolean> E...A...... (default false)
        
        """
        
        raise NotImplementedError
        
    def block_size(self, *args, **kwargs):
        """
        <int> E...A...... set the block size (from 32 to 8192) (default 1024)
        
        """
        
        raise NotImplementedError
        
    def code_size(self, *args, **kwargs):
        """
        <int> E...A...... Bits per code (from 2 to 5) (default 4)
        
        """
        
        raise NotImplementedError
        
    def palette(self, *args, **kwargs):
        """
        <string> E....S..... set the global palette
        
        """
        
        raise NotImplementedError
        
    def even_rows_fix(self, *args, **kwargs):
        """
        <boolean> E....S..... Make number of rows even (workaround for some players) (default false)
        
        """
        
        raise NotImplementedError
        
    def aac_at_mode(self, *args, **kwargs):
        """
        <int> E...A...... ratecontrol mode (from -1 to 3) (default auto)
        
        auto            -1           E...A...... VBR if global quality is given; CBR otherwise
        cbr             0            E...A...... constant bitrate
        abr             1            E...A...... long-term average bitrate
        cvbr            2            E...A...... constrained variable bitrate
        vbr             3            E...A...... variable bitrate
        """
        
        raise NotImplementedError
        
    def aac_at_quality(self, *args, **kwargs):
        """
        <int> E...A...... quality vs speed control (from 0 to 2) (default 0)
        
        """
        
        raise NotImplementedError
        
    def cpu(self, *args, **kwargs):
        """
        -used <int> E..V....... Quality/Speed ratio modifier (from 0 to 8) (default 1)
        
        """
        
        raise NotImplementedError
        
    def auto(self, *args, **kwargs):
        """
        -alt-ref <int> E..V....... Enable use of alternate reference frames (2-pass only) (from -1 to 2) (default -1)
        
        """
        
        raise NotImplementedError
        
    def lag(self, *args, **kwargs):
        """
        -in-frames <int> E..V....... Number of frames to look ahead at for alternate reference frame selection (from -1 to INT_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def arnr(self, *args, **kwargs):
        """
        -max-frames <int> E..V....... altref noise reduction max frame count (from -1 to INT_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def error(self, *args, **kwargs):
        """
        -resilience <flags> E..V....... Error resilience configuration (default 0)
        
        default                      E..V....... Improve resiliency against losses of whole frames
        """
        
        raise NotImplementedError
        
    def crf(self, *args, **kwargs):
        """
        <int> E..V....... Select the quality for constant quality mode (from -1 to 63) (default -1)
        
        """
        
        raise NotImplementedError
        
    def static(self, *args, **kwargs):
        """
        -thresh <int> E..V....... A change threshold on blocks below which they will be skipped by the encoder (from 0 to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def drop(self, *args, **kwargs):
        """
        -threshold <int> E..V....... Frame drop threshold (from INT_MIN to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def denoise(self, *args, **kwargs):
        """
        -noise-level <int> E..V....... Amount of noise to be removed (from -1 to INT_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def undershoot(self, *args, **kwargs):
        """
        -pct <int> E..V....... Datarate undershoot (min) target (%) (from -1 to 100) (default -1)
        
        """
        
        raise NotImplementedError
        
    def overshoot(self, *args, **kwargs):
        """
        -pct <int> E..V....... Datarate overshoot (max) target (%) (from -1 to 1000) (default -1)
        
        """
        
        raise NotImplementedError
        
    def minsection(self, *args, **kwargs):
        """
        -pct <int> E..V....... GOP min bitrate (% of target) (from -1 to 100) (default -1)
        
        """
        
        raise NotImplementedError
        
    def maxsection(self, *args, **kwargs):
        """
        -pct <int> E..V....... GOP max bitrate (% of target) (from -1 to 5000) (default -1)
        
        """
        
        raise NotImplementedError
        
    def frame(self, *args, **kwargs):
        """
        -parallel <boolean> E..V....... Enable frame parallel decodability features (default auto)
        
        """
        
        raise NotImplementedError
        
    def tiles(self, *args, **kwargs):
        """
        <image_size> E..V....... Tile columns x rows
        
        """
        
        raise NotImplementedError
        
    def tile(self, *args, **kwargs):
        """
        -columns <int> E..V....... Log2 of number of tile columns to use (from -1 to 6) (default -1)
        
        """
        
        raise NotImplementedError
        
    def row(self, *args, **kwargs):
        """
        -mt <boolean> E..V....... Enable row based multi-threading (default auto)
        
        """
        
        raise NotImplementedError
        
    def enable(self, *args, **kwargs):
        """
        -cdef <boolean> E..V....... Enable CDEF filtering (default auto)
        
        """
        
        raise NotImplementedError
        
    def usage(self, *args, **kwargs):
        """
        <int> E..V....... Quality and compression efficiency vs speed trade-off (from 0 to INT_MAX) (default good)
        
        good            0            E..V....... Good quality
        realtime        1            E..V....... Realtime encoding
        allintra        2            E..V....... All Intra encoding
        """
        
        raise NotImplementedError
        
    def tune(self, *args, **kwargs):
        """
        <int> E..V....... The metric that the encoder tunes for. Automatically chosen by the encoder by default (from -1 to 1) (default -1)
        
        psnr            0            E..V.......
        ssim            1            E..V.......
        """
        
        raise NotImplementedError
        
    def still(self, *args, **kwargs):
        """
        -picture <boolean> E..V....... Encode in single frame mode (typically used for still AVIF images). (default false)
        
        """
        
        raise NotImplementedError
        
    def reduced(self, *args, **kwargs):
        """
        -tx-type-set <boolean> E..V....... Use reduced set of transform types (default auto)
        
        """
        
        raise NotImplementedError
        
    def use(self, *args, **kwargs):
        """
        -intra-dct-only <boolean> E..V....... Use DCT only for INTRA modes (default auto)
        
        """
        
        raise NotImplementedError
        
    def aom(self, *args, **kwargs):
        """
        -params <dictionary> E..V....... Set libaom options using a :-separated list of key=value pairs
        
        """
        
        raise NotImplementedError
        
    def effort(self, *args, **kwargs):
        """
        <int> E..V....... Encoding effort (from 1 to 9) (default 7)
        
        """
        
        raise NotImplementedError
        
    def distance(self, *args, **kwargs):
        """
        <float> E..V....... Maximum Butteraugli distance (quality setting, lower = better, zero = lossless, default 1.0) (from -1 to 15) (default -1)
        
        """
        
        raise NotImplementedError
        
    def modular(self, *args, **kwargs):
        """
        <int> E..V....... Force modular mode (from 0 to 1) (default 0)
        
        """
        
        raise NotImplementedError
        
    def xyb(self, *args, **kwargs):
        """
        <int> E..V....... Use XYB-encoding for lossy images (from 0 to 1) (default 1)
        
        """
        
        raise NotImplementedError
        
    def reservoir(self, *args, **kwargs):
        """
        <boolean> E...A...... use bit reservoir (default true)
        
        """
        
        raise NotImplementedError
        
    def abr(self, *args, **kwargs):
        """
        <boolean> E...A...... use ABR (default false)
        
        """
        
        raise NotImplementedError
        
    def cinema_mode(self, *args, **kwargs):
        """
        <int> E..V....... Digital Cinema (from 0 to 3) (default off)
        
        off             0            E..V.......
        2k_24           1            E..V.......
        2k_48           2            E..V.......
        4k_24           3            E..V.......
        """
        
        raise NotImplementedError
        
    def prog_order(self, *args, **kwargs):
        """
        <int> E..V....... Progression Order (from 0 to 4) (default lrcp)
        
        lrcp            0            E..V.......
        rlcp            1            E..V.......
        rpcl            2            E..V.......
        pcrl            3            E..V.......
        cprl            4            E..V.......
        """
        
        raise NotImplementedError
        
    def numresolution(self, *args, **kwargs):
        """
        <int> E..V....... (from 0 to 33) (default 6)
        
        """
        
        raise NotImplementedError
        
    def irreversible(self, *args, **kwargs):
        """
        <int> E..V....... (from 0 to 1) (default 0)
        
        """
        
        raise NotImplementedError
        
    def disto_alloc(self, *args, **kwargs):
        """
        <int> E..V....... (from 0 to 1) (default 1)
        
        """
        
        raise NotImplementedError
        
    def fixed_quality(self, *args, **kwargs):
        """
        <int> E..V....... (from 0 to 1) (default 0)
        
        """
        
        raise NotImplementedError
        
    def application(self, *args, **kwargs):
        """
        <int> E...A...... Intended application type (from 2048 to 2051) (default audio)
        
        voip            2048         E...A...... Favor improved speech intelligibility
        audio           2049         E...A...... Favor faithfulness to the input
        lowdelay        2051         E...A...... Restrict to only the lowest delay modes, disable voice-optimized modes
        """
        
        raise NotImplementedError
        
    def frame_duration(self, *args, **kwargs):
        """
        <float> E...A...... Duration of a frame in milliseconds (from 2.5 to 120) (default 20)
        
        """
        
        raise NotImplementedError
        
    def packet_loss(self, *args, **kwargs):
        """
        <int> E...A...... Expected packet loss percentage (from 0 to 100) (default 0)
        
        """
        
        raise NotImplementedError
        
    def fec(self, *args, **kwargs):
        """
        <boolean> E...A...... Enable inband FEC. Expected packet loss must be non-zero (default false)
        
        """
        
        raise NotImplementedError
        
    def vbr(self, *args, **kwargs):
        """
        <int> E...A...... Variable bit rate mode (from 0 to 2) (default on)
        
        off             0            E...A...... Use constant bit rate
        on              1            E...A...... Use variable bit rate
        constrained     2            E...A...... Use constrained VBR
        """
        
        raise NotImplementedError
        
    def mapping_family(self, *args, **kwargs):
        """
        <int> E...A...... Channel Mapping Family (from -1 to 255) (default -1)
        
        """
        
        raise NotImplementedError
        
    def qp(self, *args, **kwargs):
        """
        <int> E..V....... use constant quantizer mode (from -1 to 255) (default -1)
        
        """
        
        raise NotImplementedError
        
    def speed(self, *args, **kwargs):
        """
        <int> E..V....... what speed preset to use (from -1 to 10) (default -1)
        
        """
        
        raise NotImplementedError
        
    def rav1e(self, *args, **kwargs):
        """
        -params <dictionary> E..V....... set the rav1e configuration using a :-separated list of key=value parameters
        
        """
        
        raise NotImplementedError
        
    def cbr_quality(self, *args, **kwargs):
        """
        <int> E...A...... Set quality value (0 to 10) for CBR (from 0 to 10) (default 8)
        
        """
        
        raise NotImplementedError
        
    def frames_per_packet(self, *args, **kwargs):
        """
        <int> E...A...... Number of frames to encode in each packet (from 1 to 8) (default 1)
        
        """
        
        raise NotImplementedError
        
    def vad(self, *args, **kwargs):
        """
        <int> E...A...... Voice Activity Detection (from 0 to 1) (default 0)
        
        """
        
        raise NotImplementedError
        
    def dtx(self, *args, **kwargs):
        """
        <int> E...A...... Discontinuous Transmission (from 0 to 1) (default 0)
        
        """
        
        raise NotImplementedError
        
    def preset(self, *args, **kwargs):
        """
        <int> E..V....... Encoding preset (from -2 to 13) (default -2)
        
        """
        
        raise NotImplementedError
        
    def svtav1(self, *args, **kwargs):
        """
        -params <dictionary> E..V....... Set the SVT-AV1 configuration using a :-separated list of key=value parameters
        
        """
        
        raise NotImplementedError
        
    def deadline(self, *args, **kwargs):
        """
        <int> E..V....... Time to spend encoding, in microseconds. (from INT_MIN to INT_MAX) (default good)
        
        best            0            E..V.......
        good            1000000      E..V.......
        realtime        1            E..V.......
        """
        
        raise NotImplementedError
        
    def max(self, *args, **kwargs):
        """
        -intra-rate <int> E..V....... Maximum I-frame bitrate (pct) 0=unlimited (from -1 to INT_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def noise(self, *args, **kwargs):
        """
        -sensitivity <int> E..V....... Noise sensitivity (from 0 to 4) (default 0)
        
        """
        
        raise NotImplementedError
        
    def ts(self, *args, **kwargs):
        """
        -parameters <dictionary> E..V....... Temporal scaling configuration using a :-separated list of key=value parameters
        
        """
        
        raise NotImplementedError
        
    def screen(self, *args, **kwargs):
        """
        -content-mode <int> E..V....... Encoder screen content mode (from -1 to 2) (default -1)
        
        """
        
        raise NotImplementedError
        
    def quality(self, *args, **kwargs):
        """
        <int> E..V....... (from INT_MIN to INT_MAX) (default good)
        
        best            0            E..V.......
        good            1000000      E..V.......
        realtime        1            E..V.......
        """
        
        raise NotImplementedError
        
    def vp8flags(self, *args, **kwargs):
        """
        <flags> E..V....... (default 0)
        
        error_resilient              E..V....... enable error resilience
        altref                       E..V....... enable use of alternate reference frames (VP8/2-pass only)
        """
        
        raise NotImplementedError
        
    def arnr_max_frames(self, *args, **kwargs):
        """
        <int> E..V....... altref noise reduction max frame count (from 0 to 15) (default 0)
        
        """
        
        raise NotImplementedError
        
    def arnr_strength(self, *args, **kwargs):
        """
        <int> E..V....... altref noise reduction filter strength (from 0 to 6) (default 3)
        
        """
        
        raise NotImplementedError
        
    def arnr_type(self, *args, **kwargs):
        """
        <int> E..V....... altref noise reduction filter type (from 1 to 3) (default 3)
        
        """
        
        raise NotImplementedError
        
    def rc_lookahead(self, *args, **kwargs):
        """
        <int> E..V....... Number of frames to look ahead for alternate reference frame selection (from 0 to 25) (default 25)
        
        """
        
        raise NotImplementedError
        
    def sharpness(self, *args, **kwargs):
        """
        <int> E..V....... Increase sharpness at the expense of lower PSNR (from -1 to 7) (default -1)
        
        """
        
        raise NotImplementedError
        
    def lossless(self, *args, **kwargs):
        """
        <int> E..V....... Lossless mode (from -1 to 1) (default -1)
        
        """
        
        raise NotImplementedError
        
    def corpus(self, *args, **kwargs):
        """
        -complexity <int> E..V....... corpus vbr complexity midpoint (from -1 to 10000) (default -1)
        
        """
        
        raise NotImplementedError
        
    def min(self, *args, **kwargs):
        """
        -gf-interval <int> E..V....... Minimum golden/alternate reference frame interval (from -1 to INT_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def cr_threshold(self, *args, **kwargs):
        """
        <int> E..V....... Conditional replenishment threshold (from 0 to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def cr_size(self, *args, **kwargs):
        """
        <int> E..V....... Conditional replenishment block size (from 0 to 256) (default 16)
        
        """
        
        raise NotImplementedError
        
    def fastfirstpass(self, *args, **kwargs):
        """
        <boolean> E..V....... Use fast settings when encoding first pass (default true)
        
        """
        
        raise NotImplementedError
        
    def wpredp(self, *args, **kwargs):
        """
        <string> E..V....... Weighted prediction for P-frames
        
        """
        
        raise NotImplementedError
        
    def x264opts(self, *args, **kwargs):
        """
        <string> E..V....... x264 options
        
        """
        
        raise NotImplementedError
        
    def crf_max(self, *args, **kwargs):
        """
        <float> E..V....... In CRF mode, prevents VBV from lowering quality beyond this point. (from -1 to FLT_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def psy(self, *args, **kwargs):
        """
        <boolean> E..V....... Use psychovisual optimizations. (default auto)
        
        """
        
        raise NotImplementedError
        
    def rc(self, *args, **kwargs):
        """
        -lookahead <int> E..V....... Number of frames to look ahead for frametype and ratecontrol (from -1 to INT_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def weightb(self, *args, **kwargs):
        """
        <boolean> E..V....... Weighted prediction for B-frames. (default auto)
        
        """
        
        raise NotImplementedError
        
    def weightp(self, *args, **kwargs):
        """
        <int> E..V....... Weighted prediction analysis method. (from -1 to INT_MAX) (default -1)
        
        none            0            E..V.......
        simple          1            E..V.......
        smart           2            E..V.......
        """
        
        raise NotImplementedError
        
    def ssim(self, *args, **kwargs):
        """
        <boolean> E..V....... Calculate and print SSIM stats. (default auto)
        
        """
        
        raise NotImplementedError
        
    def intra(self, *args, **kwargs):
        """
        -refresh <boolean> E..V....... Use Periodic Intra Refresh instead of IDR frames. (default auto)
        
        """
        
        raise NotImplementedError
        
    def bluray(self, *args, **kwargs):
        """
        -compat <boolean> E..V....... Bluray compatibility workarounds. (default auto)
        
        """
        
        raise NotImplementedError
        
    def mixed(self, *args, **kwargs):
        """
        -refs <boolean> E..V....... One reference per partition, as opposed to one reference per macroblock (default auto)
        
        """
        
        raise NotImplementedError
        
    def fast(self, *args, **kwargs):
        """
        -pskip <boolean> E..V....... (default auto)
        
        """
        
        raise NotImplementedError
        
    def aud(self, *args, **kwargs):
        """
        <boolean> E..V....... Use access unit delimiters. (default auto)
        
        """
        
        raise NotImplementedError
        
    def mbtree(self, *args, **kwargs):
        """
        <boolean> E..V....... Use macroblock tree ratecontrol. (default auto)
        
        """
        
        raise NotImplementedError
        
    def deblock(self, *args, **kwargs):
        """
        <string> E..V....... Loop filter parameters, in <alpha:beta> form.
        
        """
        
        raise NotImplementedError
        
    def cplxblur(self, *args, **kwargs):
        """
        <float> E..V....... Reduce fluctuations in QP (before curve compression) (from -1 to FLT_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def partitions(self, *args, **kwargs):
        """
        <string> E..V....... A comma-separated list of partitions to consider. Possible values: p8x8, p4x4, b8x8, i8x8, i4x4, none, all
        
        """
        
        raise NotImplementedError
        
    def direct(self, *args, **kwargs):
        """
        -pred <int> E..V....... Direct MV prediction mode (from -1 to INT_MAX) (default -1)
        
        none            0            E..V.......
        spatial         1            E..V.......
        temporal        2            E..V.......
        auto            3            E..V.......
        """
        
        raise NotImplementedError
        
    def slice(self, *args, **kwargs):
        """
        -max-size <int> E..V....... Limit the size of each slice in bytes (from -1 to INT_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def nal(self, *args, **kwargs):
        """
        -hrd <int> E..V....... Signal HRD information (requires vbv-bufsize; cbr not allowed in .mp4) (from -1 to INT_MAX) (default -1)
        
        none            0            E..V.......
        vbr             1            E..V.......
        cbr             2            E..V.......
        """
        
        raise NotImplementedError
        
    def avcintra(self, *args, **kwargs):
        """
        -class <int> E..V....... AVC-Intra class 50/100/200/300/480 (from -1 to 480) (default -1)
        
        """
        
        raise NotImplementedError
        
    def me_method(self, *args, **kwargs):
        """
        <int> E..V....... Set motion estimation method (from -1 to 4) (default -1)
        
        dia             0            E..V.......
        hex             1            E..V.......
        umh             2            E..V.......
        esa             3            E..V.......
        tesa            4            E..V.......
        """
        
        raise NotImplementedError
        
    def motion(self, *args, **kwargs):
        """
        -est <int> E..V....... Set motion estimation method (from -1 to 4) (default -1)
        
        dia             0            E..V.......
        hex             1            E..V.......
        umh             2            E..V.......
        esa             3            E..V.......
        tesa            4            E..V.......
        """
        
        raise NotImplementedError
        
    def forced(self, *args, **kwargs):
        """
        -idr <boolean> E..V....... If forcing keyframes, force them as IDR frames. (default false)
        
        """
        
        raise NotImplementedError
        
    def chromaoffset(self, *args, **kwargs):
        """
        <int> E..V....... QP difference between chroma and luma (from INT_MIN to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def udu_sei(self, *args, **kwargs):
        """
        <boolean> E..V....... Use user data unregistered SEI if available (default false)
        
        """
        
        raise NotImplementedError
        
    def x264(self, *args, **kwargs):
        """
        -params <dictionary> E..V....... Override the x264 configuration using a :-separated list of key=value parameters
        
        """
        
        raise NotImplementedError
        
    def x265(self, *args, **kwargs):
        """
        -params <dictionary> E..V....... set the x265 configuration using a :-separated list of key=value parameters
        
        """
        
        raise NotImplementedError
        
    def lumi_aq(self, *args, **kwargs):
        """
        <int> E..V....... Luminance masking AQ (from 0 to 1) (default 0)
        
        """
        
        raise NotImplementedError
        
    def variance_aq(self, *args, **kwargs):
        """
        <int> E..V....... Variance AQ (from 0 to 1) (default 0)
        
        """
        
        raise NotImplementedError
        
    def ssim_acc(self, *args, **kwargs):
        """
        <int> E..V....... SSIM accuracy (from 0 to 4) (default 2)
        
        """
        
        raise NotImplementedError
        
    def gmc(self, *args, **kwargs):
        """
        <int> E..V....... use GMC (from 0 to 1) (default 0)
        
        """
        
        raise NotImplementedError
        
    def me_quality(self, *args, **kwargs):
        """
        <int> E..V....... Motion estimation quality (from 0 to 6) (default 4)
        
        """
        
        raise NotImplementedError
        
    def constant_bit_rate(self, *args, **kwargs):
        """
        <boolean> E..V....... Require constant bit rate (macOS 13 or newer) (default false)
        
        """
        
        raise NotImplementedError
        
    def max_slice_bytes(self, *args, **kwargs):
        """
        <int> E..V....... Set the maximum number of bytes in an H.264 slice. (from -1 to INT_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def allow_sw(self, *args, **kwargs):
        """
        <boolean> E..V....... Allow software encoding (default false)
        
        """
        
        raise NotImplementedError
        
    def require_sw(self, *args, **kwargs):
        """
        <boolean> E..V....... Require software encoding (default false)
        
        """
        
        raise NotImplementedError
        
    def realtime(self, *args, **kwargs):
        """
        <boolean> E..V....... Hint that encoding should happen in real-time if not faster (e.g. capturing from camera). (default false)
        
        """
        
        raise NotImplementedError
        
    def frames_before(self, *args, **kwargs):
        """
        <boolean> E..V....... Other frames will come before the frames in this session. This helps smooth concatenation issues. (default false)
        
        """
        
        raise NotImplementedError
        
    def frames_after(self, *args, **kwargs):
        """
        <boolean> E..V....... Other frames will come after the frames in this session. This helps smooth concatenation issues. (default false)
        
        """
        
        raise NotImplementedError
        
    def prio_speed(self, *args, **kwargs):
        """
        <boolean> E..V....... prioritize encoding speed (default auto)
        
        """
        
        raise NotImplementedError
        
    def power_efficient(self, *args, **kwargs):
        """
        <int> E..V....... Set to 1 to enable more power-efficient encoding if supported. (from -1 to 1) (default -1)
        
        """
        
        raise NotImplementedError
        
    def max_ref_frames(self, *args, **kwargs):
        """
        <int> E..V....... Sets the maximum number of reference frames. This only has an effect when the value is less than the maximum allowed by the profile/level. (from 0 to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def alpha_quality(self, *args, **kwargs):
        """
        <double> E..V....... Compression quality for the alpha channel (from 0 to 1) (default 0)
        
        """
        
        raise NotImplementedError
        
    def layer(self, *args, **kwargs):
        """
        <string> .D.V....... Set the decoding layer (default "")
        
        """
        
        raise NotImplementedError
        
    def part(self, *args, **kwargs):
        """
        <int> .D.V....... Set the decoding part (from 0 to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def apply_trc(self, *args, **kwargs):
        """
        <int> .D.V....... color transfer characteristics to apply to EXR linear input (from 1 to 18) (default gamma)
        
        bt709           1            .D.V....... BT.709
        gamma           2            .D.V....... gamma
        gamma22         4            .D.V....... BT.470 M
        gamma28         5            .D.V....... BT.470 BG
        smpte170m       6            .D.V....... SMPTE 170 M
        smpte240m       7            .D.V....... SMPTE 240 M
        linear          8            .D.V....... Linear
        log             9            .D.V....... Log
        log_sqrt        10           .D.V....... Log square root
        iec61966_2_4    11           .D.V....... IEC 61966-2-4
        bt1361          12           .D.V....... BT.1361
        iec61966_2_1    13           .D.V....... IEC 61966-2-1
        bt2020_10bit    14           .D.V....... BT.2020 - 10 bit
        bt2020_12bit    15           .D.V....... BT.2020 - 12 bit
        smpte2084       16           .D.V....... SMPTE ST 2084
        smpte428_1      17           .D.V....... SMPTE ST 428-1
        """
        
        raise NotImplementedError
        
    def is_avc(self, *args, **kwargs):
        """
        <boolean> .D.V..X.... is avc (default false)
        
        """
        
        raise NotImplementedError
        
    def nal_length_size(self, *args, **kwargs):
        """
        <int> .D.V..X.... nal_length_size (from 0 to 4) (default 0)
        
        """
        
        raise NotImplementedError
        
    def enable_er(self, *args, **kwargs):
        """
        <boolean> .D.V....... Enable error resilience on damaged frames (unsafe) (default auto)
        
        """
        
        raise NotImplementedError
        
    def x264_build(self, *args, **kwargs):
        """
        <int> .D.V....... Assume this x264 version if no x264 version found in any SEI (from -1 to INT_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def skip_gray(self, *args, **kwargs):
        """
        <boolean> .D.V....... Do not return gray gap frames (default false)
        
        """
        
        raise NotImplementedError
        
    def noref_gray(self, *args, **kwargs):
        """
        <boolean> .D.V....... Avoid using gray gap frames as references (default true)
        
        """
        
        raise NotImplementedError
        
    def apply_defdispwin(self, *args, **kwargs):
        """
        <boolean> .D.V....... Apply default display window from VUI (default false)
        
        """
        
        raise NotImplementedError
        
    def subimage(self, *args, **kwargs):
        """
        <boolean> .D.V....... decode subimage instead if available (default false)
        
        """
        
        raise NotImplementedError
        
    def thumbnail(self, *args, **kwargs):
        """
        <boolean> .D.V....... decode embedded thumbnail subimage instead if available (default false)
        
        """
        
        raise NotImplementedError
        
    def page(self, *args, **kwargs):
        """
        <int> .D.V....... page number of multi-page image to decode (starting from 1) (from 0 to 65535) (default 0)
        
        """
        
        raise NotImplementedError
        
    def dual_mono_mode(self, *args, **kwargs):
        """
        <int> .D..A...... Select the channel to decode for dual mono (from -1 to 2) (default auto)
        
        auto            -1           .D..A...... autoselection
        main            1            .D..A...... Select Main/Left channel
        sub             2            .D..A...... Select Sub/Right channel
        both            0            .D..A...... Select both channels
        """
        
        raise NotImplementedError
        
    def channel_order(self, *args, **kwargs):
        """
        <int> .D..A...... Order in which the channels are to be exported (from 0 to 1) (default default)
        
        default         0            .D..A...... normal libavcodec channel order
        coded           1            .D..A...... order in which the channels are coded in the bitstream
        """
        
        raise NotImplementedError
        
    def cons_noisegen(self, *args, **kwargs):
        """
        <boolean> .D..A...... enable consistent noise generation (default false)
        
        """
        
        raise NotImplementedError
        
    def drc_scale(self, *args, **kwargs):
        """
        <float> .D..A...... percentage of dynamic range compression to apply (from 0 to 6) (default 1)
        
        """
        
        raise NotImplementedError
        
    def heavy_compr(self, *args, **kwargs):
        """
        <boolean> .D..A...... enable heavy dynamic range compression (default false)
        
        """
        
        raise NotImplementedError
        
    def target_level(self, *args, **kwargs):
        """
        <int> .D..A...... target level in -dBFS (0 not applied) (from -31 to 0) (default 0)
        
        """
        
        raise NotImplementedError
        
    def downmix(self, *args, **kwargs):
        """
        <channel_layout> .D..A...... Request a specific channel layout from the decoder
        
        """
        
        raise NotImplementedError
        
    def core_only(self, *args, **kwargs):
        """
        <boolean> .D..A...... Decode core only without extensions (default false)
        
        """
        
        raise NotImplementedError
        
    def real_time(self, *args, **kwargs):
        """
        <boolean> .D...S..... emit subtitle events as they are decoded for real-time display (default false)
        
        """
        
        raise NotImplementedError
        
    def real_time_latency_msec(self, *args, **kwargs):
        """
        <int> .D...S..... minimum elapsed time between emitting real-time subtitle events (from 0 to 500) (default 200)
        
        """
        
        raise NotImplementedError
        
    def data_field(self, *args, **kwargs):
        """
        <int> .D...S..... select data field (from -1 to 1) (default auto)
        
        auto            -1           .D...S..... pick first one that appears
        first           0            .D...S.....
        second          1            .D...S.....
        """
        
        raise NotImplementedError
        
    def compute_edt(self, *args, **kwargs):
        """
        <boolean> .D...S..... compute end of time using pts or timeout (default false)
        
        """
        
        raise NotImplementedError
        
    def compute_clut(self, *args, **kwargs):
        """
        <boolean> .D...S..... compute clut when not available(-1) or only once (-2) or always(1) or never(0) (default auto)
        
        """
        
        raise NotImplementedError
        
    def dvb_substream(self, *args, **kwargs):
        """
        <int> .D...S..... (from -1 to 63) (default -1)
        
        """
        
        raise NotImplementedError
        
    def ifo_palette(self, *args, **kwargs):
        """
        <string> .D...S..... obtain the global palette from .IFO file
        
        """
        
        raise NotImplementedError
        
    def forced_subs_only(self, *args, **kwargs):
        """
        <boolean> .D...S..... Only show forced subtitles (default false)
        
        """
        
        raise NotImplementedError
        
    def width(self, *args, **kwargs):
        """
        <int> .D...S..... Frame width, usually video width (from 0 to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def height(self, *args, **kwargs):
        """
        <int> .D...S..... Frame height, usually video height (from 0 to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def keep_ass_markup(self, *args, **kwargs):
        """
        <boolean> .D...S..... Set if ASS tags must be escaped (default false)
        
        """
        
        raise NotImplementedError
        
    def aribb24(self, *args, **kwargs):
        """
        -base-path <string> .D...S..... set the base path for the libaribb24 library
        
        """
        
        raise NotImplementedError
        
    def default_profile(self, *args, **kwargs):
        """
        <int> .D...S..... default profile to use if not specified in the stream parameters (from -99 to 1) (default -99)
        
        a               0            .D...S..... Profile A
        c               1            .D...S..... Profile C
        """
        
        raise NotImplementedError
        
    def tilethreads(self, *args, **kwargs):
        """
        <int> .D.V......P Tile threads (from 0 to 256) (default 0)
        
        """
        
        raise NotImplementedError
        
    def framethreads(self, *args, **kwargs):
        """
        <int> .D.V......P Frame threads (from 0 to 256) (default 0)
        
        """
        
        raise NotImplementedError
        
    def max_frame_delay(self, *args, **kwargs):
        """
        <int> .D.V....... Max frame delay (from 0 to 256) (default 0)
        
        """
        
        raise NotImplementedError
        
    def filmgrain(self, *args, **kwargs):
        """
        <boolean> .D.V......P Apply Film Grain (default auto)
        
        """
        
        raise NotImplementedError
        
    def oppoint(self, *args, **kwargs):
        """
        <int> .D.V....... Select an operating point of the scalable bitstream (from -1 to 31) (default -1)
        
        """
        
        raise NotImplementedError
        
    def alllayers(self, *args, **kwargs):
        """
        <boolean> .D.V....... Output all spatial layers (default false)
        
        """
        
        raise NotImplementedError
        
    def avioflags(self, *args, **kwargs):
        """
        <flags> ED......... (default 0)
        
        direct                       ED......... reduce buffering
        """
        
        raise NotImplementedError
        
    def probesize(self, *args, **kwargs):
        """
        <int64> .D......... set probing size (from 32 to I64_MAX) (default 5000000)
        
        """
        
        raise NotImplementedError
        
    def formatprobesize(self, *args, **kwargs):
        """
        <int> .D......... number of bytes to probe file format (from 0 to 2.14748e+09) (default 1048576)
        
        """
        
        raise NotImplementedError
        
    def packetsize(self, *args, **kwargs):
        """
        <int> E.......... set packet size (from 0 to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def fflags(self, *args, **kwargs):
        """
        <flags> ED......... (default autobsf)
        
        flush_packets                E.......... reduce the latency by flushing out packets immediately
        ignidx                       .D......... ignore index
        genpts                       .D......... generate pts
        nofillin                     .D......... do not fill in missing values that can be exactly calculated
        noparse                      .D......... disable AVParsers, this needs nofillin too
        igndts                       .D......... ignore dts
        discardcorrupt               .D......... discard corrupted frames
        sortdts                      .D......... try to interleave outputted packets by dts
        fastseek                     .D......... fast but inaccurate seeks
        nobuffer                     .D......... reduce the latency introduced by optional buffering
        bitexact                     E.......... do not write random/volatile data
        shortest                     E.........P stop muxing with the shortest stream
        autobsf                      E.......... add needed bsfs automatically
        """
        
        raise NotImplementedError
        
    def seek2any(self, *args, **kwargs):
        """
        <boolean> .D......... allow seeking to non-keyframes on demuxer level when supported (default false)
        
        """
        
        raise NotImplementedError
        
    def analyzeduration(self, *args, **kwargs):
        """
        <int64> .D......... specify how many microseconds are analyzed to probe the input (from 0 to I64_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def cryptokey(self, *args, **kwargs):
        """
        <binary> .D......... decryption key
        
        """
        
        raise NotImplementedError
        
    def indexmem(self, *args, **kwargs):
        """
        <int> .D......... max memory used for timestamp index (per stream) (from 0 to INT_MAX) (default 1048576)
        
        """
        
        raise NotImplementedError
        
    def rtbufsize(self, *args, **kwargs):
        """
        <int> .D......... max memory used for buffering real-time frames (from 0 to INT_MAX) (default 3041280)
        
        """
        
        raise NotImplementedError
        
    def fdebug(self, *args, **kwargs):
        """
        <flags> ED......... print specific debug info (default 0)
        
        ts                           ED.........
        """
        
        raise NotImplementedError
        
    def max_delay(self, *args, **kwargs):
        """
        <int> ED......... maximum muxing or demuxing delay in microseconds (from -1 to INT_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def start_time_realtime(self, *args, **kwargs):
        """
        <int64> E.......... wall-clock time when stream begins (PTS==0) (from I64_MIN to I64_MAX) (default I64_MIN)
        
        """
        
        raise NotImplementedError
        
    def fpsprobesize(self, *args, **kwargs):
        """
        <int> .D......... number of frames used to probe fps (from -1 to 2.14748e+09) (default -1)
        
        """
        
        raise NotImplementedError
        
    def audio_preload(self, *args, **kwargs):
        """
        <int> E.......... microseconds by which audio packets should be interleaved earlier (from 0 to 2.14748e+09) (default 0)
        
        """
        
        raise NotImplementedError
        
    def chunk_duration(self, *args, **kwargs):
        """
        <int> E.......... microseconds for each chunk (from 0 to 2.14748e+09) (default 0)
        
        """
        
        raise NotImplementedError
        
    def chunk_size(self, *args, **kwargs):
        """
        <int> E.......... size in bytes for each chunk (from 0 to 2.14748e+09) (default 0)
        
        """
        
        raise NotImplementedError
        
    def f_err_detect(self, *args, **kwargs):
        """
        <flags> .D......... set error detection flags (deprecated; use err_detect, save via avconv) (default crccheck)
        
        crccheck                     .D......... verify embedded CRCs
        bitstream                    .D......... detect bitstream specification deviations
        buffer                       .D......... detect improper bitstream length
        explode                      .D......... abort decoding on minor error detection
        ignore_err                   .D......... ignore errors
        careful                      .D......... consider things that violate the spec, are fast to check and have not been seen in the wild as errors
        compliant                    .D......... consider all spec non compliancies as errors
        aggressive                   .D......... consider things that a sane encoder shouldn't do as an error
        """
        
        raise NotImplementedError
        
    def use_wallclock_as_timestamps(self, *args, **kwargs):
        """
        <boolean> .D......... use wallclock as timestamps (default false)
        
        """
        
        raise NotImplementedError
        
    def skip_initial_bytes(self, *args, **kwargs):
        """
        <int64> .D......... set number of bytes to skip before reading header and frames (from 0 to I64_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def correct_ts_overflow(self, *args, **kwargs):
        """
        <boolean> .D......... correct single timestamp overflows (default true)
        
        """
        
        raise NotImplementedError
        
    def flush_packets(self, *args, **kwargs):
        """
        <int> E.......... enable flushing of the I/O context after each packet (from -1 to 1) (default -1)
        
        """
        
        raise NotImplementedError
        
    def metadata_header_padding(self, *args, **kwargs):
        """
        <int> E.......... set number of bytes to be written as padding in a metadata header (from -1 to INT_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def output_ts_offset(self, *args, **kwargs):
        """
        <duration> E.......... set output timestamp offset (default 0)
        
        """
        
        raise NotImplementedError
        
    def max_interleave_delta(self, *args, **kwargs):
        """
        <int64> E.......... maximum buffering duration for interleaving (from 0 to I64_MAX) (default 10000000)
        
        """
        
        raise NotImplementedError
        
    def f_strict(self, *args, **kwargs):
        """
        <int> ED......... how strictly to follow the standards (deprecated; use strict, save via avconv) (from INT_MIN to INT_MAX) (default normal)
        
        very            2            ED......... strictly conform to a older more strict version of the spec or reference software
        strict          1            ED......... strictly conform to all the things in the spec no matter what the consequences
        normal          0            ED.........
        unofficial      -1           ED......... allow unofficial extensions
        experimental    -2           ED......... allow non-standardized experimental variants
        """
        
        raise NotImplementedError
        
    def max_ts_probe(self, *args, **kwargs):
        """
        <int> .D......... maximum number of packets to read while waiting for the first timestamp (from 0 to INT_MAX) (default 50)
        
        """
        
        raise NotImplementedError
        
    def avoid_negative_ts(self, *args, **kwargs):
        """
        <int> E.......... shift timestamps so they start at 0 (from -1 to 2) (default auto)
        
        auto            -1           E.......... enabled when required by target format
        disabled        0            E.......... do not change timestamps
        make_non_negative 1            E.......... shift timestamps so they are non negative
        make_zero       2            E.......... shift timestamps so they start at 0
        """
        
        raise NotImplementedError
        
    def format_whitelist(self, *args, **kwargs):
        """
        <string> .D......... List of demuxers that are allowed to be used
        
        """
        
        raise NotImplementedError
        
    def protocol_whitelist(self, *args, **kwargs):
        """
        <string> .D......... List of protocols that are allowed to be used
        
        """
        
        raise NotImplementedError
        
    def protocol_blacklist(self, *args, **kwargs):
        """
        <string> .D......... List of protocols that are not allowed to be used
        
        """
        
        raise NotImplementedError
        
    def max_streams(self, *args, **kwargs):
        """
        <int> .D......... maximum number of streams (from 0 to INT_MAX) (default 1000)
        
        """
        
        raise NotImplementedError
        
    def skip_estimate_duration_from_pts(self, *args, **kwargs):
        """
        <boolean> .D......... skip duration calculation in estimate_timings_from_pts (default false)
        
        """
        
        raise NotImplementedError
        
    def max_probe_packets(self, *args, **kwargs):
        """
        <int> .D......... Maximum number of packets to probe a codec (from 0 to INT_MAX) (default 2500)
        
        """
        
        raise NotImplementedError
        
    def rw_timeout(self, *args, **kwargs):
        """
        <int64> ED......... Timeout for IO operations (in microseconds) (from 0 to I64_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def playlist(self, *args, **kwargs):
        """
        <int> .D......... (from -1 to 99999) (default -1)
        
        """
        
        raise NotImplementedError
        
    def angle(self, *args, **kwargs):
        """
        <int> .D......... (from 0 to 254) (default 0)
        
        """
        
        raise NotImplementedError
        
    def chapter(self, *args, **kwargs):
        """
        <int> .D......... (from 1 to 65534) (default 1)
        
        """
        
        raise NotImplementedError
        
    def key(self, *args, **kwargs):
        """
        <binary> ED......... AES encryption/decryption key
        
        """
        
        raise NotImplementedError
        
    def iv(self, *args, **kwargs):
        """
        <binary> ED......... AES encryption/decryption initialization vector
        
        """
        
        raise NotImplementedError
        
    def decryption_key(self, *args, **kwargs):
        """
        <binary> .D......... AES decryption key
        
        """
        
        raise NotImplementedError
        
    def decryption_iv(self, *args, **kwargs):
        """
        <binary> .D......... AES decryption initialization vector
        
        """
        
        raise NotImplementedError
        
    def encryption_key(self, *args, **kwargs):
        """
        <binary> E.......... AES encryption key
        
        """
        
        raise NotImplementedError
        
    def encryption_iv(self, *args, **kwargs):
        """
        <binary> E.......... AES encryption initialization vector
        
        """
        
        raise NotImplementedError
        
    def blocksize(self, *args, **kwargs):
        """
        <int> E.......... set I/O operation maximum block size (from 1 to INT_MAX) (default INT_MAX)
        
        """
        
        raise NotImplementedError
        
    def fd(self, *args, **kwargs):
        """
        <int> E.......... set file descriptor (from -1 to INT_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def truncate(self, *args, **kwargs):
        """
        <boolean> E.......... truncate existing files on write (default true)
        
        """
        
        raise NotImplementedError
        
    def follow(self, *args, **kwargs):
        """
        <int> .D......... Follow a file as it is being written (from 0 to 1) (default 0)
        
        """
        
        raise NotImplementedError
        
    def seekable(self, *args, **kwargs):
        """
        <int> ED......... Sets if the file is seekable (from -1 to 0) (default -1)
        
        """
        
        raise NotImplementedError
        
    def timeout(self, *args, **kwargs):
        """
        <int> ED......... set timeout of socket I/O operations (from -1 to INT_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def ftp(self, *args, **kwargs):
        """
        -write-seekable <boolean> E.......... control seekability of connection during encoding (default false)
        
        """
        
        raise NotImplementedError
        
    def chunked_post(self, *args, **kwargs):
        """
        <boolean> E.......... use chunked transfer-encoding for posts (default true)
        
        """
        
        raise NotImplementedError
        
    def http_proxy(self, *args, **kwargs):
        """
        <string> ED......... set HTTP proxy to tunnel through
        
        """
        
        raise NotImplementedError
        
    def headers(self, *args, **kwargs):
        """
        <string> ED......... set custom HTTP headers, can override built in default headers
        
        """
        
        raise NotImplementedError
        
    def content_type(self, *args, **kwargs):
        """
        <string> ED......... set a specific content type for the POST messages
        
        """
        
        raise NotImplementedError
        
    def user_agent(self, *args, **kwargs):
        """
        <string> .D......... override User-Agent header (default "Lavf/61.1.100")
        
        """
        
        raise NotImplementedError
        
    def referer(self, *args, **kwargs):
        """
        <string> .D......... override referer header
        
        """
        
        raise NotImplementedError
        
    def multiple_requests(self, *args, **kwargs):
        """
        <boolean> ED......... use persistent connections (default false)
        
        """
        
        raise NotImplementedError
        
    def post_data(self, *args, **kwargs):
        """
        <binary> ED......... set custom HTTP post data
        
        """
        
        raise NotImplementedError
        
    def cookies(self, *args, **kwargs):
        """
        <string> .D......... set cookies to be sent in applicable future requests, use newline delimited Set-Cookie HTTP field value syntax
        
        """
        
        raise NotImplementedError
        
    def icy(self, *args, **kwargs):
        """
        <boolean> .D......... request ICY metadata (default true)
        
        """
        
        raise NotImplementedError
        
    def auth_type(self, *args, **kwargs):
        """
        <int> ED......... HTTP authentication type (from 0 to 1) (default none)
        
        none            0            ED......... No auth method set, autodetect
        basic           1            ED......... HTTP basic authentication
        """
        
        raise NotImplementedError
        
    def send_expect_100(self, *args, **kwargs):
        """
        <boolean> E.......... Force sending an Expect: 100-continue header for POST (default auto)
        
        """
        
        raise NotImplementedError
        
    def location(self, *args, **kwargs):
        """
        <string> ED......... The actual location of the data received
        
        """
        
        raise NotImplementedError
        
    def offset(self, *args, **kwargs):
        """
        <int64> .D......... initial byte offset (from 0 to I64_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def end_offset(self, *args, **kwargs):
        """
        <int64> .D......... try to limit the request to bytes preceding this offset (from 0 to I64_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def method(self, *args, **kwargs):
        """
        <string> ED......... Override the HTTP method or set the expected HTTP method from a client
        
        """
        
        raise NotImplementedError
        
    def reconnect(self, *args, **kwargs):
        """
        <boolean> .D......... auto reconnect after disconnect before EOF (default false)
        
        """
        
        raise NotImplementedError
        
    def reconnect_at_eof(self, *args, **kwargs):
        """
        <boolean> .D......... auto reconnect at EOF (default false)
        
        """
        
        raise NotImplementedError
        
    def reconnect_on_network_error(self, *args, **kwargs):
        """
        <boolean> .D......... auto reconnect in case of tcp/tls error during connect (default false)
        
        """
        
        raise NotImplementedError
        
    def reconnect_on_http_error(self, *args, **kwargs):
        """
        <string> .D......... list of http status codes to reconnect on
        
        """
        
        raise NotImplementedError
        
    def reconnect_streamed(self, *args, **kwargs):
        """
        <boolean> .D......... auto reconnect streamed / non seekable streams (default false)
        
        """
        
        raise NotImplementedError
        
    def reconnect_delay_max(self, *args, **kwargs):
        """
        <int> .D......... max reconnect delay in seconds after which to give up (from 0 to 4294) (default 120)
        
        """
        
        raise NotImplementedError
        
    def listen(self, *args, **kwargs):
        """
        <int> ED......... listen on HTTP (from 0 to 2) (default 0)
        
        """
        
        raise NotImplementedError
        
    def resource(self, *args, **kwargs):
        """
        <string> E.......... The resource requested by a client
        
        """
        
        raise NotImplementedError
        
    def reply_code(self, *args, **kwargs):
        """
        <int> E.......... The http status code to return to a client (from INT_MIN to 599) (default 200)
        
        """
        
        raise NotImplementedError
        
    def short_seek_size(self, *args, **kwargs):
        """
        <int> .D......... Threshold to favor readahead over seek. (from 0 to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def ice_genre(self, *args, **kwargs):
        """
        <string> E.......... set stream genre
        
        """
        
        raise NotImplementedError
        
    def ice_name(self, *args, **kwargs):
        """
        <string> E.......... set stream description
        
        """
        
        raise NotImplementedError
        
    def ice_description(self, *args, **kwargs):
        """
        <string> E.......... set stream description
        
        """
        
        raise NotImplementedError
        
    def ice_url(self, *args, **kwargs):
        """
        <string> E.......... set stream website
        
        """
        
        raise NotImplementedError
        
    def ice_public(self, *args, **kwargs):
        """
        <boolean> E.......... set if stream is public (default false)
        
        """
        
        raise NotImplementedError
        
    def password(self, *args, **kwargs):
        """
        <string> E.......... set password
        
        """
        
        raise NotImplementedError
        
    def legacy_icecast(self, *args, **kwargs):
        """
        <boolean> E.......... use legacy SOURCE method, for Icecast < v2.4 (default false)
        
        """
        
        raise NotImplementedError
        
    def tls(self, *args, **kwargs):
        """
        <boolean> E.......... use a TLS connection (default false)
        
        """
        
        raise NotImplementedError
        
    def ttl(self, *args, **kwargs):
        """
        <int> E.......... Time to live (in milliseconds, multicast only) (from -1 to INT_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def l(self, *args, **kwargs):
        """
        <int> E.......... FEC L (from 4 to 20) (default 5)
        
        """
        
        raise NotImplementedError
        
    def d(self, *args, **kwargs):
        """
        <int> E.......... FEC D (from 4 to 20) (default 5)
        
        """
        
        raise NotImplementedError
        
    def rtmp_app(self, *args, **kwargs):
        """
        <string> ED......... Name of application to connect to on the RTMP server
        
        """
        
        raise NotImplementedError
        
    def rtmp_buffer(self, *args, **kwargs):
        """
        <int> ED......... Set buffer time in milliseconds. The default is 3000. (from 0 to INT_MAX) (default 3000)
        
        """
        
        raise NotImplementedError
        
    def rtmp_conn(self, *args, **kwargs):
        """
        <string> ED......... Append arbitrary AMF data to the Connect message
        
        """
        
        raise NotImplementedError
        
    def rtmp_flashver(self, *args, **kwargs):
        """
        <string> ED......... Version of the Flash plugin used to run the SWF player.
        
        """
        
        raise NotImplementedError
        
    def rtmp_flush_interval(self, *args, **kwargs):
        """
        <int> E.......... Number of packets flushed in the same request (RTMPT only). (from 0 to INT_MAX) (default 10)
        
        """
        
        raise NotImplementedError
        
    def rtmp_enhanced_codecs(self, *args, **kwargs):
        """
        <string> E.......... Specify the codec(s) to use in an enhanced rtmp live stream
        
        """
        
        raise NotImplementedError
        
    def rtmp_live(self, *args, **kwargs):
        """
        <int> .D......... Specify that the media is a live stream. (from INT_MIN to INT_MAX) (default any)
        
        any             -2           .D......... both
        live            -1           .D......... live stream
        recorded        0            .D......... recorded stream
        """
        
        raise NotImplementedError
        
    def rtmp_pageurl(self, *args, **kwargs):
        """
        <string> .D......... URL of the web page in which the media was embedded. By default no value will be sent.
        
        """
        
        raise NotImplementedError
        
    def rtmp_playpath(self, *args, **kwargs):
        """
        <string> ED......... Stream identifier to play or to publish
        
        """
        
        raise NotImplementedError
        
    def rtmp_subscribe(self, *args, **kwargs):
        """
        <string> .D......... Name of live stream to subscribe to. Defaults to rtmp_playpath.
        
        """
        
        raise NotImplementedError
        
    def rtmp_swfhash(self, *args, **kwargs):
        """
        <binary> .D......... SHA256 hash of the decompressed SWF file (32 bytes).
        
        """
        
        raise NotImplementedError
        
    def rtmp_swfsize(self, *args, **kwargs):
        """
        <int> .D......... Size of the decompressed SWF file, required for SWFVerification. (from 0 to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def rtmp_swfurl(self, *args, **kwargs):
        """
        <string> ED......... URL of the SWF player. By default no value will be sent
        
        """
        
        raise NotImplementedError
        
    def rtmp_swfverify(self, *args, **kwargs):
        """
        <string> .D......... URL to player swf file, compute hash/size automatically.
        
        """
        
        raise NotImplementedError
        
    def rtmp_tcurl(self, *args, **kwargs):
        """
        <string> ED......... URL of the target stream. Defaults to proto://host[:port]/app.
        
        """
        
        raise NotImplementedError
        
    def rtmp_listen(self, *args, **kwargs):
        """
        <int> .D......... Listen for incoming rtmp connections (from INT_MIN to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def tcp_nodelay(self, *args, **kwargs):
        """
        <int> ED......... Use TCP_NODELAY to disable Nagle's algorithm (from 0 to 1) (default 0)
        
        """
        
        raise NotImplementedError
        
    def buffer_size(self, *args, **kwargs):
        """
        <int> ED......... Send/Receive buffer size (in bytes) (from -1 to INT_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def rtcp_port(self, *args, **kwargs):
        """
        <int> ED......... Custom rtcp port (from -1 to INT_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def local_rtpport(self, *args, **kwargs):
        """
        <int> ED......... Local rtp port (from -1 to INT_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def local_rtcpport(self, *args, **kwargs):
        """
        <int> ED......... Local rtcp port (from -1 to INT_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def connect(self, *args, **kwargs):
        """
        <boolean> ED......... Connect socket (default false)
        
        """
        
        raise NotImplementedError
        
    def write_to_source(self, *args, **kwargs):
        """
        <boolean> ED......... Send packets to the source address of the latest received packet (default false)
        
        """
        
        raise NotImplementedError
        
    def pkt_size(self, *args, **kwargs):
        """
        <int> ED......... Maximum packet size (from -1 to INT_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def dscp(self, *args, **kwargs):
        """
        <int> ED......... DSCP class (from -1 to INT_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def block(self, *args, **kwargs):
        """
        <string> ED......... Block list
        
        """
        
        raise NotImplementedError
        
    def localaddr(self, *args, **kwargs):
        """
        <string> ED......... Local address
        
        """
        
        raise NotImplementedError
        
    def srtp_out_suite(self, *args, **kwargs):
        """
        <string> E..........
        
        """
        
        raise NotImplementedError
        
    def srtp_out_params(self, *args, **kwargs):
        """
        <string> E..........
        
        """
        
        raise NotImplementedError
        
    def srtp_in_suite(self, *args, **kwargs):
        """
        <string> .D.........
        
        """
        
        raise NotImplementedError
        
    def srtp_in_params(self, *args, **kwargs):
        """
        <string> .D.........
        
        """
        
        raise NotImplementedError
        
    def start(self, *args, **kwargs):
        """
        <int64> .D......... start offset (from 0 to I64_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def end(self, *args, **kwargs):
        """
        <int64> .D......... end offset (from 0 to I64_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def local_port(self, *args, **kwargs):
        """
        <string> ED......... Local port
        
        """
        
        raise NotImplementedError
        
    def local_addr(self, *args, **kwargs):
        """
        <string> ED......... Local address
        
        """
        
        raise NotImplementedError
        
    def listen_timeout(self, *args, **kwargs):
        """
        <int> ED......... Connection awaiting timeout (in milliseconds) (from -1 to INT_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def send_buffer_size(self, *args, **kwargs):
        """
        <int> ED......... Socket send buffer size (in bytes) (from -1 to INT_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def recv_buffer_size(self, *args, **kwargs):
        """
        <int> ED......... Socket receive buffer size (in bytes) (from -1 to INT_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def tcp_mss(self, *args, **kwargs):
        """
        <int> ED......... Maximum segment size for outgoing TCP packets (from -1 to INT_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def ca_file(self, *args, **kwargs):
        """
        <string> ED......... Certificate Authority database file
        
        """
        
        raise NotImplementedError
        
    def cafile(self, *args, **kwargs):
        """
        <string> ED......... Certificate Authority database file
        
        """
        
        raise NotImplementedError
        
    def tls_verify(self, *args, **kwargs):
        """
        <int> ED......... Verify the peer certificate (from 0 to 1) (default 0)
        
        """
        
        raise NotImplementedError
        
    def cert_file(self, *args, **kwargs):
        """
        <string> ED......... Certificate file
        
        """
        
        raise NotImplementedError
        
    def key_file(self, *args, **kwargs):
        """
        <string> ED......... Private key file
        
        """
        
        raise NotImplementedError
        
    def verifyhost(self, *args, **kwargs):
        """
        <string> ED......... Verify against a specific hostname
        
        """
        
        raise NotImplementedError
        
    def bitrate(self, *args, **kwargs):
        """
        <int64> E.......... Bits to send per second (from 0 to I64_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def burst_bits(self, *args, **kwargs):
        """
        <int64> E.......... Max length of bursts in bits (when using bitrate) (from 0 to I64_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def localport(self, *args, **kwargs):
        """
        <int> ED......... Local port (from -1 to INT_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def udplite_coverage(self, *args, **kwargs):
        """
        <int> ED......... choose UDPLite head size which should be validated by checksum (from 0 to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def reuse(self, *args, **kwargs):
        """
        <boolean> ED......... explicitly allow reusing UDP sockets (default auto)
        
        """
        
        raise NotImplementedError
        
    def reuse_socket(self, *args, **kwargs):
        """
        <boolean> ED......... explicitly allow reusing UDP sockets (default auto)
        
        """
        
        raise NotImplementedError
        
    def broadcast(self, *args, **kwargs):
        """
        <boolean> E.......... explicitly allow or disallow broadcast destination (default false)
        
        """
        
        raise NotImplementedError
        
    def fifo_size(self, *args, **kwargs):
        """
        <int> .D......... set the UDP receiving circular buffer size, expressed as a number of packets with size of 188 bytes (from 0 to INT_MAX) (default 28672)
        
        """
        
        raise NotImplementedError
        
    def overrun_nonfatal(self, *args, **kwargs):
        """
        <boolean> .D......... survive in case of UDP receiving circular buffer overrun (default false)
        
        """
        
        raise NotImplementedError
        
    def type(self, *args, **kwargs):
        """
        <int> ED......... Socket type (from INT_MIN to INT_MAX) (default stream)
        
        stream          1            ED......... Stream (reliable stream-oriented)
        datagram        2            ED......... Datagram (unreliable packet-oriented)
        seqpacket       5            ED......... Seqpacket (reliable packet-oriented
        """
        
        raise NotImplementedError
        
    def rist_profile(self, *args, **kwargs):
        """
        <int> ED......... set profile (from 0 to 2) (default main)
        
        simple          0            ED.........
        main            1            ED.........
        advanced        2            ED.........
        """
        
        raise NotImplementedError
        
    def log_level(self, *args, **kwargs):
        """
        <int> ED......... set loglevel (from -1 to INT_MAX) (default 6)
        
        """
        
        raise NotImplementedError
        
    def secret(self, *args, **kwargs):
        """
        <string> ED......... set encryption secret
        
        """
        
        raise NotImplementedError
        
    def encryption(self, *args, **kwargs):
        """
        <int> ED......... set encryption type (from 0 to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def payload_size(self, *args, **kwargs):
        """
        <int> ED......... Maximum SRT packet size (from -1 to 1456) (default -1)
        
        ts_size         1316         ED.........
        max_size        1456         ED.........
        """
        
        raise NotImplementedError
        
    def maxbw(self, *args, **kwargs):
        """
        <int64> ED......... Maximum bandwidth (bytes per second) that the connection can use (from -1 to I64_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def pbkeylen(self, *args, **kwargs):
        """
        <int> ED......... Crypto key len in bytes {16,24,32} Default: 16 (128-bit) (from -1 to 32) (default -1)
        
        """
        
        raise NotImplementedError
        
    def passphrase(self, *args, **kwargs):
        """
        <string> ED......... Crypto PBKDF2 Passphrase size[0,10..64] 0:disable crypto
        
        """
        
        raise NotImplementedError
        
    def enforced_encryption(self, *args, **kwargs):
        """
        <boolean> ED......... Enforces that both connection parties have the same passphrase set (default auto)
        
        """
        
        raise NotImplementedError
        
    def kmrefreshrate(self, *args, **kwargs):
        """
        <int> ED......... The number of packets to be transmitted after which the encryption key is switched to a new key (from -1 to INT_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def kmpreannounce(self, *args, **kwargs):
        """
        <int> ED......... The interval between when a new encryption key is sent and when switchover occurs (from -1 to INT_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def snddropdelay(self, *args, **kwargs):
        """
        <int64> ED......... The sender's extra delay(in microseconds) before dropping packets (from -2 to I64_MAX) (default -2)
        
        """
        
        raise NotImplementedError
        
    def mss(self, *args, **kwargs):
        """
        <int> ED......... The Maximum Segment Size (from -1 to 1500) (default -1)
        
        """
        
        raise NotImplementedError
        
    def ffs(self, *args, **kwargs):
        """
        <int> ED......... Flight flag size (window size) (in bytes) (from -1 to INT_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def ipttl(self, *args, **kwargs):
        """
        <int> ED......... IP Time To Live (from -1 to 255) (default -1)
        
        """
        
        raise NotImplementedError
        
    def iptos(self, *args, **kwargs):
        """
        <int> ED......... IP Type of Service (from -1 to 255) (default -1)
        
        """
        
        raise NotImplementedError
        
    def inputbw(self, *args, **kwargs):
        """
        <int64> ED......... Estimated input stream rate (from -1 to I64_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def oheadbw(self, *args, **kwargs):
        """
        <int> ED......... MaxBW ceiling based on % over input stream rate (from -1 to 100) (default -1)
        
        """
        
        raise NotImplementedError
        
    def latency(self, *args, **kwargs):
        """
        <int64> ED......... receiver delay (in microseconds) to absorb bursts of missed packet retransmissions (from -1 to I64_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def tsbpddelay(self, *args, **kwargs):
        """
        <int64> ED......... deprecated, same effect as latency option (from -1 to I64_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def rcvlatency(self, *args, **kwargs):
        """
        <int64> ED......... receive latency (in microseconds) (from -1 to I64_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def peerlatency(self, *args, **kwargs):
        """
        <int64> ED......... peer latency (in microseconds) (from -1 to I64_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def tlpktdrop(self, *args, **kwargs):
        """
        <boolean> ED......... Enable too-late pkt drop (default auto)
        
        """
        
        raise NotImplementedError
        
    def nakreport(self, *args, **kwargs):
        """
        <boolean> ED......... Enable receiver to send periodic NAK reports (default auto)
        
        """
        
        raise NotImplementedError
        
    def connect_timeout(self, *args, **kwargs):
        """
        <int64> ED......... Connect timeout(in milliseconds). Caller default: 3000, rendezvous (x 10) (from -1 to I64_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def mode(self, *args, **kwargs):
        """
        <int> ED......... Connection mode (caller, listener, rendezvous) (from 0 to 2) (default caller)
        
        caller          0            ED.........
        listener        1            ED.........
        rendezvous      2            ED.........
        """
        
        raise NotImplementedError
        
    def sndbuf(self, *args, **kwargs):
        """
        <int> ED......... Send buffer size (in bytes) (from -1 to INT_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def rcvbuf(self, *args, **kwargs):
        """
        <int> ED......... Receive buffer size (in bytes) (from -1 to INT_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def lossmaxttl(self, *args, **kwargs):
        """
        <int> ED......... Maximum possible packet reorder tolerance (from -1 to INT_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def minversion(self, *args, **kwargs):
        """
        <int> ED......... The minimum SRT version that is required from the peer (from -1 to INT_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def srt_streamid(self, *args, **kwargs):
        """
        <string> ED......... A string of up to 512 characters that an Initiator can pass to a Responder
        
        """
        
        raise NotImplementedError
        
    def smoother(self, *args, **kwargs):
        """
        <string> ED......... The type of Smoother used for the transmission for that socket
        
        """
        
        raise NotImplementedError
        
    def messageapi(self, *args, **kwargs):
        """
        <boolean> ED......... Enable message API (default auto)
        
        """
        
        raise NotImplementedError
        
    def transtype(self, *args, **kwargs):
        """
        <int> ED......... The transmission type for the socket (from 0 to 2) (default 2)
        
        live            0            ED.........
        file            1            ED.........
        """
        
        raise NotImplementedError
        
    def linger(self, *args, **kwargs):
        """
        <int> ED......... Number of seconds that the socket waits for unsent data when closing (from -1 to INT_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def tsbpd(self, *args, **kwargs):
        """
        <boolean> ED......... Timestamp-based packet delivery (default auto)
        
        """
        
        raise NotImplementedError
        
    def private_key(self, *args, **kwargs):
        """
        <string> ED......... set path to private key
        
        """
        
        raise NotImplementedError
        
    def gateway(self, *args, **kwargs):
        """
        <string> .D......... The gateway to ask for IPFS data.
        
        """
        
        raise NotImplementedError
        
    def write_id3v2(self, *args, **kwargs):
        """
        <boolean> E.......... Enable ID3v2 tag writing (default false)
        
        """
        
        raise NotImplementedError
        
    def write_apetag(self, *args, **kwargs):
        """
        <boolean> E.......... Enable APE tag writing (default false)
        
        """
        
        raise NotImplementedError
        
    def write_mpeg2(self, *args, **kwargs):
        """
        <boolean> E.......... Set MPEG version to MPEG-2 (default false)
        
        """
        
        raise NotImplementedError
        
    def id3v2_version(self, *args, **kwargs):
        """
        <int> E.......... Select ID3v2 version to write. Currently 3 and 4 are supported. (from 3 to 4) (default 4)
        
        """
        
        raise NotImplementedError
        
    def plays(self, *args, **kwargs):
        """
        <int> E.......... Number of times to play the output: 0 - infinite loop, 1 - no loop (from 0 to 65535) (default 1)
        
        """
        
        raise NotImplementedError
        
    def final_delay(self, *args, **kwargs):
        """
        <rational> E.......... Force delay after the last frame (from 0 to 65535) (default 0/1)
        
        """
        
        raise NotImplementedError
        
    def version_major(self, *args, **kwargs):
        """
        <int> E.......... override file major version (from 0 to 65535) (default 2)
        
        """
        
        raise NotImplementedError
        
    def version_minor(self, *args, **kwargs):
        """
        <int> E.......... override file minor version (from 0 to 65535) (default 1)
        
        """
        
        raise NotImplementedError
        
    def name(self, *args, **kwargs):
        """
        <string> E.......... embedded file name (max 8 characters)
        
        """
        
        raise NotImplementedError
        
    def skip_rate_check(self, *args, **kwargs):
        """
        <boolean> E.......... skip sample rate check (default false)
        
        """
        
        raise NotImplementedError
        
    def loop(self, *args, **kwargs):
        """
        <boolean> E.......... set loop flag (default false)
        
        """
        
        raise NotImplementedError
        
    def reverb(self, *args, **kwargs):
        """
        <boolean> E.......... set reverb flag (default true)
        
        """
        
        raise NotImplementedError
        
    def packet_size(self, *args, **kwargs):
        """
        <int> E.......... Packet size (from 100 to 65536) (default 3200)
        
        """
        
        raise NotImplementedError
        
    def loopstart(self, *args, **kwargs):
        """
        <int64> E.......... Loopstart position in milliseconds. (from -1 to INT_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def loopend(self, *args, **kwargs):
        """
        <int64> E.......... Loopend position in milliseconds. (from 0 to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def reserve_index_space(self, *args, **kwargs):
        """
        <int> E.......... reserve space (in bytes) at the beginning of the file for each stream index (from 0 to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def write_channel_mask(self, *args, **kwargs):
        """
        <boolean> E.......... write channel mask into wave format header (default true)
        
        """
        
        raise NotImplementedError
        
    def flipped_raw_rgb(self, *args, **kwargs):
        """
        <boolean> E.......... Raw RGB bitmaps are stored bottom-up (default false)
        
        """
        
        raise NotImplementedError
        
    def movie_timescale(self, *args, **kwargs):
        """
        <int> E.......... set movie timescale (from 1 to INT_MAX) (default 1000)
        
        """
        
        raise NotImplementedError
        
    def adaptation_sets(self, *args, **kwargs):
        """
        <string> E.......... Adaptation sets. Syntax: id=0,streams=0,1,2 id=1,streams=3,4 and so on
        
        """
        
        raise NotImplementedError
        
    def dash_segment_type(self, *args, **kwargs):
        """
        <int> E.......... set dash segment files type (from 0 to 2) (default auto)
        
        auto            0            E.......... select segment file format based on codec
        mp4             1            E.......... make segment file in ISOBMFF format
        webm            2            E.......... make segment file in WebM format
        """
        
        raise NotImplementedError
        
    def extra_window_size(self, *args, **kwargs):
        """
        <int> E.......... number of segments kept outside of the manifest before removing from disk (from 0 to INT_MAX) (default 5)
        
        """
        
        raise NotImplementedError
        
    def format_options(self, *args, **kwargs):
        """
        <dictionary> E.......... set list of options for the container format (mp4/webm) used for dash
        
        """
        
        raise NotImplementedError
        
    def frag_duration(self, *args, **kwargs):
        """
        <duration> E.......... fragment duration (in seconds, fractional value can be set) (default 0)
        
        """
        
        raise NotImplementedError
        
    def frag_type(self, *args, **kwargs):
        """
        <int> E.......... set type of interval for fragments (from 0 to 3) (default none)
        
        none            0            E.......... one fragment per segment
        every_frame     1            E.......... fragment at every frame
        duration        2            E.......... fragment at specific time intervals
        pframes         3            E.......... fragment at keyframes and following P-Frame reordering (Video only, experimental)
        """
        
        raise NotImplementedError
        
    def global_sidx(self, *args, **kwargs):
        """
        <boolean> E.......... Write global SIDX atom. Applicable only for single file, mp4 output, non-streaming mode (default false)
        
        """
        
        raise NotImplementedError
        
    def hls_master_name(self, *args, **kwargs):
        """
        <string> E.......... HLS master playlist name (default "master.m3u8")
        
        """
        
        raise NotImplementedError
        
    def hls_playlist(self, *args, **kwargs):
        """
        <boolean> E.......... Generate HLS playlist files(master.m3u8, media_%d.m3u8) (default false)
        
        """
        
        raise NotImplementedError
        
    def http_opts(self, *args, **kwargs):
        """
        <dictionary> E.......... HTTP protocol options
        
        """
        
        raise NotImplementedError
        
    def http_persistent(self, *args, **kwargs):
        """
        <boolean> E.......... Use persistent HTTP connections (default false)
        
        """
        
        raise NotImplementedError
        
    def http_user_agent(self, *args, **kwargs):
        """
        <string> E.......... override User-Agent field in HTTP header
        
        """
        
        raise NotImplementedError
        
    def ignore_io_errors(self, *args, **kwargs):
        """
        <boolean> E.......... Ignore IO errors during open and write. Useful for long-duration runs with network output (default false)
        
        """
        
        raise NotImplementedError
        
    def index_correction(self, *args, **kwargs):
        """
        <boolean> E.......... Enable/Disable segment index correction logic (default false)
        
        """
        
        raise NotImplementedError
        
    def init_seg_name(self, *args, **kwargs):
        """
        <string> E.......... DASH-templated name to used for the initialization segment (default "init-stream$RepresentationID$.$ext$")
        
        """
        
        raise NotImplementedError
        
    def ldash(self, *args, **kwargs):
        """
        <boolean> E.......... Enable Low-latency dash. Constrains the value of a few elements (default false)
        
        """
        
        raise NotImplementedError
        
    def lhls(self, *args, **kwargs):
        """
        <boolean> E.......... Enable Low-latency HLS(Experimental). Adds #EXT-X-PREFETCH tag with current segment's URI (default false)
        
        """
        
        raise NotImplementedError
        
    def master_m3u8_publish_rate(self, *args, **kwargs):
        """
        <int> E.......... Publish master playlist every after this many segment intervals (from 0 to UINT32_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def max_playback_rate(self, *args, **kwargs):
        """
        <rational> E.......... Set desired maximum playback rate (from 0.5 to 1.5) (default 1/1)
        
        """
        
        raise NotImplementedError
        
    def media_seg_name(self, *args, **kwargs):
        """
        <string> E.......... DASH-templated name to used for the media segments (default "chunk-stream$RepresentationID$-$Number%05d$.$ext$")
        
        """
        
        raise NotImplementedError
        
    def min_playback_rate(self, *args, **kwargs):
        """
        <rational> E.......... Set desired minimum playback rate (from 0.5 to 1.5) (default 1/1)
        
        """
        
        raise NotImplementedError
        
    def mpd_profile(self, *args, **kwargs):
        """
        <flags> E.......... Set profiles. Elements and values used in the manifest may be constrained by them (default dash)
        
        dash                         E.......... MPEG-DASH ISO Base media file format live profile
        dvb_dash                     E.......... DVB-DASH profile
        """
        
        raise NotImplementedError
        
    def remove_at_exit(self, *args, **kwargs):
        """
        <boolean> E.......... remove all segments when finished (default false)
        
        """
        
        raise NotImplementedError
        
    def seg_duration(self, *args, **kwargs):
        """
        <duration> E.......... segment duration (in seconds, fractional value can be set) (default 5)
        
        """
        
        raise NotImplementedError
        
    def single_file(self, *args, **kwargs):
        """
        <boolean> E.......... Store all segments in one file, accessed using byte ranges (default false)
        
        """
        
        raise NotImplementedError
        
    def single_file_name(self, *args, **kwargs):
        """
        <string> E.......... DASH-templated name to be used for baseURL. Implies storing all segments in one file, accessed using byte ranges
        
        """
        
        raise NotImplementedError
        
    def streaming(self, *args, **kwargs):
        """
        <boolean> E.......... Enable/Disable streaming mode of output. Each frame will be moof fragment (default false)
        
        """
        
        raise NotImplementedError
        
    def target_latency(self, *args, **kwargs):
        """
        <duration> E.......... Set desired target latency for Low-latency dash (default 0)
        
        """
        
        raise NotImplementedError
        
    def update_period(self, *args, **kwargs):
        """
        <int64> E.......... Set the mpd update interval (from 0 to I64_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def use_template(self, *args, **kwargs):
        """
        <boolean> E.......... Use SegmentTemplate instead of SegmentList (default true)
        
        """
        
        raise NotImplementedError
        
    def use_timeline(self, *args, **kwargs):
        """
        <boolean> E.......... Use SegmentTimeline in SegmentTemplate (default true)
        
        """
        
        raise NotImplementedError
        
    def utc_timing_url(self, *args, **kwargs):
        """
        <string> E.......... URL of the page that will return the UTC timestamp in ISO format
        
        """
        
        raise NotImplementedError
        
    def window_size(self, *args, **kwargs):
        """
        <int> E.......... number of segments kept in the manifest (from 0 to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def write_prft(self, *args, **kwargs):
        """
        <boolean> E.......... Write producer reference time element (default auto)
        
        """
        
        raise NotImplementedError
        
    def brand(self, *args, **kwargs):
        """
        <string> E.......... Override major brand
        
        """
        
        raise NotImplementedError
        
    def empty_hdlr_name(self, *args, **kwargs):
        """
        <boolean> E.......... write zero-length name string in hdlr atoms within mdia and minf atoms (default false)
        
        """
        
        raise NotImplementedError
        
    def encryption_kid(self, *args, **kwargs):
        """
        <binary> E.......... The media encryption key identifier (hex)
        
        """
        
        raise NotImplementedError
        
    def encryption_scheme(self, *args, **kwargs):
        """
        <string> E.......... Configures the encryption scheme, allowed values are none, cenc-aes-ctr
        
        """
        
        raise NotImplementedError
        
    def frag_interleave(self, *args, **kwargs):
        """
        <int> E.......... Interleave samples within fragments (max number of consecutive samples, lower is tighter interleaving, but with more overhead) (from 0 to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def frag_size(self, *args, **kwargs):
        """
        <int> E.......... Maximum fragment size (from 0 to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def fragment_index(self, *args, **kwargs):
        """
        <int> E.......... Fragment number of the next fragment (from 1 to INT_MAX) (default 1)
        
        """
        
        raise NotImplementedError
        
    def iods_audio_profile(self, *args, **kwargs):
        """
        <int> E.......... iods audio profile atom. (from -1 to 255) (default -1)
        
        """
        
        raise NotImplementedError
        
    def iods_video_profile(self, *args, **kwargs):
        """
        <int> E.......... iods video profile atom. (from -1 to 255) (default -1)
        
        """
        
        raise NotImplementedError
        
    def ism_lookahead(self, *args, **kwargs):
        """
        <int> E.......... Number of lookahead entries for ISM files (from 0 to 255) (default 0)
        
        """
        
        raise NotImplementedError
        
    def movflags(self, *args, **kwargs):
        """
        <flags> E.......... MOV muxer flags (default 0)
        
        cmaf                         E.......... Write CMAF compatible fragmented MP4
        dash                         E.......... Write DASH compatible fragmented MP4
        default_base_moof              E.......... Set the default-base-is-moof flag in tfhd atoms
        delay_moov                   E.......... Delay writing the initial moov until the first fragment is cut, or until the first fragment flush
        disable_chpl                 E.......... Disable Nero chapter atom
        empty_moov                   E.......... Make the initial moov atom empty
        faststart                    E.......... Run a second pass to put the index (moov atom) at the beginning of the file
        frag_custom                  E.......... Flush fragments on caller requests
        frag_discont                 E.......... Signal that the next fragment is discontinuous from earlier ones
        frag_every_frame              E.......... Fragment at every frame
        frag_keyframe                E.......... Fragment at video keyframes
        global_sidx                  E.......... Write a global sidx index at the start of the file
        isml                         E.......... Create a live smooth streaming feed (for pushing to a publishing point)
        negative_cts_offsets              E.......... Use negative CTS offsets (reducing the need for edit lists)
        omit_tfhd_offset              E.......... Omit the base data offset in tfhd atoms
        prefer_icc                   E.......... If writing colr atom prioritise usage of ICC profile if it exists in stream packet side data
        rtphint                      E.......... Add RTP hint tracks
        separate_moof                E.......... Write separate moof/mdat atoms for each track
        skip_sidx                    E.......... Skip writing of sidx atom
        skip_trailer                 E.......... Skip writing the mfra/tfra/mfro trailer for fragmented files
        use_metadata_tags              E.......... Use mdta atom for metadata.
        write_colr                   E.......... Write colr atom even if the color info is unspecified (Experimental, may be renamed or changed, do not use from scripts)
        write_gama                   E.......... Write deprecated gama atom
        """
        
        raise NotImplementedError
        
    def moov_size(self, *args, **kwargs):
        """
        <int> E.......... maximum moov size so it can be placed at the begin (from 0 to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def min_frag_duration(self, *args, **kwargs):
        """
        <int> E.......... Minimum fragment duration (from 0 to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def mov_gamma(self, *args, **kwargs):
        """
        <float> E.......... gamma value for gama atom (from 0 to 10) (default 0)
        
        """
        
        raise NotImplementedError
        
    def rtpflags(self, *args, **kwargs):
        """
        <flags> E.......... RTP muxer flags (default 0)
        
        latm                         E.......... Use MP4A-LATM packetization instead of MPEG4-GENERIC for AAC
        rfc2190                      E.......... Use RFC 2190 packetization instead of RFC 4629 for H.263
        skip_rtcp                    E.......... Don't send RTCP sender reports
        h264_mode0                   E.......... Use mode 0 for H.264 in RTP
        send_bye                     E.......... Send RTCP BYE packets when finishing
        """
        
        raise NotImplementedError
        
    def skip_iods(self, *args, **kwargs):
        """
        <boolean> E.......... Skip writing iods atom. (default true)
        
        """
        
        raise NotImplementedError
        
    def use_editlist(self, *args, **kwargs):
        """
        <boolean> E.......... use edit list (default auto)
        
        """
        
        raise NotImplementedError
        
    def use_stream_ids_as_track_ids(self, *args, **kwargs):
        """
        <boolean> E.......... use stream ids as track ids (default false)
        
        """
        
        raise NotImplementedError
        
    def video_track_timescale(self, *args, **kwargs):
        """
        <int> E.......... set timescale of all video tracks (from 0 to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def write_btrt(self, *args, **kwargs):
        """
        <boolean> E.......... force or disable writing btrt (default auto)
        
        """
        
        raise NotImplementedError
        
    def write_tmcd(self, *args, **kwargs):
        """
        <boolean> E.......... force or disable writing tmcd (default auto)
        
        """
        
        raise NotImplementedError
        
    def attempt_recovery(self, *args, **kwargs):
        """
        <boolean> E.......... Attempt recovery in case of failure (default false)
        
        """
        
        raise NotImplementedError
        
    def drop_pkts_on_overflow(self, *args, **kwargs):
        """
        <boolean> E.......... Drop packets on fifo queue overflow not to block encoder (default false)
        
        """
        
        raise NotImplementedError
        
    def fifo_format(self, *args, **kwargs):
        """
        <string> E.......... Target muxer
        
        """
        
        raise NotImplementedError
        
    def format_opts(self, *args, **kwargs):
        """
        <dictionary> E.......... Options to be passed to underlying muxer
        
        """
        
        raise NotImplementedError
        
    def max_recovery_attempts(self, *args, **kwargs):
        """
        <int> E.......... Maximal number of recovery attempts (from 0 to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def queue_size(self, *args, **kwargs):
        """
        <int> E.......... Size of fifo queue (from 1 to INT_MAX) (default 60)
        
        """
        
        raise NotImplementedError
        
    def recovery_wait_streamtime(self, *args, **kwargs):
        """
        <boolean> E.......... Use stream time instead of real time while waiting for recovery (default false)
        
        """
        
        raise NotImplementedError
        
    def recovery_wait_time(self, *args, **kwargs):
        """
        <duration> E.......... Waiting time between recovery attempts (default 5)
        
        """
        
        raise NotImplementedError
        
    def recover_any_error(self, *args, **kwargs):
        """
        <boolean> E.......... Attempt recovery regardless of type of the error (default false)
        
        """
        
        raise NotImplementedError
        
    def restart_with_keyframe(self, *args, **kwargs):
        """
        <boolean> E.......... Wait for keyframe when restarting output (default false)
        
        """
        
        raise NotImplementedError
        
    def timeshift(self, *args, **kwargs):
        """
        <duration> E.......... Delay fifo output (default 0)
        
        """
        
        raise NotImplementedError
        
    def hash(self, *args, **kwargs):
        """
        <string> E.......... set hash to use (default "sha256")
        
        """
        
        raise NotImplementedError
        
    def format_version(self, *args, **kwargs):
        """
        <int> E.......... file format version (from 1 to 2) (default 2)
        
        """
        
        raise NotImplementedError
        
    def start_number(self, *args, **kwargs):
        """
        <int64> E.......... set first number in the sequence (from 0 to I64_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def hls_time(self, *args, **kwargs):
        """
        <duration> E.......... set segment length (default 2)
        
        """
        
        raise NotImplementedError
        
    def hls_init_time(self, *args, **kwargs):
        """
        <duration> E.......... set segment length at init list (default 0)
        
        """
        
        raise NotImplementedError
        
    def hls_list_size(self, *args, **kwargs):
        """
        <int> E.......... set maximum number of playlist entries (from 0 to INT_MAX) (default 5)
        
        """
        
        raise NotImplementedError
        
    def hls_delete_threshold(self, *args, **kwargs):
        """
        <int> E.......... set number of unreferenced segments to keep before deleting (from 1 to INT_MAX) (default 1)
        
        """
        
        raise NotImplementedError
        
    def hls_vtt_options(self, *args, **kwargs):
        """
        <string> E.......... set hls vtt list of options for the container format used for hls
        
        """
        
        raise NotImplementedError
        
    def hls_allow_cache(self, *args, **kwargs):
        """
        <int> E.......... explicitly set whether the client MAY (1) or MUST NOT (0) cache media segments (from INT_MIN to INT_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def hls_base_url(self, *args, **kwargs):
        """
        <string> E.......... url to prepend to each playlist entry
        
        """
        
        raise NotImplementedError
        
    def hls_segment_filename(self, *args, **kwargs):
        """
        <string> E.......... filename template for segment files
        
        """
        
        raise NotImplementedError
        
    def hls_segment_options(self, *args, **kwargs):
        """
        <dictionary> E.......... set segments files format options of hls
        
        """
        
        raise NotImplementedError
        
    def hls_segment_size(self, *args, **kwargs):
        """
        <int> E.......... maximum size per segment file, (in bytes) (from 0 to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def hls_key_info_file(self, *args, **kwargs):
        """
        <string> E.......... file with key URI and key file path
        
        """
        
        raise NotImplementedError
        
    def hls_enc(self, *args, **kwargs):
        """
        <boolean> E.......... enable AES128 encryption support (default false)
        
        """
        
        raise NotImplementedError
        
    def hls_enc_key(self, *args, **kwargs):
        """
        <string> E.......... hex-coded 16 byte key to encrypt the segments
        
        """
        
        raise NotImplementedError
        
    def hls_enc_key_url(self, *args, **kwargs):
        """
        <string> E.......... url to access the key to decrypt the segments
        
        """
        
        raise NotImplementedError
        
    def hls_enc_iv(self, *args, **kwargs):
        """
        <string> E.......... hex-coded 16 byte initialization vector
        
        """
        
        raise NotImplementedError
        
    def hls_subtitle_path(self, *args, **kwargs):
        """
        <string> E.......... set path of hls subtitles
        
        """
        
        raise NotImplementedError
        
    def hls_segment_type(self, *args, **kwargs):
        """
        <int> E.......... set hls segment files type (from 0 to 1) (default mpegts)
        
        mpegts          0            E.......... make segment file to mpegts files in m3u8
        fmp4            1            E.......... make segment file to fragment mp4 files in m3u8
        """
        
        raise NotImplementedError
        
    def hls_fmp4_init_filename(self, *args, **kwargs):
        """
        <string> E.......... set fragment mp4 file init filename (default "init.mp4")
        
        """
        
        raise NotImplementedError
        
    def hls_fmp4_init_resend(self, *args, **kwargs):
        """
        <boolean> E.......... resend fragment mp4 init file after refresh m3u8 every time (default false)
        
        """
        
        raise NotImplementedError
        
    def hls_flags(self, *args, **kwargs):
        """
        <flags> E.......... set flags affecting HLS playlist and media file generation (default 0)
        
        single_file                  E.......... generate a single media file indexed with byte ranges
        temp_file                    E.......... write segment and playlist to temporary file and rename when complete
        delete_segments              E.......... delete segment files that are no longer part of the playlist
        round_durations              E.......... round durations in m3u8 to whole numbers
        discont_start                E.......... start the playlist with a discontinuity tag
        omit_endlist                 E.......... Do not append an endlist when ending stream
        split_by_time                E.......... split the hls segment by time which user set by hls_time
        append_list                  E.......... append the new segments into old hls segment list
        program_date_time              E.......... add EXT-X-PROGRAM-DATE-TIME
        second_level_segment_index              E.......... include segment index in segment filenames when use_localtime
        second_level_segment_duration              E.......... include segment duration in segment filenames when use_localtime
        second_level_segment_size              E.......... include segment size in segment filenames when use_localtime
        periodic_rekey               E.......... reload keyinfo file periodically for re-keying
        independent_segments              E.......... add EXT-X-INDEPENDENT-SEGMENTS, whenever applicable
        iframes_only                 E.......... add EXT-X-I-FRAMES-ONLY, whenever applicable
        """
        
        raise NotImplementedError
        
    def strftime(self, *args, **kwargs):
        """
        <boolean> E.......... set filename expansion with strftime at segment creation (default false)
        
        """
        
        raise NotImplementedError
        
    def strftime_mkdir(self, *args, **kwargs):
        """
        <boolean> E.......... create last directory component in strftime-generated filename (default false)
        
        """
        
        raise NotImplementedError
        
    def hls_playlist_type(self, *args, **kwargs):
        """
        <int> E.......... set the HLS playlist type (from 0 to 2) (default 0)
        
        event           1            E.......... EVENT playlist
        vod             2            E.......... VOD playlist
        """
        
        raise NotImplementedError
        
    def hls_start_number_source(self, *args, **kwargs):
        """
        <int> E.......... set source of first number in sequence (from 0 to 3) (default generic)
        
        generic         0            E.......... start_number value (default)
        epoch           1            E.......... seconds since epoch
        epoch_us        3            E.......... microseconds since epoch
        datetime        2            E.......... current datetime as YYYYMMDDhhmmss
        """
        
        raise NotImplementedError
        
    def var_stream_map(self, *args, **kwargs):
        """
        <string> E.......... Variant stream map string
        
        """
        
        raise NotImplementedError
        
    def cc_stream_map(self, *args, **kwargs):
        """
        <string> E.......... Closed captions stream map string
        
        """
        
        raise NotImplementedError
        
    def master_pl_name(self, *args, **kwargs):
        """
        <string> E.......... Create HLS master playlist with this name
        
        """
        
        raise NotImplementedError
        
    def master_pl_publish_rate(self, *args, **kwargs):
        """
        <int> E.......... Publish master play list every after this many segment intervals (from 0 to UINT32_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def update(self, *args, **kwargs):
        """
        <boolean> E.......... continuously overwrite one file (default false)
        
        """
        
        raise NotImplementedError
        
    def frame_pts(self, *args, **kwargs):
        """
        <boolean> E.......... use current frame pts for filename (default false)
        
        """
        
        raise NotImplementedError
        
    def atomic_writing(self, *args, **kwargs):
        """
        <boolean> E.......... write files atomically (using temporary files and renames) (default false)
        
        """
        
        raise NotImplementedError
        
    def protocol_opts(self, *args, **kwargs):
        """
        <dictionary> E.......... specify protocol options for the opened files
        
        """
        
        raise NotImplementedError
        
    def cues_to_front(self, *args, **kwargs):
        """
        <boolean> E.......... Move Cues (the index) to the front by shifting data if necessary (default false)
        
        """
        
        raise NotImplementedError
        
    def cluster_size_limit(self, *args, **kwargs):
        """
        <int> E.......... Store at most the provided amount of bytes in a cluster. (from -1 to INT_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def cluster_time_limit(self, *args, **kwargs):
        """
        <int64> E.......... Store at most the provided number of milliseconds in a cluster. (from -1 to I64_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def dash(self, *args, **kwargs):
        """
        <boolean> E.......... Create a WebM file conforming to WebM DASH specification (default false)
        
        """
        
        raise NotImplementedError
        
    def dash_track_number(self, *args, **kwargs):
        """
        <int> E.......... Track number for the DASH stream (from 1 to INT_MAX) (default 1)
        
        """
        
        raise NotImplementedError
        
    def live(self, *args, **kwargs):
        """
        <boolean> E.......... Write files assuming it is a live stream. (default false)
        
        """
        
        raise NotImplementedError
        
    def allow_raw_vfw(self, *args, **kwargs):
        """
        <boolean> E.......... allow RAW VFW mode (default false)
        
        """
        
        raise NotImplementedError
        
    def write_crc32(self, *args, **kwargs):
        """
        <boolean> E.......... write a CRC32 element inside every Level 1 element (default true)
        
        """
        
        raise NotImplementedError
        
    def default_mode(self, *args, **kwargs):
        """
        <int> E.......... Controls how a track's FlagDefault is inferred (from 0 to 2) (default passthrough)
        
        infer           0            E.......... For each track type, mark each track of disposition default as default; if none exists, mark the first track as default.
        infer_no_subs   1            E.......... For each track type, mark each track of disposition default as default; for audio and video: if none exists, mark the first track as default.
        passthrough     2            E.......... Use the disposition flag as-is
        """
        
        raise NotImplementedError
        
    def write_id3v1(self, *args, **kwargs):
        """
        <boolean> E.......... Enable ID3v1 writing. ID3v1 tags are written in UTF-8 which may not be supported by most software. (default false)
        
        """
        
        raise NotImplementedError
        
    def write_xing(self, *args, **kwargs):
        """
        <boolean> E.......... Write the Xing header containing file duration. (default true)
        
        """
        
        raise NotImplementedError
        
    def muxrate(self, *args, **kwargs):
        """
        <int> E.......... mux rate as bits/s (from 0 to 1.67772e+09) (default 0)
        
        """
        
        raise NotImplementedError
        
    def preload(self, *args, **kwargs):
        """
        <int> E.......... initial demux-decode delay in microseconds (from 0 to INT_MAX) (default 500000)
        
        """
        
        raise NotImplementedError
        
    def mpegts_transport_stream_id(self, *args, **kwargs):
        """
        <int> E.......... Set transport_stream_id field. (from 1 to 65535) (default 1)
        
        """
        
        raise NotImplementedError
        
    def mpegts_original_network_id(self, *args, **kwargs):
        """
        <int> E.......... Set original_network_id field. (from 1 to 65535) (default 65281)
        
        """
        
        raise NotImplementedError
        
    def mpegts_service_id(self, *args, **kwargs):
        """
        <int> E.......... Set service_id field. (from 1 to 65535) (default 1)
        
        """
        
        raise NotImplementedError
        
    def mpegts_service_type(self, *args, **kwargs):
        """
        <int> E.......... Set service_type field. (from 1 to 255) (default digital_tv)
        
        digital_tv      1            E.......... Digital Television.
        digital_radio   2            E.......... Digital Radio.
        teletext        3            E.......... Teletext.
        advanced_codec_digital_radio 10           E.......... Advanced Codec Digital Radio.
        mpeg2_digital_hdtv 17           E.......... MPEG2 Digital HDTV.
        advanced_codec_digital_sdtv 22           E.......... Advanced Codec Digital SDTV.
        advanced_codec_digital_hdtv 25           E.......... Advanced Codec Digital HDTV.
        hevc_digital_hdtv 31           E.......... HEVC Digital Television Service.
        """
        
        raise NotImplementedError
        
    def mpegts_pmt_start_pid(self, *args, **kwargs):
        """
        <int> E.......... Set the first pid of the PMT. (from 32 to 8186) (default 4096)
        
        """
        
        raise NotImplementedError
        
    def mpegts_start_pid(self, *args, **kwargs):
        """
        <int> E.......... Set the first pid. (from 32 to 8186) (default 256)
        
        """
        
        raise NotImplementedError
        
    def mpegts_m2ts_mode(self, *args, **kwargs):
        """
        <boolean> E.......... Enable m2ts mode. (default auto)
        
        """
        
        raise NotImplementedError
        
    def pes_payload_size(self, *args, **kwargs):
        """
        <int> E.......... Minimum PES packet payload in bytes (from 0 to INT_MAX) (default 2930)
        
        """
        
        raise NotImplementedError
        
    def mpegts_flags(self, *args, **kwargs):
        """
        <flags> E.......... MPEG-TS muxing flags (default 0)
        
        resend_headers               E.......... Reemit PAT/PMT before writing the next packet
        latm                         E.......... Use LATM packetization for AAC
        pat_pmt_at_frames              E.......... Reemit PAT and PMT at each video frame
        system_b                     E.......... Conform to System B (DVB) instead of System A (ATSC)
        initial_discontinuity              E.......... Mark initial packets as discontinuous
        nit                          E.......... Enable NIT transmission
        omit_rai                     E.......... Disable writing of random access indicator
        """
        
        raise NotImplementedError
        
    def mpegts_copyts(self, *args, **kwargs):
        """
        <boolean> E.......... don't offset dts/pts (default auto)
        
        """
        
        raise NotImplementedError
        
    def tables_version(self, *args, **kwargs):
        """
        <int> E.......... set PAT, PMT, SDT and NIT version (from 0 to 31) (default 0)
        
        """
        
        raise NotImplementedError
        
    def omit_video_pes_length(self, *args, **kwargs):
        """
        <boolean> E.......... Omit the PES packet length for video packets (default true)
        
        """
        
        raise NotImplementedError
        
    def pcr_period(self, *args, **kwargs):
        """
        <int> E.......... PCR retransmission time in milliseconds (from -1 to INT_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def pat_period(self, *args, **kwargs):
        """
        <duration> E.......... PAT/PMT retransmission time limit in seconds (default 0.1)
        
        """
        
        raise NotImplementedError
        
    def sdt_period(self, *args, **kwargs):
        """
        <duration> E.......... SDT retransmission time limit in seconds (default 0.5)
        
        """
        
        raise NotImplementedError
        
    def nit_period(self, *args, **kwargs):
        """
        <duration> E.......... NIT retransmission time limit in seconds (default 0.5)
        
        """
        
        raise NotImplementedError
        
    def signal_standard(self, *args, **kwargs):
        """
        <int> E.......... Force/set Signal Standard (from -1 to 7) (default -1)
        
        bt601           1            E.......... ITU-R BT.601 and BT.656, also SMPTE 125M (525 and 625 line interlaced)
        bt1358          2            E.......... ITU-R BT.1358 and ITU-R BT.799-3, also SMPTE 293M (525 and 625 line progressive)
        smpte347m       3            E.......... SMPTE 347M (540 Mbps mappings)
        smpte274m       4            E.......... SMPTE 274M (1125 line)
        smpte296m       5            E.......... SMPTE 296M (750 line progressive)
        smpte349m       6            E.......... SMPTE 349M (1485 Mbps mappings)
        smpte428        7            E.......... SMPTE 428-1 DCDM
        """
        
        raise NotImplementedError
        
    def store_user_comments(self, *args, **kwargs):
        """
        <boolean> E.......... (default true)
        
        """
        
        raise NotImplementedError
        
    def d10_channelcount(self, *args, **kwargs):
        """
        <int> E.......... Force/set channelcount in generic sound essence descriptor (from -1 to 8) (default -1)
        
        """
        
        raise NotImplementedError
        
    def mxf_audio_edit_rate(self, *args, **kwargs):
        """
        <rational> E.......... Audio edit rate for timecode (from 0 to INT_MAX) (default 25/1)
        
        """
        
        raise NotImplementedError
        
    def syncpoints(self, *args, **kwargs):
        """
        <flags> E.......... NUT syncpoint behaviour (default 0)
        
        default                      E..........
        none                         E.......... Disable syncpoints, low overhead and unseekable
        timestamped                  E.......... Extend syncpoints with a wallclock timestamp
        """
        
        raise NotImplementedError
        
    def write_index(self, *args, **kwargs):
        """
        <boolean> E.......... Write index (default true)
        
        """
        
        raise NotImplementedError
        
    def serial_offset(self, *args, **kwargs):
        """
        <int> E.......... serial number offset (from 0 to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def oggpagesize(self, *args, **kwargs):
        """
        <int> E.......... Set preferred Ogg page size. (from 0 to 65025) (default 0)
        
        """
        
        raise NotImplementedError
        
    def pagesize(self, *args, **kwargs):
        """
        <int> E.......... preferred page size in bytes (deprecated) (from 0 to 65025) (default 0)
        
        """
        
        raise NotImplementedError
        
    def page_duration(self, *args, **kwargs):
        """
        <int64> E.......... preferred page duration, in microseconds (from 0 to I64_MAX) (default 1000000)
        
        """
        
        raise NotImplementedError
        
    def payload_type(self, *args, **kwargs):
        """
        <int> E.......... Specify RTP payload type (from -1 to 127) (default -1)
        
        """
        
        raise NotImplementedError
        
    def ssrc(self, *args, **kwargs):
        """
        <int> E.......... Stream identifier (from INT_MIN to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def cname(self, *args, **kwargs):
        """
        <string> E.......... CNAME to include in RTCP SR packets
        
        """
        
        raise NotImplementedError
        
    def seq(self, *args, **kwargs):
        """
        <int> E.......... Starting sequence number (from -1 to 65535) (default -1)
        
        """
        
        raise NotImplementedError
        
    def mpegts_muxer_options(self, *args, **kwargs):
        """
        <dictionary> E.......... set list of options for the MPEG-TS muxer
        
        """
        
        raise NotImplementedError
        
    def rtp_muxer_options(self, *args, **kwargs):
        """
        <dictionary> E.......... set list of options for the RTP muxer
        
        """
        
        raise NotImplementedError
        
    def initial_pause(self, *args, **kwargs):
        """
        <boolean> .D......... do not start playing the stream immediately (default false)
        
        """
        
        raise NotImplementedError
        
    def rtsp_transport(self, *args, **kwargs):
        """
        <flags> ED......... set RTSP transport protocols (default 0)
        
        udp                          ED......... UDP
        tcp                          ED......... TCP
        udp_multicast                .D......... UDP multicast
        http                         .D......... HTTP tunneling
        https                        .D......... HTTPS tunneling
        """
        
        raise NotImplementedError
        
    def rtsp_flags(self, *args, **kwargs):
        """
        <flags> .D......... set RTSP flags (default 0)
        
        filter_src                   .D......... only receive packets from the negotiated peer IP
        listen                       .D......... wait for incoming connections
        prefer_tcp                   ED......... try RTP via TCP first, if available
        satip_raw                    .D......... export raw MPEG-TS stream instead of demuxing
        """
        
        raise NotImplementedError
        
    def allowed_media_types(self, *args, **kwargs):
        """
        <flags> .D......... set media types to accept from the server (default video+audio+data+subtitle)
        
        video                        .D......... Video
        audio                        .D......... Audio
        data                         .D......... Data
        subtitle                     .D......... Subtitle
        """
        
        raise NotImplementedError
        
    def min_port(self, *args, **kwargs):
        """
        <int> ED......... set minimum local UDP port (from 0 to 65535) (default 5000)
        
        """
        
        raise NotImplementedError
        
    def max_port(self, *args, **kwargs):
        """
        <int> ED......... set maximum local UDP port (from 0 to 65535) (default 65000)
        
        """
        
        raise NotImplementedError
        
    def reorder_queue_size(self, *args, **kwargs):
        """
        <int> .D......... set number of packets to buffer for handling of reordered packets (from -1 to INT_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def reference_stream(self, *args, **kwargs):
        """
        <string> E.......... set reference stream (default "auto")
        
        """
        
        raise NotImplementedError
        
    def segment_format(self, *args, **kwargs):
        """
        <string> E.......... set container format used for the segments
        
        """
        
        raise NotImplementedError
        
    def segment_format_options(self, *args, **kwargs):
        """
        <dictionary> E.......... set list of options for the container format used for the segments
        
        """
        
        raise NotImplementedError
        
    def segment_list(self, *args, **kwargs):
        """
        <string> E.......... set the segment list filename
        
        """
        
        raise NotImplementedError
        
    def segment_header_filename(self, *args, **kwargs):
        """
        <string> E.......... write a single file containing the header
        
        """
        
        raise NotImplementedError
        
    def segment_list_flags(self, *args, **kwargs):
        """
        <flags> E.......... set flags affecting segment list generation (default cache)
        
        cache                        E.......... allow list caching
        live                         E.......... enable live-friendly list generation (useful for HLS)
        """
        
        raise NotImplementedError
        
    def segment_list_size(self, *args, **kwargs):
        """
        <int> E.......... set the maximum number of playlist entries (from 0 to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def segment_list_type(self, *args, **kwargs):
        """
        <int> E.......... set the segment list type (from -1 to 4) (default -1)
        
        flat            0            E.......... flat format
        csv             1            E.......... csv format
        ext             3            E.......... extended format
        ffconcat        4            E.......... ffconcat format
        m3u8            2            E.......... M3U8 format
        hls             2            E.......... Apple HTTP Live Streaming compatible
        """
        
        raise NotImplementedError
        
    def segment_atclocktime(self, *args, **kwargs):
        """
        <boolean> E.......... set segment to be cut at clocktime (default false)
        
        """
        
        raise NotImplementedError
        
    def segment_clocktime_offset(self, *args, **kwargs):
        """
        <duration> E.......... set segment clocktime offset (default 0)
        
        """
        
        raise NotImplementedError
        
    def segment_clocktime_wrap_duration(self, *args, **kwargs):
        """
        <duration> E.......... set segment clocktime wrapping duration (default INT64_MAX)
        
        """
        
        raise NotImplementedError
        
    def segment_time(self, *args, **kwargs):
        """
        <duration> E.......... set segment duration (default 2)
        
        """
        
        raise NotImplementedError
        
    def segment_time_delta(self, *args, **kwargs):
        """
        <duration> E.......... set approximation value used for the segment times (default 0)
        
        """
        
        raise NotImplementedError
        
    def min_seg_duration(self, *args, **kwargs):
        """
        <duration> E.......... set minimum segment duration (default 0)
        
        """
        
        raise NotImplementedError
        
    def segment_times(self, *args, **kwargs):
        """
        <string> E.......... set segment split time points
        
        """
        
        raise NotImplementedError
        
    def segment_frames(self, *args, **kwargs):
        """
        <string> E.......... set segment split frame numbers
        
        """
        
        raise NotImplementedError
        
    def segment_wrap(self, *args, **kwargs):
        """
        <int> E.......... set number after which the index wraps (from 0 to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def segment_list_entry_prefix(self, *args, **kwargs):
        """
        <string> E.......... set base url prefix for segments
        
        """
        
        raise NotImplementedError
        
    def segment_start_number(self, *args, **kwargs):
        """
        <int> E.......... set the sequence number of the first segment (from 0 to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def segment_wrap_number(self, *args, **kwargs):
        """
        <int> E.......... set the number of wrap before the first segment (from 0 to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def increment_tc(self, *args, **kwargs):
        """
        <boolean> E.......... increment timecode between each segment (default false)
        
        """
        
        raise NotImplementedError
        
    def break_non_keyframes(self, *args, **kwargs):
        """
        <boolean> E.......... allow breaking segments on non-keyframes (default false)
        
        """
        
        raise NotImplementedError
        
    def individual_header_trailer(self, *args, **kwargs):
        """
        <boolean> E.......... write header/trailer to each segment (default true)
        
        """
        
        raise NotImplementedError
        
    def write_header_trailer(self, *args, **kwargs):
        """
        <boolean> E.......... write a header to the first segment and a trailer to the last one (default true)
        
        """
        
        raise NotImplementedError
        
    def reset_timestamps(self, *args, **kwargs):
        """
        <boolean> E.......... reset timestamps at the beginning of each segment (default false)
        
        """
        
        raise NotImplementedError
        
    def initial_offset(self, *args, **kwargs):
        """
        <duration> E.......... set initial timestamp offset (default 0)
        
        """
        
        raise NotImplementedError
        
    def write_empty_segments(self, *args, **kwargs):
        """
        <boolean> E.......... allow writing empty 'filler' segments (default false)
        
        """
        
        raise NotImplementedError
        
    def lookahead_count(self, *args, **kwargs):
        """
        <int> E.......... number of lookahead fragments (from 0 to INT_MAX) (default 2)
        
        """
        
        raise NotImplementedError
        
    def spdif_flags(self, *args, **kwargs):
        """
        <flags> E.......... IEC 61937 encapsulation flags (default 0)
        
        be                           E.......... output in big-endian format (for use as s16be)
        """
        
        raise NotImplementedError
        
    def dtshd_rate(self, *args, **kwargs):
        """
        <int> E.......... mux complete DTS frames in HD mode at the specified IEC958 rate (in Hz, default 0=disabled) (from 0 to 768000) (default 0)
        
        """
        
        raise NotImplementedError
        
    def dtshd_fallback_time(self, *args, **kwargs):
        """
        <int> E.......... min secs to strip HD for after an overflow (-1: till the end, default 60) (from -1 to INT_MAX) (default 60)
        
        """
        
        raise NotImplementedError
        
    def use_fifo(self, *args, **kwargs):
        """
        <boolean> E.......... Use fifo pseudo-muxer to separate actual muxers from encoder (default false)
        
        """
        
        raise NotImplementedError
        
    def fifo_options(self, *args, **kwargs):
        """
        <dictionary> E.......... fifo pseudo-muxer options
        
        """
        
        raise NotImplementedError
        
    def write_bext(self, *args, **kwargs):
        """
        <boolean> E.......... Write BEXT chunk. (default false)
        
        """
        
        raise NotImplementedError
        
    def write_peak(self, *args, **kwargs):
        """
        <int> E.......... Write Peak Envelope chunk. (from 0 to 2) (default off)
        
        off             0            E.......... Do not write peak chunk.
        on              1            E.......... Append peak chunk after wav data.
        only            2            E.......... Write only peak chunk, omit wav data.
        """
        
        raise NotImplementedError
        
    def rf64(self, *args, **kwargs):
        """
        <int> E.......... Use RF64 header rather than RIFF for large files. (from -1 to 1) (default never)
        
        auto            -1           E.......... Write RF64 header if file grows large enough.
        always          1            E.......... Always write RF64 header regardless of file size.
        never           0            E.......... Never write RF64 header regardless of file size.
        """
        
        raise NotImplementedError
        
    def peak_block_size(self, *args, **kwargs):
        """
        <int> E.......... Number of audio samples used to generate each peak frame. (from 0 to 65536) (default 256)
        
        """
        
        raise NotImplementedError
        
    def peak_format(self, *args, **kwargs):
        """
        <int> E.......... The format of the peak envelope data (1: uint8, 2: uint16). (from 1 to 2) (default 2)
        
        """
        
        raise NotImplementedError
        
    def peak_ppv(self, *args, **kwargs):
        """
        <int> E.......... Number of peak points per peak value (1 or 2). (from 1 to 2) (default 2)
        
        """
        
        raise NotImplementedError
        
    def chunk_start_index(self, *args, **kwargs):
        """
        <int> E.......... start index of the chunk (from 0 to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def chunk_duration_ms(self, *args, **kwargs):
        """
        <int> E.......... duration of each chunk (in milliseconds) (from 0 to INT_MAX) (default 1000)
        
        """
        
        raise NotImplementedError
        
    def time_shift_buffer_depth(self, *args, **kwargs):
        """
        <double> E.......... Smallest time (in seconds) shifting buffer for which any Representation is guaranteed to be available. (from 1 to DBL_MAX) (default 60)
        
        """
        
        raise NotImplementedError
        
    def minimum_update_period(self, *args, **kwargs):
        """
        <int> E.......... Minimum Update Period (in seconds) of the manifest. (from 0 to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def header(self, *args, **kwargs):
        """
        <string> E.......... filename of the header where the initialization data will be written
        
        """
        
        raise NotImplementedError
        
    def audio_chunk_duration(self, *args, **kwargs):
        """
        <int> E.......... duration of each chunk in milliseconds (from 0 to INT_MAX) (default 5000)
        
        """
        
        raise NotImplementedError
        
    def list_devices(self, *args, **kwargs):
        """
        <boolean> E.......... list available audio devices (default false)
        
        """
        
        raise NotImplementedError
        
    def audio_device_index(self, *args, **kwargs):
        """
        <int> E.......... select audio device by index (starts at 0) (from -1 to INT_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def window_title(self, *args, **kwargs):
        """
        <string> E.......... set SDL window title
        
        """
        
        raise NotImplementedError
        
    def window_x(self, *args, **kwargs):
        """
        <int> E.......... set SDL window x position (from INT_MIN to INT_MAX) (default 805240832)
        
        """
        
        raise NotImplementedError
        
    def window_y(self, *args, **kwargs):
        """
        <int> E.......... set SDL window y position (from INT_MIN to INT_MAX) (default 805240832)
        
        """
        
        raise NotImplementedError
        
    def window_fullscreen(self, *args, **kwargs):
        """
        <boolean> E.......... set SDL window fullscreen (default false)
        
        """
        
        raise NotImplementedError
        
    def window_borderless(self, *args, **kwargs):
        """
        <boolean> E.......... set SDL window border off (default false)
        
        """
        
        raise NotImplementedError
        
    def window_enable_quit(self, *args, **kwargs):
        """
        <int> E.......... set if quit action is available (from 0 to 1) (default 1)
        
        """
        
        raise NotImplementedError
        
    def raw_packet_size(self, *args, **kwargs):
        """
        <int> .D......... (from 1 to INT_MAX) (default 1024)
        
        """
        
        raise NotImplementedError
        
    def linespeed(self, *args, **kwargs):
        """
        <int> .D......... set simulated line speed (bytes per second) (from 1 to INT_MAX) (default 6000)
        
        """
        
        raise NotImplementedError
        
    def video_size(self, *args, **kwargs):
        """
        <image_size> .D......... set video size, such as 640x480 or hd720.
        
        """
        
        raise NotImplementedError
        
    def framerate(self, *args, **kwargs):
        """
        <video_rate> .D......... set framerate (frames per second) (default "25")
        
        """
        
        raise NotImplementedError
        
    def ignore_loop(self, *args, **kwargs):
        """
        <boolean> .D......... ignore loop setting (default true)
        
        """
        
        raise NotImplementedError
        
    def max_fps(self, *args, **kwargs):
        """
        <int> .D......... maximum framerate (0 is no limit) (from 0 to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def default_fps(self, *args, **kwargs):
        """
        <int> .D......... default framerate (0 is as fast as possible) (from 0 to INT_MAX) (default 15)
        
        """
        
        raise NotImplementedError
        
    def sample_rate(self, *args, **kwargs):
        """
        <int> .D......... (from 0 to INT_MAX) (default 48000)
        
        """
        
        raise NotImplementedError
        
    def no_resync_search(self, *args, **kwargs):
        """
        <boolean> .D......... Don't try to resynchronize by looking for a certain optional start code (default false)
        
        """
        
        raise NotImplementedError
        
    def export_xmp(self, *args, **kwargs):
        """
        <boolean> .D......... Export full XMP metadata (default false)
        
        """
        
        raise NotImplementedError
        
    def pixel_format(self, *args, **kwargs):
        """
        <string> .D......... set pixel format (default "yuv420p")
        
        """
        
        raise NotImplementedError
        
    def frame_rate(self, *args, **kwargs):
        """
        <video_rate> .D......... (default "15")
        
        """
        
        raise NotImplementedError
        
    def safe(self, *args, **kwargs):
        """
        <boolean> .D......... enable safe mode (default true)
        
        """
        
        raise NotImplementedError
        
    def auto_convert(self, *args, **kwargs):
        """
        <boolean> .D......... automatically convert bitstream format (default true)
        
        """
        
        raise NotImplementedError
        
    def segment_time_metadata(self, *args, **kwargs):
        """
        <boolean> .D......... output file segment start time and duration as packet metadata (default false)
        
        """
        
        raise NotImplementedError
        
    def allowed_extensions(self, *args, **kwargs):
        """
        <string> .D......... List of file extensions that dash is allowed to access (default "aac,m4a,m4s,m4v,mov,mp4,webm,ts")
        
        """
        
        raise NotImplementedError
        
    def cenc_decryption_key(self, *args, **kwargs):
        """
        <string> .D......... Media decryption key (hex)
        
        """
        
        raise NotImplementedError
        
    def flv_metadata(self, *args, **kwargs):
        """
        <boolean> .D.V....... Allocate streams according to the onMetaData array (default false)
        
        """
        
        raise NotImplementedError
        
    def flv_full_metadata(self, *args, **kwargs):
        """
        <boolean> .D.V....... Dump full metadata of the onMetadata (default false)
        
        """
        
        raise NotImplementedError
        
    def flv_ignore_prevtag(self, *args, **kwargs):
        """
        <boolean> .D.V....... Ignore the Size of previous tag (default false)
        
        """
        
        raise NotImplementedError
        
    def missing_streams(self, *args, **kwargs):
        """
        <int> .D.V..XR... (from 0 to 255) (default 0)
        
        """
        
        raise NotImplementedError
        
    def min_delay(self, *args, **kwargs):
        """
        <int> .D......... minimum valid delay between frames (in hundredths of second) (from 0 to 6000) (default 2)
        
        """
        
        raise NotImplementedError
        
    def max_gif_delay(self, *args, **kwargs):
        """
        <int> .D......... maximum valid delay between frames (in hundredths of seconds) (from 0 to 65535) (default 65535)
        
        """
        
        raise NotImplementedError
        
    def default_delay(self, *args, **kwargs):
        """
        <int> .D......... default delay between frames (in hundredths of second) (from 0 to 6000) (default 10)
        
        """
        
        raise NotImplementedError
        
    def hca_lowkey(self, *args, **kwargs):
        """
        <int64> .D......... Low key used for handling CRI HCA files (from 0 to UINT32_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def hca_highkey(self, *args, **kwargs):
        """
        <int64> .D......... High key used for handling CRI HCA files (from 0 to UINT32_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def hca_subkey(self, *args, **kwargs):
        """
        <int> .D......... Subkey used for handling CRI HCA files (from 0 to 65535) (default 0)
        
        """
        
        raise NotImplementedError
        
    def live_start_index(self, *args, **kwargs):
        """
        <int> .D......... segment index to start live streams at (negative values are from the end) (from INT_MIN to INT_MAX) (default -3)
        
        """
        
        raise NotImplementedError
        
    def prefer_x_start(self, *args, **kwargs):
        """
        <boolean> .D......... prefer to use #EXT-X-START if it's in playlist instead of live_start_index (default false)
        
        """
        
        raise NotImplementedError
        
    def max_reload(self, *args, **kwargs):
        """
        <int> .D......... Maximum number of times a insufficient list is attempted to be reloaded (from 0 to INT_MAX) (default 3)
        
        """
        
        raise NotImplementedError
        
    def m3u8_hold_counters(self, *args, **kwargs):
        """
        <int> .D......... The maximum number of times to load m3u8 when it refreshes without new segments (from 0 to INT_MAX) (default 1000)
        
        """
        
        raise NotImplementedError
        
    def http_multiple(self, *args, **kwargs):
        """
        <boolean> .D......... Use multiple HTTP connections for fetching segments (default auto)
        
        """
        
        raise NotImplementedError
        
    def http_seekable(self, *args, **kwargs):
        """
        <boolean> .D......... Use HTTP partial requests, 0 = disable, 1 = enable, -1 = auto (default auto)
        
        """
        
        raise NotImplementedError
        
    def seg_format_options(self, *args, **kwargs):
        """
        <dictionary> .D......... Set options for segment demuxer
        
        """
        
        raise NotImplementedError
        
    def seg_max_retry(self, *args, **kwargs):
        """
        <int> .D......... Maximum number of times to reload a segment on error. (from 0 to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def pattern_type(self, *args, **kwargs):
        """
        <int> .D......... set pattern type (from 0 to INT_MAX) (default 4)
        
        glob_sequence   0            .D......... select glob/sequence pattern type
        glob            1            .D......... select glob pattern type
        sequence        2            .D......... select sequence pattern type
        none            3            .D......... disable pattern matching
        """
        
        raise NotImplementedError
        
    def start_number_range(self, *args, **kwargs):
        """
        <int> .D......... set range for looking at the first sequence number (from 1 to INT_MAX) (default 5)
        
        """
        
        raise NotImplementedError
        
    def ts_from_file(self, *args, **kwargs):
        """
        <int> .D......... set frame timestamp from file's one (from 0 to 2) (default none)
        
        none            0            .D......... none
        sec             1            .D......... second precision
        ns              2            .D......... nano second precision
        """
        
        raise NotImplementedError
        
    def export_path_metadata(self, *args, **kwargs):
        """
        <boolean> .D......... enable metadata containing input path information (default false)
        
        """
        
        raise NotImplementedError
        
    def use_absolute_path(self, *args, **kwargs):
        """
        <boolean> .D.V....... allow using absolute path when opening alias, this is a possible security issue (default false)
        
        """
        
        raise NotImplementedError
        
    def seek_streams_individually(self, *args, **kwargs):
        """
        <boolean> .D.V....... Seek each stream individually to the closest point (default true)
        
        """
        
        raise NotImplementedError
        
    def ignore_editlist(self, *args, **kwargs):
        """
        <boolean> .D.V....... Ignore the edit list atom. (default false)
        
        """
        
        raise NotImplementedError
        
    def advanced_editlist(self, *args, **kwargs):
        """
        <boolean> .D.V....... Modify the AVIndex according to the editlists. Use this option to decode in the order specified by the edits. (default true)
        
        """
        
        raise NotImplementedError
        
    def ignore_chapters(self, *args, **kwargs):
        """
        <boolean> .D.V....... (default false)
        
        """
        
        raise NotImplementedError
        
    def use_mfra_for(self, *args, **kwargs):
        """
        <int> .D.V....... use mfra for fragment timestamps (from -1 to 2) (default auto)
        
        auto            -1           .D.V....... auto
        dts             1            .D.V....... dts
        pts             2            .D.V....... pts
        """
        
        raise NotImplementedError
        
    def use_tfdt(self, *args, **kwargs):
        """
        <boolean> .D.V....... use tfdt for fragment timestamps (default true)
        
        """
        
        raise NotImplementedError
        
    def export_all(self, *args, **kwargs):
        """
        <boolean> .D.V....... Export unrecognized metadata entries (default false)
        
        """
        
        raise NotImplementedError
        
    def activation_bytes(self, *args, **kwargs):
        """
        <binary> .D......... Secret bytes for Audible AAX files
        
        """
        
        raise NotImplementedError
        
    def audible_key(self, *args, **kwargs):
        """
        <binary> .D......... AES-128 Key for Audible AAXC files
        
        """
        
        raise NotImplementedError
        
    def audible_iv(self, *args, **kwargs):
        """
        <binary> .D......... AES-128 IV for Audible AAXC files
        
        """
        
        raise NotImplementedError
        
    def audible_fixed_key(self, *args, **kwargs):
        """
        <binary> .D......... Fixed key used for handling Audible AAX files
        
        """
        
        raise NotImplementedError
        
    def enable_drefs(self, *args, **kwargs):
        """
        <boolean> .D.V....... Enable external track support. (default false)
        
        """
        
        raise NotImplementedError
        
    def max_stts_delta(self, *args, **kwargs):
        """
        <int> .D......... treat offsets above this value as invalid (from 0 to UINT32_MAX) (default 4294487295)
        
        """
        
        raise NotImplementedError
        
    def interleaved_read(self, *args, **kwargs):
        """
        <boolean> .D......... Interleave packets from multiple tracks at demuxer level (default true)
        
        """
        
        raise NotImplementedError
        
    def resync_size(self, *args, **kwargs):
        """
        <int> .D......... set size limit for looking up a new synchronization (from 0 to INT_MAX) (default 65536)
        
        """
        
        raise NotImplementedError
        
    def fix_teletext_pts(self, *args, **kwargs):
        """
        <boolean> .D......... try to fix pts values of dvb teletext streams (default true)
        
        """
        
        raise NotImplementedError
        
    def scan_all_pmts(self, *args, **kwargs):
        """
        <boolean> .D......... scan and combine all PMTs (default auto)
        
        """
        
        raise NotImplementedError
        
    def skip_unknown_pmt(self, *args, **kwargs):
        """
        <boolean> .D......... skip PMTs for programs not advertised in the PAT (default false)
        
        """
        
        raise NotImplementedError
        
    def merge_pmt_versions(self, *args, **kwargs):
        """
        <boolean> .D......... re-use streams when PMT's version/pids change (default false)
        
        """
        
        raise NotImplementedError
        
    def max_packet_size(self, *args, **kwargs):
        """
        <int> .D......... maximum size of emitted packet (from 1 to 1.07374e+09) (default 204800)
        
        """
        
        raise NotImplementedError
        
    def compute_pcr(self, *args, **kwargs):
        """
        <boolean> .D......... compute exact PCR for each transport stream packet (default false)
        
        """
        
        raise NotImplementedError
        
    def rtp_flags(self, *args, **kwargs):
        """
        <flags> .D......... set RTP flags (default 0)
        
        filter_src                   .D......... only receive packets from the negotiated peer IP
        """
        
        raise NotImplementedError
        
    def max_file_size(self, *args, **kwargs):
        """
        <int> .D......... (from 0 to INT_MAX) (default 5000000)
        
        """
        
        raise NotImplementedError
        
    def sdp_flags(self, *args, **kwargs):
        """
        <flags> .D......... SDP flags (default 0)
        
        filter_src                   .D......... only receive packets from the negotiated peer IP
        custom_io                    .D......... use custom I/O
        rtcp_to_source               .D......... send RTCP packets to the source address of received packets
        """
        
        raise NotImplementedError
        
    def chars_per_frame(self, *args, **kwargs):
        """
        <int> .D......... (from 1 to INT_MAX) (default 6000)
        
        """
        
        raise NotImplementedError
        
    def ignore_length(self, *args, **kwargs):
        """
        <boolean> .D......... Ignore length (default false)
        
        """
        
        raise NotImplementedError
        
    def max_size(self, *args, **kwargs):
        """
        <int> .D......... max size of single packet (from 0 to 4.1943e+06) (default 0)
        
        """
        
        raise NotImplementedError
        
    def bandwidth(self, *args, **kwargs):
        """
        <int> .D......... bandwidth of this stream to be specified in the DASH manifest. (from 0 to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def video_device_index(self, *args, **kwargs):
        """
        <int> .D......... select video device by index for devices with same name (starts at 0) (from -1 to INT_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def capture_cursor(self, *args, **kwargs):
        """
        <boolean> .D......... capture the screen cursor (default false)
        
        """
        
        raise NotImplementedError
        
    def capture_mouse_clicks(self, *args, **kwargs):
        """
        <boolean> .D......... capture the screen mouse clicks (default false)
        
        """
        
        raise NotImplementedError
        
    def capture_raw_data(self, *args, **kwargs):
        """
        <boolean> .D......... capture the raw data from device connection (default false)
        
        """
        
        raise NotImplementedError
        
    def drop_late_frames(self, *args, **kwargs):
        """
        <boolean> .D......... drop frames that are available later than expected (default true)
        
        """
        
        raise NotImplementedError
        
    def graph(self, *args, **kwargs):
        """
        <string> .D......... set libavfilter graph
        
        """
        
        raise NotImplementedError
        
    def graph_file(self, *args, **kwargs):
        """
        <string> .D......... set libavfilter graph filename
        
        """
        
        raise NotImplementedError
        
    def dumpgraph(self, *args, **kwargs):
        """
        <string> .D......... dump graph to stderr
        
        """
        
        raise NotImplementedError
        
    def window_id(self, *args, **kwargs):
        """
        <int> .D......... Window to capture. (from 0 to UINT32_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def x(self, *args, **kwargs):
        """
        <int> .D......... Initial x coordinate. (from 0 to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def grab_x(self, *args, **kwargs):
        """
        <int> .D......... Initial x coordinate. (from 0 to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def grab_y(self, *args, **kwargs):
        """
        <int> .D......... Initial y coordinate. (from 0 to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def draw_mouse(self, *args, **kwargs):
        """
        <int> .D......... Draw the mouse pointer. (from 0 to 1) (default 1)
        
        """
        
        raise NotImplementedError
        
    def follow_mouse(self, *args, **kwargs):
        """
        <int> .D......... Move the grabbing region when the mouse pointer reaches within specified amount of pixels to the edge of region. (from -1 to INT_MAX) (default 0)
        
        centered        -1           .D......... Keep the mouse pointer at the center of grabbing region when following.
        """
        
        raise NotImplementedError
        
    def show_region(self, *args, **kwargs):
        """
        <int> .D......... Show the grabbing region. (from 0 to 1) (default 0)
        
        """
        
        raise NotImplementedError
        
    def region_border(self, *args, **kwargs):
        """
        <int> .D......... Set the region border thickness. (from 1 to 128) (default 3)
        
        """
        
        raise NotImplementedError
        
    def select_region(self, *args, **kwargs):
        """
        <boolean> .D......... Select the grabbing region graphically using the pointer. (default false)
        
        """
        
        raise NotImplementedError
        
    def sws_flags(self, *args, **kwargs):
        """
        <flags> E..V....... scaler flags (default bicubic)
        
        fast_bilinear                E..V....... fast bilinear
        bilinear                     E..V....... bilinear
        bicubic                      E..V....... bicubic
        experimental                 E..V....... experimental
        neighbor                     E..V....... nearest neighbor
        area                         E..V....... averaging area
        bicublin                     E..V....... luma bicubic, chroma bilinear
        gauss                        E..V....... Gaussian
        sinc                         E..V....... sinc
        lanczos                      E..V....... Lanczos
        spline                       E..V....... natural bicubic spline
        print_info                   E..V....... print info
        accurate_rnd                 E..V....... accurate rounding
        full_chroma_int              E..V....... full chroma interpolation
        full_chroma_inp              E..V....... full chroma input
        bitexact                     E..V.......
        error_diffusion              E..V....... error diffusion dither
        """
        
        raise NotImplementedError
        
    def srcw(self, *args, **kwargs):
        """
        <int> E..V....... source width (from 1 to INT_MAX) (default 16)
        
        """
        
        raise NotImplementedError
        
    def srch(self, *args, **kwargs):
        """
        <int> E..V....... source height (from 1 to INT_MAX) (default 16)
        
        """
        
        raise NotImplementedError
        
    def dstw(self, *args, **kwargs):
        """
        <int> E..V....... destination width (from 1 to INT_MAX) (default 16)
        
        """
        
        raise NotImplementedError
        
    def dsth(self, *args, **kwargs):
        """
        <int> E..V....... destination height (from 1 to INT_MAX) (default 16)
        
        """
        
        raise NotImplementedError
        
    def src_format(self, *args, **kwargs):
        """
        <pix_fmt> E..V....... source format (default yuv420p)
        
        """
        
        raise NotImplementedError
        
    def dst_format(self, *args, **kwargs):
        """
        <pix_fmt> E..V....... destination format (default yuv420p)
        
        """
        
        raise NotImplementedError
        
    def src_range(self, *args, **kwargs):
        """
        <boolean> E..V....... source is full range (default false)
        
        """
        
        raise NotImplementedError
        
    def dst_range(self, *args, **kwargs):
        """
        <boolean> E..V....... destination is full range (default false)
        
        """
        
        raise NotImplementedError
        
    def param0(self, *args, **kwargs):
        """
        <double> E..V....... scaler param 0 (from INT_MIN to INT_MAX) (default 123456)
        
        """
        
        raise NotImplementedError
        
    def param1(self, *args, **kwargs):
        """
        <double> E..V....... scaler param 1 (from INT_MIN to INT_MAX) (default 123456)
        
        """
        
        raise NotImplementedError
        
    def src_v_chr_pos(self, *args, **kwargs):
        """
        <int> E..V....... source vertical chroma position in luma grid/256 (from -513 to 512) (default -513)
        
        """
        
        raise NotImplementedError
        
    def src_h_chr_pos(self, *args, **kwargs):
        """
        <int> E..V....... source horizontal chroma position in luma grid/256 (from -513 to 512) (default -513)
        
        """
        
        raise NotImplementedError
        
    def dst_v_chr_pos(self, *args, **kwargs):
        """
        <int> E..V....... destination vertical chroma position in luma grid/256 (from -513 to 512) (default -513)
        
        """
        
        raise NotImplementedError
        
    def dst_h_chr_pos(self, *args, **kwargs):
        """
        <int> E..V....... destination horizontal chroma position in luma grid/256 (from -513 to 512) (default -513)
        
        """
        
        raise NotImplementedError
        
    def sws_dither(self, *args, **kwargs):
        """
        <int> E..V....... set dithering algorithm (from 0 to 6) (default auto)
        
        auto            1            E..V....... leave choice to sws
        bayer           2            E..V....... bayer dither
        ed              3            E..V....... error diffusion
        a_dither        4            E..V....... arithmetic addition dither
        x_dither        5            E..V....... arithmetic xor dither
        """
        
        raise NotImplementedError
        
    def alphablend(self, *args, **kwargs):
        """
        <int> E..V....... mode for alpha -> non alpha (from 0 to 2) (default none)
        
        none            0            E..V....... ignore alpha
        uniform_color   1            E..V....... blend onto a uniform color
        checkerboard    2            E..V....... blend onto a checkerboard
        """
        
        raise NotImplementedError
        
    def isr(self, *args, **kwargs):
        """
        <int> ....A...... set input sample rate (from 0 to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def in_sample_rate(self, *args, **kwargs):
        """
        <int> ....A...... set input sample rate (from 0 to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def osr(self, *args, **kwargs):
        """
        <int> ....A...... set output sample rate (from 0 to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def out_sample_rate(self, *args, **kwargs):
        """
        <int> ....A...... set output sample rate (from 0 to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def isf(self, *args, **kwargs):
        """
        <sample_fmt> ....A...... set input sample format (default none)
        
        """
        
        raise NotImplementedError
        
    def in_sample_fmt(self, *args, **kwargs):
        """
        <sample_fmt> ....A...... set input sample format (default none)
        
        """
        
        raise NotImplementedError
        
    def osf(self, *args, **kwargs):
        """
        <sample_fmt> ....A...... set output sample format (default none)
        
        """
        
        raise NotImplementedError
        
    def out_sample_fmt(self, *args, **kwargs):
        """
        <sample_fmt> ....A...... set output sample format (default none)
        
        """
        
        raise NotImplementedError
        
    def tsf(self, *args, **kwargs):
        """
        <sample_fmt> ....A...... set internal sample format (default none)
        
        """
        
        raise NotImplementedError
        
    def internal_sample_fmt(self, *args, **kwargs):
        """
        <sample_fmt> ....A...... set internal sample format (default none)
        
        """
        
        raise NotImplementedError
        
    def ichl(self, *args, **kwargs):
        """
        <channel_layout> ....A...... set input channel layout
        
        """
        
        raise NotImplementedError
        
    def in_chlayout(self, *args, **kwargs):
        """
        <channel_layout> ....A...... set input channel layout
        
        """
        
        raise NotImplementedError
        
    def ochl(self, *args, **kwargs):
        """
        <channel_layout> ....A...... set output channel layout
        
        """
        
        raise NotImplementedError
        
    def out_chlayout(self, *args, **kwargs):
        """
        <channel_layout> ....A...... set output channel layout
        
        """
        
        raise NotImplementedError
        
    def uchl(self, *args, **kwargs):
        """
        <channel_layout> ....A...... set used channel layout
        
        """
        
        raise NotImplementedError
        
    def used_chlayout(self, *args, **kwargs):
        """
        <channel_layout> ....A...... set used channel layout
        
        """
        
        raise NotImplementedError
        
    def clev(self, *args, **kwargs):
        """
        <float> ....A...... set center mix level (from -32 to 32) (default 0.707107)
        
        """
        
        raise NotImplementedError
        
    def center_mix_level(self, *args, **kwargs):
        """
        <float> ....A...... set center mix level (from -32 to 32) (default 0.707107)
        
        """
        
        raise NotImplementedError
        
    def slev(self, *args, **kwargs):
        """
        <float> ....A...... set surround mix level (from -32 to 32) (default 0.707107)
        
        """
        
        raise NotImplementedError
        
    def surround_mix_level(self, *args, **kwargs):
        """
        <float> ....A...... set surround mix Level (from -32 to 32) (default 0.707107)
        
        """
        
        raise NotImplementedError
        
    def lfe_mix_level(self, *args, **kwargs):
        """
        <float> ....A...... set LFE mix level (from -32 to 32) (default 0)
        
        """
        
        raise NotImplementedError
        
    def rmvol(self, *args, **kwargs):
        """
        <float> ....A...... set rematrix volume (from -1000 to 1000) (default 1)
        
        """
        
        raise NotImplementedError
        
    def rematrix_volume(self, *args, **kwargs):
        """
        <float> ....A...... set rematrix volume (from -1000 to 1000) (default 1)
        
        """
        
        raise NotImplementedError
        
    def rematrix_maxval(self, *args, **kwargs):
        """
        <float> ....A...... set rematrix maxval (from 0 to 1000) (default 0)
        
        """
        
        raise NotImplementedError
        
    def swr_flags(self, *args, **kwargs):
        """
        <flags> ....A...... set flags (default 0)
        
        res                          ....A...... force resampling
        """
        
        raise NotImplementedError
        
    def dither_scale(self, *args, **kwargs):
        """
        <float> ....A...... set dither scale (from 0 to INT_MAX) (default 1)
        
        """
        
        raise NotImplementedError
        
    def dither_method(self, *args, **kwargs):
        """
        <int> ....A...... set dither method (from 0 to 71) (default 0)
        
        rectangular     1            ....A...... select rectangular dither
        triangular      2            ....A...... select triangular dither
        triangular_hp   3            ....A...... select triangular dither with high pass
        lipshitz        65           ....A...... select Lipshitz noise shaping dither
        shibata         69           ....A...... select Shibata noise shaping dither
        low_shibata     70           ....A...... select low Shibata noise shaping dither
        high_shibata    71           ....A...... select high Shibata noise shaping dither
        f_weighted      66           ....A...... select f-weighted noise shaping dither
        modified_e_weighted 67           ....A...... select modified-e-weighted noise shaping dither
        improved_e_weighted 68           ....A...... select improved-e-weighted noise shaping dither
        """
        
        raise NotImplementedError
        
    def filter_size(self, *args, **kwargs):
        """
        <int> ....A...... set swr resampling filter size (from 0 to INT_MAX) (default 32)
        
        """
        
        raise NotImplementedError
        
    def phase_shift(self, *args, **kwargs):
        """
        <int> ....A...... set swr resampling phase shift (from 0 to 24) (default 10)
        
        """
        
        raise NotImplementedError
        
    def linear_interp(self, *args, **kwargs):
        """
        <boolean> ....A...... enable linear interpolation (default true)
        
        """
        
        raise NotImplementedError
        
    def exact_rational(self, *args, **kwargs):
        """
        <boolean> ....A...... enable exact rational (default true)
        
        """
        
        raise NotImplementedError
        
    def resample_cutoff(self, *args, **kwargs):
        """
        <double> ....A...... set cutoff frequency ratio (from 0 to 1) (default 0)
        
        """
        
        raise NotImplementedError
        
    def resampler(self, *args, **kwargs):
        """
        <int> ....A...... set resampling Engine (from 0 to 1) (default swr)
        
        swr             0            ....A...... select SW Resampler
        soxr            1            ....A...... select SoX Resampler
        """
        
        raise NotImplementedError
        
    def precision(self, *args, **kwargs):
        """
        <double> ....A...... set soxr resampling precision (in bits) (from 15 to 33) (default 20)
        
        """
        
        raise NotImplementedError
        
    def cheby(self, *args, **kwargs):
        """
        <boolean> ....A...... enable soxr Chebyshev passband & higher-precision irrational ratio approximation (default false)
        
        """
        
        raise NotImplementedError
        
    def min_comp(self, *args, **kwargs):
        """
        <float> ....A...... set minimum difference between timestamps and audio data (in seconds) below which no timestamp compensation of either kind is applied (from 0 to FLT_MAX) (default FLT_MAX)
        
        """
        
        raise NotImplementedError
        
    def min_hard_comp(self, *args, **kwargs):
        """
        <float> ....A...... set minimum difference between timestamps and audio data (in seconds) to trigger padding/trimming the data. (from 0 to INT_MAX) (default 0.1)
        
        """
        
        raise NotImplementedError
        
    def comp_duration(self, *args, **kwargs):
        """
        <float> ....A...... set duration (in seconds) over which data is stretched/squeezed to make it match the timestamps. (from 0 to INT_MAX) (default 1)
        
        """
        
        raise NotImplementedError
        
    def max_soft_comp(self, *args, **kwargs):
        """
        <float> ....A...... set maximum factor by which data is stretched/squeezed to make it match the timestamps. (from INT_MIN to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def first_pts(self, *args, **kwargs):
        """
        <int64> ....A...... Assume the first pts should be this value (in samples). (from I64_MIN to I64_MAX) (default I64_MIN)
        
        """
        
        raise NotImplementedError
        
    def matrix_encoding(self, *args, **kwargs):
        """
        <int> ....A...... set matrixed stereo encoding (from 0 to 6) (default none)
        
        none            0            ....A...... select none
        dolby           1            ....A...... select Dolby
        dplii           2            ....A...... select Dolby Pro Logic II
        """
        
        raise NotImplementedError
        
    def filter_type(self, *args, **kwargs):
        """
        <int> ....A...... select swr filter type (from 0 to 2) (default kaiser)
        
        cubic           0            ....A...... select cubic
        blackman_nuttall 1            ....A...... select Blackman Nuttall windowed sinc
        kaiser          2            ....A...... select Kaiser windowed sinc
        """
        
        raise NotImplementedError
        
    def kaiser_beta(self, *args, **kwargs):
        """
        <double> ....A...... set swr Kaiser window beta (from 2 to 16) (default 9)
        
        """
        
        raise NotImplementedError
        
    def output_sample_bits(self, *args, **kwargs):
        """
        <int> ....A...... set swr number of output sample bits (from 0 to 64) (default 0)
        
        """
        
        raise NotImplementedError
        
    def amount(self, *args, **kwargs):
        """
        <string> ...VA...B..
        
        """
        
        raise NotImplementedError
        
    def dropamount(self, *args, **kwargs):
        """
        <int> ...VA...B.. (from 0 to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def tilt(self, *args, **kwargs):
        """
        <int> ...V....... Tilt the video horizontally while shifting (from 0 to 1) (default 1)
        
        """
        
        raise NotImplementedError
        
    def hold(self, *args, **kwargs):
        """
        <int> ...V....... Number of columns to hold at the start of the video (from 0 to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def pad(self, *args, **kwargs):
        """
        <int> ...V....... Number of columns to pad at the end of the video (from 0 to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def td(self, *args, **kwargs):
        """
        <int> ...V....B.. Temporal Delimiter OBU (from 0 to 2) (default pass)
        
        pass            0            ...V....B..
        insert          1            ...V....B..
        remove          2            ...V....B..
        """
        
        raise NotImplementedError
        
    def transfer_characteristics(self, *args, **kwargs):
        """
        <int> ...V....B.. Set transfer characteristics (section 6.4.2) (from -1 to 255) (default -1)
        
        """
        
        raise NotImplementedError
        
    def matrix_coefficients(self, *args, **kwargs):
        """
        <int> ...V....B.. Set matrix coefficients (section 6.4.2) (from -1 to 255) (default -1)
        
        """
        
        raise NotImplementedError
        
    def chroma_sample_position(self, *args, **kwargs):
        """
        <int> ...V....B.. Set chroma sample position (section 6.4.2) (from -1 to 3) (default -1)
        
        unknown         0            ...V....B.. Unknown chroma sample position
        vertical        1            ...V....B.. Left chroma sample position
        colocated       2            ...V....B.. Top-left chroma sample position
        """
        
        raise NotImplementedError
        
    def tick_rate(self, *args, **kwargs):
        """
        <rational> ...V....B.. Set display tick rate (time_scale / num_units_in_display_tick) (from 0 to UINT32_MAX) (default 0/1)
        
        """
        
        raise NotImplementedError
        
    def num_ticks_per_picture(self, *args, **kwargs):
        """
        <int> ...V....B.. Set display ticks per picture for CFR streams (from -1 to INT_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def delete_padding(self, *args, **kwargs):
        """
        <boolean> ...V....B.. Delete all Padding OBUs (default false)
        
        """
        
        raise NotImplementedError
        
    def color(self, *args, **kwargs):
        """
        <color> ...V....B.. set color (default "yellow")
        
        """
        
        raise NotImplementedError
        
    def sta(self, *args, **kwargs):
        """
        <flags> ...V....B.. specify which error status value to match (default Aa+Ba+Ca+erri+erru+err+Ab+Bb+Cb+A+B+C+a+b+res+notok+notres)
        
        ok                           ...V....B.. No error, no concealment
        Aa                           ...V....B.. No error, concealment from previous frame type a
        Ba                           ...V....B.. No error, concealment from next frame type a
        Ca                           ...V....B.. No error, unspecified concealment type a
        erri                         ...V....B.. Error with inserted code, No concealment
        erru                         ...V....B.. Error with unidentified pos, No concealment
        err                          ...V....B.. Error, No concealment
        Ab                           ...V....B.. No error, concealment from previous frame type b
        Bb                           ...V....B.. No error, concealment from next frame type b
        Cb                           ...V....B.. No error, unspecified concealment type b
        A                            ...V....B.. No error, concealment from previous frame
        B                            ...V....B.. No error, concealment from next frame
        C                            ...V....B.. No error, unspecified concealment
        a                            ...V....B.. No error, concealment type a
        b                            ...V....B.. No error, concealment type b
        res                          ...V....B.. Reserved
        notok                        ...V....B.. Error or concealment
        notres                       ...V....B.. Not reserved
        """
        
        raise NotImplementedError
        
    def pass_types(self, *args, **kwargs):
        """
        <string> ...V....B.. List of unit types to pass through the filter.
        
        """
        
        raise NotImplementedError
        
    def remove_types(self, *args, **kwargs):
        """
        <string> ...V....B.. List of unit types to remove in the filter.
        
        """
        
        raise NotImplementedError
        
    def discard_flags(self, *args, **kwargs):
        """
        <flags> ...V....B.. flags to control the discard frame behavior (default 0)
        
        keep_non_vcl                 ...V....B.. non-vcl units even if the picture has been dropped
        """
        
        raise NotImplementedError
        
    def sample_aspect_ratio(self, *args, **kwargs):
        """
        <rational> ...V....B.. Set sample aspect ratio (table E-1) (from 0 to 65535) (default 0/1)
        
        """
        
        raise NotImplementedError
        
    def overscan_appropriate_flag(self, *args, **kwargs):
        """
        <int> ...V....B.. Set VUI overscan appropriate flag (from -1 to 1) (default -1)
        
        """
        
        raise NotImplementedError
        
    def video_full_range_flag(self, *args, **kwargs):
        """
        <int> ...V....B.. Set video full range flag (from -1 to 1) (default -1)
        
        """
        
        raise NotImplementedError
        
    def colour_primaries(self, *args, **kwargs):
        """
        <int> ...V....B.. Set colour primaries (table E-3) (from -1 to 255) (default -1)
        
        """
        
        raise NotImplementedError
        
    def chroma_sample_loc_type(self, *args, **kwargs):
        """
        <int> ...V....B.. Set chroma sample location type (figure E-1) (from -1 to 5) (default -1)
        
        """
        
        raise NotImplementedError
        
    def fixed_frame_rate_flag(self, *args, **kwargs):
        """
        <int> ...V....B.. Set VUI fixed frame rate flag (from -1 to 1) (default -1)
        
        """
        
        raise NotImplementedError
        
    def zero_new_constraint_set_flags(self, *args, **kwargs):
        """
        <boolean> ...V....B.. Set constraint_set4_flag / constraint_set5_flag to zero (default false)
        
        """
        
        raise NotImplementedError
        
    def crop_left(self, *args, **kwargs):
        """
        <int> ...V....B.. Set left border crop offset (from -1 to 16880) (default -1)
        
        """
        
        raise NotImplementedError
        
    def crop_right(self, *args, **kwargs):
        """
        <int> ...V....B.. Set right border crop offset (from -1 to 16880) (default -1)
        
        """
        
        raise NotImplementedError
        
    def crop_top(self, *args, **kwargs):
        """
        <int> ...V....B.. Set top border crop offset (from -1 to 16880) (default -1)
        
        """
        
        raise NotImplementedError
        
    def crop_bottom(self, *args, **kwargs):
        """
        <int> ...V....B.. Set bottom border crop offset (from -1 to 16880) (default -1)
        
        """
        
        raise NotImplementedError
        
    def sei_user_data(self, *args, **kwargs):
        """
        <string> ...V....B.. Insert SEI user data (UUID+string)
        
        """
        
        raise NotImplementedError
        
    def delete_filler(self, *args, **kwargs):
        """
        <int> ...V....B.. Delete all filler (both NAL and SEI) (from 0 to 1) (default 0)
        
        """
        
        raise NotImplementedError
        
    def display_orientation(self, *args, **kwargs):
        """
        <int> ...V....B.. Display orientation SEI (from 0 to 3) (default pass)
        
        pass            0            ...V....B..
        insert          1            ...V....B..
        remove          2            ...V....B..
        extract         3            ...V....B..
        """
        
        raise NotImplementedError
        
    def rotate(self, *args, **kwargs):
        """
        <double> ...V....B.. Set rotation in display orientation SEI (anticlockwise angle in degrees) (from -360 to 360) (default nan)
        
        """
        
        raise NotImplementedError
        
    def flip(self, *args, **kwargs):
        """
        <flags> ...V....B.. Set flip in display orientation SEI (default 0)
        
        horizontal                   ...V....B.. Set hor_flip
        vertical                     ...V....B.. Set ver_flip
        """
        
        raise NotImplementedError
        
    def num_ticks_poc_diff_one(self, *args, **kwargs):
        """
        <int> ...V....B.. Set VPS and VUI number of ticks per POC increment (from -1 to INT_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def display_aspect_ratio(self, *args, **kwargs):
        """
        <rational> ...V....B.. Set display aspect ratio (table 6-3) (from 0 to 65535) (default 0/1)
        
        """
        
        raise NotImplementedError
        
    def nb_out_samples(self, *args, **kwargs):
        """
        <int> ....A...B.. set the number of per-packet output samples (from 1 to INT_MAX) (default 1024)
        
        """
        
        raise NotImplementedError
        
    def p(self, *args, **kwargs):
        """
        <boolean> ....A...B.. pad last packet with zeros (default true)
        
        """
        
        raise NotImplementedError
        
    def pts(self, *args, **kwargs):
        """
        <string> ...VAS..B.. set expression for packet PTS
        
        """
        
        raise NotImplementedError
        
    def dts(self, *args, **kwargs):
        """
        <string> ...VAS..B.. set expression for packet DTS
        
        """
        
        raise NotImplementedError
        
    def duration(self, *args, **kwargs):
        """
        <string> ...VAS..B.. set expression for packet duration (default "DURATION")
        
        """
        
        raise NotImplementedError
        
    def color_space(self, *args, **kwargs):
        """
        <int> ...V....B.. Set colour space (section 7.2.2) (from -1 to 7) (default -1)
        
        unknown         0            ...V....B.. Unknown/unspecified
        bt601           1            ...V....B.. ITU-R BT.601-7
        bt709           2            ...V....B.. ITU-R BT.709-6
        smpte170        3            ...V....B.. SMPTE-170
        smpte240        4            ...V....B.. SMPTE-240
        bt2020          5            ...V....B.. ITU-R BT.2020-2
        rgb             7            ...V....B.. sRGB / IEC 61966-2-1
        """
        
        raise NotImplementedError
        

