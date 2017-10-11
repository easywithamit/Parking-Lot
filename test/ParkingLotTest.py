#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@author: Amit Kumar
@mail: haywithamit@gmail.com
"""
import unittest
from src.ParkingLot import create_parking_lot, ParkingSlot


class ParkingLotTest(unittest.TestCase):
    def setUp(self):
        self.parking_lot_instance = create_parking_lot(5)

    def test_park(self):
        self.assertEqual(
            self.parking_lot_instance.get_next_available().parking_slot_id, 1
        )
        self.parking_lot_instance.park(['KA-01-HH-1234', 'White'])
        self.assertEqual(
            self.parking_lot_instance.get_next_available().parking_slot_id, 2
        )
        self.parking_lot_instance.park(['KA-01-HH-124', 'White'])
        self.assertEqual(len(self.parking_lot_instance.slots_available), 3)
        self.parking_lot_instance.park(['KA-01-HH-124', 'Blue'])
        self.parking_lot_instance.park(['KA-01-HH-1334', 'White'])
        self.parking_lot_instance.park(['KA-01-HH-1434', 'Blue'])
        self.assertFalse(self.parking_lot_instance.get_next_available())

    def test_leave(self):
        self.assertEqual(
            len(self.parking_lot_instance.slots_occupied["slots"]), 0
        )
        self.parking_lot_instance.park(['KA-01-HH-1234', 'White'])
        self.parking_lot_instance.park(['KA-01-HH-124', 'Blue'])
        self.assertIn(1, self.parking_lot_instance.slots_occupied["slots"])
        self.assertIn(2, self.parking_lot_instance.slots_occupied["slots"])
        self.assertNotIn(3, self.parking_lot_instance.slots_occupied["slots"])
        self.parking_lot_instance.park(['KA-01-HH-1334', 'White'])
        self.parking_lot_instance.leave(2)
        self.assertNotIn(2, self.parking_lot_instance.slots_occupied["slots"])
        self.assertIn(3, self.parking_lot_instance.slots_occupied["slots"])
        self.parking_lot_instance.park(['KA-01-HH-1434', 'Blue'])
        self.assertNotIn(4, self.parking_lot_instance.slots_occupied["slots"])
        self.assertIn(2, self.parking_lot_instance.slots_occupied["slots"])

    def test_registration_slot_numbers_for_cars_with_colour(self):
        self.assertEqual(
            len(self.parking_lot_instance.slots_occupied["colors"]), 0
        )
        self.parking_lot_instance.park(['KA-01-HH-1234', 'White'])
        self.parking_lot_instance.park(['KA-01-HH-124', 'Blue'])
        self.parking_lot_instance.park(['KA-01-HH-1334', 'White'])
        self.parking_lot_instance.park(['KA-01-HH-1434', 'Blue'])
        self.assertEqual(
            len(self.parking_lot_instance.slots_occupied["colors"]["White"]), 2
        )
        self.assertNotEqual(
            len(self.parking_lot_instance.slots_occupied["colors"]["Blue"]), 0
        )

    def test_slot_number_for_registration_number(self):
        self.assertEqual(
            len(self.parking_lot_instance.slots_occupied["slots"]), 0
        )
        self.parking_lot_instance.park(['KA-01-HH-1234', 'White'])
        self.parking_lot_instance.park(['KA-01-HH-124', 'Blue'])
        self.parking_lot_instance.park(['KA-01-HH-1334', 'White'])
        self.parking_lot_instance.park(['KA-01-HH-1434', 'Blue'])
        self.parking_lot_instance.leave(2)
        self.assertEqual(self.parking_lot_instance.slots_occupied["slots"][1].parked_car.get_registration(),"KA-01-HH-1234")
        self.assertIsInstance(self.parking_lot_instance.slots_occupied["slots"][1], ParkingSlot)


if __name__ == '__main__':
    unittest.main()

