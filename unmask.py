
def unmask(mask_filename, parameters,
        output_filename=None, strict=False):

    with open(mask_filename, 'r') as fid:
        content = fid.read()

    for kk in parameters.keys():
        content = content.replace(kk, str(parameters[kk]))

    if output_filename is None:
        outfname = None
    elif output_filename == 'auto':
        outfname = mask_filename+'.unmasked'
    else:
        outfname = output_filename

    if outfname is not None:
        with open(outfname, 'w') as fid:
            fid.write(content)

    if strict:
        if '%%' in content:
            raise ValueError(
              ('There is still a %% after unmasking!\n'
               '--> Incompatible with strict=True'))

    return content

def parse_parameter_file(fname):
    with open(fname, 'r') as fid:
        lines = fid.readlines()

    ddd = {}
    for ii, ll in enumerate(lines):
        if ':' not in ll:
            print('Warning! line %d is skipped! Its content is:'%(ii+1))
            print(ll)
            continue

        nn = ll.split(':')[0].replace(' ', '').replace('\n', '')
        vv = ll.split(':')[1].replace(' ', '').replace('\n', '')
        ddd[nn] = vv

    return ddd

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Unmasks a madx maskfile.')
    parser.add_argument('mask_filename', help='Name of the maskfile to be unmasked')
    parser.add_argument('parameters', nargs='+', help=('Parameters for unmasking (can be a filename,'
                    'or given inline as: %%PARAM1%%:value1, %%PARAM2:value2, ...'))
    parser.add_argument('--output_filename', help='Name of the output file', default='auto')
    parser.add_argument('--run', help='Execute in madx after unmasking', action='store_true')
    args = parser.parse_args()

    if ':' in args.parameters[0]:
        par_dict = {}
        for pp in args.parameters:
            kk = pp.split(':')[0].replace(' ', '')
            vv = pp.split(':')[1].replace(' ', '')
            par_dict[kk] = vv
    else:
        par_dict = parse_parameter_file(args.parameters[0])

    unmask(args.mask_filename, par_dict, output_filename=args.output_filename)

    if args.run:
        import os
        if args.output_filename == 'auto':
            outfname = args.mask_filename+'.unmasked'
        else:
            outfname = args.output_filename

        os.system('madx ' + outfname) 
