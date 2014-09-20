/*
CRC module automated random data testbench: data[15:0],
polynomial function crc[8:0] = x^9 + x^8 + x^5 + x^4 + x^1 + x^0
developed by Yiyang Feng, yiyangfe@usc.edu
*/

`timescale 1ns / 100ps
`define DELAY 1

module tb;

   reg [15:0] data_in_tb; /* data message */
   wire [8:0] crc_out_tb; /* crc value */

   reg [15:0] data_mem [0:199]; /* data_mem reading automated random input data from txt file */
   integer fd1; /* file descriptor */
   integer index; /* test case index */

   reg [8:0] golden_crc_out_mem [0:199]; /* golden crc_out precomputed and stored */

   /* CRC module instantiation */
   CRC crc_tb(.data(data_in_tb), .crc_out(crc_out_tb));


   initial begin
      $readmemb("rand_test_data.txt", data_mem);
      $readmemb("./golden_crc_out.txt", golden_crc_out_mem);
      fd1 = $fopen("CRC_tb.out");

      /* 200 random test data entries */
      for (index = 1; index <= 200; index = index + 1) begin
         Compute_CRC(data_mem[index - 1]);
      end
      $fclose(fd1);
      $finish;

   end

   always @(crc_out_tb) begin
      if (crc_out_tb == golden_crc_out_mem[index - 1])
         $fstrobe(fd1, "Test case #%12d:    data_in = 0x%h,    crc_out = 0x%h, golden_crc_out = 0x%h, TEST MATCH!", index, data_in_tb, crc_out_tb, golden_crc_out_mem[index - 1]);
      else
         $fstrobe(fd1, "Test case #%12d:    data_in = 0x%h,    crc_out = 0x%h, golden_crc_out = 0x%h, TEST MISMATCH!", index, data_in_tb, crc_out_tb, golden_crc_out_mem[index - 1]);   end


   task Compute_CRC;
      input [15:0] data_in_task;

      begin
         data_in_tb = data_in_task;
         #`DELAY;
      end
   endtask

endmodule