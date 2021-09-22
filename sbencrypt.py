#!/usr/bin/env python3
import os
import sys
import struct
import random
import string
from string import ascii_uppercase as l
from itertools import cycle, islice
from ctypes import c_ulong
from functools import reduce



# Repeats keystream to desired length
def rep(lst, m):
    return list(islice(cycle(lst), m))

# Generates Vigenere table
def generate_table():
  l = list(range(0, 256))
  table = [l[i:]+l[:i] for i in range(len(l))]
  return table


# Encrypts cipher
def vencrypt(keystream, plaintext, ciphertext_file ):
  table = generate_table()

  c = 0
  f = open(ciphertext_file, "wb")
  for c in range(len(plaintext)):
    ##("c = ", c)
    n = int.from_bytes(plaintext[c], "big") 
    ##("Ptextbyte: "+str(plaintext[c]) + " -> int -> " + str(n))

    i = int.from_bytes(keystream[c], "big") 
    ##("Keybyte: "+ str(keystream[c]) + " -> int -> " + str(i))
    ##("Writing byte: "+ str (table[n][i].to_bytes(1, 'big')) + " -> int -> " + str(table[n][i] ) + " -> ascii -> "+ chr(table[n][i]) )
    f.write(table[n][i].to_bytes(1, 'big'))

  f.close()
  return


def vdecrypt(keystream, ciphertext, message_file ):
  #table = generate_table()
  c = 0
  i = 0
  # for i in range(len(table[60])):
  #   ##(table[i][200])


  f = open(message_file, "wb")

  for c in range(len(ciphertext)):
    ##("c = ", c)

    n = int.from_bytes(ciphertext[c], "big")
    ##("Ciphertextbyte: "+str(ciphertext[c]) + " -> int -> " + str(n))

    i = int.from_bytes(keystream[c], "big") 
    ##("Keybyte: "+ str(keystream[c]) + " -> int -> " + str(i))
    #tt = 0
    # for tt in range(len(table[60])):
    #   ##("row: ",tt,table[tt][i])
    
    v = n - i
    if (v < 0):
      v = v + 256
    
    ##("ptext row value: ", v)
    ##("Writing byte: "+ str (v.to_bytes(1, 'big')) + " -> int -> " + str(v) + " -> ascii -> "+ chr(v) )
    f.write(v.to_bytes(1, 'big'))

  f.close()

def ulong(i): return c_ulong(i).value

def sdbm_hash(s):
  return reduce(lambda h,c: ulong(ord(c) + (h << 6) + (h << 16) - h), s, 0)


def generate_lck(password, n):
  a  = 1103515245 # magic number a
  c = 12345 # magic number c
  m = 256 # modulus 2^(8) - 1 byte

  seed = sdbm_hash(password) # seed generated by hashing password
  keystream_blist = []

  ##("seed: ", seed)
  x_value = seed
  i = 0
  while(i<n):
    x_value = (a * x_value + c) % m
    keystream_blist.append( x_value )
    ##("i: "+ str(i)+ " value: "+ str(x_value))
    i = i+1

  return keystream_blist



def scrypt(n, keystream_blist, file_blist, output_file):
  i = 0
  f = open(output_file, "wb")
  for i in range(n):
    ##("i= "+ str(i))
    #key_byte = int.from_bytes(keystream_blist[i], "big")
    key_byte = keystream_blist[i]
    ##("Keybyte: "+ str(key_byte) + " -> int -> " + str(key_byte))

    file_byte = int.from_bytes(file_blist[i], "big")
    ##("Filebyte: "+ str(file_byte) + " -> int -> " + str(file_byte))

    v = key_byte ^ file_byte
    ##("Writing byte: "+ str (v.to_bytes(1, 'big')) + " -> int -> " + str(v) + " -> ascii -> "+ chr(v) )
    f.write(v.to_bytes(1, 'big'))
    ##()
    
  return



def blocks(lst, n):
    n = max(1, n)
    return list(lst[i:i+n] for i in range(0, len(lst), n))

# Swap two elements in a list 
def swap(list, pos1, pos2): 
    list[pos1], list[pos2] = list[pos2], list[pos1] 
    return list


def sbdecrypt(password, c_f_blist, output_file):
  
  
  f = open(output_file, "wb")
  ciphertext_block_blist = []
  prev_ciphertext_block_blist = []
  temp_block_blist = []
  blocksize = 16
  keystream = generate_lck(password, (16 * (len(c_f1_blist)+1)) )
  # Creating 16 byte blocks
  keystream= blocks(keystream,16 )
  ####("keystream: ",keystream)
  IV = keystream[0]
  e =  1
  p =[]
  tt = 0
  for block in c_f1_blist:
    tt = tt + 1
    ciphertext_block_blist = block.copy()
    ##("BLOCK::::::::: " , ciphertext_block_blist)
    keystream_blist = keystream[e]
    ##("keystream_blist:: ", keystream_blist)
    e = e + 1
    ##("XOR cipher block with keystream block")
    i = 0
    for i in range(blocksize): # XOR temp block with keystream block
      ##("i= "+ str(i))
      keystream_byte = int(keystream_blist[i])
      ##("c_byte: "+ str(keystream_byte) + " -> int -> " + str(keystream_byte))
      if (isinstance(ciphertext_block_blist[i],int)):
        cipher_byte = ciphertext_block_blist[i]
      else:
        cipher_byte = int.from_bytes(ciphertext_block_blist[i], "big")
      ##("filebyte: ", cipher_byte)
      ###("Filebyte: "+ temp_byte + " -> int -> " + str(temp_byte))
      v = cipher_byte ^ keystream_byte
      ##("Writing byte: "+ str (v.to_bytes(1, 'big')) + " -> int -> " + str(v) + " -> ascii -> "+ chr(v) )
      temp_block_blist.append(v) # Storing for next iteration     
    
    # Do keystream stuff now

    ##("keystream_blist: ", keystream_blist)
    ##("temp_block_blist: ", temp_block_blist)
    
    ##("BLOCK MANIUPLATION")
    i =0
    for i in range(blocksize): # Iterating through keystream and manipulating each byte
      ##("\nkey i: ",i)
      ##("keystream blist val: ", bin(keystream_blist[15-i]),keystream_blist[15-i])
      first = int(keystream_blist[15-i]) & int(hex(0xf), 16)
      ##("first: ", int(first), bin(first))
      second = ( int(keystream_blist[15-i]) >> 4) & int(hex(0xf), 16)
      ##("sec: ", int(second), bin(second))
      ##("swapping: ",temp_block_blist[first],"<>" ,temp_block_blist[second]) #inverse swapping
      temp_block_blist = swap(temp_block_blist,first,second)
    
    ##("temp_block_blist : ",temp_block_blist)
      
    if ( len(prev_ciphertext_block_blist) == 0):
        prev_ciphertext_block_blist = IV.copy()
    
    ##("XOR temp block with prev_ciphertext_block")
    i = 0 
    for i in range(blocksize): # XOR temp block with keystream block
      ##("i= "+ str(i))
      if (isinstance(prev_ciphertext_block_blist[i], int)):
        prev_ciphertext_byte = int(prev_ciphertext_block_blist[i])
      else:
        prev_ciphertext_byte = int.from_bytes(prev_ciphertext_block_blist[i], byteorder="big")
      ##("c_byte: "+ str(prev_ciphertext_byte) + " -> int -> " + str(prev_ciphertext_byte))
      temp_byte = int(temp_block_blist[i])
      ##("filebyte: ", temp_byte)
      ###("Filebyte: "+ temp_byte + " -> int -> " + str(temp_byte))
      v = temp_byte ^ prev_ciphertext_byte
      ##("Writing byte: "+ str (v.to_bytes(1, 'big')) + " -> int -> " + str(v) + " -> ascii -> "+ chr(v) )
      p.append(v)
    
    # Removing padding if last block in list
    if (tt == len(c_f_blist) ):
      end = 16 - p[-1]
      p = p[0:end]
    # Writting bytes to file
    for v in range(len(p) ):
      f.write((p[v]).to_bytes(1, 'big')) # Writing plaintext byte

    
    p = []
    ##("done")
    temp_block_blist = []
    prev_ciphertext_block_blist = block.copy()

       
 

def sbencrypt(password, c_f_blist, output_file):
  keystream = generate_lck(password, (16 * (len(c_f1_blist)+1)) )
  # Creating 16 byte blocks
  keystream= blocks(keystream,16 )
  ##("keystream: ",keystream)
  IV = keystream[0]
  e = 1
  blocksize = 16
  ##("IV: ", IV)
  f = open(output_file, "wb")
  ciphertext_block_blist = []
  temp_block_blist = []
  for block in c_f1_blist:
    ##("BLOCK::::::::: " , block)
    if (len(ciphertext_block_blist) == 0 ): # Ciphertext block is empty, thus first block
      ciphertext_block_blist = IV.copy() 
    
    ##("XOR plaintextblock with ciphertext block")
    for i in range(blocksize): # XOR plaintextblock with ciphertext block
      ##("i= "+ str(i))
      c_byte = ciphertext_block_blist[i]
      ##("c_byte: "+ str(c_byte) + " -> int -> " + str(c_byte))
      
      if (isinstance(block[i],int)):
        file_byte = block[i]
      else:
        file_byte = int.from_bytes(block[i], "big")
      ##("Filebyte: "+ str(file_byte) + " -> int -> " + str(file_byte))
      v = file_byte ^ c_byte
      ##("Writing byte: "+ str (v.to_bytes(1, 'big')) + " -> int -> " + str(v) + " -> ascii -> "+ chr(v) )
      
      temp_block_blist.append(v)  
    
    
    ciphertext_block_blist = [] # Setting ciphertext blist to empty since we dont need it anymore, we got our temp blist
    # Do keystream stuff now
    
    keystream_blist = keystream[e]
    e = e+1
    ##("keystream_blist: ", keystream_blist)
    ##("temp_block_list: ", temp_block_blist)
    
    ##("BLOCK MANIUPLATION")
    i = 0
    for i in range(blocksize): # Iterating through keystream and manipulating each byte
      ##("\nkey i: ",i)
      ##("keystream blist val: ", bin(keystream_blist[i]),keystream_blist[i])
      first = int(keystream_blist[i]) & int(hex(0xf), 16)
      ##("first: ", int(first), bin(first))
      second = ( int(keystream_blist[i]) >> 4) & int(hex(0xf), 16)
      ##("sec: ", int(second), bin(second))
      ##("swapping: ",temp_block_blist[first],"<>" ,temp_block_blist[second])
      temp_block_blist = swap(temp_block_blist,first,second)
    
    ##("tempblock b list: ",temp_block_blist)
    
    
    ##("XOR temp block with keystream block")
    i = 0
    for i in range(blocksize): # XOR temp block with keystream block
      ##("i= "+ str(i))
      keystream_byte = int(keystream_blist[i])
      ##("c_byte: "+ str(keystream_byte) + " -> int -> " + str(keystream_byte))
      temp_byte = int(temp_block_blist[i])
      ##("filebyte: ", temp_byte)
      ###("Filebyte: "+ temp_byte + " -> int -> " + str(temp_byte))
      v = temp_byte ^ keystream_byte
      ##("Writing byte: "+ str (v.to_bytes(1, 'big')) + " -> int -> " + str(v) + " -> ascii -> "+ chr(v) )
      f.write(v.to_bytes(1, 'big')) # Writing ciphertext byte
      ciphertext_block_blist.append(v) # Storing for next iteration 
    
    temp_block_blist = [] # Emptying temp block list
    
    ##("block complete: ",block)
  




password = str(sys.argv[1])
##("password: "+ password)

f1_blist = []
file = open(str(sys.argv[2]), 'rb')
while True:
  byte = file.read(1)
  if not byte:
    break
  f1_blist.append(bytes(byte))
##("f1 list: ", f1_blist)

# Creating 16 byte blocks
c_f1_blist = blocks(f1_blist,16 )
##("f1 list-blocks: ", c_f1_blist )

# Applying padding to last block
padding = 16 - int( len(c_f1_blist[-1]) )
for i in range(16 - len(c_f1_blist[-1])):
  (c_f1_blist[-1]).append(padding)

# Adding whole new block in the case that padding is equal to 0
if (padding == 0):
  t = 0
  lst = []
  for t in range(16):
    lst.append(16)
    t = t+1
  c_f1_blist.append(lst)

##("final: ", c_f1_blist)
sbencrypt(password,c_f1_blist,str(sys.argv[3]))
file.close()
print("program complete!")


#python3 cipher.py vencrypt k.txt p.txt t.txt
#python3 cipher.py vdecrypt k.txt t.txt message.txt
#python3 cipher.py scrypt monkey01 p.txt stream_out.txt
#python3 cipher.py sbencrypt monkey01 p.txt stream_out.txt
#python3 cipher.py sbdecrypt monkey01 stream_out.txt stream_out1.txt