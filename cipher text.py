import string


def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    '''
    in_file = open(file_name, 'r')
    line = in_file.readline()
    word_list = line.split()
    in_file.close()
    return word_list

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


WORDLIST_FILENAME = 'words.txt'

class Message(object):
    def __init__(self, text):
        '''
        text (string): the message's text
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def get_message_text(self):

        return self.message_text

    def get_valid_words(self):

        return self.valid_words[:]
        
    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        shifted_dict = {}
        low_cas_let = string.ascii_lowercase
        upp_cas_let = string.ascii_uppercase
        for letter in low_cas_let:
            x = low_cas_let.index(letter)
            try:
                shifted_dict[letter] = low_cas_let[x + shift]
            except IndexError:
                while (x + shift) > 25:
                    x = x - 26
                    x + shift
                shifted_dict[letter] = low_cas_let[x + shift]
        for letter in upp_cas_let:
            y = upp_cas_let.index(letter)
            try:
                shifted_dict[letter] = upp_cas_let[y + shift]
            except IndexError:
                while (y + shift) > 25:
                    y = y - 26
                    y + shift
                shifted_dict[letter] = upp_cas_let[y + shift]
        return shifted_dict

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.       
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26
        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        shifted_dict = self.build_shift_dict(shift)
        ciphertext = ''
        for letter in self.message_text:
            if letter in shifted_dict:
                ciphertext += shifted_dict[letter]
            else:
                ciphertext += letter
        return ciphertext

class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''   
        text (string): the message's text
        shift (integer): the shift associated with this message

        '''
        super().__init__(text)
        self.shift = shift
        self.encrypting_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)   

    def get_shift(self):

        return self.shift

    def get_encrypting_dict(self):

        return self.encrypting_dict.copy()

    def get_message_text_encrypted(self):

        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift (ie. self.encrypting_dict and 
        message_text_encrypted).
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.__init__(self.message_text, shift)


class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        text (string): the message's text
        '''
        super().__init__(text)

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. 

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        
        shift_guess = 0
        result = []
        actual_score = 0
        best_score = [0, 0]
        for number in range(0, 27):
            shift_guess = number
            shift_applied = self.apply_shift(shift_guess)
            for word in shift_applied.split(' '):
                if is_word(self.get_valid_words(), word):
                    actual_score += 1
                else: 
                    pass
            if actual_score > best_score[1]:
                best_score = [shift_guess, actual_score]
                result.append((shift_guess, shift_applied))
            else:
                pass
            actual_score = 0
        result.append((best_score[0], self.apply_shift(best_score[0])))
        return result[len(result)-1]
    
            
#TOOL TESTING
    
action = ''
encrypt_text = ''
decrytp_text = ''
caesar_shift = 0 
print('Welcome to Caesar cipher tool')
print('This tool allows You to easily encrypt / decrypt text using Caesar cipher')
while action not in ('encrypt', 'decrypt', 'exit'):
    action = input('What You would like to do? \nType "encrypt" to encrypt text, "decrypt" to decrypt text, or exit to leave: ')
    if action not in ('encrypt', 'decrypt', 'exit'):
        print('Incorrect input, please try again')
if action == 'encrypt':
    encrypt_text = input('Type text You would like to encrypt: ')
    caesar_shift = input('Type shift: ')
    plaintext = PlaintextMessage(encrypt_text, int(caesar_shift))
    print('After encrypting Your text looks like this: ', plaintext.get_message_text_encrypted())
elif action == 'decrypt':
    decrypt_text = input('Type text You would like to decrypt: ')
    ciphertext = CiphertextMessage(decrypt_text)
    ciphertext_decrypt = ciphertext.decrypt_message()
    print('Decrypted message is: ', ciphertext_decrypt[1])
    print('Shift used to decrypt the message: ', ciphertext_decrypt[0])
else:
    pass

    