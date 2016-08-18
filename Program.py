# -*- coding: utf-8 -*-

import sys
import os
import os.path
import platform
from NanoCluster import NanoCluster
from Plane import Plane
from Shape import Shape
from math import pi, sqrt

class Program:

    def __init__(self):
        if len(sys.argv) > 1:
            self.sirfile = sys.argv[1]
        else:
            self.sirfile = ""

        self.plane = Plane(0.0,0.0,1.0,0.0)
        self.tolx = 1.0
        self.toly = 0.1
        self.tolm = 0.2
        self.told = 1.0
        self.rot = 0.0
        self.pieces = 10

    def __show_params__(self):
        print ""
        print u"Нанокластер: " + self.sirfile
        print ""
        print u"Проективная плоскость: " + self.plane.__str__().encode('UTF-8')
        print u"Допустимая толщина плоскости: " + self.told.__str__().encode('UTF-8')
        print ""
        print u"Допустимое отклонение по X:   " + self.tolx.__str__().encode('UTF-8')
        print u"Допустимое отклонение по Y:   " + self.toly.__str__().encode('UTF-8')
        print ""
        print u"Текущий угол поворота [град]: " + (self.rot*180.0/pi).__str__().encode('UTF-8')
        print u"Количество кусков (углов) по которым произвести усреднение от 0 до 360 [град]: " + self.pieces.__str__().encode('UTF-8')
        print ""
        print u"Рассматривать линии, тангенсы которых по модулю больше, чем " + self.tolm.__str__().encode('UTF-8')

    def __show_help__(self):
        print u"params - просмотор текущих параметров"
        print u"tolx [param] - изменение параметра tolx (допустимые отклонения по оси x)"
        print u"toly [param] - изменение параметра toly (допустимые отклонения по оси y)"
        print u"tolm [param] - изменение параметра tolm (допустимые тангенсы углов должны быть не ниже этого значения)"
        print u"pieces [param] - количество кусков на которые разбивается интервал [0..360] град"
        print u"load [sirenfile] - загрузить siren-файл"
        print u"orun - единичный запуск анализа для текущего угла попорота."
        print u"run - запуск анализа для всех углов, на которые разбит интервал [0..360] град"
        print u"stat [symbol] - запуск сбора статистики. Необязательный параметр symbol включает в статистику только те варианты (в файле stat.dat), которые помечены этим символом (по умолчанию в статистику включаются все результаты)"
        print u"plane - изменение текущей плоскости"
        print u"exit - выход из оболочки"

    def __run__(self, fi):
        if os.path.isfile(self.sirfile):
            cluster = NanoCluster(self.sirfile)
            cluster.centrate()
            cluster.rotate(fi, (1, 0, 0))

            plane = Plane(self.plane.A, self.plane.B, self.plane.C, self.plane.D)
            pats = cluster.get_plane_atoms(plane, self.told)

            shape = Shape(pats)

            left_lines = shape.find_left_lines(self.tolx, self.toly, self.tolm)
            right_lines = shape.find_right_lines(self.tolx, self.toly, self.tolm)

            dir = "Result_" + self.sirfile.replace(".sir","")+"_fi=" + str(fi*180.0/pi)

            if not os.path.exists(dir):
                os.makedirs(dir)

            print u"Выполняю анализ при повороте " + str(fi*180.0/pi) + u" [град] вокруг оси"
            print u"Результаты сохраняю в " + dir

            if len(left_lines) != 0 and len(right_lines) != 0:
                num = 1
                c_fi = fi * 180.0 / pi

                result = open(os.path.join(dir,"stat.dat"), 'w')
                angles = open(os.path.join(dir,"angles.dat"), 'w')

                result.writelines(str(c_fi) + "\n")

                for ll in left_lines:
                    for lr in right_lines:
                        fname = self.sirfile + "_fi=" + str(c_fi) + "_var(" + str(num)+").png"
                        shape.save_result(lr.m, lr.c, ll.m, ll.c, c_fi, os.path.join(dir,fname))
                        shape.save_shape(os.path.join(dir,"shape.dat"))
                        an = shape.get_angle(ll.m, lr.m)
                        result.writelines(str(num) + " " + str(an) + "\n")
                        angles.writelines(str(num) + " " + str(ll.m) + " " + str(ll.c) + " " + str(lr.m) +" " +str(lr.c) + "\n")
                        num +=1

                result.close()
                angles.close()

                print u"Во время анализа было обнаружено " + str(num-1) + u" вар."
                print u"Резульаты сохранены..."
                print ""
            else:
                print u"Что то пошло не так..."
                shape.visualize2D(True)

        else:
            print u"Не обнаружен файл для анализа"

    def get_dirs(self, p):
        p = os.path.abspath(p)
        return [n for n in os.listdir(p) if os.path.isdir(os.path.join(p, n))]


    def __stat_run__(self, dir, symbol):

        dirs = self.get_dirs(dir)
        out = open("stats.dat",'w')
        psis = []

        for d in dirs:
            statname = os.path.join(d, "stat.dat")

            if os.path.exists(statname):
                stat = open(statname)
                line = stat.readline()
                fi = line.replace("\n","")
                flag = False
                s = 0.0
                ss = 0.0
                count = 0

                print u"Сбор статистики для угла " + fi

                while line:
                    if flag and line.find(symbol)!=-1:
                        spl = line.split()
                        psi = float(spl[1])
                        s += psi
                        ss += psi*psi
                        count += 1
                    else:
                        flag = True

                    line = stat.readline()

                if count == 0:
                    count = 1

                aver = s/count
                sigma = sqrt(ss/count - aver*aver)

                psis.append(aver)
                out.writelines(fi + " " + str(aver) + " " + str(sigma) + "\n")
                print u"Среднее значение " + str(aver) + " +- " + str(sigma)
                print ""

                stat.close()

        print u"Усреднение результатов..."
        count = 0
        s = 0.0
        ss = 0.0

        for psi in psis:
            s += psi
            ss += psi*psi
            count += 1

        if count == 0:
            count = 1

        aver = s / count
        sigma = sqrt(ss / count - aver * aver)
        out.writelines("<psi> = " + str(aver) + " +- " + str(sigma) + "/r/n")

        print "<psi> = " + str(aver) + " +- " + str(sigma)
        print u"Сбор статистики завершён, результаты сохранены в stat.dat"

        out.close()

    def __execute__(self, comand):
        chunks = comand.split(' ')

        if len(comand) == 0:
            return

        if len(chunks)>0:
            if chunks[0] == "params":
                self.__show_params__()
                return

            if chunks[0] == "load":
                file = ""
                if len(chunks)==1:
                    file = raw_input(u"Введите имя файла: ")
                else:
                    file = chunks[1].strip('"')

                if os.path.isfile(file):
                    self.sirfile = file
                else:
                    print u"Файла " + file + u" не найдено"
                return

            if chunks[0] == "tolx":
                if len(chunks)>1:
                    self.tolx = float(chunks[1])
                    return
                self.tolx = float(raw_input(u"Допустимое отклонение по X: "))
                return

            if chunks[0] == "toly":
                if len(chunks)>1:
                    self.toly = float(chunks[1])
                    return
                self.toly = float(raw_input(u"Допустимое отклонение по Y: "))
                return

            if chunks[0] == "tolm":
                if len(chunks)>1:
                    self.tolm = float(chunks[1])
                    return
                self.tolx = float(raw_input(u"Минимальный допустимый тангенс угла: "))
                return

            if chunks[0] == "rot":
                if len(chunks)>1:
                    self.rot = float(chunks[1])*pi/180.0
                    return
                self.rot = float(raw_input(u"Введите текущий угол поворота [град]: "))*pi/180.0
                return

            if chunks[0] == "pieces":
                if len(chunks)>1:
                    self.pieces = int(chunks[1])
                    return
                self.pieces = int(raw_input(u"Количество кусков(углов) на которые разбить интервал от 0 до 360 град: "))
                return

            if chunks[0] == "vis":
                if os.path.isfile(self.sirfile):
                    cl = NanoCluster(self.sirfile)
                    cl.centrate()
                    cl.rotate(self.rot,(1,0,0))
                    cl.visualize()
                else:
                    print u"Не обнаружен файл для визуализации"
                return

            if chunks[0] == "orun":
                self.__run__(self.rot)
                return

            if chunks[0] == "run":
                temp = self.rot
                dfi = 2.0 * pi/self.pieces

                for i in xrange(0,self.pieces):
                    self.__run__(self.rot)
                    self.rot += dfi

                self.rot = temp
                return

            if chunks[0] == "stat":
                symbol = ""
                if len(chunks)>1:
                    symbol = chunks[1]
                self.__stat_run__(os.curdir,symbol)
                return

            if chunks[0] == "visp":
                if os.path.isfile(self.sirfile):
                    cl = NanoCluster(self.sirfile)
                    cl.centrate()
                    cl.rotate(self.rot, (1, 0, 0))
                    cl.visualize_plane_atoms(self.plane,self.told)
                else:
                    print u"Не обнаружен файл для визуализации"
                return

            if chunks[0] == "plane":
                print u"Измените параметры плоскости Ax + By + Cz + D = 0"
                self.plane.A = float(raw_input("A: "))
                self.plane.B = float(raw_input("B: "))
                self.plane.C = float(raw_input("C: "))
                self.plane.D = float(raw_input("D: "))
                self.told = float(raw_input("Допустимая толщина: "))
                print u"Проективная плоскость: " + self.plane.__str__().encode('UTF-8')

            if chunks[0] == "help":
                self.__show_help__()
                return

        os.system(comand)

    def run(self):

        if platform.system() == 'Windows':
            reload(sys)
            sys.setdefaultencoding('cp866')
            os.system("cls")
        else:
            os.system("clear")

        print "\t\tDIH ANGLE v. 1.2"
        print u"\t\tПрограмма для определения углов манжеты"
        print u"\t\tТвГУ (кафедра общей физики)"
        print u"\t\tАвтор: к.ф.-м.н. Соколов Денис (C) 2016"
        print u"\t\tВведите help для справки"
        print ""

        comand = raw_input("dihangle> ")

        while comand.strip()!="exit":
            self.__execute__(comand)
            print ""
            comand = raw_input("dihangle> ")
