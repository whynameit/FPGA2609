`timescale 1ns/1ns

module comparator_1bit_tb;
    reg key_a = 1;
    reg key_b = 1;
    wire led_lt, led_eq, led_gt;

    comparator_1bit dut (
        .a(key_a),
        .b(key_b),
        .lt(led_lt),
        .eq(led_eq),
        .gt(led_gt)
    );

    initial begin
        $dumpfile("comparator_1bit_tb.vcd");
        $dumpvars(0, comparator_1bit_tb);

        #20 key_b = 0;
        #20 begin
            key_a = 0;
            key_b = 1;
        end
        #20 key_b = 0;
        #20 $finish;
    end
endmodule