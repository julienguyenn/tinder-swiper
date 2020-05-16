import subprocess


def process_pics(in_file="", in_dir="") -> None:
    args = ['OpenFace_2.2.0_win_x64\FaceLandmarkImg.exe', '-2Dfp']

    if in_file and not in_dir:
        args += ['-f', in_file]
    elif not in_file and in_dir:
        args += ['-fdir', in_dir]

    subprocess.run(args)
