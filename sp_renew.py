import math
import matplotlib.pyplot as plt
#----------------------------------------------------------------------------------
# Part1: methods that for extracting information between cities from document, the information includes
# cityCoordinateArray, cityNameArray and cityBinaryRelationshipArray
#----------------------------------------------------------------------------------
def readfile(tour,graph):
#read the content of the tour file, add city name and coordinates into list cityCoordinateArray
    ftour = open(tour,'r')


    cityCoordinateArray = []
    for line in ftour:
        c = line.split(';')
        for i in range(0,len(c)):
            c[i] = c[i].rstrip('\n')
        cityCoordinateArray.append(c)
    for i in range(len(cityCoordinateArray)):
        for j in range(1,len(cityCoordinateArray[0])):
            cityCoordinateArray[i][j] = int(cityCoordinateArray[i][j])
    ftour.close()
#read the content of graph file, create a cityname list,which is responsible for storing cities'names
#add original relationships between cities into matrix RlM

    fgraph = open(graph,'r')
    name = fgraph.readline()
    cityNameArray = name.split(';')
    for i in range(0,len(cityNameArray)):
        cityNameArray[i] = cityNameArray[i].rstrip('\n')
        cityNameArray[i] = cityNameArray[i].upper()
    cityNameArray = cityNameArray[1:]
    RlM = []
    for line in fgraph:
        rls = line.split(';')
        for i in range(len(rls)):
            rls[i] = rls[i].rstrip('\n')
        rls = rls[1:]
        RlM.append(rls)
    fgraph.close()
#convert the strings in RlM to number, put them into a new matrix cityBinaryRelationshipArray
#RlM is original binary matrix extracted from graph, it contains useless space
#create a new matrix called cityBinaryRelationshipArray that will store binary relationship between cities
    cityBinaryRelationshipArray = []
    for i in range(len(cityNameArray)):
        col = []
        for j in range(len(cityNameArray)):
            col.append(0)
        cityBinaryRelationshipArray.append(col)
    for j in range(len(cityNameArray)):
        for i in range(len(cityNameArray)):
            if RlM[i][j] == '0' or RlM[i][j] == '1':
                number = int(RlM[i][j])
                cityBinaryRelationshipArray[j][i] = number
                cityBinaryRelationshipArray[i][j] = number
    return cityCoordinateArray, cityNameArray, cityBinaryRelationshipArray

#---------------------------------------------------------------
# Part2: methods for caculating distance between any any two cities,which will used in map
#storing these distance into a matrix called cityDisRelationshipArray
#---------------------------------------------------------------

def getDistance(city1, city2):
    if city1 in cityNameArray and city2 in cityNameArray:
        for e in cityCoordinateArray:
            if e[0].upper() == city1.upper():
                coor1 = [e[1],e[2]]
            if e[0].upper() == city2.upper():
                coor2 = [e[1],e[2]]
    else:
        print('At least one city is not in our travel list')
#get the distance between two cities using their coordinate
    distance = math.sqrt((coor1[0] - coor2[0])**2 + (coor1[1] - coor2[1])**2)
    return distance
#get new relationship matrix with distance in it
def getCityDisRelationship(cityBinaryRelationshipArray, cityName):
    cityDisRelationshipArray=[]
    for i in range(len(cityName)):
        cityDisRelationshipArray.append([])
        for j in range(len(cityName)):
            if cityBinaryRelationshipArray[i][j]==1:
                 cityDisRelationshipArray[i].append(getDistance(cityName[i], cityName[j]))
            else:
                 cityDisRelationshipArray[i].append(0)
    return cityDisRelationshipArray

#-----------------------------------------------------------------------------------------
# Part3: methods for drawing cities' points on the map and drawing paths between any cities

#-----------------------------------------------------------------------------------------

def drawCity(cityCoordinateArray):
    for city in cityCoordinateArray:
        plt.plot(city[1],city[2],'ro')
        plt.text(city[1]+0.5,city[2]+0.5,city[0],fontsize=10)
    plt.axis([0,50,0,50])
#draw routes between cities
def darwPath(cityCoordinateArray,cityBinaryRelationshipArray):
#Draw paths between two cities if they are connected
#Dis is coordiante matrix
#R is binary distance matrix
    for i in range(len(cityBinaryRelationshipArray)):
        for j in range(i):
            cx=[]
            cy=[]
            if cityBinaryRelationshipArray[i][j]==1:
                cx.append(cityCoordinateArray[i][1])
                cx.append(cityCoordinateArray[j][1])
                cy.append(cityCoordinateArray[i][2])
                cy.append(cityCoordinateArray[j][2])
                plt.plot(cx, cy,'k--')
#-------------------------------------------------------------------------------------------------------------------------
# Part4: Construct Class path,which is used for storing information of each path.
# Construct Class Graph,which is responsible for calculating shortest path, second shortest path and third shortest path
# using the algorithm dijkstra

#-------------------------------------------------------------------------------------------------------------------------
class Path:
#initialize object path, the nodeList will be used to store all nodes for one path, each path is distinguished
#  by its nodeId(the nodeId is index of city in city name array )
# isInS is used to mark those cities which shortest path from the root has been confirmed
    def __init__(self,nodeId):
        self.nodeId=nodeId
        self.nodeList=[]
        self.isInS=False
        self.distance=10000
#setPathList is a static method in Class Path, which is used to generate a pathList to store paths for every city
# from the root
    def setPathList(nodeIdList):
        pathList=[]
        for e in nodeIdList:
            p=Path(e)
            pathList.append(p)
        return pathList

class Graph:
# shortestPathNodeList will be used for store the index of cities in the shortest path
# secondShortestPathNodeList will be used for store the index of cities in the second shortest path
    def __init__(self, cityDisRelationshipArray, cityIndexList):
        self.pathList=Path.setPathList(cityIndexList)
        self.pathDict={}
        self.cityDisRelationshipArray=cityDisRelationshipArray
        self.cityIndexList=cityIndexList
        self.shortestPathNodeList=None
        self.secondShortestNodeList=None
# this method is used to get the nodeId that has the shortest path from the root(startPoint)
    def getMinPath(self):
        minDistance=10000
        destNode=None
        for i in self.pathList:
            if i.distance<minDistance and i.isInS==False:
                minDistance=i.distance
                destNode=i.nodeId
        return destNode
    def iniPathDict(self,startNodeId):
        flag=False
#make sure the startPoint inputed from the keyboard is exist
#generate is dictionary,which key is nodeId, value is path for this nodeId
        for e in self.pathList:
            self.pathDict[e.nodeId]=e
            if(startNodeId==e.nodeId):
                flag=True
        if flag==False:
            print("No starNodeId exist")
            return
        for i in range(len(self.cityDisRelationshipArray[startNodeId])):
            distance=self.cityDisRelationshipArray[startNodeId][i]
#if distance is 0, that means there is no rute between two cities
            if distance ==0:
              continue
            else:
              path=self.pathDict[i]
              path.distance=distance
# add startNodeId to each path,because each path should contain startpoint
              path.nodeList.append(startNodeId)
# we don't need to consider the shortest path for startPoint, so mark the startpoint's shortest path to be true
        path=self.pathDict[startNodeId]
        path.isInS=True
    def getMinroute(self,startNodeId,destNodeId):
        if(startNodeId==destNodeId):
            return "StartNode is the same as the destNode. There is No Shortestdistance"
        self.iniPathDict(startNodeId)
        destNode=self.getMinPath()
        while destNode !=None:
#mark the city which shortest path has been made sure
            path=self.pathDict[destNode]
            path.isInS=True
            for i in range(len(self.cityDisRelationshipArray[destNode])):
                    distance=self.cityDisRelationshipArray[destNode][i]
                    if distance ==0:
                      continue
                    else:
                      if self.pathDict[i].distance>path.distance+distance:
                          self.pathDict[i].distance=path.distance+distance
                          self.pathDict[i].nodeList=path.nodeList+[destNode]
            destNode=self.getMinPath()
#when the loop finish and each shortest path route is extracted,find the destNodeId's shortest path
#return a String that has informaton of shortest path
        if len(self.pathDict[destNodeId].nodeList)>0:
            a=self.pathDict[destNodeId].nodeList+[destNodeId]
            self.shortestPathNodeList=a
            st='The Shortest Route is: '
            for i in range(len(a)):
                if i==len(a)-1:
                    st+=cityNameArray[a[i]]
                else:
                    st+= cityNameArray[a[i]] + '--' + str(getDistance(cityNameArray[a[i]], cityNameArray[a[i + 1]])) + '--'
            st+='. The Shortest Distance is: '+str(self.pathDict[destNodeId].distance)
            return st
        else:
            return 'There is No route between '+ str(cityNameArray[startNodeId]) + ' and ' + str(cityNameArray[destNodeId])
    def secondMinRoute(self,startNodeId,destNodeId):
        if startNodeId==destNodeId:
            return 'StartNode is the same as the destNode. There is No SecondShortestdistance'
        else:
            path=None
            distance=10000
            self.pathDict={}
            self.pathList=Path.setPathList(self.cityIndexList)
            self.getMinroute(startNodeId,destNodeId)
            if len(self.pathDict[destNodeId].nodeList)>0:
                shortestRoute=self.pathDict[destNodeId].nodeList+[destNodeId]
# using a loop to make any route in shortest path to be zero so to make the shortest path
# does not exist, than using dijkstra algorithm to get the shortest path and compare them to get
#the most shortest, this path will be the second shortest path
                for i in range(len(shortestRoute)-1):
#make one of the route between the shortest path which we have got to be zero in order to make the shortest not exist
                    temp=self.cityDisRelationshipArray[shortestRoute[i]][shortestRoute[i + 1]]
                    self.cityDisRelationshipArray[shortestRoute[i]][shortestRoute[i + 1]]=0
                    self.cityDisRelationshipArray[shortestRoute[i + 1]][shortestRoute[i]]=0
                    self.pathDict={}
                    self.pathList=Path.setPathList(self.cityIndexList)
                    self.getMinroute(startNodeId,destNodeId)
                    if self.pathDict[destNodeId].distance<=distance:
                        distance=self.pathDict[destNodeId].distance
                        path=self.pathDict[destNodeId]
                        cityIndex=i
#recover the route in the end of each loop
#find the second shortest path when the shortest path is not exist
# cityIndex is the city index
#it  means that when the route cityIndex to cityIndex+1 in the shortest is not exist
#we can find the second shortest path
                    self.cityDisRelationshipArray[shortestRoute[i]][shortestRoute[i + 1]]=temp
                    self.cityDisRelationshipArray[shortestRoute[i + 1]][shortestRoute[i]]=temp
                self.cityDisRelationshipArray[shortestRoute[cityIndex]][shortestRoute[cityIndex + 1]]=0
                self.cityDisRelationshipArray[shortestRoute[cityIndex + 1]][shortestRoute[cityIndex]]=0
#return a String that has informaton of second shortest path
                if len(self.pathDict[destNodeId].nodeList)>0:
                    a=path.nodeList+[destNodeId]
                    self.secondShortestNodeList=a
                    st='The SecondShortest route is: '
                    for i in range(len(a)):
                        if i==len(a)-1:
                            st+=cityNameArray[a[i]]
                        else:
                            st+= cityNameArray[a[i]] + '--' + str(getDistance(cityNameArray[a[i]], cityNameArray[a[i + 1]])) + '--'
                    st+='. The SecondShortest distance is: '+str(path.distance)

                    return st
                else:
                    return 'There is No SecondRoute between '+ str(cityNameArray[startNodeId]) + ' and ' + str(cityNameArray[destNodeId])
            else:
                return 'There is No SecondRoute between '+ str(cityNameArray[startNodeId]) + ' and ' + str(cityNameArray[destNodeId])
    def thirdMinRoute(self,startNodeId,destNodeId):
        if startNodeId==destNodeId:
            return 'StartNode is the same as the destNode. There is No ThirdShortestdistance'
        else:
            path=None
            distance=10000
            self.pathDict={}
            self.pathList=Path.setPathList(self.cityIndexList)
            self.getMinroute(startNodeId,destNodeId)
            shortestRoute=self.pathDict[destNodeId].nodeList+[destNodeId]
            for i in range(len(shortestRoute)-1):
                temp=self.cityDisRelationshipArray[shortestRoute[i]][shortestRoute[i + 1]]
                self.cityDisRelationshipArray[shortestRoute[i]][shortestRoute[i + 1]]=0
                self.cityDisRelationshipArray[shortestRoute[i + 1]][shortestRoute[i]]=0
                self.pathDict={}
                self.pathList=Path.setPathList(self.cityIndexList)
                self.getMinroute(startNodeId,destNodeId)
                if self.pathDict[destNodeId].distance<=distance:
                    distance=self.pathDict[destNodeId].distance
                    path=self.pathDict[destNodeId]
                self.cityDisRelationshipArray[shortestRoute[i]][shortestRoute[i + 1]]=temp
                self.cityDisRelationshipArray[shortestRoute[i + 1]][shortestRoute[i]]=temp
            if len(self.pathDict[destNodeId].nodeList)>0:
                a=path.nodeList+[destNodeId]
                st='The ThirdShortest route is: '
                for i in range(len(a)):
                    if i==len(a)-1:
                        st+=cityNameArray[a[i]]
                    else:
                        st+= cityNameArray[a[i]]  + '--' + str(getDistance(cityNameArray[a[i]], cityNameArray[a[i + 1]])) + '--'
                st+=' The ThirdShortest distance is: '+str(path.distance)

                return st
            else:
                return ''
#-----------------------------------------------------------------------------------------
# Part5: realize algorithm

#-----------------------------------------------------------------------------------------

namet=input("Please input the tour name:")
nameg=input("Please input the graph name:")
try:
    cityCoordinateArray, cityNameArray, cityBinaryRelationshipArray = readfile(namet, nameg)
    cityDisRelationshipArray = getCityDisRelationship(cityBinaryRelationshipArray, cityNameArray)
    print("You can choose from:")
    print(cityNameArray)
    cityIndexList = list(range(len(cityNameArray)))
    s=input("please input startPoint:")
    e=input("please input endPoint:")
    if s.upper() in cityNameArray and e.upper() in cityNameArray:
        startPoint=cityNameArray.index(s.upper())
        endPoint=cityNameArray.index(e.upper())
#because method in class will change cityDisRelationshipArray, so we create three object to prevent mistakes
        graph1=Graph(cityDisRelationshipArray, cityIndexList)
        graph2=Graph(cityDisRelationshipArray, cityIndexList)
        graph3=Graph(cityDisRelationshipArray, cityIndexList)
        print(graph1.getMinroute(startPoint,endPoint))
        print(graph2.secondMinRoute(startPoint,endPoint))
        print(graph3.thirdMinRoute(startPoint,endPoint))
        routePoints1 = len(graph1.shortestPathNodeList)
        routePoints2 = len(graph2.secondShortestNodeList)
#judge whether the shortest is exist
        if graph1.shortestPathNodeList!=None:
#state two array that will be used to store x and y for the cities' coordinate in the shortest path
            cx1=[]
            cy1=[]
            for n in range(routePoints1):
# cityIndex is the index of city in cityNameArray
# the order of the city in the cityNameArray is the same as the order of city in cityCoordinateArray
                cityIndex = graph1.shortestPathNodeList[n]
                cx1.append(cityCoordinateArray[cityIndex][1])
                cy1.append(cityCoordinateArray[cityIndex][2])
            plt.subplot(1,2,1)
            plt.plot(cx1, cy1,label='ShortestPath',color='b')
            darwPath(cityCoordinateArray, cityBinaryRelationshipArray)
            drawCity(cityCoordinateArray)
            plt.legend(loc="lower right")
            plt.xlabel('x')
            plt.ylabel('y')
            plt.title('City map and path')
#judge whether the second shortest is exist
        if graph2.secondShortestNodeList!=None:
            cx2=[]
            cy2=[]
            for cityPointers in range(routePoints2):
                city = graph2.secondShortestNodeList[cityPointers]
                cx2.append(cityCoordinateArray[city][1])
                cy2.append(cityCoordinateArray[city][2])
            plt.subplot(1,2,2)
            plt.plot(cx2, cy2,label='SecondShortestPath',color='r')
            darwPath(cityCoordinateArray, cityBinaryRelationshipArray)
            drawCity(cityCoordinateArray)
            plt.legend(loc="lower right")
            plt.xlabel('x')
            plt.ylabel('y')
            plt.title('City map and path')
        plt.show()
    else:
        print('startPoint or destination is not in map')
except IOError as e:
     print('can not find file')


