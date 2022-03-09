filename = 'test_file.hpgl'
operation = []
raw_st = ''
st = ''
test_str = ''
cu = 0
cd = 0
with open(filename) as f:
    ## A variable that reads lines of code from the Nucleo.
    raw_data = f.readlines()
    data = ''.join(raw_data)
    ## A variable that separates strings into ordered lists of data.
    #for x in data:
    data = data.split(';')
    for x in data:
        try:
            float(x)
        except:
            if 'PU' in x:
                operation.append('PU')
                raw_st = x
                l = len(x)
                for y in raw_st:
                    try:
                        float(y)
                    except:
                        if y == ',' and cu == 0:
                            st += ','
                            cu = 1
                        elif y == ',' and cu == 1:
                            operation.append(st)
                            cu = 0
                            st = ''
                    else:
                        st += y
                operation.append(st)
                st = ''
                cu = 0
            elif 'PD' in x:
                operation.append('PD')
                raw_st = x
                l = len(x)
                for y in raw_st:
                    try:
                        float(y)
                    except:
                        if y == ',' and cd == 0:
                            st += ','
                            cd = 1
                        elif y == ',' and cd == 1:
                            operation.append(st)
                            cd = 0
                            st = ''
                    else:
                        st += y
                operation.append(st)
                st = ''
                cd = 0
            else:
                operation.append(x)
                        
    #print(data)
    for i in operation:
        print(i)
    # try:
    #     float(data[0])
    #     float(data[1])
    # except:
    #     if len(data) >= 2:
    #         if data[0].strip() == ' ' or data[1].strip() == ' ':
    #             continue
    #         elif data[0].strip().isalpha() == True or data[1].strip().isalpha() == True:
    #             continue             
    #     elif 'MicroPython' in data[0]:
    #         break
    # else:
    #     x_val.append(float(data[0].strip()))
    #     y_val.append(float(data[1].strip()))
