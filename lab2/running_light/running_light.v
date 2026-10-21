module running_light (
    input wire sys_clk,
    input wire sys_rst_n,
    output reg led_out1,
    output reg led_out2,
    output reg led_out3,
    output reg led_out4
);

    parameter [26:0] CNT_MAX = 27'd99_999_999;
    reg [26:0] cnt; // 2500-0000 * 4
    
    always @(posedge sys_clk
           or negedge sys_rst_n) 
    begin
        if (!sys_rst_n) begin
            cnt <= 27'd0;
            {led_out1, led_out2, led_out3, led_out4} <= 4'b0111;
        end

        else begin
            if (cnt == CNT_MAX)
                cnt <= 27'd0;
            else
                cnt <= cnt + 25'd1;

            if (cnt == (CNT_MAX+1)/4-1)
                {led_out1, led_out2, led_out3, led_out4} <= 4'b1011;
            else if (cnt == (CNT_MAX+1)/2-1)
                {led_out1, led_out2, led_out3, led_out4} <= 4'b1101;
            else if (cnt == (CNT_MAX+1)/4*3-1)
                {led_out1, led_out2, led_out3, led_out4} <= 4'b1110;
            else if (cnt == CNT_MAX)
                {led_out1, led_out2, led_out3, led_out4} <= 4'b0111;
        end
    end

endmodule