# Purpose
CLI utility for verifying if a bulk file copy operation was successful.

# Usage
This tool is meant to be used after all files have been copied from a 'source' to 'destination' directory.

1. Run `bulk_checksum_generate` to create a checksum for every file in the source root directory.
The output of this will be a `checksum.json` file.
1. Run the same command in the destination directory.
1. Run `bulk_checksum_compare` on the two checksum files.
If there were any erros in copying the data, the resulting mismatches will be reported by the output of this function.
