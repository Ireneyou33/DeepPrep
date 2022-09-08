import os
import time
import argparse


def run_cmd_with_timing(cmd):
    print('*' * 50)
    print(cmd)
    print('*' * 50)
    start = time.time()
    os.system(cmd)
    print('=' * 50)
    print(cmd)
    print('=' * 50, 'runtime:', ' ' * 3, time.time() - start)


def set_envrion(threads: int = 1):
    # FreeSurfer recon-all env
    os.environ['FREESURFER_HOME'] = '/usr/local/freesurfer'
    os.environ['FREESURFER'] = '/usr/local/freesurfer'
    os.environ['SUBJECTS_DIR'] = '/usr/local/freesurfer/subjects'
    os.environ['PATH'] = '/usr/local/freesurfer/bin:/usr/local/freesurfer/mni/bin:/usr/local/freesurfer/tktools:' + \
                         '/usr/local/freesurfer/fsfast/bin:' + os.environ['PATH']
    os.environ['MINC_BIN_DIR'] = '/usr/local/freesurfer/mni/bin'
    os.environ['MINC_LIB_DIR'] = '/usr/local/freesurfer/mni/lib'
    os.environ['PERL5LIB'] = '/usr/local/freesurfer/mni/share/perl5'
    os.environ['MNI_PERL5LIB'] = '/usr/local/freesurfer/mni/share/perl5'
    # FreeSurfer fsfast env
    os.environ['FSF_OUTPUT_FORMAT'] = 'nii.gz'
    os.environ['FSLOUTPUTTYPE'] = 'NIFTI_GZ'

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bd', required=True, help='directory of bids type')
    parser.add_argument('--fsd', default=os.environ.get('FREESURFER_HOME'),
                        help='Output directory $FREESURFER_HOME (pass via environment or here)')
    parser.add_argument('--respective', default='off',
                        help='if on, while processing T1w file respectively')
    parser.add_argument('--rewrite', default='on',
                        help='set off, while not preprocess if subject recon path exist')
    parser.add_argument('--python', default='python3',
                        help='which python version to use')

    args = parser.parse_args()
    args_dict = vars(args)

    if args.fsd is None:
        args_dict['fsd'] = '/usr/local/freesurfer'
    args_dict['respective'] = True if args.respective == 'on' else False
    args_dict['rewrite'] = True if args.rewrite == 'on' else False

    return argparse.Namespace(**args_dict)