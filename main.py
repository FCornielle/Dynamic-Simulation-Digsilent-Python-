# Acceder a PowerFactory
import os
os.environ["PATH"] = r"C:\Program Files\DIgSILENT\PowerFactory 2021 SP2" + os.environ["PATH"]

import sys
sys.path.append(r"C:\Program Files\DIgSILENT\PowerFactory 2021 SP2\Python\3.9")

#importar powerfactory
import powerfactory as pf #comentarios
app=pf.GetApplication() #obtneer la app

#acceder al proyecto y activar
user = app.GetCurrentUser()
project = app.ActivateProject("Nine-bus System") #activar el proyecto que quiero
prj = app.GetActiveProject()

# app.Show() #(optativo)

#objeto creado desde pf con las barras
buses = app.GetCalcRelevantObjects('*.ElmTerm')

#crar diccionario de buses
bus_dict = {}
for bus in buses:
    bus_dict[bus.loc_name] = bus

bus_dict['Bus 1'] # ejemplo para acceder al objeto "bus1" del diccioanrio

# Crear diccionario de cargas
loads = app.GetCalcRelevantObjects('*.ElmLoad')
load_dict = {}
for load in loads:
    load_dict[load.loc_name] = load

#correr loadflow
ldf = app.GetFromStudyCase('ComLdf')
ldf.Execute()

# Acceder a atributos de buses
for i in buses:
    voltaje = bus_dict[i].GetAttribute('m:u')
    print(f"Voltaje de la barra {i}: {voltaje}")

# Acceder a atributos de cargas
for i in loads:
    potencia = load_dict[i].GetAttribute('m:p')
    print(f"Potencia de la carga {i}: {potencia}")

"""
ldf = app.GetFromStudyCase('ComLdf')
ini = app.GetFromStudyCase('ComInc')
sim = app.GetFromStudyCase('ComSim')
"""


# voltaje - bus_dict['Bus 1'].GetAttribute('m:u')

# Acceso a resultados ----------------------------------------------
"""
elmres = app.GetFromStudyCase('All calculations.ElmRes')
comres = app.GetFromStudyCase('ComRes')
comres.iopt_csel = 0
comres.iopt_tsel = 0
comres.iopt_locn = 2
comres.ciopt_head = 1
comres.pResult = elmres
comres.f_name = 'results.txt'
comres.ipt_exp = 4
comres.Execute()
"""
# Definicion de eventos ----------------------------------------------

"""
Shc_folder.CreateObject('EvtParam', 'evento de parametros')
EventSet = Shc_folder.GetContents()
evt = EventSet[0]

evt.time = 20

evt.p_target = control[2]
evt.variable = 'vref'
evt.value = '1.05'
evt.Delete()
app.ResetCalculation() #No olvidar en simulaciones dinamicas resetear
"""