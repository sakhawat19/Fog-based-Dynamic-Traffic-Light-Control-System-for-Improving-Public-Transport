#!/usr/bin/env python
"""
@file    runner.py
@author  Sakhawat Hossan
@date    20-10-2016

"""

import os
import sys
import optparse
import subprocess
import random

import distributed





# we need to import python modules from the $SUMO_HOME/tools directory
try:
    sys.path.append(os.path.join(os.path.dirname(
        __file__), '..', '..', '..', '..', "tools"))  # tutorial in tests
    sys.path.append(os.path.join(os.environ.get("SUMO_HOME", os.path.join(
        os.path.dirname(__file__), "..", "..", "..")), "tools"))  # tutorial in docs
    from sumolib import checkBinary
except ImportError:
    sys.exit(
        "'SUMO_HOME' is not decleared properly..')")

import traci

PORT = 8874

PRG1 = "rrgrrrgr"

PRG2 = "rrrrrrgg"

PRG3 = "rrrgrrrg"

PRG4 = "rrggrrrr"


PRG5 = "grrrgrrr"

PRG6 = "ggrrrrrr"

PRG7 = "rgrrrgrr"

PRG8 = "rrrrggrr"


PRG9 = "rgrrrrgr"

PRG10 = "rrrrgrrg"

PRG11 = "rrgrrgrr"

PRG12 = "grrgrrrr"




# Intersection info initialise

intId = 902




PROGRAM = [PRG1, PRG2, PRG3, PRG4, PRG5, PRG6, PRG7, PRG8, PRG9, PRG10, PRG11, PRG12]


def generate_routefile():
    random.seed(42)  # make tests reproducible
    N = 1000  # number of time steps
    # demand per second from different directions
    R1 = 0.11  #0.113   #0.0455 
    R2 = 0.1027   #0.102   #0.042 
    R3 = 0.05   #0.050   #0.01 
    R4 = 0.05   #0.050   #0.01
    R5 = 0.01

    with open("data/cross.rou.xml", "w") as routes:
        print >> routes, """<routes>
        <vType id="923" accel="1.4" decel="2" sigma="0.5" length="5" minGap="2.5" maxSpeed="60" guiShape="passenger"/>
        <vType id="924" accel="1.4" decel="2" sigma="0.5" length="10" minGap="2.5" maxSpeed="60" guiShape="bus"/>

        <route id="route1" edges="1to0 0to2" />
        <route id="route2" edges="2to0 0to1" />
        <route id="route3" edges="3to0 0to4" />
        <route id="route4" edges="4to0 0to3" />
        <route id="route5" edges="0to4 0to2" />
        
        """

        lastVeh = 0
        vehNr = 0
        for i in range(N):
            if random.uniform(0, 1) < R1:
                print >> routes, '    <vehicle id="%i" type="923" route="route1" depart="%i" color="0,1,0"/>' % (
                    vehNr, i)
                vehNr += 1
                lastVeh = i
            if random.uniform(0, 1) < R2:
                print >> routes, '    <vehicle id="%i" type="923" route="route2" depart="%i" color="0,0,1"/>' % (
                    vehNr, i)
                vehNr += 1
                lastVeh = i
            if random.uniform(0, 1) < R3:
                print >> routes, '    <vehicle id="%i" type="924" route="route3" depart="%i" color="1,0,0"/>' % (
                    vehNr, i)
                vehNr += 1
                lastVeh = i
            if random.uniform(0, 1) < R4:
                print >> routes, '    <vehicle id="%i" type="924" route="route4" depart="%i" color="1,1,0"/>' % (
                    vehNr, i)
                vehNr += 1
                lastVeh = i
            if random.uniform(0, 1) < R5:
                print >> routes, '    <vehicle id="%i" type="923" route="route5" depart="%i" color="1,1,0"/>' % (
                    vehNr, i)
                vehNr += 1
                lastVeh = i
            

        print >> routes, "</routes>"

def run():
    """execute the TraCI control loop"""
    traci.init(PORT)
    programPointer = 0
    step = 1
    

    len_Priority_1 = 0
    len_Priority_2 = 0
    len_Priority_3 = 0
    len_Priority_4 = 0

    len_Priority_5 = 0
    len_Priority_6 = 0
    len_Priority_7 = 0
    len_Priority_8 = 0

    wpt1 = 0
    wpt2 = 0
    wpt3 = 0
    wpt4 = 0
    wpt5 = 0
    wpt6 = 0
    wpt7 = 0
    wpt8 = 0

    maxlwat1 = 0
    maxlwat2 = 0
    maxlwat3 = 0
    maxlwat4 = 0

    maxlwat5 = 0
    maxlwat6 = 0
    maxlwat7 = 0
    maxlwat8 = 0
    
    maxAvgWT = 0
    nextPhaseDu = 1
    currentState = 1
    nextState = 1
    flag1 = 0
    totalAvgFuelCons = 0
    thrPut = 0

    maxList1 = 0
    maxList2 = 0
    maxList3 = 0
    maxList4 = 0
    maxList5 = 0
    maxList6 = 0
    maxList7 = 0
    maxList8 = 0
    lastVeId = 0.0

    maxJam1 = 0
    maxJam2 = 0
    maxJam3 = 0
    maxJam4 = 0
    maxJam5 = 0
    maxJam6 = 0
    maxJam7 = 0
    maxJam8 = 0



    totalFuelConsumption = 0.0
    totalElecConsumption = 0.0
    totalWaitingTime = 0.0
    avgSpeed = 0.0

    realtime = 0
    nextCal = 0

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        


        #set yello phase

        #if currentState != nextState:
        #    traci.trafficlights.setRedYellowGreenState("0", PROGRAM[12])
        #    flag1 = 1
        #else:
        #    pass

        #flag1 = 0

        #Enter into calculation step

        #traci.trafficlights.setRedYellowGreenState("0", PROGRAM[12])
        #print "---- Enter ineer While: ----"

        currentTime = traci.simulation.getCurrentTime()
        realtime = currentTime/1000

        while realtime >= nextCal: #step % nextPhaseDu == 0:

            #Set special circumastance 

            Spc1 = 0
            Spc2 = 0
            Spc3 = 0
            Spc4 = 0
            Spc5 = 0
            Spc6 = 0
            Spc7 = 0
            Spc8 = 0
       
            #Add priority depending on number of velicle waiting on each lane

            lenHalt1 = traci.multientryexit.getLastStepHaltingNumber("0")
            lenHalt2 = traci.multientryexit.getLastStepHaltingNumber("1")
            lenHalt3 = traci.multientryexit.getLastStepHaltingNumber("2")
            lenHalt4 = traci.multientryexit.getLastStepHaltingNumber("3")
            lenHalt5 = traci.multientryexit.getLastStepHaltingNumber("4")
            lenHalt6 = traci.multientryexit.getLastStepHaltingNumber("5")
            lenHalt7 = traci.multientryexit.getLastStepHaltingNumber("6")
            lenHalt8 = traci.multientryexit.getLastStepHaltingNumber("7")

                     
                        


            #Add priority depending on number of velicle within the intersection 

            lenNumVehi1 = traci.multientryexit.getLastStepVehicleNumber("0")
            lenNumVehi2 = traci.multientryexit.getLastStepVehicleNumber("1")
            lenNumVehi3 = traci.multientryexit.getLastStepVehicleNumber("2")
            lenNumVehi4 = traci.multientryexit.getLastStepVehicleNumber("3")
            lenNumVehi5 = traci.multientryexit.getLastStepVehicleNumber("4")
            lenNumVehi6 = traci.multientryexit.getLastStepVehicleNumber("5")
            lenNumVehi7 = traci.multientryexit.getLastStepVehicleNumber("6")
            lenNumVehi8 = traci.multientryexit.getLastStepVehicleNumber("7")
            
            
            
            

            #Add priority by vehicle waiting time

            lenVehiWt1 = traci.multientryexit.getLastStepVehicleIDs("0")
            lenVehiWt2 = traci.multientryexit.getLastStepVehicleIDs("1")
            lenVehiWt3 = traci.multientryexit.getLastStepVehicleIDs("2")
            lenVehiWt4 = traci.multientryexit.getLastStepVehicleIDs("3")
            lenVehiWt5 = traci.multientryexit.getLastStepVehicleIDs("4")
            lenVehiWt6 = traci.multientryexit.getLastStepVehicleIDs("5")
            lenVehiWt7 = traci.multientryexit.getLastStepVehicleIDs("6")
            lenVehiWt8 = traci.multientryexit.getLastStepVehicleIDs("7")


            vtyp1 = 923

            if lenVehiWt1:
                for number1 in lenVehiWt1:
                    lenVWt1 = traci.vehicle.getWaitingTime(number1)
                    fc1 = traci.vehicle.getFuelConsumption(number1)
                    totalFuelConsumption = totalFuelConsumption + fc1
                    #ec1 = traci.vehicle.getElectricityConsumption(number1)
                    #totalElecConsumption = totalElecConsumption + ec1
                    vt1 = traci.vehicle.getTypeID(number1)
                    if lenVWt1 > 1:
                        if vt1 == vtyp1:
                            wpt1 = wpt1 + 1
                        else:
                            wpt1 = wpt1 + 2
                            

            if lenVehiWt2:
                for number2 in lenVehiWt2:
                    lenVWt2 = traci.vehicle.getWaitingTime(number2)
                    fc2 = traci.vehicle.getFuelConsumption(number2)
                    totalFuelConsumption = totalFuelConsumption + fc2
                    #ec2 = traci.vehicle.getElectricityConsumption(number2)
                    #totalElecConsumption = totalElecConsumption + ec2
                    vt2 = traci.vehicle.getTypeID(number2)
                    if lenVWt2 > 1:
                        if vt2 == vtyp1:
                            wpt2 = wpt2 + 1
                        else:
                            wpt2 = wpt2 + 2

            if lenVehiWt3:
                for number3 in lenVehiWt3:
                    lenVWt3 = traci.vehicle.getWaitingTime(number3)
                    fc3 = traci.vehicle.getFuelConsumption(number3)
                    totalFuelConsumption = totalFuelConsumption + fc3
                    #ec3 = traci.vehicle.getElectricityConsumption(number3)
                    #totalElecConsumption = totalElecConsumption + ec3
                    vt3 = traci.vehicle.getTypeID(number3)
                    if lenVWt3 > 1:
                        if vt3 == vtyp1:
                            wpt3 = wpt3 + 1
                        else:
                            wpt3 = wpt3 + 2

            if lenVehiWt4:
                for number4 in lenVehiWt4:
                    lenVWt4 = traci.vehicle.getWaitingTime(number4)
                    fc4 = traci.vehicle.getFuelConsumption(number4)
                    totalFuelConsumption = totalFuelConsumption + fc4
                    #ec4 = traci.vehicle.getElectricityConsumption(number4)
                    #totalElecConsumption = totalElecConsumption + ec4
                    vt4 = traci.vehicle.getTypeID(number4)
                    if lenVWt4 > 1:
                        if vt4 == vtyp1:
                            wpt4 = wpt4 + 1   
                        else:
                            wpt4 = wpt4 + 2

            if lenVehiWt5:
                for number5 in lenVehiWt5:
                    lenVWt5 = traci.vehicle.getWaitingTime(number5)
                    fc5 = traci.vehicle.getFuelConsumption(number5)
                    totalFuelConsumption = totalFuelConsumption + fc5
                    #ec5 = traci.vehicle.getElectricityConsumption(number5)
                    #totalElecConsumption = totalElecConsumption + ec5
                    vt5 = traci.vehicle.getTypeID(number5)
                    if lenVWt5 > 1:
                        if vt5 == vtyp1:
                            wpt5 = wpt5 + 1
                        else:
                            wpt5 = wpt5 + 2


            if lenVehiWt6:
                for number6 in lenVehiWt6:
                    lenVWt6 = traci.vehicle.getWaitingTime(number6)
                    fc6 = traci.vehicle.getFuelConsumption(number6)
                    totalFuelConsumption = totalFuelConsumption + fc6
                    #ec6 = traci.vehicle.getElectricityConsumption(number6)
                    #totalElecConsumption = totalElecConsumption + ec6
                    vt6 = traci.vehicle.getTypeID(number6)
                    if lenVWt6 > 1:
                        if vt6 == vtyp1:
                            wpt6 = wpt6 + 1
                        else:
                            wpt6 = wpt6 + 2


            if lenVehiWt7:
                for number7 in lenVehiWt7:
                    lenVWt7 = traci.vehicle.getWaitingTime(number7)
                    fc7 = traci.vehicle.getFuelConsumption(number7)
                    totalFuelConsumption = totalFuelConsumption + fc7
                    #ec7 = traci.vehicle.getElectricityConsumption(number7)
                    #totalElecConsumption = totalElecConsumption + ec7
                    vt7 = traci.vehicle.getTypeID(number7)
                    if lenVWt7 > 1:
                        if vt7 == vtyp1:
                            wpt7 = wpt7 + 1
                        else:
                            wpt7 = wpt7 + 2


            if lenVehiWt8:
                for number8 in lenVehiWt8:
                    lenVWt8 = traci.vehicle.getWaitingTime(number8)
                    fc8 = traci.vehicle.getFuelConsumption(number8)
                    totalFuelConsumption = totalFuelConsumption + fc8
                    #ec8 = traci.vehicle.getElectricityConsumption(number8)
                    #totalElecConsumption = totalElecConsumption + ec8
                    vt8 = traci.vehicle.getTypeID(number8)
                    if lenVWt8 > 1:
                        if vt8 == vtyp1:
                            wpt8 = wpt8 + 1
                        else:
                            wpt8 = wpt8 + 2
            
            

            




            #find the max priority lane


            len_Priority_1 = lenHalt1 + lenNumVehi1 + wpt1 + Spc1
            len_Priority_2 = lenHalt2 + lenNumVehi2 + wpt2 + Spc2
            len_Priority_3 = lenHalt3 + lenNumVehi3 + wpt3 + Spc3
            len_Priority_4 = lenHalt4 + lenNumVehi4 + wpt4 + Spc4
            len_Priority_5 = lenHalt5 + lenNumVehi5 + wpt5 + Spc5
            len_Priority_6 = lenHalt6 + lenNumVehi6 + wpt6 + Spc6
            len_Priority_7 = lenHalt7 + lenNumVehi7 + wpt7 + Spc7
            len_Priority_8 = lenHalt8 + lenNumVehi8 + wpt8 + Spc8


           

        # Disributed architerture Addition Start


            #Calculate corrosponding lane Neighbering Impact
            #
            sumAllLanePriority = float(len_Priority_1+len_Priority_2+len_Priority_3+len_Priority_4+len_Priority_5+len_Priority_6+len_Priority_7+len_Priority_8)
            

            #print "Sum of All Lane Priority: ", sumAllLanePriority
            


            naiLaneImcactForLane_1 = 0.0
            naiLaneImcactForLane_2 = 0.0
            naiLaneImcactForLane_3 = 0.0
            naiLaneImcactForLane_4 = 0.0

            naiLaneImcactForLane_5 = 0.0
            naiLaneImcactForLane_6 = 0.0
            naiLaneImcactForLane_7 = 0.0
            naiLaneImcactForLane_8 = 0.0



            print "LP1: ", len_Priority_1
            if(len_Priority_1 > 0):
                naiLaneImcactForLane_1 = len_Priority_1 / sumAllLanePriority
                print "NLI-LP1:", naiLaneImcactForLane_1
                #insert corrosponding lane Neighbering Impact to Central DB
                #
                ins1 = distributed.insertDt(intId,'1',naiLaneImcactForLane_1)
            
            print "Inserted Lane neibering impact: ", naiLaneImcactForLane_1


            print "LP2: ", len_Priority_2
            if(len_Priority_2 > 0):
                naiLaneImcactForLane_2 = len_Priority_2 / sumAllLanePriority
                print "NLI-LP2:", naiLaneImcactForLane_2
                #insert corrosponding lane Neighbering Impact to Central DB
                #
                ins2 = distributed.insertDt(intId,'2',naiLaneImcactForLane_2)
            
            print "Inserted Lane neibering impact: ", naiLaneImcactForLane_2


            print "LP3: ", len_Priority_3
            if(len_Priority_3 > 0):
                naiLaneImcactForLane_3 = len_Priority_3 / sumAllLanePriority
                print "NLI-LP3:", naiLaneImcactForLane_3
                #insert corrosponding lane Neighbering Impact to Central DB
                #
                ins3 = distributed.insertDt(intId,'3',naiLaneImcactForLane_3)
            
            print "Inserted Lane neibering impact: ", naiLaneImcactForLane_3


            print "LP4: ", len_Priority_4
            if(len_Priority_4 > 0):
                naiLaneImcactForLane_4 = len_Priority_4 / sumAllLanePriority
                print "NLI-LP4:", naiLaneImcactForLane_4
                #insert corrosponding lane Neighbering Impact to Central DB
                #
                ins4 = distributed.insertDt(intId,'4',naiLaneImcactForLane_4)
            
            print "Inserted Lane neibering impact: ", naiLaneImcactForLane_4


            print "LP5: ", len_Priority_5
            if(len_Priority_5 > 0):
                naiLaneImcactForLane_5 = len_Priority_5 / sumAllLanePriority
                print "NLI-LP5:", naiLaneImcactForLane_5
                #insert corrosponding lane Neighbering Impact to Central DB
                #
                ins5 = distributed.insertDt2(intId,'5',naiLaneImcactForLane_5)
            
            print "Inserted Lane neibering impact: ", naiLaneImcactForLane_5


            print "LP6: ", len_Priority_6
            if(len_Priority_6 > 0):
                naiLaneImcactForLane_6 = len_Priority_6 / sumAllLanePriority
                print "NLI-LP6:", naiLaneImcactForLane_6
                #insert corrosponding lane Neighbering Impact to Central DB
                #
                ins6 = distributed.insertDt2(intId,'6',naiLaneImcactForLane_6)
            
            print "Inserted Lane neibering impact: ", naiLaneImcactForLane_6


            print "LP7: ", len_Priority_7
            if(len_Priority_7 > 0):
                naiLaneImcactForLane_7 = len_Priority_7 / sumAllLanePriority
                print "NLI-LP7:", naiLaneImcactForLane_7
                #insert corrosponding lane Neighbering Impact to Central DB
                #
                ins7 = distributed.insertDt(intId,'7',naiLaneImcactForLane_7)
            
            print "Inserted Lane neibering impact: ", naiLaneImcactForLane_7


            print "LP8: ", len_Priority_8
            if(len_Priority_8 > 0):
                naiLaneImcactForLane_8 = len_Priority_8 / sumAllLanePriority
                print "NLI-LP8:", naiLaneImcactForLane_8
                #insert corrosponding lane Neighbering Impact to Central DB
                #
                ins8 = distributed.insertDt(intId,'8',naiLaneImcactForLane_8)
            
            print "Inserted Lane neibering impact: ", naiLaneImcactForLane_8





            #Fetch corrosponding lane Neighbering Impact
            #

            rows1 = distributed.fetchDependency(intId,'1')
            neiLaneImpSum_1 = 0.0
            for row in rows1:
            #    print "Neighbering Lane Impact for 902_1:",row[0], " ", row[1], " ", row[2], " ", row[3], " ", row[4]
                print "Neighbering Lane Impact for Int: ",row[1], " and Node: ", row[2], " is: "
                neiImpact = distributed.fetchNeiberingImpact(row[1],row[2])
                print neiImpact[0][0]
                neiLaneImpSum_1 = neiLaneImpSum_1 + neiImpact[0][0]

            print "Naibaring Impact Sum for Lane 1 : ",neiLaneImpSum_1
            len_Priority_1 = len_Priority_1 - (neiLaneImpSum_1*5)


            rows2 = distributed.fetchDependency(intId,'2')
            neiLaneImpSum_2 = 0.0
            for row in rows2:
            #    print "Neighbering Lane Impact for 902_1:",row[0], " ", row[1], " ", row[2], " ", row[3], " ", row[4]
                print "Neighbering Lane Impact for Int: ",row[1], " and Node: ", row[2], " is: "
                neiImpact = distributed.fetchNeiberingImpact(row[1],row[2])
                print neiImpact[0][0]
                neiLaneImpSum_2 = neiLaneImpSum_2 + neiImpact[0][0]

            print "Naibaring Impact Sum for Lane 2 : ",neiLaneImpSum_2
            len_Priority_2 = len_Priority_2 - (neiLaneImpSum_2 * 5)


            rows3 = distributed.fetchDependency(intId,'3')
            neiLaneImpSum_3 = 0.0
            for row in rows3:
            #    print "Neighbering Lane Impact for 902_1:",row[0], " ", row[1], " ", row[2], " ", row[3], " ", row[4]
                print "Neighbering Lane Impact for Int: ",row[1], " and Node: ", row[2], " is: "
                neiImpact = distributed.fetchNeiberingImpact(row[1],row[2])
                print neiImpact[0][0]
                neiLaneImpSum_3 = neiLaneImpSum_3 + neiImpact[0][0]

            print "Naibaring Impact Sum for Lane 3 : ",neiLaneImpSum_3
            len_Priority_3 = len_Priority_3 - (neiLaneImpSum_3 * 5)


            rows4 = distributed.fetchDependency(intId,'4')
            neiLaneImpSum_4 = 0.0
            for row in rows4:
            #    print "Neighbering Lane Impact for 902_1:",row[0], " ", row[1], " ", row[2], " ", row[3], " ", row[4]
                print "Neighbering Lane Impact for Int: ",row[1], " and Node: ", row[2], " is: "
                neiImpact = distributed.fetchNeiberingImpact(row[1],row[2])
                print neiImpact[0][0]
                neiLaneImpSum_4 = neiLaneImpSum_4 + neiImpact[0][0]

            print "Naibaring Impact Sum for Lane 4 : ",neiLaneImpSum_4
            len_Priority_4 = len_Priority_4 - (neiLaneImpSum_4 * 5)


            rows5 = distributed.fetchDependency(intId,'5')
            neiLaneImpSum_5 = 0.0
            for row in rows5:
            #    print "Neighbering Lane Impact for 902_1:",row[0], " ", row[1], " ", row[2], " ", row[3], " ", row[4]
                print "Neighbering Lane Impact for Int: ",row[1], " and Node: ", row[2], " is: "
                neiImpact = distributed.fetchNeiberingImpact(row[1],row[2])
                print neiImpact[0][0]
                neiLaneImpSum_5 = neiLaneImpSum_5 + neiImpact[0][0]

            print "Naibaring Impact Sum for Lane 5 : ",neiLaneImpSum_5
            len_Priority_5 = len_Priority_5 - (neiLaneImpSum_5 * 5)


            rows6 = distributed.fetchDependency(intId,'6')
            neiLaneImpSum_6 = 0.0
            for row in rows6:
            #    print "Neighbering Lane Impact for 902_1:",row[0], " ", row[1], " ", row[2], " ", row[3], " ", row[4]
                print "Neighbering Lane Impact for Int: ",row[1], " and Node: ", row[2], " is: "
                neiImpact = distributed.fetchNeiberingImpact(row[1],row[2])
                print neiImpact[0][0]
                neiLaneImpSum_6 = neiLaneImpSum_6 + neiImpact[0][0]

            print "Naibaring Impact Sum for Lane 6 : ",neiLaneImpSum_6
            len_Priority_6 = len_Priority_6 - (neiLaneImpSum_6 * 5)


            rows7 = distributed.fetchDependency(intId,'7')
            neiLaneImpSum_7 = 0.0
            for row in rows7:
            #    print "Neighbering Lane Impact for 902_1:",row[0], " ", row[1], " ", row[2], " ", row[3], " ", row[4]
                print "Neighbering Lane Impact for Int: ",row[1], " and Node: ", row[2], " is: "
                neiImpact = distributed.fetchNeiberingImpact(row[1],row[2])
                print neiImpact[0][0]
                neiLaneImpSum_7 = neiLaneImpSum_7 + neiImpact[0][0]

            print "Naibaring Impact Sum for Lane 7 : ",neiLaneImpSum_7
            len_Priority_7 = len_Priority_7 - (neiLaneImpSum_7 * 5)


            rows8 = distributed.fetchDependency(intId,'8')
            neiLaneImpSum_8 = 0.0
            for row in rows8:
            #    print "Neighbering Lane Impact for 902_1:",row[0], " ", row[1], " ", row[2], " ", row[3], " ", row[4]
                print "Neighbering Lane Impact for Int: ",row[1], " and Node: ", row[2], " is: "
                neiImpact = distributed.fetchNeiberingImpact(row[1],row[2])
                print neiImpact[0][0]
                neiLaneImpSum_8 = neiLaneImpSum_8 + neiImpact[0][0]

            print "Naibaring Impact Sum for Lane 8 : ",neiLaneImpSum_8
            len_Priority_8 = len_Priority_8 - (neiLaneImpSum_8 * 5)










        # Disributed architerture Addition End


            
            
            #Find Case priority

            Cp1 = len_Priority_1 + len_Priority_3
            Cp2 = len_Priority_1 + len_Priority_2
            Cp3 = len_Priority_1 + len_Priority_8
            Cp4 = len_Priority_2 + len_Priority_4

            Cp5 = len_Priority_2 + len_Priority_5
            Cp6 = len_Priority_3 + len_Priority_4
            Cp7 = len_Priority_3 + len_Priority_6
            Cp8 = len_Priority_4 + len_Priority_7

            Cp9 = len_Priority_5 + len_Priority_6
            Cp10 = len_Priority_6 + len_Priority_8
            Cp11 = len_Priority_7 + len_Priority_8
            Cp12 = len_Priority_5 + len_Priority_7


            #choose best case

        
            list2 = [Cp1, Cp2, Cp3, Cp4, Cp5, Cp6, Cp7, Cp8, Cp9, Cp10, Cp11, Cp12]
        

            data = {key: value for key, value in locals().iteritems() if 'Cp' in key}

            key, value = max(data.iteritems(), key=lambda x: x[1])

            

            #set program pointer




            if value > 0:         
                if value == Cp1:
                    programPointer = 0; Cp1=0;
                    

                elif value == Cp2:
                    programPointer = 1; Cp2=0;
                    

                elif value == Cp3:
                    programPointer = 8; Cp3=0;
                    

                elif value == Cp4:
                    programPointer = 2; Cp4=0;


                elif value == Cp5:
                    programPointer = 9; Cp5=0;
                    

                elif value == Cp6:
                    programPointer = 3; Cp6=0;
                    

                elif value == Cp7:
                    programPointer = 10; Cp7=0;
                    
           
                elif value == Cp8:
                    programPointer = 11; Cp8=0;


                elif value == Cp9:
                    programPointer = 7; Cp9=0;


                elif value == Cp10:
                    programPointer = 6; Cp10=0;


                elif value == Cp11:
                    programPointer = 5; Cp11=0;

            
                else: programPointer = 4; Cp12=0;


                #set next phase duration



                

                temp = programPointer + 1

                if temp == 1:
                    temp2 = max(lenNumVehi1, lenNumVehi3)
                    if temp2 > 1:
                        nextPhaseDu = temp2 / 1
                elif temp == 2:
                    temp2 = max(lenNumVehi1, lenNumVehi2)
                    if temp2 > 1:
                        nextPhaseDu = temp2 / 1
                elif temp == 3:
                    temp2 = max(lenNumVehi2, lenNumVehi4)
                    if temp2 > 1:
                        nextPhaseDu = temp2 / 1
                elif temp == 4:
                    temp2 = max(lenNumVehi3, lenNumVehi4)
                    if temp2 > 1:
                        nextPhaseDu = temp2 / 1

                elif temp == 5:
                    temp2 = max(lenNumVehi7, lenNumVehi5)
                    if temp2 > 1:
                        nextPhaseDu = temp2 / 1
                elif temp == 6:
                    temp2 = max(lenNumVehi7, lenNumVehi8)
                    if temp2 > 1:
                        nextPhaseDu = temp2 / 1
                elif temp == 7:
                    temp2 = max(lenNumVehi8, lenNumVehi6)
                    if temp2 > 1:
                        nextPhaseDu = temp2 / 1
                elif temp == 8:
                    temp2 = max(lenNumVehi5, lenNumVehi6)
                    if temp2 > 1:
                        nextPhaseDu = temp2 / 1

                elif temp == 9:
                    temp2 = max(lenNumVehi1, lenNumVehi8)
                    if temp2 > 1:
                        nextPhaseDu = temp2 / 1
                elif temp == 10:
                    temp2 = max(lenNumVehi5, lenNumVehi2)
                    if temp2 > 1:
                        nextPhaseDu = temp2 / 1
                elif temp == 11:
                    temp2 = max(lenNumVehi6, lenNumVehi3)
                    if temp2 > 1:
                        nextPhaseDu = temp2 / 1
                else:
                    temp2 = max(lenNumVehi7, lenNumVehi4)
                    if temp2 > 1:
                        nextPhaseDu = temp2 / 1



                if nextPhaseDu < 1:
                    nextPhaseDu = 1
                else:
                    pass


            # determine fuel consumption of the vehicles

            lfc1 = traci.lane.getFuelConsumption("1to0_0")
            lfc2 = traci.lane.getFuelConsumption("1to0_1")
            lfc3 = traci.lane.getFuelConsumption("2to0_0")
            lfc4 = traci.lane.getFuelConsumption("2to0_1")
            lfc5 = traci.lane.getFuelConsumption("3to0_0")
            lfc6 = traci.lane.getFuelConsumption("3to0_1")
            lfc7 = traci.lane.getFuelConsumption("4to0_0")
            lfc8 = traci.lane.getFuelConsumption("4to0_1")

            PerStepAvgFuelCons = (lfc1+lfc2+lfc3+lfc4+lfc5+lfc6+lfc7+lfc8)/8

            totalAvgFuelCons = totalAvgFuelCons + PerStepAvgFuelCons



            
            # determine throughput of the junction

            if lenVehiWt1:
                maxList1 = max(lenVehiWt1)
            else:
                pass
            if lenVehiWt2:
                maxList2 = max(lenVehiWt2)
            else:
                pass
            if lenVehiWt3:
                maxList3 = max(lenVehiWt3)
            else:
                pass
            if lenVehiWt4:
                maxList4 = max(lenVehiWt4)
            else:
                pass
            if lenVehiWt5:
                maxList5 = max(lenVehiWt5)
            else:
                pass
            if lenVehiWt6:
                maxList6 = max(lenVehiWt6)
            else:
                pass
            if lenVehiWt7:
                maxList7 = max(lenVehiWt7)
            else:
                pass
            if lenVehiWt8:
                maxList8 = max(lenVehiWt8)
            else:
                pass

            list3 = [maxList1, maxList2, maxList3, maxList4, maxList5, maxList6, maxList7, maxList8]
        
            lastVeId = max(list3)

            lastVeId1 = float(lastVeId)
            step1 = float(step)
            if (step1 > 0.0):
                if (lastVeId1 > 0.0):
                    thrPut = (lastVeId1/step1)
                else:
                    pass
            else:
                pass
            

            # determine waiting time of the vehicles


            lwat1 = traci.lane.getWaitingTime("1to0_0")
            lwat2 = traci.lane.getWaitingTime("1to0_1")
            lwat3 = traci.lane.getWaitingTime("2to0_0")
            lwat4 = traci.lane.getWaitingTime("2to0_1")
            lwat5 = traci.lane.getWaitingTime("3to0_0")
            lwat6 = traci.lane.getWaitingTime("3to0_1")
            lwat7 = traci.lane.getWaitingTime("4to0_0")
            lwat8 = traci.lane.getWaitingTime("4to0_1")

            totalWaitingTimeStep = lwat1 + lwat2 + lwat3 + lwat4 + lwat5 + lwat6 + lwat7 + lwat8
            totalWaitingTime = totalWaitingTime + totalWaitingTimeStep

            if lwat1 > maxlwat1:
                maxlwat1 = lwat1
            elif lwat2 > maxlwat2:
                maxlwat2 = lwat2
            elif lwat3 > maxlwat3:
                maxlwat3 = lwat3
            elif lwat4 > maxlwat4:
                maxlwat4 = lwat4
            elif lwat5 > maxlwat5:
                maxlwat5 = lwat5
            elif lwat6 > maxlwat6:
                maxlwat6 = lwat6
            elif lwat7 > maxlwat7:
                maxlwat7 = lwat7
            elif lwat8 > maxlwat8:
                maxlwat8 = lwat8

            AvgWT = (lwat1+lwat2+lwat3+lwat4+lwat5+lwat6+lwat7+lwat8)/8

            if AvgWT > maxAvgWT:
                maxAvgWT = AvgWT
            else:
                pass

             # determine Travel time of the vehicles


            Tvt1 = traci.lane.getMaxSpeed("1to0_0")
            Tvt2 = traci.lane.getMaxSpeed("1to0_1")
            Tvt3 = traci.lane.getMaxSpeed("2to0_0")
            Tvt4 = traci.lane.getMaxSpeed("2to0_1")
            Tvt5 = traci.lane.getMaxSpeed("3to0_0")
            Tvt6 = traci.lane.getMaxSpeed("3to0_1")
            Tvt7 = traci.lane.getMaxSpeed("4to0_0")
            Tvt8 = traci.lane.getMaxSpeed("4to0_1")

            avgSpeedStep = (Tvt1 + Tvt2 + Tvt3 + Tvt4 + Tvt5 + Tvt6 + Tvt7 + Tvt8) / 8
            
            avgSpeed = avgSpeed + avgSpeedStep

            totalAvgSeppd = avgSpeed / step



            # determine jam length

            jamLength1 = traci.areal.getJamLengthMeters("lad1")
            jamLength2 = traci.areal.getJamLengthMeters("lad2")
            jamLength3 = traci.areal.getJamLengthMeters("lad3")
            jamLength4 = traci.areal.getJamLengthMeters("lad4")

            jamLength5 = traci.areal.getJamLengthMeters("lad5")
            jamLength6 = traci.areal.getJamLengthMeters("lad6")
            jamLength7 = traci.areal.getJamLengthMeters("lad7")
            jamLength8 = traci.areal.getJamLengthMeters("lad8")


            if jamLength1 > maxJam1:
                maxJam1 = jamLength1
            elif jamLength2 > maxJam2:
                maxJam2 = jamLength2
            elif jamLength3 > maxJam3:
                maxJam3 = jamLength3
            elif jamLength4 > maxJam4:
                maxJam4 = jamLength4
            elif jamLength5 > maxJam5:
                maxJam5 = jamLength5
            elif jamLength6 > maxJam6:
                maxJam6 = jamLength6
            elif jamLength7 > maxJam7:
                maxJam7 = jamLength7
            elif jamLength8 > maxJam8:
                maxJam8 = jamLength8
            
            maxJam = max(maxJam1, maxJam2, maxJam3, maxJam4, maxJam5, maxJam6, maxJam7, maxJam8)
            # show output :  

            print "For step: ",step


            
            



            print "1to0_0 lane Max waiting time: ",maxlwat1
            print "1to0_0 Lane Max Jam Length : ",maxJam1
            #print "1to0_0 Lane Max priority : ",len_Priority_1
            print "1to0_1 lane Max waiting time: ",maxlwat2
            print "1to0_1 Lane Max Jam Length : ",maxJam2
            #print "1to0_0 Lane Max priority : ",len_Priority_2
            print "2to0_0 lane Max waiting time: ",maxlwat3
            print "2to0_0 Lane Max Jam Length : ",maxJam3
            #print "1to0_0 Lane Max priority : ",len_Priority_3
            print "2to0_1 lane Max waiting time: ",maxlwat4
            print "2to0_1 Lane Max Jam Length : ",maxJam4
            #print "1to0_0 Lane Max priority : ",len_Priority_4
            print "3to0_0 lane Max waiting time: ",maxlwat5
            print "3to0_0 Lane Max Jam Length : ",maxJam5
            #print "1to0_0 Lane Max priority : ",len_Priority_1
            print "3to0_1 lane Max waiting time: ",maxlwat6
            print "3to0_1 Lane Max Jam Length : ",maxJam6
            #print "1to0_0 Lane Max priority : ",len_Priority_1
            print "4to0_0 lane Max waiting time: ",maxlwat7
            print "4to0_0 Lane Max Jam Length : ",maxJam7
            #print "1to0_0 Lane Max priority : ",len_Priority_7
            print "4to0_1 lane Max waiting time: ",maxlwat8
            print "4to0_1 Lane Max Jam Length : ",maxJam8
            #print "1to0_0 Lane Max priority : ",len_Priority_8

            currentState = traci.trafficlights.getRedYellowGreenState("0")
            phaseDuration = traci.trafficlights.getPhaseDuration("0")
            

            list1 = ['rrgrrrgr', 'rrrrrrgg', 'rrrgrrrg', 'rrggrrrr', 'grrrgrrr', 'ggrrrrrr', 'rgrrrgrr', 'rrrrggrr', 'rgrrrrgr', 'rrrrgrrg', 'rrgrrgrr', 'grrgrrrr', 'yyyyyyyy']


            nextState  = list1[programPointer]



            var1 ="Not Set"

            if Spc1 > 0:
                var1 = "Priority Added on lane 1to0_0"
            elif Spc2 > 0:
                var1 = "Priority Added on lane 1to0_1"
            elif Spc3 > 0:
                var1 = "Priority Added on lane 2to0_0"
            elif Spc4 > 0:
                var1 = "Priority Added on lane 2to0_1"
            elif Spc5 > 0:
                var1 = "Priority Added on lane 3to0_0"
            elif Spc6 > 0:
                var1 = "Priority Added on lane 3to0_1"
            elif Spc7 > 0:
                var1 = "Priority Added on lane 4to0_0"
            elif Spc8 > 0:
                var1 = "Priority Added on lane 4to0_1"


            print "Current State: ",currentState
            print "Next State: ",nextState
            print "Next Case: ",key, value
            print "Next Phase Duration: ",nextPhaseDu
            print "Avarage Waiting Time: ",AvgWT
            print " "

            print "Print priority statue: ",var1
            print "Max Avarage Waiting Time (per lane): ",maxAvgWT
            print "Max Jam Length: ",maxJam
            print "Total Fuel Consumption: ",totalFuelConsumption
            print "Total Waiting Time: ",totalWaitingTime
            nextCal = realtime + nextPhaseDu
            print "Real Time: ", realtime
            print "Next Calculation Time: ", nextCal
            print "Throughput: ",thrPut
            print " ---- ---- ---- ----"





            #set next phase to the len

            #traci.trafficlights.setRedYellowGreenState(
            #    "0", PROGRAM[programPointer])
            traci.trafficlights.setPhase('0', programPointer)
            traci.trafficlights.setPhaseDuration('0',nextPhaseDu)

            break;

        step += 1

    traci.close()
    sys.stdout.flush()



def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options


# this is the main entry point of this script
if __name__ == "__main__":
    options = get_options()

    # this script has been called from the command line. It will start sumo as a
    # server, then connect and run
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # first, generate the route file for this simulation
    #generate_routefile()

    # this is the normal way of using traci. sumo is started as a
    # subprocess and then the python script connects and runs
    sumoProcess = subprocess.Popen([sumoBinary, "-c", "data/cross.sumocfg", "--tripinfo-output",
                                    "tripinfo.xml", "--remote-port", str(PORT)], stdout=sys.stdout, stderr=sys.stderr)
    run()
    sumoProcess.wait()
