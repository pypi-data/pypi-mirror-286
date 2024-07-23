from moviepy.editor import VideoFileClip

def rescale_video_file(video_filename: str, output_width: int = 1920, output_height: int = 1080, output_filename: str = 'scaled.mp4'):
    """
    This method was created to rescale videos upper to 1920x1080 or 1080x1920. This is,
    when a 4k video appears, we simplify it to 1080p resolution to work with only that
    resolution.

    This method is used in the script-guided video generation. Please, do not touch =).

    # TODO: This method is very strict, so it will need a revision
    """
    from yta_general_utils.file_processor import file_is_video_file

    if not file_is_video_file(video_filename):
        return None
    
    return rescale_video_clip(VideoFileClip(video_filename), output_width, output_height, output_filename)

def rescale_video_clip(videoclip: VideoFileClip, output_width: int = 1920, output_height: int = 1080, output_filename: str = 'scaled.mp4'):
    """
    This method was created to rescale videos upper to 1920x1080 or 1080x1920. This is,
    when a 4k video appears, we simplify it to 1080p resolution to work with only that
    resolution.

    This method is used in the script-guided video generation. Please, do not touch =).

    # TODO: This method is very strict, so it will need a revision
    """
    # We only want to accept 16/9 or 9/16 by now, so:
    if not (output_width == 1920 and output_height == 1080) and not (output_width == 1080 and output_height == 1920):
        print('Sorry, not valid input parameters.')
        return None
    
    if not output_filename:
        return None
    
    from math import floor
    from yta_general_utils.tmp_processor import create_tmp_filename
    from yta_general_utils.file_processor import rename_file

    SCALE_WIDTH = 16
    SCALE_HEIGHT = 9
    if output_width == 1080 and output_height == 1920:
        SCALE_WIDTH = 9
        SCALE_HEIGHT = 16

    width = videoclip.w
    height = videoclip.h

    # We avoid things like 1927 instead of 1920
    new_width = width - width % SCALE_WIDTH
    new_height = height - height % SCALE_HEIGHT

    proportion = new_width / new_height

    if proportion > (SCALE_WIDTH / SCALE_HEIGHT):
        print('This video has more width than expected. Cropping horizontally.')
        while (new_width / new_height) != (SCALE_WIDTH / SCALE_HEIGHT):
            new_width -= SCALE_WIDTH
    elif proportion < (SCALE_WIDTH / SCALE_HEIGHT):
        print('This video has more height than expected. Cropping vertically.')
        while (new_width / new_height) != (SCALE_WIDTH / SCALE_HEIGHT):
            new_height -= SCALE_HEIGHT

    print('Final: W' + str(new_width) + ' H' + str(new_height))
    videoclip_rescaled = videoclip.crop(x_center = floor(width / 2), y_center = floor(height / 2), width = new_width, height = new_height)
    
    # Force output dimensions
    if new_width != output_width:
        print('Forcing W' + str(output_width) + ' H' + str(output_height))
        videoclip_rescaled = videoclip_rescaled.resize(width = output_width, height = output_height)

    # This fixes the problem of rewriting over an existing video
    tmp_video_filename = create_tmp_filename('scaled.mp4')
    tmp_audio_filename = create_tmp_filename('temp-audio.m4a')
    videoclip_rescaled.write_videofile(tmp_video_filename, codec = 'libx264', audio_codec = 'aac', temp_audiofile = tmp_audio_filename, remove_temp = True)
    #os.remove(video_filename) # TODO: Why deleting the input? This is unexpected
    rename_file(tmp_video_filename, output_filename, True)

    return True