"""Motion image processing functions."""
import os
import subprocess
from pathlib import Path

from hyfi.graphics.utils import load_images
from hyfi.utils.iolibs import IOLIBs
from hyfi.utils.logging import LOGGING
from hyfi.utils.notebooks import NBs

logger = LOGGING.getLogger(__name__)


def make_gif(
    image_filepaths=None,
    filename_patterns: str = "",
    base_dir: str = "",
    output_filepath: str = "",
    duration: int = 100,
    loop: int = 0,
    width: int = 0,
    optimize: bool = True,
    quality: int = 50,
    show: bool = False,
    force: bool = False,
    **kwargs,
):
    """
    Create a GIF from a list of images or a list of filenames.
    """
    logger.info("Making GIF from %s", filename_patterns)
    if os.path.exists(output_filepath) and not force:
        logger.info("Skipping GIF creation, already exists: %s", output_filepath)
        logger.info("If you want to re-create the GIF, set force=True")
    else:
        if image_filepaths is None:
            image_filepaths = sorted(
                IOLIBs.get_filepaths(filename_patterns, base_dir=base_dir)
            )
        if not image_filepaths:
            logger.warning("no images found")
            return
        if frames := load_images(image_filepaths):
            frame_one = frames[0]
            frame_one.save(
                output_filepath,
                format="GIF",
                append_images=frames,
                save_all=True,
                duration=duration,
                loop=loop,
                optimize=optimize,
                quality=quality,
            )
            logger.info("Saved GIF to %s", output_filepath)
        else:
            logger.warning("No frames found for %s", filename_patterns)

    if show and os.path.exists(output_filepath):
        NBs.display_image(data=open(output_filepath, "rb").read(), width=width)

    return output_filepath


def extract_frames(
    video_path: str,
    extract_nth_frame: int,
    extracted_frame_dir: str,
    frame_filename: str = "%04d.jpg",
):
    """
    Extract frames from a video.
    """
    logger.info("Exporting Video Frames (1 every %s)...", extract_nth_frame)
    try:
        for f in Path(f"{extracted_frame_dir}").glob("*.jpg"):
            f.unlink()
    except FileNotFoundError:
        logger.info("No video frames found in %s", extracted_frame_dir)
    vf = f"select=not(mod(n\\,{extract_nth_frame}))"

    ffmpeg_path = "/usr/bin/ffmpeg"
    if not os.path.exists(ffmpeg_path):
        ffmpeg_path = "ffmpeg"
    if os.path.exists(video_path):
        subprocess.run(
            [
                ffmpeg_path,
                "-i",
                f"{video_path}",
                "-vf",
                f"{vf}",
                "-vsync",
                "vfr",
                "-q:v",
                "2",
                "-loglevel",
                "error",
                "-stats",
                f"{extracted_frame_dir}/{frame_filename}",
            ],
            stdout=subprocess.PIPE,
        ).stdout.decode("utf-8")
    else:
        logger.warning(
            "WARNING!\n\nVideo not found: %s.\nPlease check your video path.",
            video_path,
        )


def create_video(
    base_dir: str,
    video_path: str,
    input_url: str,
    fps: int,
    start_number: int,
    vframes: int,
    force: bool = False,
):
    """
    Create a video from a list of images.
    """

    logger.info("Creating video from %s", input_url)
    if os.path.exists(video_path) and not force:
        logger.info("Skipping video creation, already exists: %s", video_path)
        logger.info("If you want to re-create the video, set force=True")
        return video_path

    cmd = [
        "ffmpeg",
        "-y",
        "-vcodec",
        "png",
        "-r",
        str(fps),
        "-start_number",
        str(start_number),
        "-i",
        input_url,
        "-frames:v",
        str(vframes),
        "-c:v",
        "libx264",
        "-vf",
        f"fps={fps}",
        "-pix_fmt",
        "yuv420p",
        "-crf",
        "17",
        "-preset",
        "veryslow",
        video_path,
    ]

    process = subprocess.Popen(
        cmd,
        cwd=f"{base_dir}",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    _, stderr = process.communicate()
    if process.returncode != 0:
        logger.error(stderr)
        raise RuntimeError(stderr)
    else:
        logger.info("Video created successfully and saved to %s", video_path)

    return video_path
