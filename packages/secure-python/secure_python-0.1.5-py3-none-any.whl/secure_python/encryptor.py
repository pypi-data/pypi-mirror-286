import os
import subprocess
import shutil
import chardet
import py_compile

def detect_encoding(requirement):
    with open(requirement, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        return result['encoding']

def reencode_requirements(requirement, encoding):
    with open(requirement, 'r', encoding=encoding) as file:
        requirements = file.read()

    with open(requirement, 'w', encoding='utf-8') as file:
        file.write(requirements)

    print("Requirements file re-encoded to UTF-8.")

def install_requirements(requirement):
    subprocess.run(['pip', 'install', '-r', requirement])

def run_pyarmor(src_folder, dist_folder):
    from pyarmor.cli.__main__ import main_entry
    args = ['gen', '-O', dist_folder, '--platform', 'linux.x86_64,windows.x86_64', src_folder]
    try:
        main_entry(args)
        print("PyArmor process completed successfully.")
    except Exception as e:
        print(f"Error during PyArmor process: {e}")

def copy_pyarmor_runtime(dist_folder):
    pyarmor_folder = os.path.join(dist_folder, 'pyarmor_runtime_000000')
    sub_folder = os.path.join(dist_folder, 'server')

    dest_folder = os.path.join(sub_folder, 'pyarmor_runtime_000000')
    if os.path.exists(dest_folder):
        shutil.rmtree(dest_folder)
    try:
        shutil.copytree(pyarmor_folder, dest_folder)
        print(f"Copied pyarmor_runtime_000000 to {dest_folder}")
    except Exception as e:
        print(f"Error copying pyarmor_runtime_000000 to {dest_folder}: {e}")

    for root, dirs, _ in os.walk(sub_folder):
        if 'pyarmor_runtime_000000' not in root:
            for dir in dirs:
                dest_folder = os.path.join(root, dir, 'pyarmor_runtime_000000')
                if os.path.exists(dest_folder):
                    shutil.rmtree(dest_folder)
                try:
                    shutil.copytree(pyarmor_folder, dest_folder)
                    print(f"Copied pyarmor_runtime_000000 to {dest_folder}")
                except Exception as e:
                    print(f"Error copying pyarmor_runtime_000000 to {dest_folder}: {e}")

    if os.path.exists(pyarmor_folder):
        shutil.rmtree(pyarmor_folder)

def compile_obfuscated_to_bytecode_and_cleanup(src_folder, dist_folder):
    for root, _, files in os.walk(dist_folder):
        for file in files:
            if file.endswith('.py'):
                obfuscated_file = os.path.join(root, file)
                relative_path = os.path.relpath(obfuscated_file, src_folder)
                bytecode_file = os.path.join(dist_folder, relative_path + 'c')
                os.makedirs(os.path.dirname(bytecode_file), exist_ok=True)
                print(f"Compiling {obfuscated_file} to bytecode.")
                py_compile.compile(obfuscated_file, cfile=bytecode_file)
                os.remove(obfuscated_file)
                print(f"Deleted original obfuscated file: {obfuscated_file}")

def encrypt_code(src_folder, dist_folder, requirement):
    print(f"encrypt_code called with src_folder={src_folder}, dist_folder={dist_folder}, requirement={requirement}")

    encoding = detect_encoding(requirement)
    print(f"Detected encoding: {encoding}")

    reencode_requirements(requirement, encoding)
    install_requirements(requirement)
    run_pyarmor(src_folder, dist_folder)
    copy_pyarmor_runtime(dist_folder)
    compile_obfuscated_to_bytecode_and_cleanup(src_folder, dist_folder)

    print("Obfuscated files compiled to bytecode and original files deleted.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: encrypt_code <src_folder> <dist_folder> <requirement>")
    else:
        encrypt_code(sys.argv[1], sys.argv[2], sys.argv[3])