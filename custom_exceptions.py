
class InvalidMonthError(Exception):
    """Raised if the raw CMS file contains an unexpected month (i.e., not Jan., Apr., Jul., Oct. to represent quarterly
        Also raised if there is no month information found in the file at all despite being expected"""
    pass

class InvalidDateRange(Exception):
    """Raised if processing attempts to process a file for which processing code has not been developed"""
    pass