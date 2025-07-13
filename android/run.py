import subprocess
import os
import shutil

ANDROID_NDK = os.environ["ANDROID_NDK"]

if not ANDROID_NDK:
    print("Please specify ANDROID_NDK env var")
    exit(1)

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    for line in process.stdout:
        print(line, end="")  # Already has newline

    process.wait()

    return process.returncode

def cleaning():
    print("----> cleaning build dir");
    if not os.path.isdir("build"):
        return
    
    for entry in os.listdir("build"):
        if entry == "_deps":
            continue
        else:
            path = os.path.join("build", entry)
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
    
    if os.path.isdir("package-export"):
        shutil.rmtree("package-export")

def configuring():
    print("----> configuring");
    exit_code = run_command(command = [
            "cmake",
            "-B",
            "build",
            "-G",
            "Ninja",
            "-DANDROID_ABI=arm64-v8a",
            "-DANDROID_PLATFORM=android-21",
            f"-DANDROID_NDK={ANDROID_NDK}",
            f"-DCMAKE_TOOLCHAIN_FILE={ANDROID_NDK}/build/cmake/android.toolchain.cmake"
        ])

    if(exit_code != 0):
        print("Exit code:", exit_code)
        exit(1)

def building():
    print("----> building...");
    exit_code = run_command(command = ["cmake", "--build", "build"])

    if(exit_code != 0):
        print("Exit code:", exit_code)
        exit(1)

def packaging():
    print("----> packaging...[libs and includes will be in the directory: package-export]");
    exit_code = run_command(command = ["cmake", "--install", "build", "--prefix", "package-export"])

    if(exit_code != 0):
        print("Exit code:", exit_code)
        exit(1)

# cleaning()
configuring()
building()
packaging()

print("------> DONE")