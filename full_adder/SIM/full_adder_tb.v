`timescale 1ns/1ns

module full_adder_tb;
    reg key_a = 1;
    reg key_b = 1;
    reg key_cin = 1;
    wire led_s, led_cout;

    full_adder dut (
        .a(key_a),
        .b(key_b),
        .cin(key_cin),
        .s(led_s),
        .cout(led_cout)
    );

    initial begin
        $dumpfile("full_adder_tb.vcd");
        $dumpvars(0, full_adder_tb);

        #20 {key_a, key_b, key_cin} = 3'b110; // 001: 01
        #20 {key_a, key_b, key_cin} = 3'b101; // 010: 01
        #20 {key_a, key_b, key_cin} = 3'b100; // 011: 10
        #20 {key_a, key_b, key_cin} = 3'b011; // 100: 01
        #20 {key_a, key_b, key_cin} = 3'b010; // 101: 10
        #20 {key_a, key_b, key_cin} = 3'b001; // 110: 10
        #20 {key_a, key_b, key_cin} = 3'b000; // 111: 00
        #20 $finish;
    end
endmodule