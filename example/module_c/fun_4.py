import module_a.fun_1 as fun_1
import module_a.fun_2 as fun_2
import module_b.fun_3 as fun_3

def fun_4():
    print('hello from module_c.fun_4')
    fun_1()
    fun_2()
    fun_3()


