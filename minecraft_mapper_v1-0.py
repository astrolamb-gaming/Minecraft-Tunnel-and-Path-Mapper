### Minecraft Map Maker
# Copyright (C) 2016 AstroLamb

# This program is a free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.





from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from visual import *
import math


#import Coordinate_input_test


__version__ = "1.0"

## Setting up visual


scene.title = "Minecraft Tunnel and Path Map"
scene.height = 600
scene.width = 600
scene.range = (100,100,100)
scene.autoscale = 0
scene.center = (0,0,0)

running = True

feature_objects = []
featurelist = [] #Array of all features.

def featuredata(featurelist,feature_objects):
    ## Opens featuredata.dat file and extracts the data inside for use in the 3d model
    count = 0
    fdr = open('featuredata.dat','r+')
    fda = open('featuredata.dat','a+')
    fdata = fdr.readlines()
    print("Opened featuredata.dat")
    for line in fdata:
        if len(line) > 2: ## Doesn't include newlines, 2 is arbitrary. 1 would work, but I wanted to be on the safe side. The min really should be 7 (feature, coords, and whitespaces for one set of coords), but I went with 2.
            print(line)
            ilist = str_list2int_list(line)
            featurelist.append(ilist)
            print("Printing ilist...")
            print(ilist)

        ## Adds feature objects
        
        newfeat = add_feature(fda,ilist,1)
        feature_objects.append(newfeat)    
        
    #from_featuredata = 0
    print("featuredata() complete. Beginning while loop.")
    return(fdr,fda,featurelist,feature_objects)

def close_featuredata(fdr,fda):
    fdr.close()
    fda.close()
    


def getFeature():
    #determines based on user input what type of feature (path, wall,
    #building, cave, other features to be added?) is being added by the user.

    # Assume for now that the feature is a linear path.

    #1 = linear path
    #2 = nonlinear path
    #3 = building
    #4 = cave
    #5 = wall

## Add this stuff when 
    
##    print("What type of feature do you want to add?")
##    print("Your options:")
##    print("1. Linear path")
##    print("2. Nonlinear path")
##    print("3. Building")
##    print("4. Cave")
##    print("5. Wall")
##    feat = raw_input("Input the number corresponding to the feature you want.")
    
    feat = 1
    return feat

def str_list2int_list(stringlist):
    #stringlist is a set of numbers in a string
    #str_list2int_lits() converts it to a list of integers
    #returns a list of integers
    slist = stringlist.split()
    ilist = []
    for i in slist:
        ilist.append(int(i))
    return ilist

class add_feature:
    #Defines object as straight tunnel or path
    def __init__(self, fda, ilist, from_featuredata=0):
        self.coords = []
        ## n refers to the line number in featuredata.dat. Default is 0.
        ## fda is the file to write new features to
        ## featurelist is the list of features present, with the data for each feature in a list of integers.
        ## from_featuredata determines whether or not the data comes from featuredata. Default is 0, coming from user input instead.
        if from_featuredata == 1:
            self.coords = ilist[1:]
            print("add_feature.coords =")
            print(self.coords)
            self.feature = ilist[0]
            print("add_feature.feature =")
            print(self.feature)
       
        else:
            self.feature = getFeature()
            if self.feature == 1:
                
                print("Coordinates of the 1st point, please.")
                co1 = getCoords()
                print("Coordinates of the 2nd point, please.")
                co2 = getCoords()
                self.coords = co1 + co2

        ## Create lines
        num_coords = len(self.coords)
        print("num_coords =")
        print(num_coords)
        if num_coords % 3 != 0:
            print("Error: the number of coordinates is wrong somehow.")
            self.__init__(fda,ilist,from_featuredata)
        num = num_coords/3
        self.lines = []
        while num > 1:
        #######################################################################
            ## Changed from shapes.line to curve
            print("Adding line object")
            line = curve(pos=[[self.coords[int(num*3-6)],
                              self.coords[int(3*num-5)],
                              self.coords[int(3*num-4)]],
                              [self.coords[int(3*num-3)],
                              self.coords[int(3*num-2)],
                              self.coords[int(3*num-1)]]], radius=0.5)
            self.lines.append(line)
            num -= 2

        ## Adds new feature to featuredata.dat if data is not already there.
        if from_featuredata == 0:
            
            outstring = ''
            a = str(self.feature) + ' '
            fda.write(a)
            for i in self.coords:
                outstring = outstring + str(i) + ' '
            fda.write(outstring)
            fda.write('\n')


def getCoords(): #gets coordinates

    #getCoords() takes user input and converts the string to coordinates.
    #Returns a list of 3 integers.
    
    _loc = [0,0,0]
    count_ = 0
    x = 0
    y = 0
    z = 0
    #returns x,y,z coordinates indicated by the minecraft debug menu (F3)
    print("What are the x, y, and z coordinates, in the following format: \n -20 50 18")
    coords = raw_input("Press F3 and look for 'Blocks':  ")
    coords_list = str_list2int_list(coords)
    print("coords_list from getCoords() =")
    print(coords_list)
    return coords_list

def keyInput(evt):
    ## Allows for keyboard input.
    s = evt.key
    print("s =")
    print(s)
    
    if s == 'up':
        scene.center.y += 1 # The up arrow moves the camera up.
    elif s == 'down':
        scene.center.y -= 1 # The down arrow moves the camera down.
    elif s == 'esc':
        running = False
    elif s == '=':
        
        new = add_feature(fda,featurelist,0)
        feature_objects.append(new)
    else:
        print("No can do, for now.")
    


    
fdr,fda,featurelist,feature_objects = featuredata(featurelist,feature_objects)

print("Featurelist =")
print(featurelist)

##Stuff for roaming
rhairs = 0.025 # half-length of crosshairs
dhairs = 2 # how far away the crosshairs are
maxcosine = dhairs/sqrt(rhairs**2+dhairs**2) # if ray inside crosshairs, don't move
haircolor = color.black
roam = 0
scene.bind('keydown', keyInput)
print("Beggining While loop")
while running == True:

    # Toggle roam option
    if scene.mouse.events:
        m = scene.mouse.getevent()
        if m.press or m.drag:
            roam = True
        elif m.release or m.drop:
            roam = False

    # If in roaming mode, change center and forward according to mouse position
    if roam:
        ray = scene.mouse.ray
        if abs(dot(ray,scene.forward)) < maxcosine: # do something only if outside crosshairs
            newray = norm(vector(ray.x, 0, ray.z))
            angle = arcsin(dot(cross(scene.forward,newray),scene.up))
            newforward = rotate(scene.forward, axis=scene.up, angle=angle/30)
            scene.center = scene.mouse.camera+newforward*mag(scene.center-scene.mouse.camera)
            scene.forward = newforward
            scene.center = scene.center+scene.forward*ray.y/2.
    rate(50)

close_featuredata(fdr,fda)
print("Closing featuredata.dat")
scene.visible = False
del scene
exit()
