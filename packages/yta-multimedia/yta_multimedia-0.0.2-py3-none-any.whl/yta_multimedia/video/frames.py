from moviepy.editor import VideoFileClip
from yta_general_utils.type_checker import variable_is_type
from yta_general_utils.file_processor import file_is_video_file
from typing import Union

def extract_frames_from_video(video_input: Union[VideoFileClip, str], output_folder: str):
    """
    This method will extract all the 'video_input' frames in the
    provided 'output_folder' with the 'frameXXXXX.png' name, starting
    from 0 to the last frame.
    """
    if not video_input:
        return None
    
    if not output_folder:
        return None
    
    if not output_folder.endswith('/'):
        output_folder += '/'
    
    if variable_is_type(video_input, str):
        if not file_is_video_file(video_input):
            return None
        
        video_input = VideoFileClip(video_input)

    video_input.write_images_sequence(output_folder + 'frame%05d.png')

    return output_folder