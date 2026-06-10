from rgbmatrix import graphics

from utilities.animator import Animator
from setup import colours, fonts, screen

from airports import airport_data
import pycountry

# Setup
PLANE_DETAILS_COLOUR = colours.PINK
PLANE_DISTANCE_FROM_TOP = 30
PLANE_TEXT_HEIGHT = 9
PLANE_FONT = fonts.regular


def airport_for_display(iata):
    airport = airport_data.get_airport_by_iata(iata)[0]

    name = (airport["airport"]
               .replace(' Airport', '')
               .replace(' International', ''))
    country_code = airport["country_code"]
    country = pycountry.countries.get(alpha_2=country_code).name
    return f'{country}, {name}'


class PlaneDetailsScene(object):
    def __init__(self):
        super().__init__()
        self.plane_position = screen.WIDTH
        self._data_all_looped = False
        self.known_airport_codes = ['LHR', 'LCY', 'LTN', 'STN', 'LGW']

    @Animator.KeyFrame.add(1)
    def plane_details(self, count):

        # Guard against no data
        if len(self._data) == 0:
            return

        origin_iata = self._data[self._data_index]["origin"]
        origin_airport_text = airport_for_display(origin_iata)

        destination_iata = self._data[self._data_index]["destination"]
        destination_airport_text = airport_for_display(destination_iata)


        known_origin = origin_iata in self.known_airport_codes
        known_destination = destination_iata in self.known_airport_codes

        plane_model_text = f'{self._data[self._data_index]["plane"]}'
        if known_origin and known_destination:
            plane = plane_model_text
        elif known_origin and not known_destination:
            plane = f'To: {destination_airport_text} - {plane_model_text}'
        elif known_destination and not known_origin:
            plane = f'From: {origin_airport_text} - {plane_model_text}'
        else:
            plane = f'From: {origin_airport_text}, To: {destination_airport_text} - {plane_model_text}'

        # Draw background
        self.draw_square(
            0,
            PLANE_DISTANCE_FROM_TOP - PLANE_TEXT_HEIGHT,
            screen.WIDTH,
            screen.HEIGHT,
            colours.BLACK,
        )

        # Draw text
        text_length = graphics.DrawText(
            self.canvas,
            PLANE_FONT,
            self.plane_position,
            PLANE_DISTANCE_FROM_TOP,
            PLANE_DETAILS_COLOUR,
            plane,
        )

        # Handle scrolling
        self.plane_position -= 1
        if self.plane_position + text_length < 0:
            self.plane_position = screen.WIDTH
            if len(self._data) > 1:
                self._data_index = (self._data_index + 1) % len(self._data)
                self._data_all_looped = (not self._data_index) or self._data_all_looped
                self.reset_scene()

    @Animator.KeyFrame.add(0)
    def reset_scrolling(self):
        self.plane_position = screen.WIDTH

