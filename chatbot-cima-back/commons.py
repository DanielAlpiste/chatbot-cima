from datetime import datetime

def convertDatetime(tiempo):
    tiempo = tiempo.strftime("%d-%b-%Y (%H:%M:%S.%f)")
    #tiempo = tiempo.replace("T"," ")
    tiempo = tiempo[:12]
    return tiempo