class QuadraticEquation:
    def __init__(self, equation):
        self.equation = equation

    def begin(self):
        first = self.checkFormat(self.equation)
        second = self.coefFinder(first)
        third = self.solutionIterate(second[0], second[1], second[2])
        return third

    def checkFormat(self, equation):
        split_eq = equation.split('=')
        left_side = split_eq[0]
        right_side = split_eq[-1]
        if(split_eq.__len__() != 2):
            print("your equation didn't corresponse the format(e.g.ax^b+cx^d+...+z=0)\nTry again...")
        else:
            if(right_side != '0'):
                if(right_side.split('-').__len__() == 2):#negative
                    format_equation = f'{left_side}+{right_side.split('-')[-1]}=0'
                    return format_equation
                else:#positive
                    format_equation = f'{left_side}-{right_side.split('-')[-1]}=0'
                    return format_equation
            else:#right side is 0
                format_equation = f'{left_side}=0'
                return format_equation

    def coefFinder(self, equation):
        split_eq = equation.split('=')
        a_temp = split_eq[0].split('x^2')
        b_temp = a_temp[-1].split('x')
        a = a_temp[0]
        b = b_temp[0]
        c = b_temp[-1]
        
        match a:
            case '':
                a = 1
            case '-':
                a = -1
            case _:
                a = float(f'{float(a):.5f}')

        match b:
            case '':
                b = 1
            case '-':
                b = -1
            case _:
                b = float(f'{float(b):.5f}')
        
        match c:
            case '':
                c = 1
            case '-':
                c = -1
            case _:
                c = float(f'{float(c):.5f}')
        
        return (a, b, c)

    def solutionIterate(self, a, b, c, positive = 1000, negative = -1000):
        def f(x):
            return a*x**2+b*x+c
        def diff_f(x):
            return 2*a*x+b
        print(a, b, c)
        print(type(a), type(b), type(c))
        print("Calculating...")
        first = f(positive)
        second = f(negative)
        x1 = x2 = 0
        time_counter = 0
        while abs(f(positive)) > 0:
            positive -= f(positive)/diff_f(positive)
            time_counter += 1
            # print(f"Calculating first answer...x={positive}\n")
        x1 = float(f'{float(positive):.5f}')
        while abs(f(negative)) > 0:
            negative -= f(negative)/diff_f(negative)
            # print(f"Calculating second answer...x={negative}\n")
            time_counter += 1
        x2 = float(f'{float(negative):.5f}')
    
        return (x1, x2)


if '__main__' == __name__:
    equation = input('enter your equation(e.g.3x^2+2x+6=0)\n >: ')
    qe = QuadraticEquation(equation)
    print(qe.begin())