import base64
import gzip
import shutil
import click
from qrcode.main import QRCode
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import hashlib

from diffsyncer import config


def get_hash(data):
    return hashlib.sha256(data).hexdigest()


def encrypt_data_aes(data, key):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(data) + encryptor.finalize()
    return iv + encrypted_data


def compress_file(input_file, method="lzma", level=9):
    with open(input_file, "rb") as file:
        data = file.read()
    if method == "gzip":
        compressed_data = gzip.compress(data, compresslevel=level)
    elif method == "lz4":
        import lz4.frame

        compressed_data = lz4.frame.compress(
            data, compression_level=lz4.frame.COMPRESSIONLEVEL_MAX
        )
    elif method == "lzma":
        import lzma

        print(f"Compressing data: {len(data)}")
        compressed_data = lzma.compress(data)
    elif method == "zstd":
        import zstd

        return zstd.compress(data, 22)
    else:
        raise ValueError("Unsupported compression method")
    return compressed_data


def generate_qrcodes(data, chunk_size=2048):
    chunks = [data[i : i + chunk_size] for i in range(0, len(data), chunk_size)]
    qr_codes = []
    chunk_len = len(chunks)
    for i, chunk in enumerate(chunks):
        qr = QRCode(
            version=1,
            # error_correction=constants.ERROR_CORRECT_L,
            box_size=10,
            border=2,
        )
        # add chunk length,index and base64 encoded data to qr code
        qr_data = f"{chunk_len}:{i}:{base64.b64encode(chunk).decode('ascii')}"
        qr.add_data(qr_data)
        qr.make(fit=True)
        qr_codes.append((i, qr.make_image(fill_color="black", back_color="white")))
        click.echo(f"Generated QR code {i + 1}/{chunk_len}")
    return qr_codes


def sava_qr_codes(qr_codes: list[QRCode], output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for index, qr in qr_codes:
        qr.save(f"{output_dir}/{index}.png")


# Generate QR codes for git diff data zip file
def execute(diff_file: str, output_dir: str = config.OUTPUT_DIR):
    with open(config.ASE_KEY_FILE, "rb") as file:
        aes_key = file.read()

    click.echo(f"Compressing file: {diff_file}")
    compressed_data = compress_file(diff_file, method=config.COMPRESS_METHOD)
    click.echo("Encoding file data with AES")
    encrypted_data = encrypt_data_aes(compressed_data, aes_key)
    click.echo("Generating QR codes")
    qr_codes = generate_qrcodes(encrypted_data, config.CHUNK_SIZE)

    # clear all files and dir in output dir
    shutil.rmtree(output_dir, ignore_errors=True)

    sava_qr_codes(qr_codes, output_dir)
