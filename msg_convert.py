import datetime

def process (msg):

    msg_rst = []
    CA_max = {'DL_LTE':0, 'UL_LTE':0, 'DL_NR':0, 'UL_NR':0}
    ENDC = False

    for i in msg:
        msg_item = {}
        marking = ''
        time = i.split('|')[0].replace(' ','')
        time = datetime.datetime.strptime(time, "%H:%M:%S.%f")
        msg_item['TIME'] = time

        if 'LML1' in i:
            marking = '_LTE'
            ENDC = True
        elif 'NR5GMAC' in i:
            marking = '_NR'

        if 'DL since last' in i:
            marking = 'DL' + marking
        elif 'UL since last' in i:
            marking = 'UL' + marking

        etc = i.split('|')[1:]
        for k in etc:
            if 'CA_ID' in k:
                if CA_max[marking] < int(k.split(':')[1].replace(' ','')):
                    CA_max[marking] = int(k.split(':')[1].replace(' ',''))
                marking += '_' + k.split(':')[1].replace(' ','') + '_'
            elif 'AvgPHY' in k:
                msg_item[marking+'Tput'] = int(k.split(':')[1].replace(' ','').replace('Kbps',''))
            elif 'BLER' in k:
                msg_item[marking+'BLER'] = int(k.split(':')[1].replace(' ','').replace('%',''))
            elif 'AvgTB' in k:
                msg_item[marking+'TB'] = int(k.split(':')[1].replace(' ','').replace('bytes',''))
            elif 'MCS' in k:
                msg_item[marking+'MCS'] = int(k.split(':')[1].replace(' ',''))
            elif 'RB' in k:
                msg_item[marking+'RB'] = int(k.split(':')[1].replace(' ',''))

        msg_rst.append(msg_item)
    # for n in msg_rst:
    #     print(n)

    max_at_once = CA_max['DL_LTE']+CA_max['UL_LTE']+CA_max['DL_NR']+CA_max['UL_NR']+4
    msg_rst_2 = []
    time_recent = msg_rst[0]['TIME'].replace(second=msg_rst[0]['TIME'].second-1)
    for n in range(len(msg_rst)):
        msg_rst_2_item = msg_rst[n]
        if time_recent != msg_rst[n]['TIME']:
            for i in range(1,max_at_once):
                try:
                    if (msg_rst[n+i]['TIME']-msg_rst[n]['TIME']).seconds == 0:
                        if (msg_rst[n+i]['TIME']-msg_rst[n]['TIME']).microseconds < 3000:
                            msg_rst_2_item.update(msg_rst[n+i])
                            time_recent = msg_rst[n+i]['TIME']
                except:
                    break
            msg_rst_2.append(msg_rst_2_item)


    msg_rst_3 =[]
    for n in msg_rst_2:
        if len(n)!=6:
            msg_rst_3.append(n)
        # else:
        #     print(n)

    # for n in msg_rst_3:
    #     print(n)


    return msg_rst_2, CA_max, ENDC