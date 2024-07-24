import base64
import gzip
import shutil
import zipfile
import click
from qrcode.main import QRCode
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from diffsyncer import config, utils


def decrypt_data_aes(data, key):
    iv = data[:16]
    encrypted_data = data[16:]
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    return decrypted_data


def decompress_file_data(compressed_data, method="lzma"):
    if method == "gzip":
        decompressed_data = gzip.decompress(compressed_data)
    elif method == "lz4":
        import lz4.frame

        decompressed_data = lz4.frame.decompress(compressed_data)
    elif method == "lzma":
        import lzma

        decompressed_data = lzma.decompress(compressed_data)
    elif method == "zstd":
        import zstd

        decompressed_data = zstd.decompress(compressed_data)
    else:
        raise ValueError("Unsupported compression method")

    return decompressed_data


def decode_by_zxing(img: str):
    import zxing

    reader = zxing.BarCodeReader()
    return reader.decode(img).raw


def decode_by_zbar(img: str):
    from pyzbar.pyzbar import decode
    from PIL import Image

    decocdeQR = decode(Image.open(img))
    return decocdeQR[0].data.decode("utf-8")


def decode_qr_codes(qr_codes_dir):
    encrypted_data: list[bytes] = []

    # read files in dir qr_codes_dir
    qr_code_imgs = [
        (i, f"{qr_codes_dir}/{i}.png") for i in range(len(os.listdir(qr_codes_dir)))
    ]

    # filter image files
    qr_code_imgs = utils.get_qrcode_images(qr_codes_dir)

    click.echo(f"Decoding {len(qr_code_imgs)} QR codes")

    for index, img in enumerate(qr_code_imgs):
        # Decode QR code and decrypt data
        dataString = decode_by_zxing(img)

        if dataString is None:
            print(f"Try again: {img}")
            dataString = decode_by_zbar(img)

        if dataString is None:
            print(f"QR code decoding failed: {img}")
            continue

        # split dataString by ":", get the last element and decode it from base64
        str_arr = dataString.split(":")
        data_index = str_arr[1]
        useful_data = str_arr[-1]
        click.echo(f"Process: {int(str_arr[1]) + 1}/{int(str_arr[0])}")

        # try to decode base64
        try:
            data = base64.b64decode(useful_data)
        except Exception:
            print(f"Failed to decode base64: {str_arr}")
            continue

        # set data_index data to decrypted data
        encrypted_data.insert(int(data_index), data)

    return b"".join(encrypted_data)


def sava_qr_codes(qr_codes: list[QRCode], output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for index, qr in qr_codes:
        qr.save(f"{output_dir}/{index}.png")


# Decode QR codes for git diff patch data
def execute(qrcode_dir: str):
    with open(config.ASE_KEY_FILE, "rb") as file:
        aes_key = file.read()

    click.echo("Decrypting QR codes")
    encrypted_data = decode_qr_codes(qrcode_dir)
    click.echo(f"Decrypting data: {len(encrypted_data)}")
    compressed_data = decrypt_data_aes(encrypted_data, aes_key)
    click.echo(f"Decompressing data: {len(compressed_data)}")
    decompressed_data = decompress_file_data(compressed_data, config.COMPRESS_METHOD)

    zip_file = os.path.join(qrcode_dir, "tmp.zip")

    # write decompressed_data to zip file
    with open(zip_file, "wb") as file:
        file.write(decompressed_data)

    # unzip file
    unzip_dir = os.path.join(qrcode_dir, "diff")

    # clear unzip dir
    shutil.rmtree(unzip_dir, ignore_errors=True)

    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        zip_ref.extractall(unzip_dir)

    # remove zip file
    shutil.rmtree(zip_file, ignore_errors=True)

    return unzip_dir


def decode_by_scan(data: list[str]):
    print("Decrypting QR codes")
    encrypted_data = decode_qr_codes_by_scan(data)
    print(f"Decrypting data: {len(encrypted_data)}")

    with open(config.ASE_KEY_FILE, "rb") as file:
        aes_key = file.read()

    compressed_data = decrypt_data_aes(encrypted_data, aes_key)
    click.echo(f"Decompressing data: {len(compressed_data)}")
    decompressed_data = decompress_file_data(compressed_data, config.COMPRESS_METHOD)

    zip_file = os.path.join(config.OUTPUT_DIR, "tmp.zip")

    # write decompressed_data to zip file
    with open(zip_file, "wb") as file:
        file.write(decompressed_data)

    # unzip file
    unzip_dir = config.DIFF_DIR

    # clear unzip dir
    shutil.rmtree(unzip_dir, ignore_errors=True)

    # unzip file
    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        unzip_dir = os.path.join(config.OUTPUT_DIR, "diff")
        zip_ref.extractall(unzip_dir)

    return unzip_dir


def decode_qr_codes_by_scan(data: list[str]):
    encrypted_data: list[bytes] = []

    for index, qr_code in enumerate(data):
        print(f"Process: {index + 1}/{len(data)}")

        # try to decode base64
        try:
            decode_data = base64.b64decode(qr_code)
        except Exception:
            print(f"Failed to decode base64: {qr_code}")
            continue

        encrypted_data.append(decode_data)

    return b"".join(encrypted_data)
