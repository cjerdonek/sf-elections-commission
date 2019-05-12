from pathlib import Path
import subprocess


def ensure_exists(path):
    if not path.exists():
        raise RuntimeError(f'file does not exist: {path}')


def make_audio_to_video_args(base_name, mp3_file_name, thumb_file_name,
    mp4_file_name
):
    args = f"""
    ffmpeg -i {mp3_file_name} -f image2 -loop 1 -r 2 -i {thumb_file_name}
        -shortest -c:a copy -c:v libx264 -crf 23 -preset veryfast
        -movflags faststart {mp4_file_name}
    """.split()

    return args


def make_finalize_video_args(base_name, mp4_file_name, dest_file_name):
    args = f"""
    ffmpeg -i {mp4_file_name} -acodec copy -vcodec copy {dest_file_name}
    """.split()

    return args


def make_video_file(source_dir, base_name):
    mp3_file_name = f'{base_name}.mp3'
    ensure_exists(source_dir / mp3_file_name)

    thumb_file_name = f'{base_name}_thumb.png'
    ensure_exists(source_dir / thumb_file_name)

    mp4_file_name = f'{base_name}.mp4'

    args = make_audio_to_video_args(base_name, mp3_file_name=mp3_file_name,
                    thumb_file_name=thumb_file_name,
                    mp4_file_name=mp4_file_name)
    subprocess.run(args, cwd=source_dir)

    ensure_exists(source_dir / mp4_file_name)

    return mp4_file_name


def finalize_video(source_dir, mp4_file_name, base_name):
    dest_file_name = f'{base_name}.mkv'
    args = make_finalize_video_args(base_name, mp4_file_name=mp4_file_name,
                        dest_file_name=dest_file_name)
    subprocess.run(args, cwd=source_dir)

    ensure_exists(source_dir / dest_file_name)


def make_video(source_dir, base_name):
    """
    Make the video file to upload to YouTube.
    """
    source_dir = Path(source_dir)
    mp4_file_name = make_video_file(source_dir, base_name=base_name)

    finalize_video(source_dir, mp4_file_name=mp4_file_name, base_name=base_name)
