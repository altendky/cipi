import os
import os.path
import shutil
import subprocess
import sys
import tempfile
import zipfile


def check_call(command, *args, **kwargs):
    command = list(command)
    print('Launching: ')
    for arg in command:
        print('    {}'.format(arg))

    return subprocess.check_call(command, *args, **kwargs)


def build(artifact, script, root):
    temporary_path = tempfile.mkdtemp()

    try:
        build_path = os.path.join(temporary_path, 'build')
        os.mkdir(build_path)

        destination_path = os.path.join(temporary_path, 'destination')
        os.mkdir(destination_path)

        to_install = (
            ('--requirement', os.path.join(root, 'requirements.txt')),
        )
        for target in to_install:
            check_call(
                (
                    sys.executable,
                    '-m', 'pip',
                    'download',
                    '--no-deps',
                    '--dest', destination_path,
                ) + target,
                cwd=build_path,
            )

        check_call(
            (
                sys.executable,
                os.path.join(root, 'setup.py'),
                'sdist',
                '--dist-dir', destination_path,
            ),
            cwd=root,
        )

        to_install = [
            os.path.join(destination_path, name)
            for name in os.listdir(destination_path)
        ]
        check_call(
            (
                sys.executable,
                '-m', 'pip',
                'install',
                '--target', build_path,
            ) + tuple(p for p in to_install),
            cwd=build_path,
        )

        shutil.copyfile(
            script,
            os.path.join(build_path, '__main__.py'),
        )

        with zipfile.ZipFile(file=str(artifact), mode='w') as zip:
            for root, directories, files in os.walk(str(build_path)):
                for name in files:
                    path = os.path.join(root, name)
                    archive_name = os.path.relpath(
                        path=path,
                        start=build_path,
                    )
                    zip.write(filename=path, arcname=archive_name)
    finally:
        shutil.rmtree(build_path)


def main():
    this = os.path.abspath(__file__)
    here = os.path.dirname(this)

    default_artifact_name = 'cipi.pyz'
    default_artifact_path = os.path.join(os.getcwd(), default_artifact_name)

    build(
        artifact=default_artifact_path,
        script=os.path.join(here, 'src', 'cipi', '__main__.py'),
        root=here,
    )


if __name__ == '__main__':
    sys.exit(main())
