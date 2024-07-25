from yta_general_utils.tmp_processor import create_tmp_filename
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, vfx
from PIL import Image, ImageDraw, ImageFont

class CustomGreenScreenImage:
    """
    This class is used to build custom green screen that has specific green screen positions and
    title and description font sizes.
    """
    def __init__(self, filename: str, rgb_color: tuple, ulx: int, uly: int, drx: int, dry: int, title: str, title_font: ImageFont.FreeTypeFont, title_color: str, title_x: int, title_y: int, description: str, description_font: ImageFont.FreeTypeFont, description_color: str, description_x: int, description_y: int):
        # TODO: What about custom values ?
        self.__filename = filename
        self.ulx = ulx
        self.uly = uly
        self.drx = drx
        self.dry = dry
        self.rgb_color = rgb_color
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

    def save(self, output_filename):
        base = Image.open(self.__filename)
        draw = ImageDraw.Draw(base)   

        # We need to write title if existing
        if self.__title:
            title_position = (self.__title_x, self.__title_y)
            draw.text(title_position, self.__title, font = self.__title_font, fill = self.__title_color)

        if self.__description:
            description_position = (self.__description_x, self.__description_y)
            draw.text(description_position, self.__description, font = self.__description_font, fill = self.__description_color)

        # Anything else to handle?

        base.save(output_filename, quality = 100)

    def __generate_green_screen(self):
        pass

    def __add_clip(self, clip):
        """
        Adds the received 'clip' to the green screen image and displays it inside the green
        screen area.
        """
        # We write title and description if needed
        tmp_filename = create_tmp_filename('tmp_gs.png')
        self.save(tmp_filename)

        green_screen_clip = ImageClip(tmp_filename, duration = clip.duration).fx(vfx.mask_color, color = self.rgb_color, thr = 100, s = 5)

        width = self.drx - self.ulx
        clip = clip.resize(width = width).set_position((self.ulx, self.uly))

        return CompositeVideoClip([clip, green_screen_clip], size = green_screen_clip.size)

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
