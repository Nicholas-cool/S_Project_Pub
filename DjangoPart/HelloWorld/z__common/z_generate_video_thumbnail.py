import ffmpeg
import os


def z_generate_video_thumbnail(video_path, thumbnail_path, time_in_seconds=1):
    """
        生成视频缩略图
        :param video_path: 视频路径
        :param thumbnail_path: 缩略图保存路径
        :param time_in_seconds: 生成缩略图的时间点（单位：秒）
    """
    # 缩略图文件夹不存在则创建
    thumbnail_folder = os.path.dirname(thumbnail_path)
    os.makedirs(thumbnail_folder, exist_ok=True)

    # 生成缩略图
    (
        ffmpeg
        .input(video_path, ss=time_in_seconds)
        .output(thumbnail_path, vframes=1)
        .run(overwrite_output=True)   # overwrite_output: 是否覆盖输出文件
    )
    print(f"缩略图已保存至: {thumbnail_path}")
