import click
import pathlib
import hashlib
import json

@click.command()
@click.option('-r', '--root', required=True, help='Path to the root directory.')
@click.option('-o', '--output', default="checksum.json", help='Path to output checksum file.')
def generate_main(root, output):
    print("generating")
    result = generate(root)
    save_checksum(result, output)


def generate(root_path):
    root = pathlib.Path(root_path)
    result = {}
    for path in root.rglob("*"):
        if path.is_file():
            print(f"processing: {path}")

            normalized_path = str(path).replace(pathlib.os.sep, '/')
            result[normalized_path] = calculate_md5(path)
    
    return result


def calculate_md5(file_path, chunk_size=4096):
    md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(chunk_size), b''):
            md5.update(chunk)
    return md5.hexdigest()

        
def save_checksum(checksums, output_path):
    print(f"writing output to -> {output_path}")
    with open(output_path, 'w') as file:
        json.dump(checksums, file)