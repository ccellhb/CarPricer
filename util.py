#!/usr/bin/env python3
# -*- coding: utf-8 -*-



def my_sort(list):
    new_list=[1,2,3,4,5]
    try:
        for li in list:
            if li == 'make':
                new_list[0] = li
            elif  li == 'mode':
                new_list[1] = li
            elif  li == 'name':
                new_list[2] = li
            elif  li == 'price':
                new_list[3] = li
            elif  li == 'url':
                new_list[4] = li
            else:
                raise FooError('invalid value: %s' % li)
    except Exception as e:
        print('Error:', e)
        return list
    else:
        return new_list
    finally:
        pass

   
    

 
if __name__ == '__main__':
    print(my_sort(['price', 'name', 'make', 'mode', 'url']))
  