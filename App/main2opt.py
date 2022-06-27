import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from time import * 

def distance(point1, point2):
    return geodesic(point1,point2).km

# Giao điểm giữa hai đoạn
def intersects(p1, q1, p2, q2):
    def on_segment(p, q, r):
        if r[0] <= max(p[0], q[0]) and r[0] >= min(p[0], q[0]) and r[1] <= max(p[1], q[1]) and r[1] >= min(p[1], q[1]):
            return True
        return False

    def orientation(p, q, r):
        val = ((q[1] - p[1]) * (r[0] - q[0])) - ((q[0] - p[0]) * (r[1] - q[1]))
        if val == 0 : return 0
        return 1 if val > 0 else -1

    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if o1 != o2 and o3 != o4:
        return True

    if o1 == 0 and on_segment(p1, q1, p2) : return True
    if o2 == 0 and on_segment(p1, q1, q2) : return True
    if o3 == 0 and on_segment(p2, q2, p1) : return True
    if o4 == 0 and on_segment(p2, q2, q1) : return True

    return False

#Khoảng cách sử dụng Double Linked Node
class Node:
    def __init__(self, dataval=None):
        self.dataval = dataval
        self.prevval = None
        self.nextval = None

class TSP_TimeTraveler():
    def __init__(self):
        self.count = 0
        self.position = None
        self.length = 0
        self.traveler = None
        self.travelert_past = None
        self.is_2opt = True

    def get_position(self):
        return self.position

    def traveler_init(self):
        self.traveler = self.position
        self.travelert_past = self.position.prevval
        return self.traveler


    def traveler_next(self):
        if self.traveler.nextval != self.travelert_past:
            self.travelert_past = self.traveler
            self.traveler = self.traveler.nextval
            return self.traveler, False
        else :
            self.travelert_past = self.traveler
            self.traveler = self.traveler.prevval
            return self.traveler, True 

    # thêm một điểm vào tuyến đường hiện tại:
    def add_city(self, point):
        node = Node(point)
        if self.count <=0 :
            self.position = node
        elif self.count == 1 :
            node.nextval = self.position
            node.prevval = node
            self.position.nextval = node
            self.position.prevval = self.position
            self.length = distance(self.position.dataval,node.dataval)
        elif self.count == 2 :
            node.nextval = self.position.nextval
            node.prevval = self.position
            self.position.nextval.prevval = node
            self.position.nextval = node
            self.length = distance(self.position.dataval,node.dataval)
        else : 
            # Tạo chuyến du lịch
            traveler = self.traveler_init()

            c = traveler #vị trí hiện tại
            prev = False # liên kết ngược

            n, prev = self.traveler_next()

            # Tính toán độ dài của việc thêm điểm vào con đường
            Min_prev = prev
            Min_L = self.length-distance(c.dataval,n.dataval)+distance(c.dataval,node.dataval)+distance(node.dataval,n.dataval)
            Min_Node = c

            traveler = n

            while traveler != self.position :
                c = n #vị trí hiện tại

                n, prev = self.traveler_next()

                # Tính toán độ dài của việc thêm điểm vào con đường
                L = self.length-distance(c.dataval,n.dataval)+distance(c.dataval,node.dataval)+distance(node.dataval,n.dataval)

                # Tìm kiếm đường dẫn đến điểm với độ dài tối thiểu
                if L < Min_L :
                    Min_prev = prev 
                    Min_L = L
                    Min_Node = c
                traveler = n    

            if Min_prev : 
                Min_Next_Node = Min_Node.prevval
            else :
                Min_Next_Node = Min_Node.nextval

            node.nextval = Min_Next_Node
            node.prevval = Min_Node

            if Min_prev :
                Min_Node.prevval = node
            else :
                Min_Node.nextval = node

            if Min_Next_Node.nextval == Min_Node:
                Min_Next_Node.nextval = node
            else :
                Min_Next_Node.prevval = node
            
            self.length = Min_L
            
            #2-OP
            if self.is_2opt == True :
                self._2opt(Min_Node, node, Min_Next_Node)

        # Tăng số lượng điểm trong tuyến đường
        self.count = self.count + 1

    #áp dụng 2opt cho a-b-c
    def _2opt(self, a, b, c):
        traveler = self.traveler_init()

        c1 = a
        c2 = b

        n1 = b
        n2 = c

        c = traveler #vị trí hiện tại
        t_prev = False
        n, t_prev = self.traveler_next()

        traveler = n

        while traveler != self.position :

            cross = False

            if (c.dataval != c1.dataval and c.dataval != c2.dataval and n.dataval != c1.dataval and n.dataval != c2.dataval) and intersects(c.dataval, n.dataval, c1.dataval, c2.dataval):
                
                self._2optswap(c,n,c1,c2)
                cross = True
                a = n
                n = c1
                c2 = a
                    
            if (c.dataval != n1.dataval and c.dataval != n2.dataval and n.dataval != n1.dataval and n.dataval != n2.dataval) and intersects(c.dataval, n.dataval, n1.dataval, n2.dataval):
                
                self._2optswap(c,n,n1,n2)
                cross = True
                a = n
                n = n1
                n2 = a

            if cross:
                return

            c = n #vị trí hiện tại
            n, t_prev = self.traveler_next()
            traveler = n            


    # Hoán đổi giữa 2 đoạn chéo a-b và c-d
    def _2optswap(self, a, b, c, d):

        if a.nextval == b :
            a.nextval = c
        else :
            a.prevval = c

        if b.prevval == a :
            b.prevval = d
        else :
            b.nextval = d

        if c.nextval == d :
            c.nextval = a
        else :
            c.prevval = a

        if d.prevval == c :
            d.prevval = b
        else :
            d.nextval = b

        self.length = self.length - distance(a.dataval,b.dataval) - distance(c.dataval,d.dataval) + distance(a.dataval,c.dataval) + distance(b.dataval,d.dataval)


    # Lấy danh sách các tuyến đường
    def getRoute(self):
        result = []

        traveler  = self.traveler_init()
        result.append(traveler.dataval)

        traveler, prev  = self.traveler_next()

        while traveler != self.position :
            result.append(traveler.dataval)
            traveler, prev = self.traveler_next()

        result.append(traveler.dataval)

        return result

    def Solve(self, Set_points, with_2opt = True):
        # Để tính toán thời gian thực hiện
        time_start = datetime.datetime.now()

        # Sao chép danh sách điểm đã đặt
        points = Set_points.copy()

        # Chuyển danh sách thành tập hợp
        points = set(tuple(i) for i in points)

        # Thêm
        while len(points)>0 :
            # sleep(2)
            # print(points)
            # print("Points left : ", len(points),'              ', end="\r")
            point = points.pop()
            self.add_city(point)

        result = self.getRoute()

        time_end = datetime.datetime.now()
        delta = (time_end-time_start).total_seconds()

        L=0
        for i in range(len(result)-1):
            # L = L + math.sqrt((result[i-1][0]-result[i][0])**2 + (result[i-1][1]-result[i][1])**2)
            L=L+geodesic(result[i-1],result[i]).km

        # print("Points left : ", len(points),' Done              ',)
        # print("Execution time : ", delta, "secs")
        # print("Average time per point : ", 1000*delta/len(Set_points), "msecs")
        # print("Length : ", L)
        return result,L,delta

def read_point(filename):
    points=[]
    data=np.loadtxt(filename,delimiter=',')
    for i in range (data.shape[0]):
        points.append( tuple(data[i]))
    return points

def main_xuli(points):
    print("Solving TSP")
    print("Start")
    # points
    # points=read_point(filename)
    #Solve TSP
    TSP = TSP_TimeTraveler()
    route,khoancach,giaythuchien = TSP.Solve(points,with_2opt = True)
    print("End")
    return route

def diachi(route):
    savediachi=[]
    geolocator = Nominatim(user_agent="user_agent")
    for i in range(len(route)):
        truydiachi = geolocator.reverse(f"{route[i][0]},{route[i][1]}")
        diachi=truydiachi.address
        savediachi.append(diachi)
    return savediachi

