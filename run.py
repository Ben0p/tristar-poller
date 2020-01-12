from pyModbusTCP.client import ModbusClient
import time



def modbus(ip):

    dip = "Offline"

    # Initiate modbus client
    c = ModbusClient(host=ip, port=502, auto_open=True, timeout=1)
    
    # Read Modbus outputs 
    reg = c.read_holding_registers(0, 100)

    # Close Modbus connection
    c.close()
    


    if reg:

        # Register 49 (array position 48) is dip switch settings
        # Convert float response to 8 bit binary string and reverse order (all in one line boiiii)
        dip = f'{reg[48]:08b}'[::-1]
        # Convert to array
        dip = [c for c in dip]

    
    return(dip)
    

def mode(dip):

    # Get MPPT mode

    if dip[0] == '0':
        mode = "Charge"

    elif dip[0] == '1' and dip[6] == '0' and dip[7] == '0':
        mode = "Load"

    elif dip[0] == '1' and dip[6] == '1' and dip[7] == '0':
        mode = "Diversion"

    elif dip[0] == '1' and dip[6] == '0' and dip[7] == '1':
        mode = "Lighting"

    return(mode)


def voltage(dip):

    # Get voltage setting
    
    if dip[1] == '0' and dip[2] == '0':
        voltage = "Auto"

    elif dip[1] == '0' and dip[2] == '1':
        voltage = "12v"

    elif dip[1] == '1' and dip[2] == '0':
        voltage = "24v"

    elif dip[1] == '1' and dip[2] == '1':
        voltage = "48v"

    return(voltage)
        

def setpoints(dip):

    # Get set point values

    if dip[3] == '0' and dip[4] == '0' and dip[5] == '0':
        ab = "14.00 V"
        fl = "13.4 V"
        eq = "None"

    elif dip[3] == '0' and dip[4] == '0' and dip[5] == '1':
        ab = "14.15 V"
        fl = "13.4 V"
        eq = "14.2 V"
        
    elif dip[3] == '0' and dip[4] == '1' and dip[5] == '0':
        ab = "14.15 V"
        fl = "13.4 V"
        eq = "14.4 V"

    elif dip[3] == '0' and dip[4] == '1' and dip[5] == '1':
        ab = "14.35 V"
        fl = "13.4 V"
        eq = "15.1 V"

    elif dip[3] == '1' and dip[4] == '0' and dip[5] == '0':
        ab = "14.40 V"
        fl = "13.4 V"
        eq = "15.3 V"

    elif dip[3] == '1' and dip[4] == '0' and dip[5] == '1':
        ab = "14.80 V"
        fl = "13.4 V"
        eq = "15.3 V"

    elif dip[3] == '1' and dip[4] == '1' and dip[5] == '0':
        ab = "15.00 V"
        fl = "13.4 V"
        eq = "15.3 V"

    else:
        ab = "Invalid"
        fl = "Invalid"
        eq = "Invalid"

    return(ab,fl,eq)


def equalize(dip):

    # Get equalize settings

    if dip[6] == '0':
        eq_mode = "Manual"

    elif dip[6] == "1":
        eq_mode = "Automatic"

    return(eq_mode)


def noise(dip):

    # Noise reduction setting

    if dip[7] == '0':
        nrm = "PWM"

    elif dip[7] == "1":
        nrm = "On-Off Charging"

    return(nrm)

   
def main():
    
    with open("export.csv", 'r') as f:
        with open("dip_sticks.csv", 'w') as o:
            # .csv heading
            o.write('Asset,IP,DIP 1,DIP 2,DIP 3,DIP 4,DIP 5,DIP 6,DIP 7,DIP 8,Mode,Voltage,Set Point - Absorb,Set Point - Float,Set Point - Equalize,Equalize,Noise Reduction\n')

            # Each line in input .csv
            for idx, line in enumerate(f):

                # Skip headings
                if idx == 0:
                    continue

                # Get ip and name of MPPTs
                line = line.split(',')
                name = line[2]
                ip = line[4]
                ip = ip.replace('"', '')

                # Get dip switch positions through modbus function
                dip = modbus(ip)

                # Convert dip switch positions to actual settings
                if dip != 'Offline':
                    _mode = mode(dip)
                    _voltage = voltage(dip)
                    _setpoints = setpoints(dip)
                    _equalize = equalize(dip)
                    _noise = noise(dip)
                    
                    print(f'{name} - {dip}')


                    # Write to output .csv 
                    o.write(f'{name},'
                            f'{ip},'
                            f'{dip[0]},{dip[1]},{dip[2]},{dip[3]},{dip[4]},{dip[5]},{dip[6]},{dip[7]},'
                            f'{_mode},'
                            f'{_voltage},'
                            f'{_setpoints[0]},'
                            f'{_setpoints[1]},'
                            f'{_setpoints[2]},'
                            f'{_equalize},'
                            f'{_noise}\n')
                elif dip == "Offline":
                    o.write(f'{name},{ip},Offline\n')

            o.close()
        f.close()

                
                
            
            



if __name__ == "__main__":
    main()
