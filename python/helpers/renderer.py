'''The renderer module has several helper functions to render graphs or images to the screen'''

from PIL import Image, ImageOps

import helpers.collections as Collections

from lib import epd2in13g as Display

# Public methods
def frame(display, black, red):
    '''Render a frame to the display.

    Args:
        display (EPD): The display to render this frame to.
        black (PIL.Image.Image): the background (black) image.
        red (PIL.Image.Image): The foreground (colored) image.
    '''
    # display.display_frame(display.get_frame_buffer(black), display.get_frame_buffer(red))
    black = black.convert('L')
    red = red.convert('L')
    blackRgb = black.convert('RGB')
    redRgb = red.convert('RGB')
    finalImage = Image.new('RGB', blackRgb.size, color=(255, 255, 255))
    blackChannel = Image.new('RGB', finalImage.size, color=(0, 0, 0))
    redChannel = Image.new('RGB', finalImage.size, color=(255, 0, 0))
    finalImage.paste(redChannel, (0, 0), ImageOps.invert(red))
    finalImage.paste(blackChannel, (0, 0), ImageOps.invert(black))
    display.display(display.getbuffer(finalImage))

def new_image():
    '''Create a new Image object.

    Returns:
        PIL.Image.Image: Description of returned object.
    '''
    return Image.new('1', (Display.EPD_HEIGHT, Display.EPD_WIDTH), 255)

def draw_logo(cfg, log, images):
    '''Render the logo to the black and red images.

    Args:
        cfg (DotMap): The configuration.
        images (dict): The images to paste the two colored parts to.
    '''
    log.info(cfg, 'Rendering logo')

    pihole_logo_top    = Image.open('img/pihole-bw-80-top.bmp')
    pihole_logo_bottom = Image.open('img/pihole-bw-80-bottom.bmp')
    images.black.paste(pihole_logo_top, (-12, 2))
    images.red.paste(pihole_logo_bottom, (-12, 2))

def draw_charts(cfg, log, image_draw, bottom_chart, top_chart):
    '''Draw the chart.

    Args:
        cfg (DotMap): The configuration.
        image_draw (DotMap { black: PIL.Image.ImageDraw, red: PIL.Image.ImageDraw}): draw targets.
        bottom_chart (dict): A dictionary containing the totals data.
        top_chart (dict): A dictionary containing the sub-data.
    '''
    log.info(cfg, 'Rendering charts')

    factor = max(bottom_chart) / cfg.chart.height

    __draw_chart(image_draw.black, bottom_chart, factor)
    __draw_chart(image_draw.red, top_chart, factor)

# Private methods
def __draw_chart(color, data, factor):
    '''Draw a chart.

    Args:
        color (PIL.Image.ImageDraw): The `ImageDraw` component this chart should be drawn on.
        data (dict): A dictionary containing the data.
        factor (float): The factor every entry in the data should be multiplied with.
    '''
    chart_bottom = Display.EPD_WIDTH - 22
    chart_left = 4
    columns = Collections.div_array(data, factor)
    for i, val in enumerate(columns):
        color.rectangle((i * 3 + chart_left, chart_bottom - val, i * 3 + chart_left + 1, chart_bottom), outline = 0, fill = 1)
