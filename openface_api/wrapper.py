import subprocess


def process_pics(in_file="", in_dir="", verbose=False, csv_only=True) -> None:
    if csv_only:
        args = ['OpenFace_2.2.0_win_x64\FaceLandmarkImg.exe', '-2Dfp']
    else:
        args = ['OpenFace_2.2.0_win_x64\FaceLandmarkImg.exe']

    if in_file and not in_dir:
        args += ['-f', in_file]
    elif not in_file and in_dir:
        args += ['-fdir', in_dir]

    if verbose:
        subprocess.run(args)
    elif not verbose:
        subprocess.run(args, stdout=subprocess.DEVNULL)
