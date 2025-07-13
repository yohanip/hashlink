import subprocess
import os

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

print("----> cleaning build dir");
exit_code = run_command(command = ["rm", "-rf", "build"])

if(exit_code != 0):
    print("Exit code:", exit_code)
    exit(1)

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

print("----> building...");
exit_code = run_command(command = ["cmake", "--build", "build"])

if(exit_code != 0):
    print("Exit code:", exit_code)
    exit(1)


print("------> DONE")
