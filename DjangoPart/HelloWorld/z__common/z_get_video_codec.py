import ffmpeg


def z_get_video_codec(video_path):
    try:
        # 使用 ffmpeg.probe 来获取视频信息
        probe = ffmpeg.probe(video_path)

        # 获取第一个视频流的信息
        video_stream = next(
            stream for stream in probe['streams'] if stream['codec_type'] == 'video'
        )

        # 提取编码格式
        codec_name = video_stream['codec_name']
        return codec_name

    except ffmpeg.Error as e:
        print(f"Error while probing video: {e}")
        return None
