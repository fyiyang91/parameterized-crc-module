import re
import random

# Paramaterized CRCGenerator class
class CRCGenerator:
   # Parse error message
   _parse_err_msg = 'Oops! You didn\'t invoke the program correctly.\n\nusage: python <sourcefile> <data_width> \
<polynomial_function>\n\nNOTE:\n1) The data_width falls within [8, 32]\n2) LSB and MSB of polynomial must be 1\n3) \
polynomial function length falls within [1,data_width)'


   # Constructor
   def __init__(self, data_width = 8, poly_function = '11101'):
      # default constructor: data_width 8 bits, 
      # default generator poly: x^4 + x^3 + x^2 + 1
      self.data_width = data_width
      self.poly = poly_function;
      self.out_mtrx = CRCGenerator.parallelCRC(data_width, poly_function)


   # Print overloading
   def __str__(self):
      return'CRC format: {0}-bit data width, generator function : {1} (0b{2})'.format(self.data_width, \
CRCGenerator.getFormatPoly(self.poly), self.poly)


   # static method perform LSFR on input bit
   @staticmethod
   def serialCRC(bit_in, crc_in, poly_str):
      # crc_in has to be a valid list of length poly_length
      poly_degree = len(poly_str) - 1
      crc_out = []
      feedback = crc_in[poly_degree - 1] ^ bit_in
      crc_out.append(feedback)
      crc_out += [feedback ^ crc_in[i - 1] if poly_str[poly_degree - i] is '1' else crc_in[i - 1] \
for i in xrange(1, poly_degree)]  	 
      return crc_out 

   	
   # static method to derive output matrix
   @staticmethod
   def parallelCRC(data_width, poly_str):
      crc_out_mtrx = []
      for i in xrange(0, data_width):
         data_in_bin = '{0:b}'.format(1 << i).zfill(data_width) # padding zero to front	
         # initialize crc_out to a list of all 0s
         crc_out = [ 0 for j in xrange(0, len(poly_str) - 1) ]
         for eachbit in data_in_bin:
            crc_out = CRCGenerator.serialCRC(int(eachbit), crc_out, poly_str)
         crc_out_mtrx.append(crc_out)		 
      return crc_out_mtrx      


   # static method to compute the crc_out of given data with given polynomial
   @staticmethod
   def computeCRC(data = 0x32, data_width = 8, poly_str = '11101'):
      crc_out = [0 for i in xrange(0, len(poly_str) - 1)]
      for i in xrange(data_width - 1, -1, -1):
         crc_out = CRCGenerator.serialCRC((data >> i) & 1, crc_out, poly_str) 
      return ''.join(reversed([str(i) for i in crc_out])) 



   # static method to get formated poly expression
   @staticmethod
   def getFormatPoly(poly_str):
      return ' + '.join(filter(None, ['x^' + str(len(poly_str) - 1 - i) if poly_str[i] is '1' else '' \
for i in xrange(len(poly_str))]))
      
  
   # static method to parse data_width and poly function format, raise ValueError
   @staticmethod
   def parseParams(user_args):
      try:
         if len(user_args) != 2: raise ValueError(CRCGenerator._parse_err_msg) # more than 2 or less than 2 arguments
         (data_width, poly_str) = (int(user_args[0]), user_args[1])
         if data_width > 32 or data_width < 8: raise ValueError(CRCGenerator._parse_err_msg) # Invalid data_width
         if not re.search(r'^1[01]*1$', poly_str) or len(poly_str) >= data_width: 
            raise ValueError(CRCGenerator._parse_err_msg) # Invalid poly function format or length
         else: 	
            return (data_width, poly_str)
      except ValueError as err: 
         raise ValueError(CRCGenerator._parse_err_msg) # rethrow with predifined error msg


   # generate verilog CRC module
   def generateVerilogFile(self, path = './CRC.v'):
      code_out = []
      code_out.append("/*\nCRC module data[{0}:0],\nCRC generator polynomial crc[{1}:0] = {2},\n\
developed by Yiyang Feng, yiyangfe@usc.edu\n*/\n\nmodule CRC (data, crc_out);\n\n\n   input [{0}:0] data;\
\n   output reg [{1}:0] crc_out;\n\n\n   always @(*) begin\n".format(self.data_width - 1, len(self.poly) - 2, \
CRCGenerator.getFormatPoly(self.poly)))

      for i in xrange(0, len(self.out_mtrx[0])):
         code_out.append('      crc_out[{0}]'.format(i,) + ' = ' + ' ^ '.join(filter(None, ['data[{0}]'.format(j,) \
if self.out_mtrx[j][i] is 1 else None for j in xrange(0, len(self.out_mtrx))])) + ';\n\n')
      code_out.append('   end\n\nendmodule')
      fd = open(path, 'w')
      fd.write(''.join(code_out))
      fd.close()   


   # generate verilog CRC module tb
   def generateVerilogTb(self, case_num = 100, tb_path = './CRC_tb.v', rand_data_path = './rand_test_data.txt', \
gold_crc_path = './golden_crc_out.txt'):
      # can't generate a very large list, list size of 2 ** 32 causes MemoryError,
      # use set or hashtable instead, trade time for space
      data_set = set([0, (1 << self.data_width) - 1])
      for i in xrange(case_num - 2):
         rand = random.randint(1, (1 << self.data_width) - 2)
         while rand in data_set: rand = random.randint(1, (1 << self.data_width) - 2)
         data_set.add(rand)
      out = list(data_set)
      # shuffle the list, in random order
      random.shuffle(out)	
      # write random test data file, and golden crc_out to gold_crc_out file
      fd = open(gold_crc_path, 'w')
      gold_crc_out = [CRCGenerator.computeCRC(each_data, self.data_width, self.poly) for each_data in out]
      fd.write('\n'.join(gold_crc_out)) 
      fd.close()

      out = [bin(item)[2:].zfill(self.data_width) for item in out]
      fd = open(rand_data_path, 'w')	
      fd.write('\n'.join(out))
      fd.close()

      # generate tb file
      out = []
      out.append('/*\nCRC module automated random data testbench: data[%d:0],\npolynomial function crc[%d:0] = %s\n\
developed by Yiyang Feng, yiyangfe@usc.edu\n*/\n\n`timescale 1ns / 100ps\n`define DELAY 1\n\nmodule tb;\n\n   reg \
[%d:0] data_in_tb; /* data message */\n   wire [%d:0] crc_out_tb; /* crc value */\n\n   reg [%d:0] data_mem [0:%d]; \
/* data_mem reading automated random input data from txt file */\n   integer fd1; /* file descriptor */\n   integer \
index; /* test case index */\n\n   reg [%d:0] golden_crc_out_mem [0:%d]; /* golden crc_out precomputed and stored */\n\n\
   /* CRC module instantiation */\n   CRC crc_tb(.data(data_in_tb), .crc_out(crc_out_tb));\n\n\n' % (self.data_width - 1, \
len(self.poly) - 2, CRCGenerator.getFormatPoly(self.poly), self.data_width - 1, len(self.poly) - 2, self.data_width - 1, \
case_num - 1, len(self.poly) - 2, case_num - 1))
      out.append('   initial begin\n      $readmemb(\"%s\", data_mem);\n      $readmemb(\"%s\", golden_crc_out_mem);\n\
      fd1 = $fopen(\"CRC_tb.out\");\n\n      /* %d random test data entries */\n      for (index = 1; index <= %d; index = \
index + 1) begin\n         Compute_CRC(data_mem[index - 1]);\n      end\n      $fclose(fd1);\n      $finish;\n\n   end\n\n'\
 % (rand_data_path, gold_crc_path, case_num, case_num))
      out.append('   always @(crc_out_tb) begin\n      if (crc_out_tb == golden_crc_out_mem[index - 1])\n         $fstrobe\
(fd1,\"Test case #%12d:    data_in = 0x%h,    crc_out = 0x%h, golden_crc_out = 0x%h, TEST MATCH!\", index, data_in_tb, \
crc_out_tb, golden_crc_out_mem[index - 1]);\n      else\n         $fstrobe(fd1, \"Test case #%12d:    data_in = 0x%h,    \
crc_out = 0x%h, golden_crc_out = 0x%h, TEST MISMATCH!\", index, data_in_tb, crc_out_tb, golden_crc_out_mem[index - 1]);\n\
   end\n\n\n')
      out.append('   task Compute_CRC;\n      input [%d:0] data_in_task;\n\n      begin\n         data_in_tb = \
data_in_task;\n         #`DELAY;\n      end\n   endtask\n\nendmodule' % (self.data_width - 1,))
      fd = open(tb_path, 'w')
      fd.write(''.join(out))
      fd.close()



 
''' Code below outside the scope of class CRCGenerator '''
# test client
def main():
   (data_width, poly_str) = parseUserInput()
   CRC_inst_0 = CRCGenerator(data_width, poly_str)
   CRC_inst_0.generateVerilogFile()
   print 'Hey, it works, check it out!'


# command line parser
def parseUserInput():
   import sys
   try:
      param_tuple =  CRCGenerator.parseParams(sys.argv[1:])
      return param_tuple 
   except (IndexError, ValueError) as err:
      print err
      sys.exit(0)

if __name__ == '__main__': main()
