from rgbmatrix import graphics

from utilities.animator import Animator
from setup import colours, fonts, screen

from airports import airport_data

# Setup
PLANE_DETAILS_COLOUR = colours.PINK
PLANE_DISTANCE_FROM_TOP = 30
PLANE_TEXT_HEIGHT = 9
PLANE_FONT = fonts.regular


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
        origin_name = (airport_data.get_airport_by_iata(origin_iata)[0]["airport"]
                       .replace(' Airport', '')
                       .replace(' International', ''))

        destination_iata = self._data[self._data_index]["destination"]
        destination_name = (airport_data.get_airport_by_iata(destination_iata)[0]["airport"]
                            .replace(' Airport', '')
                            .replace(' International', ''))

        known_origin = origin_iata in self.known_airport_codes
        known_destination = destination_iata in self.known_airport_codes

        if known_origin and known_destination:
            plane = f'{self._data[self._data_index]["plane"]}'
        elif known_origin:
            plane = f'To: {destination_name} - {self._data[self._data_index]["plane"]}'
        elif known_destination:
            plane = f'From: {origin_name} - {self._data[self._data_index]["plane"]}'

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
