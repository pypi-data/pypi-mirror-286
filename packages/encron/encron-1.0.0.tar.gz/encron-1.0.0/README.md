#module offers a first and secure way of encryting anything..

#string encrytion
dat='awesomeness is my thing'
passwd='password'

#encryptpy
encrypted_data=encrypt_data(dat,passwd)

#decrypt
decrypt_data(encrypted_data,passwd)

#find_file in current upto / dir to return path of file
file_path=find_file('file.txt')

#encrypt_file -enc a whole file and with the tool and phrase the data can be retrieved
encrypt_file('file_name')

#decrypt_file
decrypt_file('file_name)

#for web the chars are encrypted to fit usability of transfering data through url as in django
web_enc=encrypt_web('dat',passwd)
decrypt_web(web_enc,passwd)

