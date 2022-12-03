
fecha_inicio=""
fecha_fin=""
fecha_inirange=[]
fecha_finrange=[]
fechainicio="05/02/2019"
fechafin="05/27/2019"
for i in fechainicio:
    if (i == "/"):
        fecha_inirange.append(fecha_inicio)
        fecha_inicio=""       
    else:
        fecha_inicio=fecha_inicio+i
fecha_inirange.append(fecha_inicio)
        


for u in fechafin:
    if (u == "/"):
        fecha_finrange.append(fecha_fin)
        fecha_fin=""       
    else:
        fecha_fin=fecha_fin + u
        

fecha_inirange.append(fecha_inicio)
fecha_finrange.append(fecha_fin)



print(fecha_inirange[2])
print(fecha_finrange[1])
   