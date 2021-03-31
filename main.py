# Input should be formatted as a Data.txt in the root folder, format is month/date
# Initial thing will just run the whole thing, later version will take user input.
# We're assuming an average month of 29.5 days.
# Error grows with the time spans considered because the calendar is not regular
# For whatever reason, Shaughnessy formated his dates in the opposite order of what seemed common sense to me
# so if you compare his data to mine, you'll see a different order.  Also my refinement algorithm is running backwards

# this is our basic date, to be read from a file.
class shang_date:
    ganzhi: int
    month: int

    def __init__(self, ganzhi, month):
        self.ganzhi = ganzhi
        self.month = month


def getmonth(day):
    return day.month


# because python dates is going to be a list of date objects

# interval is the possible days a month could begin and end on
class interval:
    month: int
    earliest: float
    latest: float
    duration: float

# potentially change the initialization since we're not using this this way anymore
    def __init__(self, month):
        self.earliest = -100
        self.latest = -100
        self.month = month
        self.duration = 31

    def update(self, first, last):
        self.earliest = first
        self.latest = last

        # this may need a compensation thing if 0 is set to 60 etc.
    def calc_duration(self):
        self.duration = (self.latest - self.earliest) % 60

    def getmonth(self):
        return interval.month

    def convert_month_1(self):
        self.earliest = (self.earliest - (29.5 * (self.month - 1))) % 60
        #    if new.first == 0:
        #        new.first = 60
        # subtract the days required to find distance to the first month and then mod 60.
        self.latest = (self.latest - (29.5 * (self.month - 1))) % 60
        self.month = 1

    # since we need to do comparisons and there are no "safe dummies", I'm using this as a way of getting around things
    def repair_first(self, first_unit):
        if self.earliest == -100:
            self.earliest = first_unit.earliest
            self.latest = first_unit.latest


# this function finds the possible beginning and ending days of the month based on the given ganzhi date
def find_beginning(d):
    r = interval(d.month)
    r.month = d.month
    r.latest = d.ganzhi
    # ^ here we assume the ganzhi is the last of of the month
    r.earliest = (d.ganzhi - 28.5) % 60
    # ^ here we assume the date is the last one in the month so we subtract average month length, then mod 60 for ganzhi
    return r


def mod_distance(first, last):
    return (last-first) % 60


# this function narrows the beginning and ending bounds based on the ranges calculated for each day given
def refine_ranges(month, intervals_list):
    # it's not the most elegant way to do it, but python is still kind of counter-intuitive for the C in me.
    shortest = interval(month)
    for intervals in intervals_list:
        if intervals.month == month:
            shortest.repair_first(intervals)
            carry_first = shortest.earliest
            carry_last = shortest.latest
            # check overlap, if they overlap, then update, else return these dates are incompatible
            if mod_distance(intervals.earliest, shortest.latest) < shortest.duration:
                carry_first = intervals.earliest
            if mod_distance(shortest.earliest, intervals.latest) < shortest.duration:
                carry_last = intervals.latest
            shortest.earliest = carry_first
            shortest.latest = carry_last
            shortest.calc_duration()
    #        if not validate(new):
    #            print("error, month:", month, "cannot be co-annual;", new.first, new.last)

        # eventually I'll turn this into a proper error/exception handling
    return shortest


def refine_range_compare(best, comparator):
    if best.month is not comparator.month:
        print("Error in comparison, months are unequal", comparator.month)
        return
    carry_first = best.earliest
    carry_last = best.latest
    # check overlap, if they overlap, then update, else return these dates are incompatible and ignore the new date
    # improve usability by telling us which dates to eject...
    if dates_overlap(best, comparator):
        if mod_distance(comparator.earliest, best.latest) < best.duration:
            carry_first = comparator.earliest
        if mod_distance(best.earliest, comparator.latest) < best.duration:
            carry_last = comparator.latest
    best.earliest = carry_first
    best.latest = carry_last
    best.calc_duration()
    return best


# this function checks to see that the intervals overlap, pretty sure I only need to check the closed interval.
def dates_overlap(interval_a, interval_b):
    if ((interval_b.earliest - interval_a.earliest) % 60 <= (interval_a.latest - interval_a.earliest) % 60) or ((interval_a.earliest - interval_b.earliest) % 60 <= (interval_b.latest - interval_b.earliest) % 60):
        return True
    else:
        print("Error: intervals do not overlap month", interval_a.month, interval_a.earliest, "to", interval_a.latest, "conflicts with new interval month", interval_b.earliest, "to", interval_b.latest)


# dates will be in month/ganzhi
def get_dates():
    dates = []
    n = 0
    file = open(r"Dates.txt", "r")
    while True:
        line = file.readline()
        if not line:
            break
        # since the format is M/G, I'm having it throw out the /.
        nums = line.split("/")
        day = shang_date(int(nums[1]), int(nums[0]))
        dates.append(day)
        n += 1
    file.close()
    return dates


def output_month_bounds(r):
    print("Month", r.month, "could have begun between", r.earliest, "and", r.latest)


# greedy recursive one, should work?
def compare_all(n, intervals):
    if intervals[n+1]:
        interval[n] = refine_range_compare(intervals[n], intervals[n+1])
        interval[n] = compare_all(n+1, intervals)
    return interval[n]


def count_months(ranges):
    months_in_data = []
    for interval_n in ranges:
        if interval_n.month not in months_in_data:
            months_in_data.append(interval_n.month)
    return months_in_data


# pick out all data from a given month and refine it.
def compile_ranges_for_month(month, ranges):
    # make a dummy for comparison
    best = interval(month)
    # now go through set passed in
    for unit in ranges:
        if unit.month == month:
            # apply the patch for the problem of the first data point
            print("Adding range:", unit.earliest, "to", unit.latest)
            best.repair_first(unit)
            best = refine_range_compare(best, unit)
    return best


# output the dates in order
def write_dates(dates):
    file = open(r"Dates.txt", "w")
    for date in dates:
        line = str(date.month) + "/" + str(date.ganzhi) + "\n"
        file.write(line)
    file.close()
    return


def main():
    # first we import the data
    dates = get_dates()
    print(len(dates), "dates imported.")
    dates.sort(key=getmonth)

    # Find the day ranges
    ranges = []
    for day in dates:
        write_dates(dates)
        ranges.append(find_beginning(day))
    months = count_months(ranges)
    month_ranges = []

    # make a dummy range for comparisons
    month_one_range = find_beginning(dates[0])

    # give us the month bounds
    iterator = 0
    for month in months:
        print("Compiling month", month, ":")
        month_ranges.append(compile_ranges_for_month(month, ranges))
        output_month_bounds(month_ranges[iterator])
        iterator += 1
    # now go through the months

    month_one_range.convert_month_1()
    for month_range in month_ranges:
        print("The corresponding month 1 to month", month_range.month)
        month_range.convert_month_1()
        output_month_bounds(month_range)
        month_one_range = refine_range_compare(month_one_range, month_range)

    print("Thus, if they're in the same year:")
    output_month_bounds(month_one_range)


if __name__ == "__main__":
    main()
