# Your name: Syeda Reza
# Your student id: 4782 7700
# Your email: syerez@umich.edu
# List who you have worked with on this homework: Elijah Cantu

import matplotlib.pyplot as plt

import os
import sqlite3
import unittest
import operator

def load_rest_data(db):
    """
    This function accepts the file name of a database as a parameter and returns a nested
    dictionary. Each outer key of the dictionary is the name of each restaurant in the database, 
    and each inner key is a dictionary, where the key:value pairs should be the category, 
    building, and rating for the restaurant.
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    cur = conn.cursor()

    cur.execute('SELECT name, rating, category_id, building_id FROM restaurants')
    dataTable = cur.fetchall()
    cur.execute('SELECT id, category FROM categories')
    categoryGroup = cur.fetchall()
    cur.execute('SELECT id, building FROM buildings')
    buildingsGroup = cur.fetchall()
    conn.commit()
    
    finalDict = {}
    #count = 0
    for item in dataTable:
        innerDict = {}
        
        for row in categoryGroup:
            if row[0] == item[2]:
                innerDict['category'] = row[1]

        for row in buildingsGroup:
            if row[0] == item[3]:
                innerDict['building'] = row[1]
        innerDict['rating'] = float(item[1])
        finalDict[item[0]] = innerDict
        #if count == 0:
            #print(finalDict)
            #count+=1


        #swapping positions of category and building keys
        #res.clear()
        #print(finalDict)
        print(finalDict)

    return finalDict

def plot_rest_categories(db):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    cur = conn.cursor()
    cur.execute('SELECT categories.category, categories.id FROM categories')
    categories = cur.fetchall()
    conn.commit()

    cur.execute('SELECT category_id, COUNT(*) as COUNT FROM restaurants GROUP BY CATEGORY_ID')
    number = cur.fetchall()
    conn.commit()

    categories = {}
    index = 0
    for category in categories:
        categories[category[0]] = number[index][1]
        index += 1

    restCategories= dict(sorted(categories.items()))
    decRestCats = dict(sorted(categories.items(), key=lambda item: item[1], reverse=False))
    restaurants = list(decRestCats.keys())
    numofRests = list(decRestCats.values())

    plt.barh(restaurants, numofRests)
    plt.title('Type of Restaurant on South University Ave')
    plt.xlabel('Number of Restaurants')
    plt.ylabel('Restaurant Categories')
    plt.tight_layout()
    plt.show()
    plt.savefig("plot_rest.png")

    return restCategories

def find_rest_in_building(building_num, db):
    '''
    This function accepts the building number and the filename of the database as parameters and returns a list of 
    restaurant names. You need to find all the restaurant names which are in the specific building. The restaurants 
    should be sorted by their rating from highest to lowest.
    '''
    result = []
    ratingAndName = {}
    database = load_rest_data(db)
    #print(database)
    tuples = database.items()
    #print(tuples)
    for item in tuples: 
        if item[1]['building'] == building_num:
            ratingAndName[item[0]] = item[1]['rating']
    
    sorted_ratingNName = dict( sorted(ratingAndName.items(), key=operator.itemgetter(1),reverse=True))
    
    for item in sorted_ratingNName.keys():
        result.append(item)

    return result


    #d = {1: 2, 3: 4, 4: 3, 2: 1, 0: 0}
    #print('Original dictionary : ', d)
    #sorted_d = sorted(d.items(), key=operator.itemgetter(1))
    #print('Dictionary in ascending order by value : ',sorted_d)
    #sorted_d = dict( sorted(d.items(), key=operator.itemgetter(1),reverse=True))
    #print('Dictionary in descending order by value : ',sorted_d)

    pass

#EXTRA CREDIT
def get_highest_rating(db): #Do this through DB as well
    """
    This function return a list of two tuples. The first tuple contains the highest-rated restaurant category 
    and the average rating of the restaurants in that category, and the second tuple contains the building number 
    which has the highest rating of restaurants and its average rating.

    This function should also plot two barcharts in one figure. The first bar chart displays the categories 
    along the y-axis and their ratings along the x-axis in descending order (by rating).
    The second bar chart displays the buildings along the y-axis and their ratings along the x-axis 
    in descending order (by rating).
    """
    pass

#Try calling your functions here
def main():
    plot_rest_categories('South_U_Restaurants.db')

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.highest_rating = [('Deli', 4.6), (1335, 4.8)]

    def test_load_rest_data(self):
        rest_data = load_rest_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, dict)
        self.assertEqual(rest_data['M-36 Coffee Roasters Cafe'], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_plot_rest_categories(self):
        cat_data = plot_rest_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_find_rest_in_building(self):
        restaurant_list = find_rest_in_building(1140, 'South_U_Restaurants.db')
        self.assertIsInstance(restaurant_list, list)
        self.assertEqual(len(restaurant_list), 3)
        self.assertEqual(restaurant_list[0], 'BTB Burrito')

    def test_get_highest_rating(self):
        highest_rating = get_highest_rating('South_U_Restaurants.db')
        self.assertEqual(highest_rating, self.highest_rating)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
