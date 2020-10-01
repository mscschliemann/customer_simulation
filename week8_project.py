
import pandas as pd
from PIL import Image
import numpy as np
import os
import random

cwd = os.getcwd()

class Goods():

    def __init__(self):
        self.goods = {'drinks': [(9,4), (9,5), (9,6), (13,6)],
                        'dairy':  [(12,2), (12,3), (12,4), (12,5)],
                        'spices': [(3,1), (3,2), (10,0), (10,3)],
                        'fruits': [(4,0), (4,1), (4,2), (4,3), (4,4)]}



        self.im = Image.open(cwd+'/week_08/tiles.png')

    def get_goods_images(self, location):
        x, y = random.choice(self.goods[location])
        x*=32
        y*=32
        tiles = np.array(self.im)
        return Image.fromarray(tiles[y:y+32, x:x+32])

    def get_good_by_location(self, location):
        return random.choice(self.goods[location])


class Shelves():

    def __init__(self):
        self.shelves = {'drinks': {(2,3): 'empty', (2,4): 'empty', (2,5): 'empty', (2,6): 'empty', (2,7): 'empty',
                                    (5,3): 'empty', (5,4): 'empty', (5,5): 'empty', (5,6): 'empty', (5,7): 'empty'},
                        'dairy':  {(6,3): 'empty', (6,4): 'empty', (6,5): 'empty', (6,6): 'empty', (6,7): 'empty',
                                    (9,3): 'empty', (9,4): 'empty', (9,5): 'empty', (9,6): 'empty', (9,7): 'empty'},
                        'spices': {(10,3): 'empty', (10,4): 'empty', (10,5): 'empty', (10,6): 'empty', (10,7): 'empty',
                                    (13,3): 'empty', (13,4): 'empty', (13,5): 'empty', (13,6): 'empty', (13,7): 'empty'},
                        'fruits': {(14,3): 'empty', (14,4): 'empty', (14,5): 'empty', (14,6): 'empty', (14,7): 'empty',
                                    (17,3): 'empty', (17,4): 'empty', (17,5): 'empty', (17,6): 'empty', (17,7): 'empty'}}

    def get_locations(self):
        return self.shelves.keys()
    
    def fill_shelf(self, market, location, good):
        x,y = (list(self.shelves[location].keys())[list(self.shelves[location].values()).index('empty')]) 
        self.shelves[location][(x,y)]='X'
        tx = (x-1) * 32
        ty = (y-1) * 32
        market_arr = np.array(market)
        good_arr = np.array(good)
        market_arr[ty:ty+32, tx:tx+32] = good_arr
        return Image.fromarray(market_arr)

    def fill_shelves(self):
        ...

class Customers():

    def __init__(self, simulation_from, simulation_to):
        ## erzeuge einen Customer am Tag <weekday> mit zufälligem Eintrittszeitpunkt
        ## zwischen Simulationsstart und /-ende

        weekday = pd.to_datetime(simulation_from).strftime("%A").lower()
        entry = random.choice(pd.date_range(simulation_from, simulation_to, freq="min"))

        print(entry)

        self.path = {'11:01:00': 'fruits',
                    '11:02:00': 'fruits',
                    '11:03:00': 'drinks',
                    '11:04:00': 'dairy',
                    '11:05:00': 'checkout'}
        self.id = 12345
        self.name = 'Johnny Depp'


class Supermarket():

    def __init__(self, simulation_from, simulation_to):
        self.load_cust_images()

        self.im = Image.open(cwd+'/week_08/supermarket.png')
        self.shelves = Shelves()
        self.goods = Goods()
        self.customers = []
        for _ in range(5):
            self.customers.append(Customers(simulation_from, simulation_to))

        self.fill_shelves()
    
    def fill_shelves(self):
        for i in self.shelves.get_locations():
            for _ in range(10):
                goods_image = self.goods.get_goods_images(i)
                self.im = self.shelves.fill_shelf(self.im, i, goods_image)
    
    def load_cust_images(self):
            im = Image.open(cwd+'/week_08/tiles.png')
            im_arr = np.array(im)
            x = 1 * 32
            y = 3 * 32
            cust = im_arr[y:y+32, x:x+32]
            yell_cust_im = Image.fromarray(cust)
            cust[:,:,0] = 0
            cust[:,:,2] = 0
            green_cust_im = Image.fromarray(cust)
            cust[:,:,1] = 0
            cust[:,:,2] = 0        
            red_cust_im = Image.fromarray(cust)
            self.cust_im = [green_cust_im, yell_cust_im, red_cust_im]

    def reset_cust_spots(self):
        self.cust_spots = {'drinks': {(3,3): 0, (3,4): 0, (3,5): 0, (3,6): 0, (3,7): 0,
                                (4,3): 0, (4,4): 0, (4,5): 0, (4,6): 0, (4,7): 0},
                    'dairy':  {(7,3): 0, (7,4): 0, (7,5): 0, (7,6): 0, (7,7): 0,
                                (8,3): 0, (8,4): 0, (8,5): 0, (8,6): 0, (8,7): 0},
                    'spices': {(11,3): 0, (11,4): 0, (11,5): 0, (11,6): 0, (11,7): 0,
                                (12,3): 0, (12,4): 0, (12,5): 0, (12,6): 0, (12,7): 0},
                    'fruits': {(15,3): 0, (15,4): 0, (15,5): 0, (15,6): 0, (15,7): 0,
                                (16,3): 0, (16,4): 0, (16,5): 0, (16,6): 0, (16,7): 0}}

    def move_customers(self, timestamp):
        self.reset_cust_spots()
        base_map = self.im
        for cust in self.customers:
            if timestamp.strftime("%X") in cust.path.keys():
                print(cust.path[timestamp.strftime("%X")])
                base_map = self.set_cust_im_to_map(base_map, cust.path[timestamp.strftime("%X")])
        return base_map

    def set_cust_im_to_map(self, map, location):
        # get next free cust spot at location
        fill_level = list(self.cust_spots[location].values())[-1]
        x,y = (list(self.cust_spots[location].keys())[list(self.cust_spots[location].values()).index(fill_level)]) 
        self.cust_spots[location][(x,y)] = fill_level + 1
        tx = (x-1) * 32
        ty = (y-1) * 32
        map_array = np.array(map)
        cust_im_array = np.array(self.cust_im[fill_level])
        map_array[ty:ty+32, tx:tx+32] = cust_im_array
        new_map = Image.fromarray(map_array)
        return new_map

    
if __name__ == '__main__':

    simulation_from = "2020-09-30 11:00"
    simulation_to   = "2020-09-30 12:00"

    weekday = pd.to_datetime(simulation_from).strftime("%A").lower()

    market = Supermarket(simulation_from, simulation_to)
    market.im.save(cwd+'/week_08/ergebnis.png')

    for i in pd.date_range(simulation_from, simulation_to, freq="min"):
        cust_im = market.move_customers(i)
        #print(i.strftime("%X"), i.strftime("%A").lower())

    cust_im.show()







