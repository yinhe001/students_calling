# -*- coding: utf-8 -*-
# Latest update: 2022/10/6
# Authors: Lai jinsong , Li zhengtao
# Method createDutyTable() By Li zhengtao    随机出勤信息生成
# Method callClass() By Lai jinsong          点名算法

import numpy as np
import random

class MyClass():
    def __init__(self, class_num):
        self.requireCalledNum = 90 * 0.1            # 单次点名学生数量
        self.callTimes = 0                          # 该班的总点名次数
        self.successCallTimes = 0                   # 该班的有效点名次数
        self.class_num = class_num                  # 班级号
        self.courseTimes = 20                       # 每门课20节
        self.no_come = []                           # call_class点名没到的
        self.table = []                             # 单日出勤表


        # 初始化学生标准正态分布绩点 均值2.9 方差0.35
        self.studentGrade = {SNo:grade for SNo,grade in list(zip(range(1, 91),np.random.normal(2.9,0.35,90)))}
        # 随机生成缺勤16节课的学生数量
        self.numOfOutDutyStudents = random.randint(5, 8)

        # 缺勤16节课的学生的学号集合
        self.outDutyStudentsSNo = []
        numlist = list(range(1, 91))

        # 假设绩点低的同学逃课率更高
        while len(self.outDutyStudentsSNo) < self.numOfOutDutyStudents:
            no_duty = random.choice(numlist)
            # 前30%绩点的人被抽到的概率约是10%
            if self.studentGrade[no_duty] >= self.rate_grade(0.7) and random.random() * 100 > 90:
                self.outDutyStudentsSNo.append(no_duty)
                numlist.remove(no_duty)
            # 前70%到前30%到%绩点的人被抽到的概率约是35%
            elif self.rate_grade(0.3) < self.studentGrade[no_duty] < self.rate_grade(0.7) and random.random() * 100 > 65:
                self.outDutyStudentsSNo.append(no_duty)
                numlist.remove(no_duty)
            # 后30%绩点的人被抽到的概率是80%
            elif self.rate_grade(0.3) > self.studentGrade[no_duty] and random.random() * 100 > 30:
                self.outDutyStudentsSNo.append(no_duty)
                numlist.remove(no_duty)
            else:
                pass
        # 注意--------------------若经常缺勤的人与绩点无关-------------------------------
        # self.outDutyStudentsSNo = random.sample(numlist,self.numOfOutDutyStudents)

        self.outDutyStudents = {}
        # 初始化80%不出勤同学的信息 每个同学是个键值对 key是学生号，value是到位次数。 该次数最终为4.
        for i in self.outDutyStudentsSNo:
            self.outDutyStudents[i] = 0

    def rate_grade(self,rate):     # rate 是一个百分比数
        grade_list = sorted(self.studentGrade.items(), key = lambda x:x[1])
        rate_grade = grade_list[int(rate*90-1)][1]
        return rate_grade          # 返回rate排名的绩点

    def createDutyTable(self):
        # 生成一次出勤表， 课程次数减一
        self.courseTimes -= 1
        print(f'创建课程{self.class_num}的第{20-self.courseTimes}课的出勤表')
        # 出勤表
        table = {}
        # 经常缺勤，且当日到位的学生
        DutySno = []
        # 先考虑生成经常缺勤同学的出勤情况
        for no in self.outDutyStudentsSNo:
            # 该学生2成概率到位
            if self.outDutyStudents[no] != 4 and self.courseTimes > 4 and \
                    random.random() * 10 > 8:
                self.outDutyStudents[no] += 1
                # 1表示到位 0表示缺席
                table[no] = 1
                DutySno.append(no)
            # 出勤未满4次， 且剩下不到四节课 则出勤。
            elif self.outDutyStudents[no] != 4 and self.courseTimes <= 4:
                self.outDutyStudents[no] += 1
                table[no] = 1
                DutySno.append(no)
            # 出勤满4次， 则缺勤。
            elif self.outDutyStudents[no] == 4:
                table[no] = 0
            else:
                table[no] = 0
        # 经常缺勤且当日没到的学生
        outDutySno = list(set(self.outDutyStudentsSNo)-set(DutySno))


        onduty = list(set(list(range(1, 91))) - set(self.outDutyStudentsSNo))
        # 除了经常缺勤的同学，还有随机缺席 0到3 人
        number = random.randint(0, 3)
        # 随机缺勤同学的学号
        SNos = random.sample(onduty, number)

        for i in SNos:
            table[i] = 0

        # 实际到位的同学
        rest = list(set(range(1,91)) - set(SNos) - set(outDutySno))
        for i in rest:
            table[i] = 1
        self.table = sorted(table.items(), key=lambda x: x[0])
        print('经常缺勤同学的出勤情况表：',self.outDutyStudents)
        print(self.table)
        return sorted(table.items(), key=lambda x: x[0])

    def callClass(self):
        # print(self.table)

        # before_call_class

        # 被点名的同学，上次没到的同学的学号，继续再点一次
        numlist = list(range(1, 91))  # 学号列表

        rets = []
        rets.extend(self.no_come)


        # 生成点名表
        while len(rets) < self.requireCalledNum:
            num_called = random.choice(numlist)
            # 前30%绩点的人被抽到的概率约是15%
            if self.studentGrade[num_called] >= self.rate_grade(0.7) and random.random() * 100 > 85:
                rets.append(num_called)
                numlist.remove(num_called)
            # 前70%到前30%绩点的人被抽到的概率是60%
            elif self.rate_grade(0.3) < self.studentGrade[num_called] < self.rate_grade(0.7) and random.random() * 100 > 40:
                rets.append(num_called)
                numlist.remove(num_called)
            # 后30%绩点的人被抽到的概率是80%
            elif self.rate_grade(0.3) >= self.studentGrade[num_called] and random.random() * 100 > 20:
                rets.append(num_called)
                numlist.remove(num_called)
            else:
                pass

        self.callTimes += self.requireCalledNum

        # 课前点名未到同学
        before_nocome = []
        if rets:
            for i in rets:
                if self.table[i - 1][1] == 0:   # 被点名的同学没到
                    before_nocome.append(i)     # 记录第一次点名未到的学号
                    self.successCallTimes += 2  # 没到的同学 call_after_class会被再次点到 +2
        # 课前点名到的同学课后不再点
        before_come = list(set(rets) - set(before_nocome))
        '''
        print('课前点名')
        print(before_nocome, '\n', before_come)
        '''
        # -----------------------------------
        # after_call_class

        # 若被点到的缺勤人数够多了 >= 5, 认为缺勤的同学基本点到了， 本次点名人数减半
        if len(before_nocome) >= 5:
            new_len = self.requireCalledNum // 2
            self.callTimes += (new_len + len(before_nocome))
        else:
            new_len = self.requireCalledNum - len(before_nocome)
            self.callTimes += self.requireCalledNum


        # 被点名的同学
        rets = []
        # 出勤的不再点，没出勤的已经 +2
        numlist = list(set(range(1, 91)) - set(before_nocome) - set(before_come))
        while len(rets) < new_len:
            num_called = random.choice(numlist)
            # 前30%绩点的人被抽到的概率约是15%
            if self.studentGrade[num_called] >= self.rate_grade(0.7) and random.random() * 100 > 85:
                rets.append(num_called)
                numlist.remove(num_called)
            # 前70%到前30%绩点的人被点到的概率是60%
            elif self.rate_grade(0.3) < self.studentGrade[num_called] < self.rate_grade(0.7) and random.random() * 100 > 40:
                rets.append(num_called)
                numlist.remove(num_called)
            # 后30%绩点的人被点到的概率是80%
            elif self.rate_grade(0.3) >= self.studentGrade[num_called] and random.random() * 100 > 20:
                rets.append(num_called)
                numlist.remove(num_called)
            else:
                pass
        # 课后点名没到的同学
        after_nocome = []
        if rets:
            for i in rets:
                if self.table[i - 1][1] == 0:
                    after_nocome.append(i)  # 记录第二次点名未到的学号
                    self.successCallTimes += 1  # 另外没到的同学+1
        after_come = list(set(rets) - set(after_nocome))
        # 今日课前课后都没有到位的同学
        no_come = []
        no_come.extend(before_nocome)
        no_come.extend(after_nocome)
        self.no_come = no_come
        '''
        print('课后点名')
        print(after_nocome, '\n', after_come)
        print(f'有效点名:{self.successCallTimes},总点名:{int(self.callTimes):},E:{self.successCallTimes / self.callTimes:.2}')
        '''
        return self.successCallTimes, self.callTimes


def create_class_data():
    for i in range(5):
        new_class = MyClass(i + 1)
        for j in range(19):
            print('*' * 50)
            # 创建出勤表
            new_class.createDutyTable()
            # 点名
            new_class.callClass()
        new_class.createDutyTable()
        # 一次返回一个班级的 有效点名 和 总点名次数
        yield new_class.callClass()

# num = 50,取50次E
def get_E_info(num=5):
    Elist = []
    for i in range(num):
        # 5个班的 有效点名 和 总点名情况
        retsList = list(create_class_data())
        fiveCourseSuccessCall = 0
        fiveTotalCall = 0
        for ret in retsList:
            fiveCourseSuccessCall += ret[0]
            fiveTotalCall += ret[1]
        E = fiveCourseSuccessCall / fiveTotalCall
        # print(f'E : {E:.2f}')
        Elist.append(E)
    print('Elist: ',Elist)
    print(f'E: 均值 {sum(Elist)/len(Elist):.2} 最大值 {max(Elist):.2} 最小值 {min(Elist):.2} 方差 {np.var(Elist):.2}')
    return sum(Elist)/len(Elist),max(Elist),min(Elist),np.var(Elist)



'''
class1 = MyClass(1)
a = class1.createDutyTable()
for i in range(20):
    print('*'*50)
    class1.createDutyTable()
    class1.call_class()

# print(class1.outDutyStudents)
'''
if __name__ == '__main__':
    # 输入函数
    create_class_data()
    # 输出函数 num默认为50,为取E的次数。
    get_E_info()





