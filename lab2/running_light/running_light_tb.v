`timescale 1ns / 1ns
module running_light_tb;

    reg sys_clk = 1'b0;
    reg sys_rst_n = 1'b0;
    wire [26:0] cnt;
    wire led_out1,led_out2,led_out3,led_out4;

    assign cnt = dut.cnt;

    running_light #(
        .CNT_MAX(27'd11)
    ) dut (
        .sys_clk (sys_clk),
        .sys_rst_n (sys_rst_n),
        .led_out1 (led_out1),
        .led_out2 (led_out2),
        .led_out3 (led_out3),
        .led_out4 (led_out4)
    );

    always #10 sys_clk = ~sys_clk;
    initial begin
        $dumpfile("running_light_tb.vcd");
        $dumpvars(0, running_light_tb);

        #20 sys_rst_n = 1'b1;
        #300 sys_rst_n = 1'b0;
        #40 sys_rst_n = 1'b1; 
        #600 $finish;
    end

endmodule