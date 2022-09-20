from bold import BoldSkipReorient
from pathlib import Path
from nipype import Node
import os


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

    # FSL
    os.environ['PATH'] = '/usr/local/fsl/bin:' + os.environ['PATH']

    # set threads
    os.environ['OMP_NUM_THREADS'] = str(threads)
    os.environ['ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS'] = str(threads)


def BoldSkipReorient_test():
    task = 'motor'
    subject_id = 'sub-MSC01'
    data_path = Path(f'/mnt/ngshare/DeepPrep/MSC')
    preprocess_dir = data_path / 'derivatives' / 'deepprep' / subject_id / 'tmp' / f'task-{task}'
    runs = sorted([d.name for d in (preprocess_dir / subject_id / 'bold').iterdir() if d.is_dir()])

    for run in runs:
        BoldSkipReorient_node = Node(BoldSkipReorient(), name='BoldSkipReorient_node')
        BoldSkipReorient_node.inputs.subject_id = subject_id
        BoldSkipReorient_node.inputs.preprocess_dir = preprocess_dir
        BoldSkipReorient_node.inputs.bold = preprocess_dir / subject_id / 'bold' / run / f'{subject_id}_bld{run}_rest.nii.gz'

        BoldSkipReorient_node.inputs.skip_bold = preprocess_dir / subject_id / 'bold' / run / f'{subject_id}_bld{run}_rest_skip.nii.gz'
        BoldSkipReorient_node.inputs.reorient_skip_bold = preprocess_dir / subject_id / 'bold' / run / f'{subject_id}_bld{run}_rest_reorient_skip.nii.gz'
        BoldSkipReorient_node.run()


if __name__ == '__main__':
    set_envrion()