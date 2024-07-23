from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, vfx, concatenate_videoclips
from PIL import ImageFont

class CustomGreenScreenVideo:
    """
    This class is used to build green screen videos by inserting videos in this green screen video.
    """
    def __init__(self, filename: str, rgb_color: tuple, ulx: int, uly: int, drx: int, dry: int, title: str, title_font: ImageFont.FreeTypeFont, title_color: str, title_x: int, title_y: int, description: str, description_font: ImageFont.FreeTypeFont, description_color: str, description_x: int, description_y: int):
        # TODO: What about custom values ?
        self.__filename = filename
        self.ulx = ulx
        self.uly = uly
        self.drx = drx
        self.dry = dry
        self.rgb_color = rgb_color
        # By now these elements are not used
        self.__title = title
        self.__title_font = title_font
        self.__title_color = title_color
        self.__title_x = title_x
        self.__title_y = title_y
        self.__description = description
        self.__description_font = description_font
        self.__description_color = description_color
        self.__description_x = description_x
        self.__description_y = description_y

    def __generate_green_screen(self):
        pass

    def __add_clip(self, clip):
        """
        Adds the received 'clip' to the green screen video and displays it inside the green
        screen area.
        """
        # TODO: Write title and description with textclips
        #green_screen_clip = VideoFileClip(self.__filename, duration = clip.duration).fx(vfx.mask_color, color = self.rgb_color, thr = 100, s = 5)
        green_screen_clip = VideoFileClip(self.__filename).fx(vfx.mask_color, color = self.rgb_color, thr = 100, s = 5)
        
        width = self.drx - self.ulx
        # If the provided clip is shorter than our green screen: easy, crop the green screen
        # If the provided clip is longer than our green screen: I use the green screen duration
        # and let the clip be original the rest of the time
        if green_screen_clip.duration > clip.duration:
            green_screen_clip = green_screen_clip.set_duration(clip.duration)
            # Clip will be displayed inside the green screen area
            clip = clip.resize(width = width).set_position((self.ulx, self.uly))
            clip = CompositeVideoClip([clip, green_screen_clip], size = green_screen_clip.size)
        elif clip.duration > green_screen_clip.duration:
            # First subclip will be displayed inside the green screen area
            first_clip = clip.subclip(0, green_screen_clip.duration).resize(width = width).set_position((self.ulx, self.uly))
            # Second clip will be as the original one
            second_clip = clip.subclip(green_screen_clip.duration, clip.duration)
            clip = concatenate_videoclips([
                CompositeVideoClip([first_clip, green_screen_clip], size = green_screen_clip.size),
                second_clip
            ])
        else:
            clip = CompositeVideoClip([clip, green_screen_clip], size = green_screen_clip.size)

        return clip
    
    def insert_video(self, video_filename, output_filename):
        """
        Inserts the provided 'video_filename' in the green screen and generates a new
        video which is stored locally as 'output_filename'.
        """
        clip = VideoFileClip(video_filename)
        final_clip = self.__add_clip(clip)
        final_clip.write_videofile(output_filename, fps = clip.fps)

    def from_clip(self, clip):
        """
        Receives a 'clip' and generates a new one that is the provided one inside of the
        green screen.
        """
        return self.__add_clip(clip)

    def insert_image(self, image_filename, output_filename):
        """
        Inserts the provided 'image_filename' in the green screen and generates a new 
        image wich is stored locally as 'output_filename'.
        """
        # I do the trick with moviepy that is working for videos...
        clip = ImageClip(image_filename, duration = 1 / 60)
        final_clip = self.__add_clip(clip)
        final_clip.save_frame(output_filename, t = 0)
