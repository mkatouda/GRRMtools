import sys
import os
import argparse
import csv


def get_parser():
    parser = argparse.ArgumentParser(
        description="Convert GRRM list files to xyz and csv files.",
        usage=f"python {os.path.basename(__file__)} LOGBASENAME --prefix PREFIX"
    )
    parser.add_argument(
        "logbasename",
        help="basename of GRRM list log file: LOGBASENAME_EQ_list.log for example",
        type=str
    )
    parser.add_argument(
        "--prefix",
        help="Prefix of Geometry ID",
        type=str
    )
    return parser.parse_args()


def get_natoms(lines):
    natoms = 0
    count_atoms = False
    for line in lines:
        if 'Geometry' in line:
            count_atoms = True
        elif 'Energy' in line:
            count_atoms = False
            break
        elif count_atoms:
            natoms += 1
    return natoms


def get_nstrucs(lines):
    nstrucs = 0
    for line in lines:
        if 'Geometry' in line:
            nstrucs += 1 
    return nstrucs


def get_summary(lines, gidprefix=None):
    find_nmode = False
    summary = [['GeomID', 'Symmetry', 'Energy1', 'Energy2', 'Spin', 'ZPVE', 'Nmode1', 'Nmode2']]
    for line in lines:
        if 'Geometry' in line:
            l = line.split()
            gid = l[3] + l[4].strip(',')
            if isinstance(gidprefix, str):
                gid = gidprefix + '-' + gid
            sym = l[7]
        elif 'Energy' in line:
            l = line.strip('(').strip(')').split()
            eng1 = l[3]
            eng2 = l[5]
        elif 'Spin' in line:
            l = line.split()
            spin = l[2]
        elif 'ZPVE' in line:
            l = line.split()
            zpve = l[2]
        elif 'Normal' in line:
            find_nmode = True
            l = line.split()
            nmode = int(l[6])
        elif find_nmode:
            nmode = line.split()          
            summary.append([gid, sym, eng1, eng2, spin, zpve, nmode[0], nmode[1]])
            find_nmode = False

    return summary


def merge_list_files(infiles):
    outlines = ''
    for infile in infiles:
        with open(infile) as f:
            print('Read ', infile)
            lines = f.read()
            if 'PT' in infile:
                lines = lines.replace('TS', 'PT').replace('Approximate PT', 'Approximate TS')
            outlines += lines
    return outlines


def get_xyzcoord(inlines, natoms, summary):

    get_coord = False
    ist = 0
    outlines = ''
    for line in inlines:
        if 'Geometry' in line:
            summary[ist]
            header = '{}={},{}={},{}={},{}={},{}={},{}={},{}={}'.format(
                summary[0][0],
                summary[ist+1][0],
                summary[0][1],
                summary[ist+1][1],
                summary[0][2],
                summary[ist+1][2],
                summary[0][3],
                summary[ist+1][3],
                summary[0][5],
                summary[ist+1][5],
                summary[0][6],
                summary[ist+1][6],
                summary[0][7],
                summary[ist+1][7]
            )
            outlines += '{}\n{}\n'.format(natoms, header)
            get_coord = True
            ist += 1
        elif 'Energy' in line:
            get_coord = False
        elif get_coord:
            outlines += line

    return outlines


def main():

    args = get_parser()
    print('Input arguments: ', args)
    inbasename = args.logbasename
    gid_prefix = args.prefix

    inlogfile_type = ['EQ', 'DC', 'TS', 'PT']
    inlogfiles = ['{}_{}_list.log'.format(inbasename, ftype) for ftype in inlogfile_type]

    outlogfile = inbasename + '_list.log'
    outxyzfile = inbasename + '_list.xyz'
    outcsvfile = inbasename + '_list.csv'

    outlines = merge_list_files(inlogfiles)
    print('Write ', outlogfile)
    with open(outlogfile, 'w') as f:
        f.write(outlines)

    with open(outlogfile) as f:
        inlines = f.readlines()

    if len(inlines) > 0:
        natoms = get_natoms(inlines)
        nstrucs = get_nstrucs(inlines)
        print('natoms: ', natoms, 'nstrucs: ', nstrucs)
        summary = get_summary(inlines, gid_prefix)

        print('Write ', outcsvfile)
        with open(outcsvfile, 'w') as f:
            writer = csv.writer(f)
            writer.writerows(summary)

        outlines = get_xyzcoord(inlines, natoms, summary)

        print('Write ', outxyzfile)
        with open(outxyzfile, 'w') as f:
            f.write(outlines)


if __name__ == '__main__':
    main()
