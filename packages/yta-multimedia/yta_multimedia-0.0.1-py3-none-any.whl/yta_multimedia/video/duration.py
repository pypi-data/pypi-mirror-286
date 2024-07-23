from moviepy.editor import VideoFileClip

def crop_video_clip_using_key_frame_second(videoclip: VideoFileClip, key_frame_second: float, duration: float, output_filename: str):
    """
    Crops the provided videoclip using the 'key_frame_second' as the center of the
    new video generated as 'output_filename'.

    This method uses that 'key_frame_second' as the center of the video, but takes care 
    about start and end limits (you cannot start in -1.2s or end after the original video
    end).

    # TODO: Review this to improve documentation and whatever we can
    """
    # TODO: Improve checkings
    from yta_general_utils.tmp_processor import create_tmp_filename

    if not key_frame_second or key_frame_second < 0 or key_frame_second > videoclip.duration:
        # We use the middle of the video as the key frame
        key_frame_second = videoclip.duration / 2
    if not duration:
        duration = videoclip.duration
    if duration > videoclip.duration or duration <= 0:
        duration = videoclip.duration

    if duration < videoclip.duration:
        start_second = 0
        end_second = videoclip.duration
        # Only if we have to crop it already
        half_duration = duration / 2
        if key_frame_second - half_duration < 0:
            # Start in 0.0
            start_second = 0
            end_second = duration
        elif key_frame_second + half_duration > videoclip.duration:
            # End in 'videoclip.duration'
            start_second = videoclip.duration - duration
            end_second = videoclip.duration
        else:
            # Use 'key_frame_second' as center
            start_second = key_frame_second - half_duration
            end_second = key_frame_second + half_duration

        videoclip = videoclip.subclip(start_second, end_second)

    tmp_audiofilename = create_tmp_filename('temp-audio.m4a')
    videoclip.to_videofile(
        output_filename,
        codec = "libx264",
        temp_audiofile = tmp_audiofilename,
        remove_temp = True,
        audio_codec = 'aac' # pcm_s16le or pcm_s32le
    )
