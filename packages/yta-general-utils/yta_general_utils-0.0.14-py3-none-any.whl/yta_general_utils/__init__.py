def round2(value):
    """
    Rounds the number to 2 decimals.
    """
    from math import round

    return round(value, 2)




# External working
def download_youtube_video_and_describeas_explained_stock_video(video_id: str, description: str, output_filename: str):
    """
    This method takes a Youtube video, downloads it as maximum quality and then
    sets the provided 'description' as the audio.
    """
    if not video_id:
        return None
    
    if not description:
        return None
    
    if not output_filename:
        return None
    
    from youtubeenhanced.objects.youtube_video import YoutubeVideo
    from yta_multimedia.audio.voice.generation.tts.google import narrate
    from yta_multimedia.video.audio import set_video_clip_audio_from_audio_file
    from tmp_processor import create_tmp_filename
    from moviepy.editor import VideoFileClip

    # We first download it at maximum quality
    YoutubeVideo(video_id).download(output_filename)
    video = VideoFileClip(output_filename)

    # Then we narrate it by adding the audio narration
    narration_filename = create_tmp_filename('tmp_narration.wav')
    narrate(description, output_filename = narration_filename)

    video = set_video_clip_audio_from_audio_file(video, narration_filename)

    video.write_videofile(output_filename)

output_filename = 'E:/stockvideosexplained/test_stock.mp4'
description = 'In this video you can see numbers from a YouTube video that keep growing and growing until they reach three million views, with the texts in English.'
video_url = 'https://www.youtube.com/watch?v=CJK5jggbFYg&'

download_youtube_video_and_describeas_explained_stock_video(video_url, description, output_filename)
