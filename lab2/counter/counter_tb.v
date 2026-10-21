`timescale 1ns / 1ns
module counter_tb;

    reg sys_clk = 1'b0;
    reg sys_rst_n = 1'b0;
    wire [24:0] cnt;
    wire led_out;

    assign cnt = dut.cnt;

    counter #(
        .CNT_MAX(25'd9)
    ) dut (
        .sys_clk (sys_clk),
        .sys_rst_n (sys_rst_n),
        .led_out (led_out)
    );

    always #10 sys_clk = ~sys_clk;
    initial begin
        $dumpfile("counter_tb.vcd");
        $dumpvars(0, counter_tb);

        #20 sys_rst_n = 1'b1;
        #300 sys_rst_n = 1'b0;
        #40 sys_rst_n = 1'b1; 
        #500 $finish; 
    end

endmodule