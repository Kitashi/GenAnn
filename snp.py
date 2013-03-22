import MySQLdb

# Owner: Matt
# Args:
#  snp: 'rsX' where X is a string of digits
#  sql_connection: resulting object from MySQLdb.connect()
#  table_name: table in which to query
# Returns:
#  array of [chromosome, starting position, ending position]
def snpToLocations(snp, sql_connection, table_name):
    cur = sql_connection.cursor()
    snp_where = 'name = "' + snp + '"'
    query = 'select chrom, chromStart, chromEnd from ' + table_name + ' where ' + snp_where + ';'
    cur.execute(query)
    return cur.fetchall()
    
# Owner: Matt
# Args:
#  snp_array: 'rsX' where X is a string of digits
#  sql_connection: resulting object from MySQLdb.connect()
#  table_name: table in which to query
#  array of [[chromosome, starting position, ending position], (...)]
def snpsToLocations(snp_array, sql_connection, table_name):
    cur = sql_connection.cursor()
    middle = '" OR name = "'
    snp_where = middle.join(snp_array)
    query = 'select chrom, chromStart, chromEnd from ' + table_name + ' where name = "' + snp_where + '";'
    cur.execute(query)
    return cur.fetchall()