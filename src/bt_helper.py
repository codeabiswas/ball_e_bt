"""
bt_helper.py
---
This file contains the BtHelper class, which allows for Bluetooth (BT) connectivity between the Jetson Nano and a BT input device (i.e.: keyboard)
---

Author: Andrei Biswas (@codeabiswas)
Date: February 22, 2021
Last Modified: February 28, 2021
"""

import datetime
import glob
import logging
import os
import sys
import threading
import time

import bluetooth as bt
import evdev
import pydbus
from evdev.device import DeviceInfo

# Log settings
log_file_name = "{}/logs/{}_debug.log".format(os.path.abspath(os.path.join(
    os.getcwd(), os.pardir)), datetime.date.today().strftime('%m_%d_%y'))

logging.basicConfig(
    format='[%(asctime)s] - %(filename)s - %(funcName)s() - %(levelname)s - %(message)s',
    level=logging.DEBUG,
    handlers=[
        logging.FileHandler(log_file_name, 'a'),
        logging.StreamHandler(sys.stdout)
    ]
)


class BtHelper:
    """
    A Helper class that allows for Bluetooth (BT) connectivity between a device and the Jetson Nano. Built for finding an input device, such as the Bluetooth button used for the Ball-E Project
    """

    def __init__(self, device_name="AB Shutter3"):
        """
        Initializing method for BtHelper

        Args:
            device_name (str, optional): Name of the BT device to be connected to. Defaults to "AB Shutter3".
        """

        # BT device name
        self.device_name = device_name
        # BT device address
        self.device_address = None
        # Jetson Nano's Bluetooth device
        self.device = None

    def set_device_address(self, device_address):
        """
        Setter for the BT device's address

        Args:
            device_address (str): The BT device's address, which is used for connecting to the BT device
        """

        self.device_address = device_address

    def get_device_address(self):
        """
        Getter for the BT device address

        Returns:
            device_address [str]: The BT device's address, which is used for connecting to the BT device
        """

        return self.device_address

    def search_bt_device(self):
        """
        Searches for the given BT device. If found, it calls the device address setter method to register its address
        """

        logging.debug(
            'Searching for BT Device Name: {}...'.format(self.device_name))

        # Get the list of nearby devices
        nearby_devices = bt.discover_devices()

        # Iterate through each address. If the name of one matches the given BT device's, then set it as the device address
        for each_address in nearby_devices:
            if self.device_name == bt.lookup_name(each_address):
                logging.debug('Found {} with address {}'.format(
                    self.device_name, each_address))
                self.set_device_address(each_address)
                return

        logging.warning('Could not find {}'.format(self.device_name))

    def connect_bt_device(self):
        """
        Connects to the BT device given its device address
        """

        # Get the BT device's address
        device_address = self.get_device_address()

        if device_address == None:
            logging.error("No device address currently stored")
        else:
            # Try connecting to the BT device
            try:
                logging.debug(
                    "Trying to connect to BT Device Address: {}...".format(device_address))

                # DBus object paths
                bluez_service = 'org.bluez'
                adapter_path = '/org/bluez/hci0'
                device_path = f"{adapter_path}/dev_{self.device_address.upper().replace(':', '_')}"

                # Setup DBus
                bus = pydbus.SystemBus()
                self.device = bus.get(bluez_service, device_path)

                self.device.Connect()

            except Exception:
                logging.error("Could not connect to BT Device Address: {}".format(
                    self.device_address), exc_info=True)

    def monitor_key_press(self):
        """
        Monitors input from the BT device
        """

        # Allow for the event input to show up
        time.sleep(2)

        # Read from the input device. When an click is registered, exit
        try:
            # Expected input event file
            input_event_path = max(
                glob.glob('/dev/input/event*'), key=os.path.getctime)
            dev = evdev.InputDevice(input_event_path)

            logging.debug("Connected to BT Device Address: {}".format(
                self.device_address))

            for event in dev.read_loop():
                # Click has been registered
                if event.type == evdev.ecodes.EV_KEY:
                    logging.debug('Keypress from Bluetooth Button detected!')
                    self.device.Disconnect()
                    logging.debug("Disonnected from BT Device Address: {}".format(
                        self.device_address))
                    return
        except:
            logging.error("Could read BT input", exc_info=True)


# Boolean for whether or not to continue the while loop in dummy_main_loop()
continue_loop = True


def dummy_main_loop():
    """
    Test loop to mimic a continuous process
    """

    while continue_loop:
        print('Ball-E Active')
        time.sleep(2)

    print("Ball-E Inactive")


def main():
    """
    Main prototype area. Code prototyping and checking happens here.
    """

    global continue_loop

    bt_helper = BtHelper()

    bt_helper.search_bt_device()

    device_address = bt_helper.get_device_address()

    # As long as a device address has been found
    if device_address != None:
        bt_helper.connect_bt_device()

        # Create 2 threads, one which monitors the keypress from the BT button and the other mimicing the main process
        t1 = threading.Thread(target=dummy_main_loop)
        t2 = threading.Thread(target=bt_helper.monitor_key_press)

        # Start the threads
        t1.start()
        t2.start()

        # If a key press has been registered, set the main loop to False
        t2.join()
        continue_loop = False


if __name__ == "__main__":
    # Run the main function
    main()
