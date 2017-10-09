#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@author: Amit Kumar
@mail: haywithamit@gmail.com
"""

import heapq
from Vehicle import Car
from sys import argv


class ParkingLot:
    def __init__(self, max_slots=0, floors=1):
        self._max_slots = max_slots
        self.total_floors = floors
        self.slots_available = [ParkingSlot(i+1) for i in xrange(self._max_slots)]
        self.slots_occupied = {"reg_numbers": dict(),
                               "colors": dict(),
                               "slots": dict()
                               }

    def get_next_available(self):
        if len(self.slots_available) > 0:
            return self.slots_available[0]
        return False

    def park_vehicle(self, reg_number, color):
        vehicle = Car()
        vehicle.set_registration(reg_number)
        vehicle.set_color(color)
        parking_slot_available = self.get_next_available()
        if parking_slot_available is False:
            print("Sorry, parking lot is full")
        else:
            is_parked = parking_slot_available.park(vehicle)
            if is_parked:
                try:
                    slot_popped = heapq.heappop(self.slots_available)
                    v_color = slot_popped.parked_car.get_color()
                    v_reg_number = slot_popped.parked_car.get_registration()
                    v_slot = slot_popped.parking_slot_id
                    try:
                        self.slots_occupied["reg_numbers"][v_reg_number] = slot_popped
                        if v_color not in self.slots_occupied["colors"]:
                            self.slots_occupied["colors"][v_color] = set()
                        self.slots_occupied["colors"][v_color].add(slot_popped)
                        self.slots_occupied["slots"][v_slot] = slot_popped
                    except KeyError:
                        print("Error in finding the values!")
                    except Exception as e:
                        print(e)
                        print("Error in occupying slot!")
                    print("Allocated slot number: {}".format(v_slot))
                except IndexError:
                    print("Error in parking")

    def unpark_vehicle(self, slot_id):
        if slot_id in self.slots_occupied["slots"]:
            slot_left = self.slots_occupied["slots"][slot_id]
            try:
                v_color = slot_left.parked_car.get_color()
                v_reg_number = slot_left.parked_car.get_registration()
                del self.slots_occupied["reg_numbers"][v_reg_number]
                del self.slots_occupied["slots"][slot_id]
                try:
                    self.slots_occupied["colors"][v_color].remove(slot_left)
                    print("Slot number {} is free".format(slot_id))
                except Exception as e:
                    print(e.message + ": This color car does not exist")
            except Exception as e:
                print(e.message + ": Unable to unpark car")
            slot_left.refresh_details()
            heapq.heappush(self.slots_available, slot_left)
        else:
            print("Slot does not exist")

    def status(self):
        try:
            total_slots_occupied = len(self.slots_occupied["reg_numbers"])
            if total_slots_occupied>0:
                print("Slot No.\tRegistration No\tColour")
                for slot_number in xrange(total_slots_occupied+1):
                    if slot_number in self.slots_occupied["slots"]:
                        print("{}\t{}\t{}".format(
                            self.slots_occupied["slots"][slot_number].parking_slot_id,
                            self.slots_occupied["slots"][slot_number].parked_car.get_registration(),
                            self.slots_occupied["slots"][slot_number].parked_car.get_color()
                        ))
            else:
                print("No cars parked yet!")
        except Exception as e:
            print("Error in showing parked cards: {}".format(e.message))

    def registration_numbers_for_cars_with_colour(self, colour):
        try:
            cars = self.slots_occupied["colors"][colour]
            if len(cars) == 0:
                print("No Cars parked with this color!")
                return
            reg_of_parked_cars = ""
            for car in cars:
                reg_of_parked_cars += car.parked_car.get_registration()+", "
            reg_of_parked_cars = reg_of_parked_cars[:-2]
            print(reg_of_parked_cars)
        except KeyError:
            print("No Cars parked!")

    def slot_numbers_for_cars_with_colour(self, colour):
        try:
            cars = self.slots_occupied["colors"][colour]
            if len(cars) == 0:
                print("No Cars parked with this color!")
                return
            slot_of_parked_cars = ""
            for car in cars:
                slot_of_parked_cars += str(car.parking_slot_id)+", "
            slot_of_parked_cars = slot_of_parked_cars[:-2]
            print(slot_of_parked_cars)
        except KeyError:
            print("No Cars parked!")

    def slot_number_for_registration_number(self, reg_number):
        try:
            car = self.slots_occupied["reg_numbers"][reg_number]
            if not car:
                print("Not found")
                return
            print(car.parking_slot_id)
        except KeyError:
            print("Not found")


class ParkingSlot:
    def __init__(self, slot_id = None):
        self.parked_car = None
        self.parking_slot_id = slot_id

    def park(self, vehicle_object):
        try:
            self.parked_car = vehicle_object
            return True
        except Exception as e:
            return False

    def refresh_details(self):
        self.parked_car = None

    def __cmp__(self, other):
        return cmp(self.parking_slot_id, other.parking_slot_id)

    def __hash__(self):
        return hash(self.parking_slot_id)


def create_parking_lot(slots):
    p_lot = ParkingLot(slots)
    print("Created a parking lot with {} slots".format(slots))
    return p_lot


if __name__ == '__main__':
    p = create_parking_lot(5)
    p.park_vehicle('KA-01- HH-1234', 'White')
    p.park_vehicle('KA-01- HH-124', 'Blue')
    p.park_vehicle('KA-01- HH-1334', 'White')
    p.park_vehicle('KA-01- HH-1434', 'Blue')
    p.unpark_vehicle(3)
    p.unpark_vehicle(4)
    p.park_vehicle('KA-01- HH-1534', 'Red')
    p.park_vehicle('KA-01- HH-1634', 'Grey')
    p.park_vehicle('KA-01- HH-1734', 'White')
    p.status()
    p.registration_numbers_for_cars_with_colour("White")
    p.slot_numbers_for_cars_with_colour("White")
    p.slot_number_for_registration_number("KA-01- HH-1734")
    p.slot_number_for_registration_number("KA-01- HH-1732")
