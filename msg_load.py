def process (msg):

    msg_filtered = []

    for i in range(len(msg)):
        if msg[i] != '':
            if 'nr5g_mac_metric_qsh.c' in msg[i]:
                time = msg[i-1].split('[')[0][12:].replace(' ','')
                etc = ' | NR5GMAC' + msg[i].split('NR5GMAC')[1]
                msg_filtered.append(time+etc)
            elif 'lte_ml1_dlm_qsh_dbg.c' in msg[i]:
                time = msg[i-1].split('[')[0][12:].replace(' ','')
                etc = ' | LML1' + msg[i].split('LML1')[1]
                msg_filtered.append(time+etc)
            elif 'lte_ml1_hp.c' in msg[i]:
                time = msg[i-1].split('[')[0][12:].replace(' ','')
                etc = ' | LML1' + msg[i].split('LML1')[1]
                msg_filtered.append(time+etc)
        # else:
        #     print("none")

    # for n in msg_filtered:
    #     print(n)

    return msg_filtered