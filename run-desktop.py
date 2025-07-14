import subprocess
import os
import shutil

build_dir = "build-linux"
package_dir = "build-export-linux"

if os.name == "nt":
    build_dir = "build-window"
    package_dir = "build-export-windows"


def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    for line in process.stdout:
        print(line, end="")  # Already has newline

    process.wait()

    return process.returncode

def cleaning():
    print(f"----> cleaning build dir<{build_dir}>");
    if not os.path.isdir(build_dir):
        return
    
    for entry in os.listdir(build_dir):
        if entry == "_deps":
            continue
        else:
            path = os.path.join(build_dir, entry)
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
    
    if os.path.isdir(package_dir):
        shutil.rmtree(package_dir)

def configuring():
    print("----> configuring");
    exit_code = run_command(command = [
            "cmake",
            "-B",
            build_dir,
            "-G",
            "Ninja",
            "-DCMAKE_CXX_COMPILER=clang++",
            "-DCMAKE_C_COMPILER=clang",
            "-DCMAKE_POSITION_INDEPENDENT_CODE=ON",
            "-DENABLE_PROGRAMS=OFF",
            "-DENABLE_TESTING=OFF",
            "-DINSTALL_DOCS=OFF",
            "-DPNG_TESTS=OFF",
            "-DPNG_TOOLS=OFF",
            f"-DCMAKE_INSTALL_PREFIX={package_dir}"
        ])

    if(exit_code != 0):
        print("Exit code:", exit_code)
        exit(1)

def building():
    print("----> building...");
    exit_code = run_command(command = ["cmake", "--build", build_dir])

    if(exit_code != 0):
        print("Exit code:", exit_code)
        exit(1)

def packaging():
    print("----> packaging...[libs and includes will be in the directory: package-export]");
    exit_code = run_command(command = ["cmake", "--install", build_dir, "--prefix", package_dir])

    if(exit_code != 0):
        print("Exit code:", exit_code)
        exit(1)

cleaning()
configuring()
building()
packaging()

print("------> DONE")