import xml.etree.ElementTree as et
import numpy as np

def VAF_Siuu(xmlfile, size_of_frame, frame_interval):
    try:
        tree = et.parse(xmlfile);
    except OSError:
        print('Failed to read XML file {}.'.format(xmlfile) )
    root =  tree.getroot()
    nTracks = int(root.attrib['nTracks'])
    tracks = {}
    for i in range(nTracks):
        trackIdx = str(i)
        tracks[trackIdx] = {}
        # nSpots = int(root[i].attrib['nSpots'])
        nSpots = len(root[i].findall('detection'))
        tracks[trackIdx]['nSpots'] = nSpots
        trackData = np.array([ ]).reshape(0, 4)
        for j in range(nSpots):
            t = float(root[i][j].attrib['t'])
            x = float(root[i][j].attrib['x'])
            y = float(root[i][j].attrib['y'])
            z = float(root[i][j].attrib['z'])
            spotData = np.array([t, x, y, z])
            trackData = np.vstack((trackData, spotData))
        tracks[trackIdx]['trackData'] = trackData
    lenth_of_frame = float(size_of_frame) #The unit of coordinates should be in microns.
    frame_time = float(frame_interval)
    # multiplier = 1331.20/1024
    Velocity_Matrix = {}
    Number_Of_Particles = len(tracks)
    for Particles in range(Number_Of_Particles):
        Coordinates_Matrix = tracks[str(Particles)]['trackData']
        Number_Of_Coordinates = len(Coordinates_Matrix)
        velo_vect = {}
        for j in range(Number_Of_Coordinates):
            if j < Number_Of_Coordinates - 1:
                #check x boundary and get the x component for the velocity vector
                absolute_displacement_x = abs(Coordinates_Matrix[j+1][1]-Coordinates_Matrix[j][1])
                if absolute_displacement_x < lenth_of_frame - absolute_displacement_x:
                    '''The cell does not cross the x boundary'''
                    # delta_x = multiplier * (Coordinates_Matrix[j+1][1]-Coordinates_Matrix[j][1])
                    delta_x = Coordinates_Matrix[j+1][1]-Coordinates_Matrix[j][1]
                else:
                    '''The cell cross the x boundary'''
                    if Coordinates_Matrix[j+1][1] > Coordinates_Matrix[j][1]:
                        # delta_x = multiplier * (Coordinates_Matrix[j+1][1]-Coordinates_Matrix[j][1] - lenth_of_frame)
                        delta_x = Coordinates_Matrix[j+1][1]-Coordinates_Matrix[j][1] - lenth_of_frame
                    if Coordinates_Matrix[j+1][1] < Coordinates_Matrix[j][1]:
                        # delta_x = multiplier * (Coordinates_Matrix[j+1][1]-Coordinates_Matrix[j][1] + lenth_of_frame)
                        delta_x = Coordinates_Matrix[j+1][1]-Coordinates_Matrix[j][1] + lenth_of_frame
                #check y boundary and get the y component for the velocity vector
                absolute_displacement_y = abs(Coordinates_Matrix[j+1][2]-Coordinates_Matrix[j][2])
                if absolute_displacement_y < lenth_of_frame - absolute_displacement_y:
                    '''The cell does not cross the y boundary'''
                    # delta_y = multiplier * (Coordinates_Matrix[j+1][2]-Coordinates_Matrix[j][2])
                    delta_y = Coordinates_Matrix[j+1][2]-Coordinates_Matrix[j][2]
                else:
                    '''The cell cross the y boundary'''
                    if Coordinates_Matrix[j+1][2] > Coordinates_Matrix[j][2]:
                        # delta_x = multiplier * (Coordinates_Matrix[j+1][2]-Coordinates_Matrix[j][2] - lenth_of_frame)
                        delta_x = Coordinates_Matrix[j+1][2]-Coordinates_Matrix[j][2] - lenth_of_frame
                    if Coordinates_Matrix[j+1][2] < Coordinates_Matrix[j][2]:
                        # delta_x = multiplier * (Coordinates_Matrix[j+1][2]-Coordinates_Matrix[j][2] + lenth_of_frame)
                        delta_x = Coordinates_Matrix[j+1][2]-Coordinates_Matrix[j][2] + lenth_of_frame
                velo_vect[j * frame_time] = np.array([delta_x, delta_y])
        Velocity_Matrix[str(Particles)] = velo_vect
        vaf = {}
    denominator_list = []
    numerator_dictionary = {}
    cells = len(Velocity_Matrix)
    time_list = []
    for cell in range(cells):
        coordinates = Velocity_Matrix[str(cell)]
        time_list.append(len(coordinates))
        # Generate the list of the dot production of the V0 and V0
        v_0 = coordinates[0]
        domi = (v_0[0] * v_0[0]) + (v_0[1] * v_0[1])
        denominator_list.append(domi)
        # Generate the dictionary of the dot production of Vt and V0
        num_list = {}
        for t in coordinates.keys():
            x = coordinates[t][0]
            y = coordinates[t][1]
            x_0 = coordinates[0][0]
            y_0 = coordinates[0][1]
            num = (x * x_0) + (y * y_0)
            num_list[t] = num
        numerator_dictionary[str(cell)] = num_list
    No_Frame_longest_TimePoint = time_list.index(max(time_list))
    time_points = numerator_dictionary[str(No_Frame_longest_TimePoint)].keys()
    elements = len(numerator_dictionary)
    Denominator = np.mean(denominator_list)
    for time in time_points:
        dot_product = []
        for element in range(elements):
            if time in numerator_dictionary[str(element)].keys():
                dot_product.append(numerator_dictionary[str(element)][time])
        vaf[time] = np.mean(dot_product) / Denominator
    return vaf            