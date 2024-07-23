#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author  : nickdecodes
@Email   : nickdecodes@163.com
@Usage   :
@FileName: ffprobe_options.py
@DateTime: 2024-07-22 17:10
@SoftWare: 
"""


from .meta import OptionMeta
from .exec import CommandExecutor


class FFProbeOptions(CommandExecutor, metaclass=OptionMeta):
    """
    https://ffmpeg.org/ffprobe.html
    """
    options = [
        '-L',  # show license
        '-h',  # <topic> show help
        '-help',  # <topic> show help
        '-version',  # show version
        '-buildconf',  # show build configuration
        '-formats',  # show available formats
        '-muxers',  # show available muxers
        '-demuxers',  # show available demuxers
        '-devices',  # show available devices
        '-codecs',  # show available codecs
        '-decoders',  # show available decoders
        '-encoders',  # show available encoders
        '-bsfs',  # show available bit stream filters
        '-protocols',  # show available protocols
        '-filters',  # show available filters
        '-pix_fmts',  # show available pixel formats
        '-layouts',  # show standard channel layouts
        '-sample_fmts',  # show available audio sample formats
        '-dispositions',  # show available stream dispositions
        '-colors',  # show available color names
        '-loglevel',  # <loglevel> set logging level
        '-v',  # <loglevel> set logging level
        '-report',  # generate a report
        '-max_alloc',  # <bytes> set maximum size of a single allocated block
        '-cpuflags',  # <flags> force specific cpu flags
        '-cpucount',  # <count> force specific cpu count
        '-hide_banner',  # <hide_banner> do not show program banner
        '-sources',  # <device> list sources of the input device
        '-sinks',  # <device> list sinks of the output device
        '-f',  # <format> force format
        '-unit',  # show unit of the displayed values
        '-prefix',  # use SI prefixes for the displayed values
        '-byte_binary_prefix',  # use binary prefixes for byte units
        '-sexagesimal',  # use sexagesimal format HOURS:MM:SS.MICROSECONDS for time units
        '-pretty',  # prettify the format of displayed values, make it more human readable
        '-output_format',  # <format> set the output printing format (available formats are: default, compact, csv, flat, ini, json, xml)
        '-print_format',  # alias for -output_format (deprecated)
        '-of',  # <format> alias for -output_format
        '-select_streams',  # <stream_specifier> select the specified streams
        '-sections',  # print sections structure and section information, and exit
        '-show_data',  # show packets data
        '-show_data_hash',  # show packets data hash
        '-show_error',  # show probing error
        '-show_format',  # show format/container info
        '-show_frames',  # show frames info
        '-show_entries',  # <entry_list> show a set of specified entries
        '-show_log',  # show log
        '-show_packets',  # show packets info
        '-show_programs',  # show programs info
        '-show_stream_groups',  # show stream groups info
        '-show_streams',  # show streams info
        '-show_chapters',  # show chapters info
        '-count_frames',  # count the number of frames per stream
        '-count_packets',  # count the number of packets per stream
        '-show_program_version',  # show ffprobe version
        '-show_library_versions',  # show library versions
        '-show_versions',  # show program and library versions
        '-show_pixel_formats',  # show pixel format descriptions
        '-show_optional_fields',  # show optional fields
        '-show_private_data',  # show private data
        '-private',  # same as show_private_data
        '-bitexact',  # force bitexact output
        '-read_intervals',  # <read_intervals> set read intervals
        '-i',  # <input_file> read specified file
        '-o',  # <output_file> write to specified output
        '-print_filename',  # <print_file> override the printed input filename
        '-find_stream_info',  # read and decode the streams to fill missing information with heuristics
        '-avioflags',  # <flags> ED......... (default 0)
        '-probesize',  # <int64> .D......... set probing size (from 32 to I64_MAX) (default 5000000)
        '-formatprobesize',  # <int> .D......... number of bytes to probe file format (from 0 to 2.14748e+09) (default 1048576)
        '-fflags',  # <flags> ED......... (default autobsf)
        '-seek2any',  # <boolean> .D......... allow seeking to non-keyframes on demuxer level when supported (default false)
        '-analyzeduration',  # <int64> .D......... specify how many microseconds are analyzed to probe the input (from 0 to I64_MAX) (default 0)
        '-cryptokey',  # <binary> .D......... decryption key
        '-indexmem',  # <int> .D......... max memory used for timestamp index (per stream) (from 0 to INT_MAX) (default 1048576)
        '-rtbufsize',  # <int> .D......... max memory used for buffering real-time frames (from 0 to INT_MAX) (default 3041280)
        '-fdebug',  # <flags> ED......... print specific debug info (default 0)
        '-max_delay',  # <int> ED......... maximum muxing or demuxing delay in microseconds (from -1 to INT_MAX) (default -1)
        '-fpsprobesize',  # <int> .D......... number of frames used to probe fps (from -1 to 2.14748e+09) (default -1)
        '-f_err_detect',  # <flags> .D......... set error detection flags (deprecated; use err_detect, save via avconv) (default crccheck)
        '-err_detect',  # <flags> .D......... set error detection flags (default crccheck)
        '-use_wallclock_as_timestamps',  # <boolean> .D......... use wallclock as timestamps (default false)
        '-skip_initial_bytes',  # <int64> .D......... set number of bytes to skip before reading header and frames (from 0 to I64_MAX) (default 0)
        '-correct_ts_overflow',  # <boolean> .D......... correct single timestamp overflows (default true)
        '-f_strict',  # <int> ED......... how strictly to follow the standards (deprecated; use strict, save via avconv) (from INT_MIN to INT_MAX) (default normal)
        '-strict',  # <int> ED......... how strictly to follow the standards (from INT_MIN to INT_MAX) (default normal)
        '-max_ts_probe',  # <int> .D......... maximum number of packets to read while waiting for the first timestamp (from 0 to INT_MAX) (default 50)
        '-dump_separator',  # <string> ED......... set information dump field separator (default ", ")
        '-codec_whitelist',  # <string> .D......... List of decoders that are allowed to be used
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
        '-follow',  # <int> .D......... Follow a file as it is being written (from 0 to 1) (default 0)
        '-seekable',  # <int> ED......... Sets if the file is seekable (from -1 to 0) (default -1)
        '-timeout',  # <int> ED......... set timeout of socket I/O operations (from -1 to INT_MAX) (default -1)
        '-ftp_anonymous_password',  # <string> ED......... password for anonymous login. E-mail address should be used.
        '-ftp_user',  # <string> ED......... user for FTP login. Overridden by whatever is in the URL.
        '-ftp_password',  # <string> ED......... password for FTP login. Overridden by whatever is in the URL.
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
        '-short_seek_size',  # <int> .D......... Threshold to favor readahead over seek. (from 0 to INT_MAX) (default 0)
        '-rtmp_app',  # <string> ED......... Name of application to connect to on the RTMP server
        '-rtmp_buffer',  # <int> ED......... Set buffer time in milliseconds. The default is 3000. (from 0 to INT_MAX) (default 3000)
        '-rtmp_conn',  # <string> ED......... Append arbitrary AMF data to the Connect message
        '-rtmp_flashver',  # <string> ED......... Version of the Flash plugin used to run the SWF player.
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
        '-ttl',  # <int> ED......... Time to live (multicast only) (from -1 to 255) (default -1)
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
        '-localport',  # <int> ED......... Local port (from -1 to INT_MAX) (default -1)
        '-udplite_coverage',  # <int> ED......... choose UDPLite head size which should be validated by checksum (from 0 to INT_MAX) (default 0)
        '-reuse',  # <boolean> ED......... explicitly allow reusing UDP sockets (default auto)
        '-reuse_socket',  # <boolean> ED......... explicitly allow reusing UDP sockets (default auto)
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
        '-streamid',  # <string> ED......... A string of up to 512 characters that an Initiator can pass to a Responder
        '-srt_streamid',  # <string> ED......... A string of up to 512 characters that an Initiator can pass to a Responder
        '-smoother',  # <string> ED......... The type of Smoother used for the transmission for that socket
        '-messageapi',  # <boolean> ED......... Enable message API (default auto)
        '-transtype',  # <int> ED......... The transmission type for the socket (from 0 to 2) (default 2)
        '-linger',  # <int> ED......... Number of seconds that the socket waits for unsent data when closing (from -1 to INT_MAX) (default -1)
        '-tsbpd',  # <boolean> ED......... Timestamp-based packet delivery (default auto)
        '-private_key',  # <string> ED......... set path to private key
        '-gateway',  # <string> .D......... The gateway to ask for IPFS data.
        '-initial_pause',  # <boolean> .D......... do not start playing the stream immediately (default false)
        '-rtsp_transport',  # <flags> ED......... set RTSP transport protocols (default 0)
        '-rtsp_flags',  # <flags> .D......... set RTSP flags (default 0)
        '-allowed_media_types',  # <flags> .D......... set media types to accept from the server (default video+audio+data+subtitle)
        '-min_port',  # <int> ED......... set minimum local UDP port (from 0 to 65535) (default 5000)
        '-max_port',  # <int> ED......... set maximum local UDP port (from 0 to 65535) (default 65000)
        '-reorder_queue_size',  # <int> .D......... set number of packets to buffer for handling of reordered packets (from -1 to INT_MAX) (default -1)
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
        '-frames_per_packet',  # <int> .D......... Number of frames to read at a time. Higher = faster decoding, lower granularity (from 1 to INT_MAX) (default 1)
        '-safe',  # <boolean> .D......... enable safe mode (default true)
        '-auto_convert',  # <boolean> .D......... automatically convert bitstream format (default true)
        '-segment_time_metadata',  # <boolean> .D......... output file segment start time and duration as packet metadata (default false)
        '-allowed_extensions',  # <string> .D......... List of file extensions that dash is allowed to access (default "aac,m4a,m4s,m4v,mov,mp4,webm,ts")
        '-cenc_decryption_key',  # <string> .D......... Media decryption key (hex)
        '-ch_layout',  # <channel_layout> .D......... (default "mono")
        '-flv_metadata',  # <boolean> .D.V....... Allocate streams according to the onMetaData array (default false)
        '-flv_full_metadata',  # <boolean> .D.V....... Dump full metadata of the onMetadata (default false)
        '-flv_ignore_prevtag',  # <boolean> .D.V....... Ignore the Size of previous tag (default false)
        '-missing_streams',  # <int> .D.V..XR... (from 0 to 255) (default 0)
        '-code_size',  # <int> .D......... Bits per G.726 code (from 2 to 5) (default 4)
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
        '-http_persistent',  # <boolean> .D......... Use persistent HTTP connections (default true)
        '-http_multiple',  # <boolean> .D......... Use multiple HTTP connections for fetching segments (default auto)
        '-http_seekable',  # <boolean> .D......... Use HTTP partial requests, 0 = disable, 1 = enable, -1 = auto (default auto)
        '-seg_format_options',  # <dictionary> .D......... Set options for segment demuxer
        '-seg_max_retry',  # <int> .D......... Maximum number of times to reload a segment on error. (from 0 to INT_MAX) (default 0)
        '-pattern_type',  # <int> .D......... set pattern type (from 0 to INT_MAX) (default 4)
        '-start_number',  # <int> .D......... set first number in the sequence (from INT_MIN to INT_MAX) (default 0)
        '-start_number_range',  # <int> .D......... set range for looking at the first sequence number (from 1 to INT_MAX) (default 5)
        '-ts_from_file',  # <int> .D......... set frame timestamp from file's one (from 0 to 2) (default none)
        '-export_path_metadata',  # <boolean> .D......... enable metadata containing input path information (default false)
        '-loop',  # <boolean> .D......... force loop over input file sequence (default false)
        '-frame_size',  # <int> .D......... force frame size in bytes (from 0 to INT_MAX) (default 0)
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
        '-live',  # <boolean> .D......... flag indicating that the input is a live file that only has the headers. (default false)
        '-bandwidth',  # <int> .D......... bandwidth of this stream to be specified in the DASH manifest. (from 0 to INT_MAX) (default 0)
        '-list_devices',  # <boolean> .D......... list available devices (default false)
        '-video_device_index',  # <int> .D......... select video device by index for devices with same name (starts at 0) (from -1 to INT_MAX) (default -1)
        '-audio_device_index',  # <int> .D......... select audio device by index for devices with same name (starts at 0) (from -1 to INT_MAX) (default -1)
        '-capture_cursor',  # <boolean> .D......... capture the screen cursor (default false)
        '-capture_mouse_clicks',  # <boolean> .D......... capture the screen mouse clicks (default false)
        '-capture_raw_data',  # <boolean> .D......... capture the raw data from device connection (default false)
        '-drop_late_frames',  # <boolean> .D......... drop frames that are available later than expected (default true)
        '-graph',  # <string> .D......... set libavfilter graph
        '-graph_file',  # <string> .D......... set libavfilter graph filename
        '-dumpgraph',  # <string> .D......... dump graph to stderr
        '-window_id',  # <int> .D......... Window to capture. (from 0 to UINT32_MAX) (default 0)
        '-x',  # <int> .D......... Initial x coordinate. (from 0 to INT_MAX) (default 0)
        '-y',  # <int> .D......... Initial y coordinate. (from 0 to INT_MAX) (default 0)
        '-grab_x',  # <int> .D......... Initial x coordinate. (from 0 to INT_MAX) (default 0)
        '-grab_y',  # <int> .D......... Initial y coordinate. (from 0 to INT_MAX) (default 0)
        '-draw_mouse',  # <int> .D......... Draw the mouse pointer. (from 0 to 1) (default 1)
        '-follow_mouse',  # <int> .D......... Move the grabbing region when the mouse pointer reaches within specified amount of pixels to the edge of region. (from -1 to INT_MAX) (default 0)
        '-show_region',  # <int> .D......... Show the grabbing region. (from 0 to 1) (default 0)
        '-region_border',  # <int> .D......... Set the region border thickness. (from 1 to 128) (default 3)
        '-select_region',  # <boolean> .D......... Select the grabbing region graphically using the pointer. (default false)
        '-flags',  # <flags> ED.VAS..... (default 0)
        '-flags2',  # <flags> ED.VAS..... (default 0)
        '-export_side_data',  # <flags> ED.VAS..... Export metadata as side data (default 0)
        '-ar',  # <int> ED..A...... set audio sampling rate (in Hz) (from 0 to INT_MAX) (default 0)
        '-bug',  # <flags> .D.V....... work around not autodetected encoder bugs (default autodetect)
        '-idct',  # <int> ED.V....... select IDCT implementation (from 0 to INT_MAX) (default auto)
        '-ec',  # <flags> .D.V....... set error concealment strategy (default guess_mvs+deblock)
        '-debug',  # <flags> ED.VAS..... print specific debug info (default 0)
        '-threads',  # <int> ED.VA...... set the number of threads (from 0 to INT_MAX) (default 1)
        '-skip_top',  # <int> .D.V....... number of macroblock rows at the top which are skipped (from INT_MIN to INT_MAX) (default 0)
        '-skip_bottom',  # <int> .D.V....... number of macroblock rows at the bottom which are skipped (from INT_MIN to INT_MAX) (default 0)
        '-lowres',  # <int> .D.VA...... decode at 1= 1/2, 2=1/4, 3=1/8 resolutions (from 0 to INT_MAX) (default 0)
        '-skip_loop_filter',  # <int> .D.V....... skip loop filtering process for the selected frames (from INT_MIN to INT_MAX) (default default)
        '-skip_idct',  # <int> .D.V....... skip IDCT/dequantization for the selected frames (from INT_MIN to INT_MAX) (default default)
        '-skip_frame',  # <int> .D.V....... skip decoding for the selected frames (from INT_MIN to INT_MAX) (default default)
        '-ticks_per_frame',  # <int> ED.VA...... (from 1 to INT_MAX) (default 1)
        '-color_primaries',  # <int> ED.V....... color primaries (from 1 to INT_MAX) (default unknown)
        '-color_trc',  # <int> ED.V....... color transfer characteristics (from 1 to INT_MAX) (default unknown)
        '-colorspace',  # <int> ED.V....... color space (from 0 to INT_MAX) (default unknown)
        '-color_range',  # <int> ED.V....... color range (from 0 to INT_MAX) (default unknown)
        '-chroma_sample_location',  # <int> ED.V....... chroma sample location (from 0 to INT_MAX) (default unknown)
        '-thread_type',  # <flags> ED.VA...... select multithreading type (default slice+frame)
        '-request_sample_fmt',  # <sample_fmt> .D..A...... sample format audio decoders should prefer (default none)
        '-sub_charenc',  # <string> .D...S..... set input text subtitles character encoding
        '-sub_charenc_mode',  # <flags> .D...S..... set input text subtitles character encoding mode (default 0)
        '-apply_cropping',  # <boolean> .D.V....... (default true)
        '-skip_alpha',  # <boolean> .D.V....... Skip processing alpha (default false)
        '-field_order',  # <int> ED.V....... Field order (from 0 to 5) (default 0)
        '-max_pixels',  # <int64> ED.VAS..... Maximum number of pixels (from 0 to INT_MAX) (default INT_MAX)
        '-max_samples',  # <int64> ED..A...... Maximum number of samples (from 0 to INT_MAX) (default INT_MAX)
        '-hwaccel_flags',  # <flags> .D.V....... (default ignore_level)
        '-extra_hw_frames',  # <int> .D.V....... Number of extra hardware frames to allocate for the user (from -1 to INT_MAX) (default -1)
        '-discard_damaged_percentage',  # <int> .D.V....... Percentage of damaged samples to discard a frame (from 0 to 100) (default 95)
        '-side_data_prefer_packet',  # [<int> ].D.VAS..... Comma-separated list of side data types for which user-supplied (container) data is preferred over coded bytestream
        '-layer',  # <string> .D.V....... Set the decoding layer (default "")
        '-part',  # <int> .D.V....... Set the decoding part (from 0 to INT_MAX) (default 0)
        '-gamma',  # <float> .D.V....... Set the float gamma value when decoding (from 0.001 to FLT_MAX) (default 1)
        '-apply_trc',  # <int> .D.V....... color transfer characteristics to apply to EXR linear input (from 1 to 18) (default gamma)
        '-is_avc',  # <boolean> .D.V..X.... is avc (default false)
        '-nal_length_size',  # <int> .D.V..X.... nal_length_size (from 0 to 4) (default 0)
        '-enable_er',  # <boolean> .D.V....... Enable error resilience on damaged frames (unsafe) (default auto)
        '-x264_build',  # <int> .D.V....... Assume this x264 version if no x264 version found in any SEI (from -1 to INT_MAX) (default -1)
        '-skip_gray',  # <boolean> .D.V....... Do not return gray gap frames (default false)
        '-noref_gray',  # <boolean> .D.V....... Avoid using gray gap frames as references (default true)
        '-apply_defdispwin',  # <boolean> .D.V....... Apply default display window from VUI (default false)
        '-strict_displaywin',  # <boolean> .D.V....... stricly apply default display window size (default false)
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
        '-palette',  # <string> .D...S..... set the global palette
        '-ifo_palette',  # <string> .D...S..... obtain the global palette from .IFO file
        '-forced_subs_only',  # <boolean> .D...S..... Only show forced subtitles (default false)
        '-width',  # <int> .D...S..... Frame width, usually video width (from 0 to INT_MAX) (default 0)
        '-height',  # <int> .D...S..... Frame height, usually video height (from 0 to INT_MAX) (default 0)
        '-keep_ass_markup',  # <boolean> .D...S..... Set if ASS tags must be escaped (default false)
        '-aribb24_base_path',  # <string> .D...S..... set the base path for the libaribb24 library
        '-aribb24_skip_ruby_text',  # <boolean> .D...S..... skip ruby text blocks during decoding (default true)
        '-default_profile',  # <int> .D...S..... default profile to use if not specified in the stream parameters (from -99 to 1) (default -99)
        '-tilethreads',  # <int> .D.V......P Tile threads (from 0 to 256) (default 0)
        '-framethreads',  # <int> .D.V......P Frame threads (from 0 to 256) (default 0)
        '-max_frame_delay',  # <int> .D.V....... Max frame delay (from 0 to 256) (default 0)
        '-filmgrain',  # <boolean> .D.V......P Apply Film Grain (default auto)
        '-oppoint',  # <int> .D.V....... Select an operating point of the scalable bitstream (from -1 to 31) (default -1)
        '-alllayers',  # <boolean> .D.V....... Output all spatial layers (default false)
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def L(self, *args, **kwargs):
        """
        show license
        
        """
        
        raise NotImplementedError
        
    def h(self, *args, **kwargs):
        """
        <topic> show help
        
        """
        
        raise NotImplementedError
        
    def help(self, *args, **kwargs):
        """
        <topic> show help
        
        """
        
        raise NotImplementedError
        
    def version(self, *args, **kwargs):
        """
        show version
        
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
        
    def codecs(self, *args, **kwargs):
        """
        show available codecs
        
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
        
    def loglevel(self, *args, **kwargs):
        """
        <loglevel> set logging level
        
        """
        
        raise NotImplementedError
        
    def v(self, *args, **kwargs):
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
        
    def f(self, *args, **kwargs):
        """
        <format> force format
        
        """
        
        raise NotImplementedError
        
    def unit(self, *args, **kwargs):
        """
        show unit of the displayed values
        
        """
        
        raise NotImplementedError
        
    def prefix(self, *args, **kwargs):
        """
        use SI prefixes for the displayed values
        
        """
        
        raise NotImplementedError
        
    def byte_binary_prefix(self, *args, **kwargs):
        """
        use binary prefixes for byte units
        
        """
        
        raise NotImplementedError
        
    def sexagesimal(self, *args, **kwargs):
        """
        use sexagesimal format HOURS:MM:SS.MICROSECONDS for time units
        
        """
        
        raise NotImplementedError
        
    def pretty(self, *args, **kwargs):
        """
        prettify the format of displayed values, make it more human readable
        
        """
        
        raise NotImplementedError
        
    def output_format(self, *args, **kwargs):
        """
        <format> set the output printing format (available formats are: default, compact, csv, flat, ini, json, xml)
        
        """
        
        raise NotImplementedError
        
    def print_format(self, *args, **kwargs):
        """
        alias for -output_format (deprecated)
        
        """
        
        raise NotImplementedError
        
    def of(self, *args, **kwargs):
        """
        <format> alias for -output_format
        
        """
        
        raise NotImplementedError
        
    def select_streams(self, *args, **kwargs):
        """
        <stream_specifier> select the specified streams
        
        """
        
        raise NotImplementedError
        
    def sections(self, *args, **kwargs):
        """
        print sections structure and section information, and exit
        
        """
        
        raise NotImplementedError
        
    def show_data(self, *args, **kwargs):
        """
        show packets data
        
        """
        
        raise NotImplementedError
        
    def show_data_hash(self, *args, **kwargs):
        """
        show packets data hash
        
        """
        
        raise NotImplementedError
        
    def show_error(self, *args, **kwargs):
        """
        show probing error
        
        """
        
        raise NotImplementedError
        
    def show_format(self, *args, **kwargs):
        """
        show format/container info
        
        """
        
        raise NotImplementedError
        
    def show_frames(self, *args, **kwargs):
        """
        show frames info
        
        """
        
        raise NotImplementedError
        
    def show_entries(self, *args, **kwargs):
        """
        <entry_list> show a set of specified entries
        
        """
        
        raise NotImplementedError
        
    def show_log(self, *args, **kwargs):
        """
        show log
        
        """
        
        raise NotImplementedError
        
    def show_packets(self, *args, **kwargs):
        """
        show packets info
        
        """
        
        raise NotImplementedError
        
    def show_programs(self, *args, **kwargs):
        """
        show programs info
        
        """
        
        raise NotImplementedError
        
    def show_stream_groups(self, *args, **kwargs):
        """
        show stream groups info
        
        """
        
        raise NotImplementedError
        
    def show_streams(self, *args, **kwargs):
        """
        show streams info
        
        """
        
        raise NotImplementedError
        
    def show_chapters(self, *args, **kwargs):
        """
        show chapters info
        
        """
        
        raise NotImplementedError
        
    def count_frames(self, *args, **kwargs):
        """
        count the number of frames per stream
        
        """
        
        raise NotImplementedError
        
    def count_packets(self, *args, **kwargs):
        """
        count the number of packets per stream
        
        """
        
        raise NotImplementedError
        
    def show_program_version(self, *args, **kwargs):
        """
        show ffprobe version
        
        """
        
        raise NotImplementedError
        
    def show_library_versions(self, *args, **kwargs):
        """
        show library versions
        
        """
        
        raise NotImplementedError
        
    def show_versions(self, *args, **kwargs):
        """
        show program and library versions
        
        """
        
        raise NotImplementedError
        
    def show_pixel_formats(self, *args, **kwargs):
        """
        show pixel format descriptions
        
        """
        
        raise NotImplementedError
        
    def show_optional_fields(self, *args, **kwargs):
        """
        show optional fields
        
        """
        
        raise NotImplementedError
        
    def show_private_data(self, *args, **kwargs):
        """
        show private data
        
        """
        
        raise NotImplementedError
        
    def private(self, *args, **kwargs):
        """
        same as show_private_data
        
        """
        
        raise NotImplementedError
        
    def bitexact(self, *args, **kwargs):
        """
        force bitexact output
        
        """
        
        raise NotImplementedError
        
    def read_intervals(self, *args, **kwargs):
        """
        <read_intervals> set read intervals
        
        """
        
        raise NotImplementedError
        
    def i(self, *args, **kwargs):
        """
        <input_file> read specified file
        
        """
        
        raise NotImplementedError
        
    def o(self, *args, **kwargs):
        """
        <output_file> write to specified output
        
        """
        
        raise NotImplementedError
        
    def print_filename(self, *args, **kwargs):
        """
        <print_file> override the printed input filename
        
        """
        
        raise NotImplementedError
        
    def find_stream_info(self, *args, **kwargs):
        """
        read and decode the streams to fill missing information with heuristics
        
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
        
    def fflags(self, *args, **kwargs):
        """
        <flags> ED......... (default autobsf)
        
        ignidx                       .D......... ignore index
        genpts                       .D......... generate pts
        nofillin                     .D......... do not fill in missing values that can be exactly calculated
        noparse                      .D......... disable AVParsers, this needs nofillin too
        igndts                       .D......... ignore dts
        discardcorrupt               .D......... discard corrupted frames
        sortdts                      .D......... try to interleave outputted packets by dts
        fastseek                     .D......... fast but inaccurate seeks
        nobuffer                     .D......... reduce the latency introduced by optional buffering
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
        
    def fpsprobesize(self, *args, **kwargs):
        """
        <int> .D......... number of frames used to probe fps (from -1 to 2.14748e+09) (default -1)
        
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
        
    def err_detect(self, *args, **kwargs):
        """
        <flags> .D......... set error detection flags (default crccheck)
        
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
        
    def strict(self, *args, **kwargs):
        """
        <int> ED......... how strictly to follow the standards (from INT_MIN to INT_MAX) (default normal)
        
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
        
    def dump_separator(self, *args, **kwargs):
        """
        <string> ED......... set information dump field separator (default ", ")
        
        """
        
        raise NotImplementedError
        
    def codec_whitelist(self, *args, **kwargs):
        """
        <string> .D......... List of decoders that are allowed to be used
        
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
        
    def ftp_anonymous_password(self, *args, **kwargs):
        """
        <string> ED......... password for anonymous login. E-mail address should be used.
        
        """
        
        raise NotImplementedError
        
    def ftp_user(self, *args, **kwargs):
        """
        <string> ED......... user for FTP login. Overridden by whatever is in the URL.
        
        """
        
        raise NotImplementedError
        
    def ftp_password(self, *args, **kwargs):
        """
        <string> ED......... password for FTP login. Overridden by whatever is in the URL.
        
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
        
    def short_seek_size(self, *args, **kwargs):
        """
        <int> .D......... Threshold to favor readahead over seek. (from 0 to INT_MAX) (default 0)
        
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
        
    def ttl(self, *args, **kwargs):
        """
        <int> ED......... Time to live (multicast only) (from -1 to 255) (default -1)
        
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
        
    def streamid(self, *args, **kwargs):
        """
        <string> ED......... A string of up to 512 characters that an Initiator can pass to a Responder
        
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
        
    def frames_per_packet(self, *args, **kwargs):
        """
        <int> .D......... Number of frames to read at a time. Higher = faster decoding, lower granularity (from 1 to INT_MAX) (default 1)
        
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
        
    def ch_layout(self, *args, **kwargs):
        """
        <channel_layout> .D......... (default "mono")
        
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
        
    def code_size(self, *args, **kwargs):
        """
        <int> .D......... Bits per G.726 code (from 2 to 5) (default 4)
        
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
        
    def http_persistent(self, *args, **kwargs):
        """
        <boolean> .D......... Use persistent HTTP connections (default true)
        
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
        
    def start_number(self, *args, **kwargs):
        """
        <int> .D......... set first number in the sequence (from INT_MIN to INT_MAX) (default 0)
        
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
        
    def loop(self, *args, **kwargs):
        """
        <boolean> .D......... force loop over input file sequence (default false)
        
        """
        
        raise NotImplementedError
        
    def frame_size(self, *args, **kwargs):
        """
        <int> .D......... force frame size in bytes (from 0 to INT_MAX) (default 0)
        
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
        
    def live(self, *args, **kwargs):
        """
        <boolean> .D......... flag indicating that the input is a live file that only has the headers. (default false)
        
        """
        
        raise NotImplementedError
        
    def bandwidth(self, *args, **kwargs):
        """
        <int> .D......... bandwidth of this stream to be specified in the DASH manifest. (from 0 to INT_MAX) (default 0)
        
        """
        
        raise NotImplementedError
        
    def list_devices(self, *args, **kwargs):
        """
        <boolean> .D......... list available devices (default false)
        
        """
        
        raise NotImplementedError
        
    def video_device_index(self, *args, **kwargs):
        """
        <int> .D......... select video device by index for devices with same name (starts at 0) (from -1 to INT_MAX) (default -1)
        
        """
        
        raise NotImplementedError
        
    def audio_device_index(self, *args, **kwargs):
        """
        <int> .D......... select audio device by index for devices with same name (starts at 0) (from -1 to INT_MAX) (default -1)
        
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
        
    def y(self, *args, **kwargs):
        """
        <int> .D......... Initial y coordinate. (from 0 to INT_MAX) (default 0)
        
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
        
    def flags(self, *args, **kwargs):
        """
        <flags> ED.VAS..... (default 0)
        
        unaligned                    .D.V....... allow decoders to produce unaligned output
        gray                         ED.V....... only decode/encode grayscale
        low_delay                    ED.V....... force low delay
        bitexact                     ED.VAS..... use only bitexact functions (except (I)DCT)
        output_corrupt               .D.V....... Output even potentially corrupted frames
        drop_changed                 .D.VA.....P Drop frames whose parameters differ from first decoded frame
        """
        
        raise NotImplementedError
        
    def flags2(self, *args, **kwargs):
        """
        <flags> ED.VAS..... (default 0)
        
        ignorecrop                   .D.V....... ignore cropping information from sps
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
        venc_params                  .D.V....... export video encoding parameters through frame side data
        film_grain                   .D.V....... export film grain parameters through frame side data
        """
        
        raise NotImplementedError
        
    def ar(self, *args, **kwargs):
        """
        <int> ED..A...... set audio sampling rate (in Hz) (from 0 to INT_MAX) (default 0)
        
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
        
    def debug(self, *args, **kwargs):
        """
        <flags> ED.VAS..... print specific debug info (default 0)
        
        pict                         .D.V....... picture info
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
        
    def threads(self, *args, **kwargs):
        """
        <int> ED.VA...... set the number of threads (from 0 to INT_MAX) (default 1)
        
        auto            0            ED.V....... autodetect a suitable number of threads to use
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
        
    def lowres(self, *args, **kwargs):
        """
        <int> .D.VA...... decode at 1= 1/2, 2=1/4, 3=1/8 resolutions (from 0 to INT_MAX) (default 0)
        
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
        
    def thread_type(self, *args, **kwargs):
        """
        <flags> ED.VA...... select multithreading type (default slice+frame)
        
        slice                        ED.V.......
        frame                        ED.V.......
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
        
    def gamma(self, *args, **kwargs):
        """
        <float> .D.V....... Set the float gamma value when decoding (from 0.001 to FLT_MAX) (default 1)
        
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
        
    def strict_displaywin(self, *args, **kwargs):
        """
        <boolean> .D.V....... stricly apply default display window size (default false)
        
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
        
    def palette(self, *args, **kwargs):
        """
        <string> .D...S..... set the global palette
        
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
        
    def aribb24_base_path(self, *args, **kwargs):
        """
        <string> .D...S..... set the base path for the libaribb24 library
        
        """
        
        raise NotImplementedError
        
    def aribb24_skip_ruby_text(self, *args, **kwargs):
        """
        <boolean> .D...S..... skip ruby text blocks during decoding (default true)
        
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
        

