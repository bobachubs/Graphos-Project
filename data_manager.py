import csv
import math


class DataField:
    def __init__(self, name, isNumeric):
        self.name = name
        self.isNumeric = isNumeric

class DataSet:
    def __init__(self, fields, data):
        self.fields = fields
        self.data = data
        self.cache = {}

    # returns an list of tuples ('bucket', count)
    def getHistogram(self, fieldString):
        # assumes fieldString contains numeric values to be bucketable
        key = f'{fieldString}-Histogram'
        if key in self.cache:
            return self.cache[key]

        histogramCounts = {}
        idx = next(i for i,v in enumerate(self.fields) if v.name == fieldString)
        for row in self.data:
            try:
                value = 0 if not row[idx] else float(row[idx])
            except:
                continue

            if value not in histogramCounts:
                histogramCounts[value] = 0
            histogramCounts[value] += 1

        # target ~11 buckets
        minValue = math.floor(min(histogramCounts.keys()))
        maxValue = math.ceil(max(histogramCounts.keys()))

        if maxValue - minValue < 11:
            bucketRange = 1
            numericBuckets = [[v, v + 1, 0] for v in range(minValue, maxValue)]
        else:
            bucketRange = math.floor((maxValue -  minValue) / 11)
            numericBuckets = [[v, v + bucketRange, 0] for v in range(minValue, maxValue + bucketRange, bucketRange)]

        bucketIdx = 0
        for (value, count) in sorted(histogramCounts.items(), key=lambda p: p[0]):
            for idx in range(bucketIdx, len(numericBuckets)):
                bucket = numericBuckets[idx]
                bucketMin = bucket[0]
                bucketMax = bucket[1]
                if bucketMin <= value and value < bucketMax:
                    bucket[2] += count
                    bucketIdx = idx
                    break

        histogramBuckets = []
        for bucket in numericBuckets:
            bucketKey = f'{bucket[0]}->{bucket[1]}' if bucketRange > 1 else str(bucket[0])
            count = bucket[2]
            histogramBuckets.append((bucketKey, count))

        self.cache[key] = histogramBuckets
        return histogramBuckets

    # returns a tuple ([(x, y), ...], xMin, xMax, yMin, yMax]
    def getScatterData(self, xfieldString, yfieldString, xMinOpt=None, xMaxOpt=None, yMinOpt=None, yMaxOpt=None):
        # assumes both x, y are numeric
        key = f'{xfieldString}-{yfieldString}-{xMinOpt}-{xMaxOpt}-{yMinOpt}-{yMaxOpt}-scatterplot'
        if key in self.cache:
            return self.cache[key]

        xIdx = next(i for i,v in enumerate(self.fields) if v.name == xfieldString)
        yIdx = next(i for i,v in enumerate(self.fields) if v.name == yfieldString)

        points = set()
        xMin = float('inf')
        xMax = float('-inf')
        yMin = float('inf')
        yMax = float('-inf')
        for row in self.data:
            try:
                x = 0 if not row[xIdx] else float(row[xIdx])
                y = 0 if not row[yIdx] else float(row[yIdx])
            except:
                continue

            if xMinOpt != None and x < xMinOpt:
                continue
            if xMaxOpt != None and x > xMaxOpt:
                continue
            if yMinOpt != None and y < yMinOpt:
                continue
            if yMaxOpt != None and y > yMaxOpt:
                continue

            points.add((x, y))
            xMin = min(xMin, x)
            xMax = max(xMax, x)
            yMin = min(yMin, y)
            yMax = max(yMax, y)

        scatterData = (list(points), xMin, xMax, yMin, yMax)
        self.cache[key] = scatterData
        return scatterData

    # returns a dictionary aggregating y grouped by x
    def getAggregates(self, xfieldString, yfieldString):
        # assumes y is numeric
        key = f'{xfieldString}-{yfieldString}-aggregates'
        if key in self.cache:
            return self.cache[key]

        xIdx = next(i for i,v in enumerate(self.fields) if v.name == xfieldString)
        yIdx = next(i for i,v in enumerate(self.fields) if v.name == yfieldString)

        aggregates = {}
        for row in self.data:
            x = row[xIdx]
            try:
                y = 0 if not row[yIdx] else float(row[yIdx])
            except:
                continue

            if x not in aggregates:
                aggregates[x] = 0
            aggregates[x] += y

        self.cache[key] = aggregates
        return aggregates

    # returns a list of cumulative aggregates as they appear in groups, sorted by group
    # [(group0, {'x', yAggregate}, ...]
    def getAggregatesGroups(self, xfieldString, yfieldString, groupFieldString):
        key = f'{xfieldString}-{yfieldString}-{groupFieldString}-groups'
        if key in self.cache:
            return self.cache[key]

        gIdx = next(i for i,v in enumerate(self.fields) if v.name == groupFieldString)
        xIdx = next(i for i,v in enumerate(self.fields) if v.name == xfieldString)
        yIdx = next(i for i,v in enumerate(self.fields) if v.name == yfieldString)

        groups = []
        gAggregates = {}
        currentGroup = None
        sortedData = sorted(self.data, key=lambda x: x[gIdx])
        for row in sortedData:
            g = row[gIdx]
            x = row[xIdx]
            try:
                y = 0 if not row[yIdx] else float(row[yIdx])
            except:
                continue

            if g != currentGroup and currentGroup is not None:
                groups.append((currentGroup, gAggregates.copy()))

            if x not in gAggregates:
                gAggregates[x] = 0
            gAggregates[x] += y
            currentGroup = g

        # add last group
        if gAggregates:
            groups.append((currentGroup, gAggregates))

        self.cache[key] = groups
        return groups

    @staticmethod
    def load(filepath):
        # todo - csv module is slow, explore pandas and alternatives after MVP
        with open(filepath) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            fields = next(reader)
            rows = list(reader)

        # preprocess data to get graphable fields
        dataFields = []

        rowSample = rows[:min(1000, len(rows))]
        for idx, field in enumerate(fields):
            floatCounter = 0
            totalCounter = 0
            for row in rowSample:
                fieldValue = row[idx]
                if not fieldValue:
                    continue
                totalCounter += 1
                try:
                    _ = float(fieldValue)
                    floatCounter += 1
                except:
                    pass
            isNumeric = floatCounter > (totalCounter / 2)
            dataFields.append(DataField(field, isNumeric))

        return DataSet(dataFields, rows)
