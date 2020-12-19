# -*- coding:utf-8 -*-
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys
import datetime
import numpy as np
import re


def transpose_content(content):
    x_dimention = len(content[0])
    y_dimention = len(content)
    content_t=[]
    for c in range(x_dimention):
        string = ''
        for y in range(y_dimention):
            string=string+content[y][c]
        content_t.append(string.strip())
    content_t = [c for c in content_t if c != '']
    return content_t


def get_head(filename):
    with open(filename , 'r' ,encoding = 'UTF-8') as file:
    #with open(filename , 'r' ) as file:
        head = []
        line_t = ''
        for _, line in enumerate(file):
            if(re.match("^;\s+[^=]",line)):
                line_t = [c for c in line if c != ';']
                head.append(line_t)

        return transpose_content(head)


def get_data(filename):
    with open(filename , 'r' ) as file:
        data = []
        for _, line in enumerate(file):
            if (re.match("^\s+\S",line)):
                line = line.replace('H','1')
                line = line.replace('L','0')
                end = line.index(';')
                data.append(line[:end].strip())

        return transpose_content((data))

def set_vcd(head,data,filename):
    var=""
    c = len(data[0])
    n = len(data)
    symble = []
    now=datetime.datetime.now().strftime("%b %d %Y %H:%M:%S")
    stc_1="$date "+now+" $end\n$version CP $end\n$timescale 10 ns $end\n$scope module A5057 $end\n"
    for i in range(n):
        if i < 94:
            symble.append(chr(33+i) + " ")
        elif i < 188:
            symble.append(chr(33) + chr(33+i-94) + " ")
        elif i < 282:
            symble.append(chr(34) + chr(33+i-94) + " ")
        elif i < 376:
            symble.append(chr(35) + chr(33+i-94) + " ")

        var += "$var wire 1 " + symble[i] + head[i] + " $end\n"

    #var2="$var wire 8 "+chr(34)+" R[7:0] $end\n"
    stc_2=stc_1+var+"$enddefinition $end\n"

    output = "#0 \n"
    for i in range(n):
        output += data[i][0] + symble[i] + " \n" # inital at #0

    flag = 0
    for j in range(1,c):
        data_time = "#" + str(j) + " \n"    # time stamp
        data_change = ''
        for i in range(n):
            if data[i][j] != data[i][j-1]:
                data_change += str(data[i][j])+symble[i]+" \n"
                flag = 1
        if flag == 1:
            output += data_time + data_change
            flag = 0


    with open(filename, 'w', encoding='UTF-8') as file:
        file.write(stc_2)
        file.write(output)



if __name__ == '__main__':
    # head = get_head(sys.argv[1])
    # data = get_data(sys.argv[1])
    # set_vcd = (head,data, sys.argv[2])
    head = get_head('A5057D_CKSUM.dat')
    data = get_data('A5057D_CKSUM.dat')
    set_vcd(head,data,'test1.vcd')
