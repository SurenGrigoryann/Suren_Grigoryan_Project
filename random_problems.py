l_of_numbers = [1,2,3,4,5,6,6,7]
i = 10

def linear_search(list,item):
    k = 0
    flag = False
    while k < len(list) and flag == False:
        if list[k] == item:
            flag = True
        else:
            k = k + 1
        # end if
    # end while

    if flag == True:
        return flag,  k
    else:
        return flag
    # end if
# end function
#print(linear_search(l_of_numbers,i))


def linear_search_recursive (list,item, total):
    if total > len(list) - 1:
        return False
    
    elif list[total] == item:
        return True
    else:
        return linear_search_recursive(list,item, total + 1)
    # end if

# end function

#print(linear_search_recursive(l_of_numbers,i,0))



def binary_search(list, item, first,last):
    if first == last:
        return False
    elif list[(first + last) //2 + 1] == item:
        return True
    elif list[(first + last) //2 + 1] > item:
        return binary_search(list,item, first, (first + last)//2 + 1)
    elif list[(first + last) //2] > item:
        return binary_search(list,item, (first + last)//2 + 1, last)
    
print(binary_search(l_of_numbers, i, 0, (len(l_of_numbers))-1))



