###################################################
##########[ Script: Drop Extra Delim Rows ]########
###################################################
"""
Sometimes CSVs pulled from SQL Server or SAP contain rows which contain an extra delimiter for some reason,
perhaps because it made its way into one of the fields.

Probably the *real* way to solve this is to use quoting.

This script simply drops those rows and writes them to a new file at `badpath`.

The original file is left unaltered and a clean version is written to `outpath`. 
"""
import os
import sys
import click


################[ main ]################

@click.command()
@click.argument("readpath", click.Path(exists=True), required=True)
@click.option('-d', '--delimiter', 'delimiter', default='|', help="Delimiter character.")
@click.option('-n', '--n-delim', 'n_delim', default='infer', help="Number of delimiters per row.")
@click.option('-o', '--outpath', 'outpath', type=click.Path(exists=False), help="Path to write filtered output.")
@click.option('-b', '--badpath', 'badpath', type=click.Path(exists=False), help="Path to write rejected rows.")
def main(readpath, delimiter, n_delim=None, outpath=None, badpath=None):
    """
    Lazily stream in file, drop lines that are too wide, write clean file, and save the offending lines to a new file.
    
    Default to the number of delimiters in the header column.

    Specify READPATH, path to a CSV.
    """
    def append_filename_suffix(path, suffix):
        """Insert a suffix between the file extension."""
        name, ext = os.path.splitext(path)
        return name + suffix + ext
    
    if outpath is None:
        outpath = append_filename_suffix(readpath, "_uniform_width")
        
    if badpath is None:
        badpath = append_filename_suffix(readpath, "_toowide_lines")
        
    with open(readpath, "r") as readfile:               # file to stream in
        with open(outpath, "w") as writefile:           # file to write clean data
            with open(badpath, "w") as badfile:         # file to write offending rows

                offset   = 0
                badlines = 0
                
                if n_delim == 'infer':
                    
                    header  = readfile.readline()  # infer number of delimiters from header
                    n_delim = header.count(delimiter)  

                    writefile.write(header)        # write header row
                    offset = 1
                else:
                    n_delim = int(n_delim)
                    
                print(' '.join(("==========[ Dropping lines with >", str(n_delim), "columns... ]==========")))
                print()
                
                for i, line in enumerate(readfile):
                    
                    try:
                        delimiter_count = line.count(delimiter)
                    except UnicodeDecodeError:
                        line = asciify(line)
                        delimiter_count = line.count(delimiter)

                    if delimiter_count > n_delim:                                                         # if too wide:
                        print(' '.join(("--> Dropping line", str(i + offset), ",", str(line.count(delimiter)), "delimiters.")))  # log
                        print(line)
                        print()
                        badlines += 1
                        
                        badfile.write(line)                                                       # write to badfile
                        continue                                                                  # skip this one

                    writefile.write(line)  # lines that pass the test get written.

                print(' '.join("==========[ Done. Dropped", str(badlines), "lines. ]=========="))
                print()
                print(' '.join("Wrote clean set to", outpath))
                print()


################[ utility to drop non-ascii characters ]################

bad_chars = str("").join([chr(i) for i in range(128, 256)])  # ascii dammit!
PY3 = sys.version_info[0] == 3
if PY3:
    translation_table = dict((ord(c), None) for c in bad_chars)

def asciionly(s):
    if PY3:
        return s.translate(translation_table)
    else:
        return s.translate(None, bad_chars)

def asciify(s):
    if type(s) is str:
        return unicode(asciionly(s))
    elif type(s) is unicode:
        return asciionly(s.encode('ascii', 'ignore'))
    else:
        return asciify(unicode(s))


if __name__ == "__main__":
    main()
