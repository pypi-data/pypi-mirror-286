from moviepy.editor import VideoFileClip, AudioFileClip

def extract_audio_from_video_clip(videoclip: VideoFileClip, output_filename: str):
    """
    Extracts the audio from the provided videoclip and stores it as the
    'output_filename' audio file.
    """
    if not output_filename:
        return None

    videoclip.audio.write_audiofile(output_filename)

def set_video_clip_audio_from_audio_clip(videoclip: VideoFileClip, audioclip: AudioFileClip):
    """
    This will set the provided 'audioclip' as the new audio for the
    provided 'videoclip'. This method must be assigned to the 
    videoclip to work well.
    """
    videoclip = videoclip.set_audio(audioclip)

    return videoclip

def set_video_clip_audio_from_audio_file(videoclip: VideoFileClip, audio_filename: str):
    """
    This will set the provided 'audio_filename' as the new audio for the
    provided 'videoclip'. This method must be assigned to the videoclip
    to work well (only if provided audio is valid).
    """
    from yta_general_utils.file_processor import file_is_audio_file
    if not audio_filename:
        return videoclip
    
    if not file_is_audio_file(audio_filename):
        return videoclip
    
    videoclip = videoclip.set_audio(AudioFileClip(audio_filename))

    return videoclip

