/*
CRC module data[15:0],
CRC generator polynomial crc[8:0] = x^9 + x^8 + x^5 + x^4 + x^1 + x^0,
developed by Yiyang Feng, yiyangfe@usc.edu
*/

module CRC (data, crc_out);


   input [15:0] data;
   output reg [8:0] crc_out;


   always @(*) begin
      crc_out[0] = data[0] ^ data[1] ^ data[2] ^ data[3] ^ data[12] ^ data[13] ^ data[14] ^ data[15];

      crc_out[1] = data[0] ^ data[4] ^ data[12];

      crc_out[2] = data[1] ^ data[5] ^ data[13];

      crc_out[3] = data[2] ^ data[6] ^ data[14];

      crc_out[4] = data[0] ^ data[1] ^ data[2] ^ data[7] ^ data[12] ^ data[13] ^ data[14];

      crc_out[5] = data[0] ^ data[8] ^ data[12];

      crc_out[6] = data[1] ^ data[9] ^ data[13];

      crc_out[7] = data[2] ^ data[10] ^ data[14];

      crc_out[8] = data[0] ^ data[1] ^ data[2] ^ data[11] ^ data[12] ^ data[13] ^ data[14];

   end

endmodule