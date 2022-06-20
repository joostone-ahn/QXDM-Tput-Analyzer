def process (msg):

    msg_filtered = []

    for i in msg:
        if i != '':
            if 'NR5GMAC'in i or 'LML1' in i:
                    if 'QSH Meas Logging' not in i:
                        if 'SR' not in i:
                            if 'No' not in i:
                                if 'QSH metrics' not in i:
                                    msg_filtered.append(i.replace('          ',' | '))
        # else:
        #     print("none")


    # realtime 로그는 시간 13자리 이상임 ms 단위를 1000ms 까지만 표시하도록 반올림
    # print(len(msg_filtered[0].split('|')[0]))
    if len(msg_filtered[0].split('|')[0]) > 13:
        for i in range(len(msg_filtered)):
            time = msg_filtered[i].split('|')[0].replace(' ', '')
            time_ms = int(time[-6:])
            time_ms = str(round(time_ms, -3))[:3]
            time = time.split('.')[0] + '.' + time_ms +' |'
            msg_filtered[i] = time + msg_filtered[i][17:]

    msg_filtered = sorted(msg_filtered)

    # for n in msg_filtered:
    #     print(n)

    return msg_filtered