def crop_audio_file(audio_filename: str, duration: float, output_filename: str):
    """
    Crops the 'audio_filename' provided to the requested 'duration'.

    This method returns the new audio 'output_filename' if valid, or
    False if it was not possible to crop it.
    """
    if not audio_filename:
        return None
    
    if not output_filename:
        return None

    from moviepy.editor import AudioFileClip

    audio_clip = AudioFileClip(audio_filename)

    if audio_clip.duration < duration:
        # TODO: Exception, None, review this
        print('audio is shorter than requested duration')
        return False
    
    audio_clip.set_duration(duration).write_audiofile(output_filename)

    return output_filename