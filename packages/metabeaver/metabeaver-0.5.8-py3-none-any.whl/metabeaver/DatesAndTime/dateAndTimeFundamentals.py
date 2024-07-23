import datetime as dt


# Creates a string for day and time, e.g. may 6th at 10:22:35 would be in the format of 06052023_223045
def getStrDateTime():

    # Get a datetime object containing current date and time
    now = dt.now()

    # Reformat the datetime to a string in the format like dd/mm/YY H:M:S
    dt_string = now.strftime("%d%m%Y_%H%M%S")

    return dt_string