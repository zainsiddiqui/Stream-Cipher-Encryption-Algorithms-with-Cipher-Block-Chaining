# Description
A program that consists of three ciphers built from scratch which can encrypt and decrypt data that is fed to them. These ciphers include a Stream Cipher, Stream Cipher with Cipher-Block-Chaining and Padding, and a Binary Vigenère Cipher.

## Created by
Zain Siddiqui

### Part 1: Stream cipher
An implementation of the stream cipher. The one-time pad is simulated by using a keystream generator to create a keystream that is the same length as the message.

The keystream generator is simply a pseudorandom number generator and the seed is derived from the password.

The cipher is implemented as follows:
1. Linear congruential generator with the following parameters:
Modulus = 256 (1 byte) Multiplier = 1103515245 Increment = 12345
2. The password is converted into a seed using the following reference: http://www.cse.yorku.ca/~oz/hash.html
3.  Apply the stream cipher byte-by-byte to generate ciphertext:
ciphertext_i = plaintext_i ⨁ keytext_i

#### Usage:
scrypt password plaintext ciphertext
scrypt password ciphertext plaintext

The password is a text string. The parameters plaintext and ciphertext are files. The same program can be used to encrypt or decrypt.


### Part 2: Block encryption with Cipher Block Chaining and Padding

This is an enhancement of Part 1 to use the concepts of shuffling data, padding – adding it and removing it correctly, and cipher block chaining.

We modify the stream cipher above to have it operate on 16-byte blocks instead of bytes. This turns it into a form of block cipher. A block cipher uses multiple iterations (rounds) through an SP-network (substitutions & permutations) to add confusion & diffusion. Confusion refers to changing bit values as a function of the key and that each bit of the ciphertext is determined by several parts of the key. Diffusion refers to the property that a change in one bit of plaintext will result in many bits of the ciphertext changing (about half).

We will not use multiple rounds of an SP network. Instead, we will keep the mechanisms of the stream cipher in place but enhance it in two ways:

1. Confusion is roughly determined by the seed and the pseudorandom output of the keystream generator in our case, but we will enhance the degree confusion by shuffling bytes of the block.
We will have the key determine which sets of bytes in the block to exchange (swap). For each 16-byte block, we do the following:
for (i=0; i < blocksize; i=i+1)
first = key[i] & 0xf (lower 4 bits of the keystream)
second = (key[i] >> 4) & 0xf (top 4 bits of the keystream) swap(block[first], block[second]) (exchange the bytes)

2. Stream ciphers have no (or low) diffusion. The change of a bit in plaintext will generally affect only that bit in ciphertext. We will enhance diffusion by adding cipher block chaining (CBC). With cipher block chaining, we exclusive-or the previous block with the next block.
The flow of the cipher is:
Create an initialization vector (IV) by reading 16 bytes from the keystream generator. For each 16-byte plaintext_block N:

1. If it is the last block, add padding.
2. Apply CBC: temp_blockN = plaintext_blockN ⨁ ciphertext_blockN-1 Use the initialization vector this is the first block.
3. Read 16 bytes from the keystream.
4. Shuffle the bytes based on the keystream data.
5. ciphertext_blockN = temp_blockN ⨁ keystreamN.
6. Write ciphertext_blockN.

#### Usage:
sbencrypt password plaintext ciphertext
sbdecrypt password ciphertext plaintext

As with Part 1, the program will take a password string, which will be hashed and used as a seed for the keystream generator. The parameters plaintext and ciphertext are both file names.

### Part 3: Binary Vigenère Cipher

The cipher is implemented by having each row containing the alphabet shifted by one position. The program encrypts data by doing the following:
1. Find the row indexed by the plaintext letter.
2. Find the column indexed by the next character of the key
3. The ciphertext letter is the intersection.

The key is repeated to make it the same length as the message.
The program will create a binary version of this cipher.

#### Usage:
vencrypt keyfile message ciphertext
This encrypts the message file using the key in keyfile and produces the file ciphertext.

vdecrypt keyfile ciphertext message
This reads the key from keyfile and decrypts the contents in cipherfile into the file message.
