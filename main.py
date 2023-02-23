import os

suffix = ".fio"
n2mSec = ["nsec", 1000000]
u2mSec = ["usec", 1000]
kb2mb = ["kB/s", 1024]
fioFilePath = "C:\\Users\\PanKai\\Desktop\\testlog\\data_pool_out_of_cache"
csvDirName = "csv"


# get fio log file paths in directory
def getFioLogPathList(path):
    fileNameList = os.listdir(path)
    fioLogPathList = []
    for fileName in fileNameList:
        if suffix in fileName:
            fioLogPathList.append(path + "\\" + fileName)
    return fioLogPathList


# read file contents by file path
def readLines(fioLogPath):
    fioLogFile = open(fioLogPath, encoding='utf-8')
    lines = fioLogFile.readlines()
    fioLogFile.close()
    return lines


def getAvgLat(line):
    lat = line.split(",")[2].split("=")[1]
    if n2mSec[0] in line:
        return round(float(lat) / n2mSec[1], 2)
    if u2mSec[0] in line:
        return round(float(lat) / u2mSec[1], 2)
    return round(float(lat), 2)


def getBW(line):
    BW = line.split(",")[0].split("(")[1]
    if kb2mb[0] in BW:
        return round(float(BW.split(kb2mb[0])[0]) / kb2mb[1], 2)

    if "MB" in BW:
        return BW.split("MB")[0]


def getCsvLine(resList, fioLines):
    for line in fioLines:
        if "read: IOPS=" in line:
            readIOPS = line.split(",")[0].split("=")[1]
            if "k" in readIOPS:
                readIOPS = float(readIOPS[:-1]) * 1000
            resList[0] = readIOPS

        if "clat (" in line:
            resList[1] = getAvgLat(line)

        if "READ: bw=" in line:
            resList[2] = getBW(line)

    for line in fioLines:
        if "write: IOPS=" in line:
            writeIOPS = line.split(",")[0].split("=")[1]
            if "k" in writeIOPS:
                writeIOPS = float(writeIOPS[:-1]) * 1000
            resList[3] = writeIOPS

        if "clat (" in line:
            resList[4] = getAvgLat(line)

        if "WRITE: bw=" in line:
            resList[5] = getBW(line)

    if int(resList[0]) == 0 and int(resList[2]) == 0:
        resList[1] = 0
    if int(resList[3]) == 0 and int(resList[5]) == 0:
        resList[4] = 0
    csvLine = ""
    for item in resList:
        csvLine = csvLine + str(item) + ","
    return csvLine[:-1]


def writeToCSV(path, sourceFilePath):
    csvName = sourceFilePath[sourceFilePath.rfind("\\") + 1:].split(".")[0] + ".csv"
    csvFilePath = path + "\\" + csvName
    csvFile = open(csvFilePath, "w")
    emptyResList = [0, 0, 0, 0, 0, 0]
    csvFile.write(getCsvLine(emptyResList, readLines(sourceFilePath)))
    csvFile.close()


if __name__ == '__main__':
    csvPath = fioFilePath + "\\" + csvDirName
    if not os.path.exists(csvPath):
        os.makedirs(csvPath)
    for logPath in getFioLogPathList(fioFilePath):
        writeToCSV(csvPath, logPath)
