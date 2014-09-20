import sys
from CRC import CRCGenerator

# command line parser
def parseUserInput():
   try:
      param_tuple = CRCGenerator.parseParams(sys.argv[1:])
      return param_tuple
   except (IndexError, ValueError) as err:
      print err
      sys.exit(0)

def main():
   (data_width, poly_str) = parseUserInput()
   CRC_inst = CRCGenerator(data_width, poly_str)

   # 200 random test data    
   CRC_inst.generateVerilogTb(rand_data_path = 'rand_test_data.txt', case_num = 200);    
   print 'Automated testbench with unique test data generated, check it out!'

if __name__ == '__main__': main() 
