import subprocess
import os
import shutil
import argparse
import git
import atexit

required_repositories = {
    "libjpeg-turbo": [
        "https://github.com/libjpeg-turbo/libjpeg-turbo.git", 
        "",
        [
            "-DENABLE_SHARED=OFF",
            "-DWITH_TOOLS=OFF",
            "-DWITH_TESTS=OFF",
        ]
    ],
    "libpng": [
        "https://github.com/pnggroup/libpng.git", 
        "",
        [
            "-DPNG_SHARED=OFF",
            "-DPNG_TESTS=OFF",
            "-DPNG_TOOLS=OFF",

        ]
    ],
    "libuv": [
        "https://github.com/libuv/libuv.git", 
        "",
        False
    ],
    "mbedtls": [
        "https://github.com/Mbed-TLS/mbedtls.git", 
        "v3.6.4",
        [
            "-DENABLE_PROGRAMS=OFF",
            "-DENABLE_TESTING=OFF",

        ]
    ],
    "ogg-vorbis": [
        "https://github.com/yohanip/android-compile-vorbis.git", 
        "",
        []
    ],
    "openal-soft": [
        "https://github.com/kcat/openal-soft.git", 
        "",
        False
    ],
    "SDL": [
        "https://github.com/libsdl-org/SDL.git", 
        "release-2.32.8",
        [
            "-DSDL_SHARED=OFF",
            "-DSDL_TEST=OFF",
        ]
    ]
}

known_repos = []

for key in required_repositories.keys():
    known_repos.append(key)

parser = argparse.ArgumentParser()

platform_group = parser.add_argument_group(title="Target Platform")
platform_group.add_argument("--android", required=False, action='store_true', help='if building for android, this should be set')

sub_parser = parser.add_subparsers(dest="command")

parser_check = sub_parser.add_parser("check", help="check for requirements")

parser_build_wellknown = sub_parser.add_parser("build-known", help=f"build the known libraries {known_repos}")
parser_build_wellknown.add_argument('--no-clean', action='store_true', required=False, help="weather we clean before building")
parser_build_wellknown.add_argument("--specific", required=False, help="If wanted to build specific well known", choices=known_repos, default='')


parser_main_build = sub_parser.add_parser("main-build", help="building Hashlink and libraries")
parser_main_build.add_argument('--no-skip-building-wellknown', action='store_true', required=False, help='also build the library on wellknown root')
parser_main_build.add_argument('--no-wellknown-clean', action='store_true', required=False, help='clean the welknown lib before building')
parser_main_build.add_argument('--no-clean', action="store_true", required=False, help='clean first before building Hashlink')

# start the parser
args = parser.parse_args()


hl_path = '' # where hl is called from
build_prefix = 'build'
install_prefix = 'build/install'
building_on_os = ''
should_change_hl_path = False
well_known = ''
android_ndk = None
'''
if target is '' then we are building for the desktop we are in
1. check if hashlink already set in the path
2. check if well_known defined
3. check if required lib cloned
'''
def do_setup(target_platform=''):
    global android_ndk, hl_path, build_prefix, install_prefix, building_on_os, should_change_hl_path, well_known, required_repositories
    
    old_cwd = os.getcwd()

    print("Checking..")

    if target_platform != '':
        if target_platform == "android":
            try:
                android_ndk = os.environ["ANDROID_NDK"]
            except Exception as e:
                pass 
        else:
            raise 'known target platforms: [android]'
        
    try:
        hl_path = subprocess.getoutput("which hl")
        cwd = os.getcwd()

        if hl_path=='':
            print("Warning: hl is not on the PATH")

        if os.name == "nt":
            building_on_os = "window"
        else:
            building_on_os = "linux"

        if target_platform == '':
            target_platform = building_on_os

        install_prefix = f'{build_prefix}-{target_platform}/install';
        build_prefix = f'build-{target_platform}'

        print(f'Building {target_platform} on {building_on_os}')
        print(f'Build Dir: {build_prefix}')
        print(f'Build Install: {install_prefix}')

        pure_hl_path = os.path.splitext(hl_path)[0]

        our_expected_hl = os.path.join(cwd, install_prefix, 'bin', 'hl')

        if pure_hl_path != our_expected_hl:
            should_change_hl_path = True

        # outcome, hl found not in the current dir, hl found and in current dir
        well_known = os.environ['CXX_WELLKNOWN_ROOT']

        if well_known == '':
            print("ERROR: Define CXX_WELLKNOWN_ROOT in the environment which points to root of needed repositories")
            exit(1)      

        found = list(required_repositories.keys())

        for key, value in required_repositories.items():
            path = os.path.join(well_known, key)
            if not os.path.isdir(path):
                print(f"ERROR: {key} not found in {well_known}, clone it from {value[0]}")
                exit(1)

            try:
                repo = git.Repo(path)
            except:
                print(f'ERROR! {path} is not a repository')
                continue

            if repo.remotes.origin.url == value[0]:
                # cd into the repo
                os.chdir(path)
                print(f"checking..{os.getcwd()}")

                # check for version
                if value[1] == '':
                    # means any latest
                    
                    default_branch = repo.remotes.origin.refs["HEAD"].reference.name.split("/")[-1]
                    latest_commit = repo.refs[default_branch].commit
                    current_commit = repo.head.commit

                    if latest_commit != current_commit:
                        print(f"Need repository {key} at the latest commit")
                else:
                    rev_head = repo.git.rev_parse(repo.head.commit.hexsha, short=True)
                    try:
                        temp = subprocess.check_output(["git", "describe", "--tags"]).decode().strip().split("-")
                        if len(temp) > 3:
                            temp = [temp[0] + '-' + temp[1], temp[2], temp[3]]
                    except:
                        pass
                    if len(temp) > 0:
                        if temp[0] != value[1]:
                            print(f"Expecting {key} @{value[1]} but it is @{temp[0]}")
                            continue
                
                # all is well
                found.remove(key)
            else:
                print(f'expecting {key} is a git of {value[0]}')

        if len(found) > 0:
            print(f"ERROR: invalid repositor{'ies' if len(found)>0 else 'y'} -> {found}")
            exit(1)
    except SystemExit:
        pass
    finally:
        os.chdir(old_cwd)

def do_build_known(target_platform='', no_clean=False, specific='', skip_confirm=False):
    old_cwd = os.getcwd()

    try:
        for dir, conf in required_repositories.items():
            # todo: still skipping(tinkering) this well known..
            if conf[2] == False:
                print(f"still tinkering with {dir} repo building, skipping {dir}")
                continue

            if specific != '':
                if dir != specific:
                    continue

            path = os.path.join(well_known, dir)            
            os.chdir(path)
                
            print(f'===>Building {dir}')

            # check if already installed
            build_path = os.path.join(well_known, dir, install_prefix)

            if os.path.isdir(build_path):
                if skip_confirm:
                    cleaning(build_prefix)
                else:
                    rebuild = input(f'{dir} already built, rebuild ? [Y/n] ')

                    if rebuild == "Y" or rebuild == '':
                        cleaning(build_prefix)
                    else:
                        # next build known
                        continue

            if not no_clean:
                cleaning(build_prefix)

            r = configuring(target_platform, conf[2])
            if not r:
                exit(1)

            r = building()
            if not r:
                exit(1)

            r = packaging()
            if not r:
                exit(1)

    except SystemExit:
        pass
    finally:
        os.chdir(old_cwd)

def main_build(target_platform, clean):
    if clean:
        cleaning(build_prefix)
    
    r = configuring(target_platform, [])
    if not r:
        exit(1)

    r = building()
    if not r:
        exit(1)

    r = packaging()
    if not r:
        exit(1)


def run_command(command, env: dict):
    my_env = os.environ.copy()

    for k,v in env.items():
        my_env[k] = v

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=my_env)

    for line in process.stdout:
        print(line, end="")  # Already has newline

    process.wait()

    return process.returncode

def cleaning(build_dir):
    print(f"----> cleaning build dir<{build_dir}>");
    if os.path.isdir(build_dir):
        shutil.rmtree(build_dir)

def configuring(target_platform='', extra_defines = []):
    print("----> configuring");

    cmd = [
        "cmake",
        "--debug-find-pkg=SDL2",
        "-B",
        build_prefix,
        "-G",
        "Ninja",
        "-DCMAKE_CXX_COMPILER=clang++-18", # using clang
        "-DCMAKE_C_COMPILER=clang-18", # using clang
        "-DCMAKE_BUILD_TYPE=Release", # type release
        f"-DCMAKE_INSTALL_PREFIX={install_prefix}", # install path
        "-DCMAKE_POSITION_INDEPENDENT_CODE=ON", # all fPIC
    ]

    cmd.extend(extra_defines)

    if target_platform=="android":
        cmd.extend([
            f"-DANDROID_PLATFORM=android-21",
            f"-DANDROID_NDK={android_ndk}",
            f"-DCMAKE_TOOLCHAIN_FILE={android_ndk}/build/cmake/android.toolchain.cmake"
        ])


    exit_code = run_command(cmd, {"RUN_DOT_PY_BUILD_PREFIX": build_prefix})

    return True if exit_code == 0 else False;

def building():
    print("----> building...");
    exit_code = run_command(["cmake", "--build", build_prefix], {"RUN_DOT_PY_BUILD_PREFIX": build_prefix})

    return True if exit_code == 0 else False;

def packaging():
    print("----> packaging");
    exit_code = run_command(["cmake", "--install", build_prefix], {"RUN_DOT_PY_BUILD_PREFIX": build_prefix})

    return True if exit_code == 0 else False;

old_cwd = os.getcwd()

atexit.register(lambda : os.chdir(old_cwd))

target_platform = 'android' if args.android else ''

if args.command == "check":
    do_setup()
elif args.command == "build-known":
    do_setup(target_platform)
    do_build_known(target_platform, args.no_clean, args.specific)
elif args.command == "main-build":
    do_setup(target_platform)
    
    if args.no_skip_building_wellknown:
        do_build_known(target_platform, args.no_wellknown_clean, '', True)

    main_build(target_platform, args.no_clean)
else:
    parser.print_help()

print("------> DONE")