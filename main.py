import subprocess
from matplotlib import pyplot as plt
import numpy as np

# Ping-to-Graph
# Python script that opens output file from ping tool from windows
# After data is loaded graphs are created and drawn
# It can be used to see anomalies in LAN network between PC and Router
# Or it can show if there is any ping spikes between Your PC and Server/Site
#
# Command to run in cmd
# ping google.com -n 350 > ping.txt
#
# After its done place ping.txt in same folder as main.py



def main():
    fileForOpening = "Ping-to-Graph\\ping.txt"
    bigGraph = "Ping-to-Graph\\Big-ping-graph.pdf"
    smallGraph = "Ping-to-Graph\\Small-ping-graph.pdf"

    convertedPingData, infoAboutServer = loadData(fileForOpening)

    under2ms = 0
    under10ms = 0
    between = 0

    xAxisData = []
    yAxisData = []

    # Converting ping data from string into
    # int for easier plotting
    for y in convertedPingData:
        yAxisData.append(int(y))

    # Based on how many packets are there we are
    # creating X Axis data 
    for x in range(0, len(yAxisData)):
        xAxisData.append(int(x))

    # Low value pings are stored here for
    # LAN network diagnostics 
    for x in convertedPingData:
        if int(x) < 3:
            under2ms = under2ms + 1
        if int(x) > 10:
            under10ms = under10ms + 1
        if 10 >= int(x) > 2:
            between = between + 1

    # Appending all low value lowPingValues to list so we
    # can work with it later

    lowPingValues = [under2ms, under10ms, between]

    # If we have any data for Y Axis (any ping info in ms)
    # we are creating 2 graphs
    if yAxisData:
        drawBigGraph(xAxisData, yAxisData, infoAboutServer, lowPingValues, bigGraph)
        drawSmallGraph(xAxisData, yAxisData, infoAboutServer, lowPingValues, smallGraph)
    else:
        print('\nInput file is either empty or it has wrong data.')

    input("Press Enter to continue...")


# Returns percentage
def percentage(part, whole):
    return 100 * float(part) / float(whole)


# Loading and parsing data
def loadData(fileToOpen):
    pingData = []
    statistics = []
    fileText = None

    try:
        openedFile = open(fileToOpen)
        print("Opened file: " + fileToOpen)
        fileText = openedFile.readlines()
    except OSError:
        print("File cannot be opened.")

    print("Reading data and processing.")
    if fileText is not None:
        for t in fileText:
            if t == '':
                continue

            if 'Pinging' in t:
                tem = t.split('Pinging ', 1)[1]
                temp = tem.split(' with', 1)[0]
                statistics.append(temp)

            if 'Reply' in t:
                tem = t.split('time', 1)[1][1:]
                temp = tem.split('ms', 1)[0]
                pingData.append(int(temp))

            if t == 'Request timed out.':
                continue

            if 'Packets: Sent =' in t:
                statistics.append(t[13:-2])
                break

    # print(ping) # For debug of data
    # print(statistics) # For debug of statistics

    return [pingData, statistics]


# Converting CM into inches for drawing purposes
def cm_to_inch(value):
    return value / 2.54


# Drawing Big ping graph
def drawBigGraph(xAxisData, yAxisData, infoAboutServer, lowPingValues, bigGraph):
    # Creating graph size and populating with data
    plt.figure(figsize=(cm_to_inch(50), cm_to_inch(25)))
    plt.plot(xAxisData, yAxisData, color='c', linewidth=1)

    # Drawing max X axis i Y axis + 25px and adding stats info
    if max(yAxisData) > 2000:
        plt.axis([0, len(yAxisData), 0, max(yAxisData) + 200])
    else:
        plt.axis([0, len(yAxisData), 0, max(yAxisData) + 25])

    # Getting all data from list for creating text info
    serverInfo = infoAboutServer[0]
    lowPingValuesList = infoAboutServer[1].split(',')
    percentage1 = percentage(lowPingValues[0], len(yAxisData))
    percentage2 = percentage(lowPingValues[1], len(yAxisData))
    percentage3 = percentage(lowPingValues[2], len(yAxisData))

    # Formatted text for low ping values
    formatted_lowPingValues = "Server:\n" + serverInfo + "\nPacket lowPingValues:\n" \
                              + lowPingValuesList[0] + "\n" \
                              + lowPingValuesList[1][1:] + "\n" \
                              + lowPingValuesList[2][1:] + "\n" \
                              + "Under 2ms: " + str(lowPingValues[0]) + ",  -- " + str(round(percentage1, 2)) + "%\n" \
                              + "In between: " + str(lowPingValues[2]) + ",  -- " + str(round(percentage3, 2)) + "%\n" \
                              + "Over 10ms: " + str(lowPingValues[1]) + ",  -- " + str(round(percentage2, 2)) + "%"

    # Adding server info text to the side of graph
    plt.text(-len(xAxisData) * 0.14, 5, formatted_lowPingValues)

    # Adding labels on x i y axis
    plt.ylabel("Time - ms", rotation=0, labelpad=40)
    plt.xlabel("packet number")

    # Drawing lines on Y axis
    if max(yAxisData) > 2000:
        plt.yticks(np.arange(0, max(yAxisData) + 200, 200))
    elif 2000 > max(yAxisData) > 200:
        plt.yticks(np.arange(0, max(yAxisData) + 1, 20))
    else:
        plt.yticks(np.arange(0, max(yAxisData) + 40, 10))

    # Drawing black lines on every 20ms till max 2000ms
    if max(yAxisData) > 2000:
        for x in range(0, 4000, 200):
            if x != 200:
                plt.hlines(x, 0, len(yAxisData), colors='k', linestyles='solid', linewidth=0.05)
    elif 2000 > max(yAxisData) > 200:
        for x in range(0, 2000, 20):
            if x != 200:
                plt.hlines(x, 0, len(yAxisData), colors='k', linestyles='solid', linewidth=0.05)
    else:
        for x in range(0, 200, 10):
            if x != 50 and x != 150:
                plt.hlines(x, 0, len(yAxisData), colors='k', linestyles='solid', linewidth=0.05)

    # Drawing lines in different color for important values
    plt.hlines(2, 0, len(yAxisData), colors='m', linestyles='solid', linewidth=0.5)
    plt.hlines(10, 0, len(yAxisData), colors='g', linestyles='solid', linewidth=0.5)
    plt.hlines(50, 0, len(yAxisData), colors='b', linestyles='dashed', linewidth=1)
    plt.hlines(150, 0, len(yAxisData), colors='r', linestyles='dashed', linewidth=1)
    plt.hlines(200, 0, len(yAxisData), colors='r', linestyles='dashed', linewidth=1)

    # Saving graph in PDF file
    plt.savefig(bigGraph)

    print("Big graph is saved in: " + bigGraph)
    # plt.show() # for debug purpose
    # Opening saved graph file in default pdf viewer
    subprocess.Popen([bigGraph], shell=True)


# Drawing small graph with low ping values
# so it can be more zoomed in for LAN diagnostics
def drawSmallGraph(xAxisData, yAxisData, infoAboutServer, lowPingValues, smallGraph):
    # Creating graph size and populating with data
    plt.figure(figsize=(cm_to_inch(50), cm_to_inch(25)))
    plt.plot(xAxisData, yAxisData, color="c", linewidth=1)

    # Drawing max X axis i Y axis + 25px and adding stats info
    plt.axis([0, len(yAxisData), 0, 60])
    lowPingValuesList = infoAboutServer[1].split(',')

    # Getting all data from list for creating text info
    serverInfo = infoAboutServer[0]
    percentage1 = percentage(lowPingValues[0], len(yAxisData))
    percentage2 = percentage(lowPingValues[1], len(yAxisData))
    percentage3 = percentage(lowPingValues[2], len(yAxisData))

    # Formatted text for low ping values
    formatted_lowPingValues = "Server:\n" + serverInfo + "\nPacket lowPingValues:\n" \
                              + lowPingValuesList[0] + "\n" \
                              + lowPingValuesList[1][1:] + "\n" \
                              + lowPingValuesList[2][1:] + "\n" \
                              + "Under 2ms: " + str(lowPingValues[0]) + ",  -- " + str(round(percentage1, 2)) + "%\n" \
                              + "In between: " + str(lowPingValues[2]) + ",  -- " + str(round(percentage3, 2)) + "%\n" \
                              + "Over 10ms: " + str(lowPingValues[1]) + ",  -- " + str(round(percentage2, 2)) + "%"

    # Adding server info text to the side of graph
    plt.text(-len(xAxisData) * 0.14, 5, formatted_lowPingValues)
    plt.text(-len(xAxisData) * 0.05, 1.6, '2')

    # Adding labels on X i Y axis
    plt.ylabel("Time - ms", rotation=0, labelpad=40)
    plt.xlabel("packet number")

    # Drawing lines on Y axis
    plt.yticks(np.arange(0, 60 + 1, 10))

    # Drawing black lines on every 10ms till max 60ms
    for x in range(0, 100, 10):
        if x != 10 and x != 50:
            plt.hlines(x, 0, len(yAxisData), colors='k', linestyles='solid', linewidth=0.1)

    # Drawing lines in different color for important values
    plt.hlines(2, 0, len(yAxisData), colors='m', linestyles='solid', linewidth=1)
    plt.hlines(10, 0, len(yAxisData), colors='g', linestyles='solid', linewidth=1)
    plt.hlines(50, 0, len(yAxisData), colors='b', linestyles='solid', linewidth=1)

    # Saving graph in PDF file
    plt.savefig(smallGraph)

    print("Small graph is saved in: " + smallGraph)
    # plt.show() # for debug purpose
    # Opening saved graph file in default pdf viewer
    subprocess.Popen([smallGraph], shell=True)


if __name__ == "__main__":
    main()
