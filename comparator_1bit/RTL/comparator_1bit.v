module comparator_1bit (
    input  wire a,
    input  wire b,
    output wire lt,
    output wire eq,
    output wire gt
);

    assign lt = (~a) | b;
    assign eq = a ^ b;
    assign gt = a | (~b);

endmodule