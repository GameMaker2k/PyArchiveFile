import os
import stat
import tempfile
import hashlib
from crc32c import crc32 as crc32c_checksum
import gzip
import bz2
import lzma
import zstandard as zstd
import brotli
import lz4.frame

# Function to get file type based on mode
def get_file_type(mode):
    if stat.S_ISREG(mode):
        return 0  # Regular file
    elif stat.S_ISLNK(mode):
        return 2  # Symbolic link
    elif stat.S_ISCHR(mode):
        return 3  # Character device
    elif stat.S_ISBLK(mode):
        return 4  # Block device
    elif stat.S_ISDIR(mode):
        return 5  # Directory
    elif stat.S_ISFIFO(mode):
        return 6  # Pipe
    return 0  # Default to regular file if unknown

# Function to calculate checksum based on method
def calculate_checksum(method, file_path):
    if method == 'none':
        return '0'
    elif method == 'crc32':
        with open(file_path, 'rb') as f:
            return "%x" % (crc32c_checksum(f.read()) & 0xffffffff)
    elif method == 'md5':
        hash_md5 = hashlib.md5()
    elif method == 'sha1':
        hash_md5 = hashlib.sha1()
    elif method == 'sha224':
        hash_md5 = hashlib.sha224()
    elif method == 'sha256':
        hash_md5 = hashlib.sha256()
    elif method == 'sha384':
        hash_md5 = hashlib.sha384()
    elif method == 'sha512':
        hash_md5 = hashlib.sha512()
    else:  # default to crc32
        with open(file_path, 'rb') as f:
            return "%x" % (crc32c_checksum(f.read()) & 0xffffffff)

    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# Function to pack files
def pack_cat_file(source_dir, output_file, compression='none', checksum_method='none'):
    inode_to_file = {}
    curinode = 0
    num_files = sum([len(files) for r, d, files in os.walk(source_dir)])
    metadata = []
    
    with open(output_file, 'wb') as out_file:
        out_file.write(f'CatFile1\x00{num_files}\x00'.encode())

        for root, dirs, files in os.walk(source_dir):
            for file in files:
                full_path = os.path.join(root, file)
                stat_info = os.stat(full_path, follow_symlinks=False)
                file_type = get_file_type(stat_info.st_mode)
                inode = stat_info.st_ino

                if file_type == 0 and inode in inode_to_file:
                    file_type = 1  # Hard link
                    link_name = inode_to_file[inode]
                else:
                    inode_to_file[inode] = full_path
                    link_name = ''
                    curinode += 1

                size = stat_info.st_size if file_type == 0 else 0
                record = f"{file_type}\x00{full_path}\x00{link_name}\x00{size:x}\x00"
                metadata.append(record)
                
                # Metadata checksum
                with tempfile.NamedTemporaryFile(delete=False) as tmp:
                    tmp.write(record.encode())
                    tmp_path = tmp.name
                
                header_checksum = calculate_checksum(checksum_method, tmp_path)
                content_checksum = calculate_checksum(checksum_method, full_path) if file_type == 0 else '0'
                
                os.unlink(tmp_path)  # Clean up temporary file
                
                out_file.write(f'{record}{header_checksum}\x00{content_checksum}\x00'.encode())

                if file_type == 0:
                    with open(full_path, 'rb') as f:
                        out_file.write(f.read())
                    out_file.write(b'\x00')

        # Compression
        if compression != 'none':
            compress_file(output_file, compression)

# Function to compress final output file
def compress_file(file_path, compression_method):
    if compression_method == 'gzip':
        with open(file_path, 'rb') as f:
            data = f.read()
        with gzip.open(file_path + '.gz', 'wb') as f:
            f.write(data)
    elif compression_method == 'bzip2':
        with open(file_path, 'rb') as f:
            data = f.read()
        with bz2.open(file_path + '.bz2', 'wb') as f:
            f.write(data)
    elif compression_method == 'lzma':
        with open(file_path, 'rb') as f:
            data = f.read()
        with lzma.open(file_path + '.xz', 'wb') as f:
            f.write(data)
    # Add other compression methods here if needed
    # Finally, replace original file with compressed file
    os.rename(file_path + '.' + compression_method, file_path)

# Example usage
# pack_cat_file('source_directory', 'output_file', 'gzip', 'md5')
