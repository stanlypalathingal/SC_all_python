from cryptography.fernet import Fernet
import asymcrypt
from publish import publish # publish.py

# creation of symmetric key
def sym_key():
    symmetricKey_KIS = b'aQOQxINtlrXU_HkbJywoMxfiFMXC-OToihHK2ApIeCs='
    KIS = Fernet(symmetricKey_KIS)
    KIE=Fernet.generate_key() # generate symmetric key
    KIE_IoTD=KIS.encrypt((KIE))
    #print(KIE_IoTD)
    encrypt_public(KIE)
    publish("sensor_sym_key",KIE_IoTD) # publish symmetric key to IoTD
    
def encrypt_public(key):
    #open the file conatining the id of DC
    name_of_dc=open('data/temporary_store.txt').read().replace('\n','')
    encrypted_data = asymcrypt.encrypt_data(key,"data/"+name_of_dc+".pem") # encrypt with the public key
    hex_str = encrypted_data.hex()
    publish(name_of_dc,hex_str) #publish the encrypted key to EDC
    
def Decryption(encrypted_data):
    encrypted_data=encrypted_data.decode("utf-8") 
    # decrypt the request
    # try except for dealing with unencrypted or not properly encrypted.
    try:
        new_rnd_bytes = bytes.fromhex(encrypted_data)
        decrypted_data = asymcrypt.decrypt_data(new_rnd_bytes,"data/private_key.pem") #decrypt with the private key
        print('Decrypted data is :', decrypted_data)
        with open('data/data_request.csv','w') as f:
            f.write("\n"+str(decrypted_data))
        f.close()
    except:
        print("not encrypted")
