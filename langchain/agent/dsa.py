def find(str1, str2):
    map = []
    
    if(len(str1)!=len(str2)):
        return False

    for ch in str1:
        map.append(ch)
        
    for ch in str2:
        if(ch not in map):
            return False
        map.remove(ch)
    
    return True

str1 = "Hello"
str2 = "ehllo"

if(find(str1, str2)):
    print("Yes strings will match on change sequence")
else:
    print("no")