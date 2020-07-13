class sha1:
    def __init__(self, message):
        self.A = 0x67452301
        self.B = 0xEFCDAB89
        self.C = 0x98BADCFE
        self.D = 0x10325476
        self.E = 0xC3D2E1F0
        self.A_inital = self.A
        self.B_inital = self.B
        self.C_inital = self.C
        self.D_inital = self.D
        self.E_inital = self.E
        self.message = message
        self.binary_message = str()
        self.w = list()

    def str_message(self): # create binary instance of message
        for char in self.message:
            self.binary_message += str(bin(ord(char))[2:].zfill(8))

    def padding(self): # add padding to message
        l = len(self.binary_message) % 512
        k = (447 - l) % 512
        temp = '1' + k * '0' +   str(bin(len(self.binary_message))[2:].zfill(64))
        self.binary_message += temp

    def divide_to_512bit(self): # divide message to 512bit blocks
        n = len(self.binary_message) // 512
        self.blocks = list()
        for i in range(n):
            self.blocks.append(self.binary_message[i*512:(i+1)*512])

    def L_circular_shift(self, str, n):
        n = len(str) - n
        for i in range(n):
            str = str[-1] + str[:-1]
        return str

    def compute_W(self, block): # compute 80 W from message
        self.w.clear()
        for i in range(80):
            if i < 16:
                temp = block[i*32 : (i+1)*32]
                temp = int(temp, 2)
                self.w.append(temp)
            else:
                temp = self.w[i-16] ^ self.w[i-14] ^ self.w[i-8] ^ self.w[i-3]
                temp = int(self.L_circular_shift(str(bin(temp))[2:].zfill(32), 1), 2)
                self.w.append(temp)

    def stages(self, mode, w): # every stage of algorithm
        a = self.A
        b = self.B
        c = self.C
        d = self.D
        e = self.E
        self.B = a
        self.C = int(self.L_circular_shift(str(bin(b))[2:].zfill(32) , 30), 2)
        self.D = c
        self.E = d
        if mode == 1:
            temp = (b & c) | (~b & d)
            k = 0x5A827999
        elif mode == 2:
            temp = b ^ c ^ d
            k = 0x6ED9EBA1
        elif mode == 3:
            temp = (b & c) | (b & d) | (c & d)
            k = 0x8F1BBCDC
        elif mode == 4:
            temp = b ^ c ^ d
            k = 0xCA62C1D6

        self.A = (e
               + temp
               + int(self.L_circular_shift(str(bin(a))[2:].zfill(32), 5), 2)
               + k
               + self.w[w]) % 2**32

    def finish_block(self): # final round of algorithm
        self.A = (self.A + self.A_inital) % 2**32
        self.B = (self.B + self.B_inital) % 2**32
        self.C = (self.C + self.C_inital) % 2**32
        self.D = (self.D + self.D_inital) % 2**32
        self.E = (self.E + self.E_inital) % 2**32
        self.A_inital = self.A
        self.B_inital = self.B
        self.C_inital = self.C
        self.D_inital = self.D
        self.E_inital = self.E

    def compute_hash(self):
        self.str_message()
        self.padding()
        self.divide_to_512bit()

        for block in self.blocks:
            self.compute_W(block)
            for i in range(80):
                if i < 20:
                    mode = 1
                elif i < 40:
                    mode = 2
                elif i < 60:
                    mode = 3
                elif i < 80:
                    mode = 4

                self.stages(mode, w = i)
                if i == 79:
                    self.finish_block()

        hash = str(hex(self.A))[2:] \
             + str(hex(self.B))[2:] \
             + str(hex(self.C))[2:] \
             + str(hex(self.D))[2:] \
             + str(hex(self.E))[2:] \

        return hash
