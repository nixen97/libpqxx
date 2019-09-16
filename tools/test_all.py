#! /usr/bin/env python3

from subprocess import (
    CalledProcessError,
    check_call,
    )

CXX = (
    'g++-7',
    'g++-8',
    'g++-9',
    'clang++-6.0',
    'clang++-7',
    'clang++-9',
    )

OPT = ('-O0', '-O3')

LINK = {
    'static': ['--enable-static', '--disable-dynamic'],
    'dynamic': ['--disable-static', '--enable-dynamic'],
}

DEBUG = {
    'plain': [],
    'audit': ['--enable-audit'],
    'maintainer': ['--enable-maintainer-mode'],
    'full': ['--enable-audit', '--enable-maintainer-mode'],
}


def run(cmd, output):
    command_line = ' '.join(cmd)
    output.write("%s\n\n" % command_line)
    check_call(cmd, stdout=output, stderr=output)


def build(configure, output):
    try:
        run(configure, output)
        run(['make', '-j8', 'clean'], output)
        run(['make', '-j8'], output)
        run(['make', '-j8', 'check'], output)
    except CalledProcessError as err:
        print("FAIL: %s" % err)
        output.write("\n\nFAIL: %s\n" % err)
    else:
        print("OK")
        output.write("\n\nOK\n")


def main():
    for cxx in sorted(CXX):
        for opt in sorted(OPT):
            for link, link_opts in sorted(LINK.items()):
                for debug, debug_opts in sorted(DEBUG.items()):
                    log = 'build-%s.out' % '_'.join(
                        [cxx, opt, link, debug])
                    print("%s... " % log, end='', flush=True)
                    configure = [
                        './configure',
                        'CXX=%s' % cxx,
                        'CXXFLAGS=%s' % opt,
                        '--disable-documentation',
                        ] + link_opts + debug_opts
                    with open(log, 'w') as output:
                        build(configure, output)

if __name__ == '__main__':
    main()