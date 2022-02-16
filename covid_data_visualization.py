# -*- coding: utf-8 -*-

import csv
import matplotlib.pyplot as plt
from datetime import datetime

DATASET_PATH = "time_series_covid19_confirmed_global.csv"

def load_dataset(filename):
    """This function loads the csv file and parse the data as dictionaries based on the existance of state, name of states, and the values
    contain number of cases in the country, or state of country if state exists.
    Arg: filename - name of the filename.
    Return: saved data in dictionary form.
    """
    data = {} #Start an empty dictionary
    with open(filename,'r') as fi:
        
        csv_fi1 = (csv.reader(fi))
        next(csv_fi1, None) #Skip header
        csv_fi = list(csv_fi1) #Make into a list so I can index
        
        for lines in range(len(csv_fi)): #Loop for number of rows
            
            #Parse the data
            state = csv_fi[lines][0]
            country = csv_fi[lines][1]
            cases = [int(i) for i in csv_fi[lines][4:]]

            if (csv_fi[lines][0]): #If the first column is not blank
                 
                if (country in data):   #If there has previously been a memory stored for this country               
                    data[country]["state_names"].append(state)      
                    data[country].update({state:cases})
                    
                else:                  
                    data.update({country:{"states":True,"state_names":[state], state:cases}})
            
            elif not(csv_fi[lines][0]): #If first column is blank
                
                if (country in data):  #If there has been states for this country               
                    data[country]["state_names"].append(country)      
                    data[country].update({country:cases})
                    
                else: #Use country as state name, and display country data
                    data.update({country:{"states":False,"state_names":[country], country:cases}})     
        return data
     
        
def get_latest_confirmed(dataset, country, state = None):
    """
    This function loads the data that was created in the previous function and returns the latest confirmed
    covid case.
    Arg: dataset - dictionary created from the previous function
         country - name of country to look for (str)
         state - name of state to look for. If there is no country, None is passed. (str)
    Return: latest - the value of the latest confirmed case. (int)
    """    
    
    if state != None:
        latest = dataset[country][state][-1]
    else:
        latest = dataset[country][country][-1]
        
    return latest

def get_timeline(dataset, country, state = None):
    """
    This function loads the data that was created in the previous function and returns the timeline of the covid
    case.
    Arg: dataset - dictionary created from the previous function
         country - name of country to look for (str)
         state - name of state to look for. If there is no country, None is passed. (str)
    Return: latest - the value of the latest confirmed case. (list)
    """
    
    if state != None:
        timeline = dataset[country][state]
    else:   
        timeline = dataset[country][country]
        
    return timeline

def get_dates(filename):
    """
    This function calls the csv file and returns the dates provided from the CSV file as an ordered list.
    Arg: filename - name of the csv file
    Return: ordered list of the dates provided from the CSV file.
    """
    
    with open(filename,'r') as fi:
        csv_fi = csv.reader(fi)
        csv_fi = list(csv_fi)
        dates = csv_fi[0][4:]
    return dates

def display_timeline(cases, dates, country, state= None):
    """
    This function display the confirmed COVID-19 cases for a particular country (and state) and
    represents a graphical display of the COVID-19 cases for the country/state.
    Arg: cases - 
    """
    x_axis = [int(i) for i in range(len(dates))]
    plt.plot(x_axis,cases)
    frequency = 15
    plt.xticks(x_axis[::frequency],dates[::frequency],rotation=45)
    
    if state != None:
        plt.title('Confirmed COVID-19 Test Cases for ' + country + ', ' + state)    
    else:   
        plt.title('Confirmed COVID-19 Test Cases for ' + country)
    plt.show()
    
def main():
    """
    This function runs all the function written above. Asks user for options 1/2, and calls either the function get_timeline
    or get_latest_confirmed. If the input is invalid, runs input until user inputs a correct country/state. Prints the outcome.
    """
    dataset = load_dataset(DATASET_PATH)
    option = int(input("Enter menu option 1,2,3: "))
    
    if option == 1:
        
        country_name = input("Input country: ")
        
        while not(country_name in dataset.keys()):            
           country_name = input("Input country: ") 
        
        if (dataset[country_name]["states"]):            
            state_name = input("Input state: ")
            
            while not(state_name in dataset[country_name]["state_names"]):               
                state_name = input("Input state: ")
        
            print(get_latest_confirmed(dataset,country_name,state_name))
            
        elif not(dataset[country_name]["states"]):
            print(get_latest_confirmed(dataset,country_name))
                
        
    elif option == 2:
        
        country_name = input("Input country: ")
        
        while not(country_name in dataset.keys()):           
           country_name = input("Input country: ") 
        
        if (dataset[country_name]["states"]):           
            state_name = input("Input state: ")
            
            while not(state_name in dataset[country_name]["state_names"]):               
                state_name = input("Input state: ")
        
            print(get_timeline(dataset,country_name,state_name))
        
        elif not(dataset[country_name]["states"]):
            print(get_timeline(dataset,country_name))   

    elif option == 3:
        
        country_name = input("Input country: ")
        
        while not(country_name in dataset.keys()):           
           country_name = input("Input country: ") 
        
        dates = get_dates(DATASET_PATH)
        
        if (dataset[country_name]["states"]):           
            state_name = input("Input state: ")
            
            while not(state_name in dataset[country_name]["state_names"]):               
                state_name = input("Input state: ")
            
            cases = get_timeline(dataset,country_name,state_name)
            display_timeline(cases, dates, country_name,state_name)
        
        elif not(dataset[country_name]["states"]):
            
            cases = get_timeline(dataset,country_name)
            display_timeline(cases, dates, country_name)
        
if __name__ == '__main__':
    main()

