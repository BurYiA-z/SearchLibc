from engine import engine

import sys
import subprocess



class SearchLibc(object):
    
    def __init__(self, func=None, address=None):
        self.condition = {}
        self.libc_so = ''
        self.PATH = 'libc-database/db/'
        if func is not None and address is not None:
            self.add(func, address)

    def add(self, name, addr):
        if not isinstance(name, str):
            print("The name should be a string")
            sys.exit()
        if not isinstance(addr, int):
            print("The addr should be an int number")
            sys.exit()
        self.condition[name] = hex(addr)


    def find(self):
        if len(self.condition) == 0:
            print("\033[0;31;40m[ERROR]\033[0m "+"You should add function and it's addr first !")
            sys.exit()
        libs = engine.find(self.condition)

        if len(libs)==0:
            print("\033[0;31;40m[ERROR]\033[0m "+"Sorry, not find ! Check that the address you added is correct !")
            sys.exit()
        else:
            print("\033[0;36;40m[*]\033[0m " + "Find libs:")
            for i in range(len(libs)):
                print("  "+str(i)+"."+libs[i])
            
            print("\033[0;36;40m[*]\033[0m " + "You can choose it by hand:", end='')
            while(1):
                num = int(input())
                if num >=0 and num < len(libs):
                    break
                print("\033[0;33;40m[!]\033[0m " + "Please enter the correct number:", end='')
            self.libc_so = libs[num]
            return libs[num]


    def dump(self, names=[]):
        if self.libc_so == '':
            libc = engine.dump(self.find(), names)
        else:
            libc = engine.dump(self.libc_so, names)

        ret = []
        if len(names) == 0:
            ret.append(libc['system'])
            ret.append(libc['str_bin_sh'])
        else:
            for i in range(len(names)):
                ret.append(libc[names[i]])

        return ret


    def one_gadget(self, filename):
        return [int(i) for i in subprocess.check_output(['one_gadget', '--raw', filename]).decode().split(' ')]

    def ogg(self):
        if self.libc_so == '':
            libc_name = self.find()
        else:
            libc_name = self.libc_so
    
        libc_path = self.PATH + libc_name + '.so'
        oggs = self.one_gadget(libc_path)

        if len(oggs) == 0:
            print("\033[0;31;40m[ERROR]\033[0m "+"Not Find!")
        elif len(oggs) == 1:
            return oggs[0]
        else:
            print("\033[0;36;40m[*]\033[0m " + "Find one_gadget:")
            for i in range(len(oggs)):
                print("  "+str(i)+"."+hex(oggs[i]))
            
            print("\033[0;36;40m[*]\033[0m " + "You can choose it by hand:", end='')
            while(1):
                num = int(input())
                if num >=0 and num < len(oggs):
                    break
                print("\033[0;33;40m[!]\033[0m " + "Please enter the correct number:", end='')
            return oggs[num]


if __name__ == '__main__':
    Libc = SearchLibc()


    Libc = SearchLibc("__libc_start_main_ret", 0xe81)
    system, binsh, atoi = Libc.dump([ 'system', 'str_bin_sh', 'atoi' ])
    system, binsh = Libc.dump()


    ogg = Libc.ogg()

