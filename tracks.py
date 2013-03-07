class Track:
    # Private members.  Technically these are public, but the '__' means they shouldn't be altered or referenced.
    __name = ''
    __col_want = ''
    
    __col_chr = ''
    __col_strand = ''
    __col_start = ''
    __col_end = ''
    
    # "constructor" method.
    # Args:
    #  name: name of table in database
    #  want: comma-separated list of column names we want to return
    #  chr: column name for chromosome number
    #  strand: column name for strand
    #  start: column name for feature start location
    #  end: column name for feature end location
    def __init__(self, name, want, chr, strand, start, end):
        self.__name = name
        self.__want = want
        self.__col_chr = chr
        self.__col_strand = strand
        self.__col_start = start
        self.__col_end = end
    
    # Args:
    #  chr: chromosome number (form: "chrX" where "X" is the chromosome number)
    #  strand: chromosome strand ("+" or "-")
    #  pos: position within chromosome (integer)
    # Returns: WHERE qualifier of a MySQL query for a specific chromosome location
    def __makeSinglePositionCheck(self, chr, strand, pos):
        chr_num = self.__col_chr + ' = "' + chr + '"'
        chr_strand = self.__col_strand + ' = "' + strand + '"'
        chr_start = pos + ' >= ' + self.__col_start
        chr_end = pos + ' <= ' + self.__col_end
        return '(' + chr_num + ' AND ' + chr_strand + ' AND '  + chr_start + ' AND ' + chr_end + ')'
    
    # Args:
    #  args: Array of argument sets.  For each x in args, 
    #          x[0] is chromosome number,
    #          x[1] is strand,
    #          x[2] is location
    # Returns: WHERE qualifier of a MySQL query requesting at least one of multiple locations
    def makePositionCheck(self, args):
        result = []
        for x in args:
            result.append(self.__makeSinglePositionCheck(x[0],x[1],x[2]))
        return ' OR '.join(result)

    # Args:
    #  chr: chromosome number (form: "chrX" where "X" is the chromosome number)
    #  strand: chromosome strand ("+" or "-")
    #  start: starting position within chromosome (integer)
    #  end: ending position within chromosome (integer)
    # Returns: WHERE qualifier of a MySQL query for a range of chromosome locations on a single strand
    def __makeSingleRangeCheck(self, chr, strand, start, end):
        # Pre-work for making the query
        chr_num = self.__col_chr + ' = "' + chr + '"'
        chr_strand = self.__col_strand + ' = "' + strand + '"'
        # Check for overlap in ranges
        inside_area = '(' + start + ' >= ' + self.__col_start + ' AND ' + start + ' <= ' + self.__col_end
        inside_area = inside_area + ') OR (' + self.__col_start + ' >= ' + start + ' AND ' + self.__col_start + ' <= ' + end + ')'
        return '((' + inside_area + ') AND ' + chr_strand + ' AND ' + chr_num + ')'

    # Args:
    #  args: Array of argument sets.  For each x in args, 
    #          x[0] is chromosome number,
    #          x[1] is strand,
    #          x[2] is start location
    #          x[3] is end location
    # Returns: WHERE qualifier of a MySQL query requesting at least one of multiple ranges
    def makeRangeCheck(self, args):
        result = []
        for x in args:
            result.append(self.__makeSingleRangeCheck(x[0],x[1],x[2],x[3]))
        return ' OR '.join(result)

    def findNearestRightPos(self, chr, strand, pos):
        return pos + ' <= ' + __col_start + ' ORDER BY ABS(' + __col_start + ' - ' + pos + ') ASC LIMIT 1'
        
    def findNearestLeftPos(self, chr, strand, pos):
        return pos + ' >= ' + __col_end + ' ORDER BY ABS(' + pos + ' - ' + __col_end + ') ASC LIMIT 1'

    # Args:
    #  args: Array of WHERE qualifiers
    # Returns: each array element concatenated into one string with " OR " between them
    def orWheres(self, args):
        return ' OR '.join(args)

    # Args:
    #  sql_check: WHERE qualifier
    # Returns: MySQL Query on this table with given WHERE qualifier
    def makeQuery(self, sql_check):
        return 'SELECT ' + self.__want + ' FROM ' + self.__name + ' WHERE ' + sql_check + ';'