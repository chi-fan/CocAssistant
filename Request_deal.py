def request_deal(code):
    """
        code is the str from request_list \n
        function will return an arrary contains three varies, namely the english name: army, spell and device\n
        if the name is None, that means we can't tell the type
    """
    electro_dragon = ['雷 龙', '电 龙']
    dragon = ['龙', '火龙']
    balloon = ['气球', '黑球', '球2']
    wizard = ['法师']
    pekka = ['皮卡']
    anything = ['随便', '随意', '要']
    army = electro_dragon + dragon + balloon + wizard + pekka + anything
    haste = ['急 速', '极 速']
    freeze = ['冰 冻', '冰']
    healing = ['治 疗'] 
    rage = ['狂 暴']    
    spells = haste + freeze + healing + rage
    devices= ['攻 城 气 球', '车', '气 艇', '城 堡']

    # find the type of army
    type_army = []
    for i in range( len(army) ):
        if ( army[i] in code ) == True:
#            print(i)
            type_army.append(army[i])
#    print( type_army[0] )
            
    # find the type of spells
    type_spells = []
    for i in range( len(spells) ):
        if ( spells[i] in code ) == True:
#            print(i)
            type_spells.append(spells[i])
#    print( type_spells )
            
    # find the type of devices
    type_devices = []
    for i in range( len(devices) ):
        if ( devices[i] in code ) == True:
#            print(i)
            type_devices.append(devices[i])
#    print( type_devices )   
    
    if len(type_army) == 0:
        type_army = None
    else:
        type_army = type_army[0]
    if len(type_spells) == 0:
        type_spells = None
    else:
        type_spells = type_spells[0]
    if len(type_devices) == 0:
        type_devices = None
    else:
        type_devices = type_devices[0]
    
    request = []
    
#    print( type_army )
#    print( type_spells )
#    print( type_devices )
#    
    if type_army in electro_dragon:
        request.append('electro_dragon')
    elif type_army in dragon:
        request.append('dragon')
    elif type_army in balloon:
        request.append( 'balloon')
    elif type_army in wizard:
        request.append('wizard')
    elif type_army in pekka:
        request.append('pekka')
    elif type_army in anything:
        request.append( 'balloon')
    else:
        request.append(None)
        
                    
    if type_spells in haste:
        request.append( 'haste')
    elif type_spells in rage:
        request.append( 'rage')
    elif type_spells in healing: 
        request.append('healing')
    else:
        request.append(None)
            
    if type_devices == 0:
        request.append('攻城气球')
    elif type_devices == 1:
        request.append( '车')
    elif type_devices == 2:
        request.append( '气艇')
    elif type_devices == 3:
        request.append( '城堡')
    else:
        request.append(None)
    
    print( request )
    return request