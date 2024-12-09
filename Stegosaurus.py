from PIL import Image
from cryptography.fernet import Fernet
import hashlib
import base64

#convert encoding data into 8-bit binary based in password
def keygen(password: str) -> bytes:
    return base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())

# Encrypt message with Fernet encryption
def encrypt(message: str, password: str) -> bytes:
    key = keygen(password)
    fernet = Fernet(key)
    return fernet.encrypt(message.encode())

# Decrypt message with Fernet decryption
def decrypt(encrypted_message: bytes, password: str) -> str:
    key = keygen(password)
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_message).decode()

# Generate binary data from text
def genData(data):
    newd = []
    for i in data:
        newd.append(format(ord(i), '08b'))
    return newd

#  modify the pixels according to the data
def modPix(pix, data):
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):
        pix = [value for value in imdata.__next__()[:3] +
               imdata.__next__()[:3] +
               imdata.__next__()[:3]]
        
        # Modify pixel values to encode data
        for j in range(8):
            if datalist[i][j] == '0' and pix[j] % 2 != 0:
                pix[j] -= 1
            elif datalist[i][j] == '1' and pix[j] % 2 == 0:
                pix[j] = pix[j] - 1 if pix[j] != 0 else pix[j] + 1

        # Set the last pixel to indicate end of data
        if i == lendata - 1:
            if pix[-1] % 2 == 0:
                pix[-1] = pix[-1] - 1 if pix[-1] != 0 else pix[-1] + 1
        else:
            if pix[-1] % 2 != 0:
                pix[-1] -= 1

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]

# Encode data into the image
def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)

    for pixel in modPix(newimg.getdata(), data):
        newimg.putpixel((x, y), pixel)
        if x == w - 1:
            x = 0
            y += 1
        else:
            x += 1

# Encode function
def encode():
    try:
        img = input("Enter image name(with extension) : ")
        image = Image.open(img, 'r')
        data = input("Enter data to be encoded : ")
        if len(data) == 0:
            raise ValueError('Data is empty')
        password = input('Enter password for encryption: ')
        encrypted_data = encrypt(data, password).decode('utf-8')

        newimg = image.copy()
        encode_enc(newimg, encrypted_data)

        new_img_name = input("Enter the name of new image(must be a PNG) : ")
        newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))
        print("Encoding successful. The image is saved as:", new_img_name)
    except Exception as e:
        print(f"Error: {e}")

# Decode data from the image
def decode():
    try:
        img = input("Enter image name(with extension) : ")
        image = Image.open(img, 'r')
        password = input('Enter password: ')

        data = ''
        imgdata = iter(image.getdata())

        while True:
            pixels = [value for value in imgdata.__next__()[:3] +
                      imgdata.__next__()[:3] +
                      imgdata.__next__()[:3]]
            binstr = ''

            for i in pixels[:8]:
                if i % 2 == 0:
                    binstr += '0'
                else:
                    binstr += '1'

            data += chr(int(binstr, 2))
            if pixels[-1] % 2 != 0:
                break

        decrypted_message = decrypt(data.encode('utf-8'), password)
        print(f"Decoded message: {decrypted_message}")
    except Exception as e:
        print(f"Error: {e}")


def stego():
    steg = '''
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⠀⣰⣶⣄⠀⠀⠀⠀⣠⣤⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣧⠀⠀⣠⣾⣿⣿⣿⠀⢀⣴⣿⣿⣿⡟⠀⠀⠀⠀⠀⢀⣀⣴⡶⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣧⠀⣿⣿⣿⣿⣿⠀⢾⣿⣿⣿⣿⡇⠀⢀⣴⣶⣶⣿⣿⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣷⡄⠀⢰⣿⣿⣿⣿⠀⠈⠉⠛⠛⠉⠀⠀⠙⠛⠛⠛⠃⠰⣿⣿⣿⣿⣿⡟⠀⠀⢀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣆⡀⠉⠉⠉⠀⣀⣴⣤⣷⣾⣷⣿⣾⣶⣿⣴⣦⣦⡄⢈⠙⠿⠿⣿⠇⢠⣾⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣀⠀⢿⣿⠿⠁⢀⣀⣾⣾⣿⣿⣿⣿⣿⣿⢿⣿⡿⢿⣿⣿⣿⣿⣿⣶⣤⡄⢀⡄⠈⠛⠻⠿⠃⢠⣶⣶⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢿⣷⡄⠀⠀⣤⣼⣿⣿⢿⣿⠻⣿⡏⠈⣿⠀⣿⡇⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣾⣠⣶⠀⣀⠀⠉⠉⠀⠀⠀⠀⠀⠀⠀⣴⠀⠀⣴⢀⠀⠀⣠
⠀⠀⠀⠀⠀⠀⢶⡌⠋⣡⣼⣿⠿⣿⣿⣿⠀⣿⠀⢹⡇⠀⣿⠀⣿⠃⠘⢿⣿⣿⣿⣿⠿⠿⠟⢻⠿⣿⠻⡿⠻⣿⢷⣷⣶⣶⣴⣦⣤⣀⠀⠀⣿⣶⠟⣡⣧⣤⣾⠋
⠀⠀⢀⣀⣀⣀⣠⣿⣿⣿⠻⠃⣴⣿⡟⢻⡇⢿⠀⢸⡇⠀⣿⠀⣿⠀⠀⣾⡿⢿⣿⣿⣆⠀⠀⠀⠀⠈⠀⠁⠀⠘⠀⠉⠙⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠁⠀
⣠⣴⣿⣶⣿⡿⠛⠋⠻⠙⠀⢸⡟⠹⣧⠸⡇⢸⡇⢸⡟⠀⡏⠀⠟⠀⣰⡿⠁⢸⣿⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠚⠛⠛⠉⠁⠀⠀⠀⠀⠀⢸⣇⠀⠸⣧⠁⠈⠇⠸⠇⠀⠇⠀⠀⢠⣿⠁⠀⠈⣿⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⡿⠀⠀⣿⡗⠀⠀⠀⠀⠀⠀⠀⠀⢸⡿⠃⠀⠀⠻⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⠀⠀⢀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣧⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠀⠀⠘⠛⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠋⠀⠀⠀⠴⠿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

'''
    print(steg)


# Main function
def main():
    a = int(input(":: ENTER STEGOSAURUS ::\n"
                  "1. Encode\n2. Decode\n3. Exit\n"))
    if a == 1:
        encode()
    elif a == 2:
        decode()
    elif a == 3:
        quit()
    else:
        print('invalid response, exitting...')

#ASCII art code
stego()

# Driver Code
if __name__ == '__main__':
    main()

#source for encryption https://cryptography.io/en/latest/fernet/#
#source for hashing https://docs.python.org/3/library/hashlib.html#
