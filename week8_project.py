import os
import random
import pandas as pd
import numpy as np
from PIL import Image
from PIL import GifImagePlugin
from PIL import ImageFont
from PIL import ImageDraw 

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

class Customer():

    def __init__(self, simulation_from, simulation_to):
        ## erzeuge einen Customer am Tag <weekday> mit zufälligem Eintrittszeitpunkt
        ## zwischen Simulationsstart und /-ende

        weekday = pd.to_datetime(simulation_from).strftime("%A").lower()
        entry = random.choice(pd.date_range(simulation_from, simulation_to, freq="min"))

        #print(entry)

        transition_matrices = {'monday': {'checkout': [1, 0, 0, 0, 0],
                                    'dairy': [0.21572720946416143,
                                    0.8433344145313006,
                                    0.12011019283746556,
                                    0.08832188420019627,
                                    0.19365079365079366],
                                    'drinks': [0.2964509394572025,
                                    0.007460265974699967,
                                    0.6887052341597796,
                                    0.09126594700686948,
                                    0.17142857142857143],
                                    'fruits': [0.36464857341684065,
                                    0.07298086279597794,
                                    0.07162534435261708,
                                    0.7620215897939157,
                                    0.1291005291005291],
                                    'spices': [0.12317327766179541,
                                    0.07622445669802141,
                                    0.11955922865013774,
                                    0.058390578999018644,
                                    0.5058201058201058]},
                      'tuesday': {'checkout': [1, 0, 0, 0, 0],
                                    'dairy': [0.2612676056338028,
                                    0.8374917925147735,
                                    0.1206896551724138,
                                    0.09369771332961517,
                                    0.2012847965738758],
                                    'drinks': [0.27887323943661974,
                                    0.005581089954038083,
                                    0.6730769230769231,
                                    0.08310094813162298,
                                    0.16167023554603854],
                                    'fruits': [0.3429577464788732,
                                    0.07616546290216678,
                                    0.08554376657824933,
                                    0.7674288901282766,
                                    0.13704496788008566],
                                    'spices': [0.11690140845070422,
                                    0.08076165462902167,
                                    0.1206896551724138,
                                    0.05577244841048522,
                                    0.5]},
                       'wednesday': {'checkout': [1, 0, 0, 0, 0],
                                    'dairy': [0.2595019659239843,
                                    0.8383139351997484,
                                    0.12193698949824971,
                                    0.0911966262519768,
                                    0.1991869918699187],
                                    'drinks': [0.26605504587155965,
                                    0.007549543881723813,
                                    0.6872812135355892,
                                    0.09699525566684239,
                                    0.16361788617886178],
                                    'fruits': [0.3492791612057667,
                                    0.07989933941491036,
                                    0.07701283547257877,
                                    0.7554032683183974,
                                    0.12398373983739837],
                                    'spices': [0.1251638269986894,
                                    0.0742371815036175,
                                    0.11376896149358226,
                                    0.05640484976278334,
                                    0.5132113821138211]},
                        'thursday': {'checkout': [1, 0, 0, 0, 0],
                                    'dairy': [0.24869451697127937,
                                    0.8425584255842559,
                                    0.12673506336753168,
                                    0.09282296650717703,
                                    0.16857142857142857],
                                    'drinks': [0.27219321148825065,
                                    0.006765067650676507,
                                    0.6632468316234158,
                                    0.07751196172248803,
                                    0.16666666666666666],
                                    'fruits': [0.34464751958224543,
                                    0.07226322263222633,
                                    0.08328304164152082,
                                    0.7727272727272727,
                                    0.13333333333333333],
                                    'spices': [0.13446475195822455,
                                    0.07841328413284133,
                                    0.12673506336753168,
                                    0.056937799043062204,
                                    0.5314285714285715]},
                        'friday': {'checkout': [1, 0, 0, 0, 0],
                                    'dairy': [0.24434087882822902,
                                    0.8262284412626099,
                                    0.11752249867654843,
                                    0.08221153846153846,
                                    0.16666666666666666],
                                    'drinks': [0.3002663115845539,
                                    0.006508298080052067,
                                    0.6770778189518264,
                                    0.08365384615384615,
                                    0.1942800788954635],
                                    'fruits': [0.3215712383488682,
                                    0.0888382687927107,
                                    0.08893594494441504,
                                    0.7735576923076923,
                                    0.1301775147928994],
                                    'spices': [0.13382157123834887,
                                    0.0784249918646274,
                                    0.11646373742721017,
                                    0.06057692307692308,
                                    0.5088757396449705]}
        }

        self.path = self.customer_transitions(transition_matrices[weekday], entry)

    def customer_transitions(self, P, entry):
        stations = ['checkout','dairy','drinks','fruits','spices']
        state = random.choices(stations[1:], weights=[0.287, 0.153, 0.377, 0.181])[0]
        result = {entry.strftime("%X"): state}
        timestamp = entry
        confid = 1
        while state != 'checkout':
            timestamp = timestamp + pd.Timedelta(seconds=60) ## eine Minute addieren
            weights = P[state]
            state = random.choices(stations, weights=weights)[0]
            index = stations.index(state)
            confid = (confid + np.abs((weights[index]-0.5)*2))/2
            result[timestamp.strftime("%X")] = state
        result[(timestamp + pd.Timedelta(seconds=60)).strftime("%X")] = 'checkout'
        result[(timestamp + pd.Timedelta(seconds=120)).strftime("%X")] = 'checkout'
        self.conf = confid
        return result

        # self.path = {'11:01:00': 'fruits',
        #             '11:02:00': 'fruits',
        #             '11:03:00': 'drinks',
        #             '11:04:00': 'dairy',
        #             '11:05:00': 'checkout'}
        # self.id = 12345
        # self.name = 'Johnny Depp'


class Supermarket():

    def __init__(self, simulation_from, simulation_to, no_of_customer):
        self.load_cust_images()

        self.im = Image.open(cwd+'/week_08/supermarket.jpg')
        self.shelves = Shelves()
        self.goods = Goods()
        self.customers = []
        for _ in range(no_of_customer):
            self.customers.append(Customer(simulation_from, simulation_to))

        self.fill_shelves()

        self.revenue_matrix = {"dairy"  : [5, 0],
                          "drinks" : [6, 0],
                          "fruits" : [4, 0],
                          "spices" : [3, 0],
                          "checkout": [0, 0]}

        self.turnover = 0
    
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
            cust1 = im_arr[y:y+32, x:x+32].copy()
            yell_cust_im = Image.fromarray(cust1)
            cust2 = im_arr[y:y+32, x:x+32].copy()
            cust2[:,:,0] = 0
            cust2[:,:,2] = 0
            green_cust_im = Image.fromarray(cust2)
            cust3 = im_arr[y:y+32, x:x+32].copy()
            cust3[:,:,1] = 0
            cust3[:,:,2] = 0        
            red_cust_im = Image.fromarray(cust3)
            self.cust_im = [green_cust_im, yell_cust_im, red_cust_im]

    def reset_cust_spots(self):
        self.cust_spots = {'drinks': {(3,3):0 , (3,4): 0, (3,5): 0, (3,6): 0, (3,7): 0,
                                        (4,3): 0, (4,4): 0, (4,5): 0, (4,6): 0, (4,7): 0},
                            'dairy':  {(7,3): 0, (7,4): 0, (7,5): 0, (7,6): 0, (7,7): 0,
                                        (8,3): 0, (8,4): 0, (8,5): 0, (8,6): 0, (8,7): 0},
                            'spices': {(11,3): 0, (11,4): 0, (11,5): 0, (11,6): 0, (11,7): 0,
                                        (12,3): 0, (12,4): 0, (12,5): 0, (12,6): 0, (12,7): 0},
                            'fruits': {(15,3): 0, (15,4): 0, (15,5): 0, (15,6): 0, (15,7): 0,
                                        (16,3): 0, (16,4): 0, (16,5): 0, (16,6): 0, (16,7): 0},
                            'checkout': {(4,9): 0, (4,10): 0, (8,9): 0, (8,10): 0, (12,9): 0, (12,10): 0}
                            }

    def move_customers(self, timestamp):
        self.reset_cust_spots()
        base_map = self.im.copy()
        conf = 0
        for cust in self.customers:
            if timestamp.strftime("%X") in cust.path.keys():
                #print(timestamp.strftime("%X"), cust.path[timestamp.strftime("%X")])
                location = cust.path[timestamp.strftime("%X")]
                base_map = self.set_cust_im_to_map(base_map, cust.path[timestamp.strftime("%X")])
                self.turnover += self.revenue_matrix[location][0]
                self.revenue_matrix[location][1] += self.revenue_matrix[location][0]
            conf += cust.conf
        conf = conf / len(self.customers)
        draw = ImageDraw.Draw(base_map)
        font = ImageFont.truetype("arial.ttf", 28, encoding="unic")
        draw.text((455, 490),timestamp.strftime("%X"),(255,255,255), font=font)
        draw.text((10, 390),'Confidence Score: '+str(np.round(conf,3)),(0,255,0), font=font)
        draw.text((10, 440),'Total Revenue: '+str(np.round(self.turnover,3)),(255,255,255), font=font)
        font = ImageFont.truetype("arial.ttf", 20, encoding="unic")
        draw.text((120, 480),'Dairy: '+str(np.round(self.revenue_matrix['dairy'][1],3)),(255,255,255), font=font)
        draw.text((10, 480),'Drinks: '+str(np.round(self.revenue_matrix['drinks'][1],3)),(255,255,255), font=font)
        draw.text((330, 480),'Fruits: '+str(np.round(self.revenue_matrix['fruits'][1],3)),(255,255,255), font=font)
        draw.text((220, 480),'Spices: '+str(np.round(self.revenue_matrix['spices'][1],3)),(255,255,255), font=font)
        draw = None
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

    simulation_from = "2020-10-05 11:00"
    simulation_to   = "2020-10-05 11:30"
    no_of_customer = 50

    market = Supermarket(simulation_from, simulation_to, no_of_customer)
    market.im.save(cwd+'/week_08/ergebnis.png')

    frames = []
    for i in pd.date_range(simulation_from, simulation_to, freq="min"):
        cust_im = market.move_customers(i)
        frames.append(cust_im)
        #cust_im.save(cwd+'/week_08/pics/'+i.strftime("%X").replace(':','_')+'.png')

    frames[0].save(cwd+'/week_08/pics/out.gif', format='GIF', save_all=True, append_images=frames[1:], duration=650, loop=0)

    for cust in market.customers:
        print(cust.conf)





