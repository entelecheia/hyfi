"""Motion image processing functions."""
import os
import subprocess
from pathlib import Path
from typing import Optional

from hyfi.utils.iolibs import IOLIBs
from hyfi.utils.logging import LOGGING
from hyfi.utils.notebooks import NBs

from .utils import GUTILs

logger = LOGGING.getLogger(__name__)


class MOTION:
    @staticmethod
    def make_gif(
        image_filepaths=None,
        filename_patterns: Optional[str] = None,
        base_dir: Optional[str] = None,
        output_file: Optional[str] = None,
        duration: int = 100,
        loop: int = 0,
        width: int = 0,
        optimize: bool = True,
        quality: int = 50,
        display_to_notebook: bool = False,
        force: bool = False,
        **kwargs,
    ) -> Optional[str]:
        """
        Create a GIF from a list of images or a list of filenames.
        """
        output_file = output_file or ""
        if os.path.exists(output_file) and not force:
            logger.info("Skipping GIF creation, already exists: %s", output_file)
            logger.info("If you want to re-create the GIF, set force=True")
        else:
            if image_filepaths is None and filename_patterns:
                image_filepaths = sorted(
                    IOLIBs.get_filepaths(filename_patterns, base_dir=base_dir)
                )
            if not image_filepaths:
                logger.warning("no images found")
                return
            if frames := GUTILs.load_images(image_filepaths):
                frame_one = frames[0]
                frame_one.save(
                    output_file,
                    format="GIF",
                    append_images=frames,
                    save_all=True,
                    duration=duration,
                    loop=loop,
                    optimize=optimize,
                    quality=quality,
                )
                logger.info("Saved GIF to %s", output_file)
            else:
                logger.warning("No frames found for %s", filename_patterns)

        if display_to_notebook and os.path.exists(output_file):
            NBs.display_image(data=IOLIBs.read(output_file), width=width)

        return output_file

    @staticmethod
    def extract_frames(
        input_video_file: str,
        every_nth_frame: int,
        ouput_dir: str,
        frame_filename_pattern: str = "%04d.jpg",
        ffmpeg_path: str = "/usr/bin/ffmpeg",
    ):
        """
        Extract frames from a video.

        Args:
            input_video_file (str): Path to the video.
            every_nth_frame (int): Extract every nth frame.
            ouput_dir (str): Path to the output directory.
            frame_filename_pattern (str, optional): Frame filename pattern. Defaults to "%04d.jpg".
        """
        logger.info(
            "Exporting Video Frames (every %sth frame) to %s",
            every_nth_frame,
            ouput_dir,
        )
        try:
            for f in Path(f"{ouput_dir}").glob("*.jpg"):
                f.unlink()
        except FileNotFoundError:
            logger.info("No video frames found in %s", ouput_dir)
        vf = f"select=not(mod(n\\,{every_nth_frame}))"

        if not os.path.exists(ffmpeg_path):
            ffmpeg_path = "ffmpeg"
        if os.path.exists(input_video_file):
            subprocess.run(
                [
                    ffmpeg_path,
                    "-i",
                    f"{input_video_file}",
                    "-vf",
                    f"{vf}",
                    "-vsync",
                    "vfr",
                    "-q:v",
                    "2",
                    "-loglevel",
                    "error",
                    "-stats",
                    f"{ouput_dir}/{frame_filename_pattern}",
                ],
                stdout=subprocess.PIPE,
            ).stdout.decode("utf-8")
        else:
            logger.warning(
                "WARNING!\n\nVideo not found: %s.\nPlease check your video path.",
                input_video_file,
            )

    @staticmethod
    def create_video(
        input_image_dir: str,
        video_output_file: str,
        input_url: str,
        fps: int,
        start_number: int,
        vframes: int,
        force: bool = False,
    ) -> Optional[str]:
        """
        Create a video from a list of images.

        Args:
            input_image_dir (str): Base directory.
            video_path (str): Path to the video.
            input_url (str): Input URL.
            fps (int): Frames per second.
            start_number (int): Start number.
            vframes (int): Number of frames.
            force (bool, optional): Force video creation. Defaults to False.

        Raises:
            FileNotFoundError: If the video is not found.

        """

        logger.info("Creating video from %s", input_url)
        if os.path.exists(video_output_file) and not force:
            logger.info(
                "Skipping video creation, already exists: %s", video_output_file
            )
            logger.info("If you want to re-create the video, set force=True")
            return video_output_file

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
            video_output_file,
        ]

        process = subprocess.Popen(
            cmd,
            cwd=f"{input_image_dir}",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        _, stderr = process.communicate()
        if process.returncode != 0:
            logger.error(stderr)
            raise RuntimeError(stderr)
        else:
            logger.info("Video created successfully and saved to %s", video_output_file)

        return video_output_file
