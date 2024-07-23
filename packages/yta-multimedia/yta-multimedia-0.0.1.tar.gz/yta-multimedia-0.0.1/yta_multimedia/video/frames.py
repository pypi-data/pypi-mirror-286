from moviepy.editor import VideoFileClip

def extract_frames_from_video_clip(videoclip: VideoFileClip, output_folder: str):
    """
    This method will extract all the 'input_videoclip' frames in the
    provided 'output_folder' with the 'frameXXXXX.png' name, starting
    from 0 to the last frame.
    """
    if not output_folder:
        return None
    
    if not output_folder.endswith('/'):
        output_folder += '/'
        
    videoclip.write_images_sequence(output_folder + 'frame%05d.png')

# TODO: Create a method to build a video from clips folder or list