from moviepy.editor import AudioFileClip, CompositeAudioClip, concatenate_audioclips
from yta_general_utils.file_processor import get_current_file_abspath

RESOURCES_ABSOLUTE_PATH = get_current_file_abspath(3) + 'resources/audio/sound/'

def create_silence_audio_file(duration, output_filename):
    """
    Creates a silence audio file that lasts the 'duration' provided in 
    seconds.
    """
    create_silence_audio_clip(duration).write_audiofile(output_filename)

def create_silence_audio_clip(duration) -> AudioFileClip:
    """
    This method creates a silence AudioFileClip of the provided 'duration' in
    seconds and returns it.
    """
    SILENT_AUDIO_FILENAME = RESOURCES_ABSOLUTE_PATH + 'silent.wav'

    return AudioFileClip(SILENT_AUDIO_FILENAME).subclip(0, duration)

def create_typing_audio_file(output_filename: str):
    """
    This method creates a typing audio of 3.5 seconds (3s of typing, 0.5 of silence).
    """
    if not output_filename:
        return None
    
    create_typing_audio_clip().write_audiofile(output_filename)

def create_typing_audio_clip() -> CompositeAudioClip:
    """
    This method creates a typing audio of 3.5 seconds (3s of typing, 0.5 of silence)
    and returns it as a clip.
    """
    AUDIO_TYPING_3S_FILENAME = RESOURCES_ABSOLUTE_PATH + 'typing_3s.mp3'

    typing_audio_clip = AudioFileClip(AUDIO_TYPING_3S_FILENAME)
    silence_audio_clip = create_silence_audio_clip(0.5)

    return concatenate_audioclips([typing_audio_clip, silence_audio_clip])
