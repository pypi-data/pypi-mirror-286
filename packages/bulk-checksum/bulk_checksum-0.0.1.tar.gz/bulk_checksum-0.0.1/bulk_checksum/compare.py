import click
import json

@click.command()
@click.option('-s', '--source', required=True, help='Filepath to the source checksum.')
@click.option('-d', '--dest', required=True, help='Filepath to the destination checksum.')
def compare_main(source, dest):
    source_checksums = load_checksum_file(source)
    dest_checksums = load_checksum_file(dest)

    diff = compare_checksums(source_checksums, dest_checksums)
    print(json.dumps(diff, indent=4))

def load_checksum_file(checksum_filepath):
    result = {}
    with open(checksum_filepath, 'r') as file:
        result = json.load(file)
    return result

def compare_checksums(source_checksum, destination_checksum):
    only_in_source = {k: v for k, v in source_checksum.items() if k not in destination_checksum}
    only_in_destination = {k: v for k, v in destination_checksum.items() if k not in source_checksum}
    mismatches = {k: (f"{source_checksum[k]} -> {destination_checksum[k]}") for k in source_checksum if k in destination_checksum and source_checksum[k] != destination_checksum[k]}

    return {
        "only_in_source": only_in_source,
        "only_in_destination": only_in_destination,
        "mismatches": mismatches
    }