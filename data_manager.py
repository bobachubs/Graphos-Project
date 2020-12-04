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
        print(fieldString, idx, key)
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
            bucketKey = f'{bucket[0]}-{bucket[1]}' if bucketRange > 1 else str(bucket[0])
            count = bucket[2]
            histogramBuckets.append((bucketKey, count))

        self.cache[key] = histogramBuckets
        return histogramBuckets

    # returns a tuple ([(x, y), ...], xMin, xMax, yMin, yMax]
    def getScatterData(self, xfieldString, yfieldString):
        # assumes both x, y are numeric
        key = f'{xfieldString}-{yfieldString}-scatterplot'
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

    # returns a list of cumulative aggregates as they appeared in time
    # [(time, {'x', yAggregate}, ...]
    def getAggregatesTimeline(self, xfieldString, yfieldString):
        # assumes data is already sorted by time
        key = f'{xfieldString}-{yfieldString}-timeline'
        if key in self.cache:
            return self.cache[key]

        tIdx = next(i for i,v in enumerate(self.fields) if v.name == "TIME")
        xIdx = next(i for i,v in enumerate(self.fields) if v.name == xfieldString)
        yIdx = next(i for i,v in enumerate(self.fields) if v.name == yfieldString)

        timeline = []
        tAggregates = {}
        currentTime = None
        for row in self.data:
            t = row[tIdx]
            x = row[xIdx]
            try:
                y = 0 if not row[yIdx] else float(row[yIdx])
            except:
                continue

            if t != currentTime and currentTime is not None:
                timeline.append((currentTime, tAggregates.copy()))

            if x not in tAggregates:
                tAggregates[x] = 0
            tAggregates[x] += y
            currentTime = t

        # add last time
        if tAggregates:
            timeline.append((currentTime, tAggregates))

        self.cache[key] = timeline
        return timeline

    @staticmethod
    def load(filepath):
        # todo - csv module is slow, explore pandas and alternatives after MVP
        with open(filepath) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            fields = next(reader)
            rows = list(reader)

        # preprocess data to get graphable fields
        dataFields = []

        rowSample = rows[:min(20, len(rows))]
        for idx, field in enumerate(fields):
            floatCounter = 0
            for row in rowSample:
                fieldValue = row[idx]
                try:
                    _ = float(fieldValue)
                    floatCounter += 1
                except:
                    pass
            isNumeric = floatCounter > (len(rowSample) / 2)
            dataFields.append(DataField(field, isNumeric))

        return DataSet(dataFields, rows)
