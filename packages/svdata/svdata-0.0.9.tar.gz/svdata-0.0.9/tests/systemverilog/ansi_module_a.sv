module ansi_module_a (
  input logic a,
  input logic [1:0] b[2:0]
);

  logic c;
  logic d;
  logic [1:0] ponta[2:0];

  ansi_module_b ansi_module_b_i (.e(d));

  ansi_module_b ansi_module_b_i (
    .e(d),
    .f(d)
  );

  ansi_module_c ansi_module_c_i (
    .e(d),
    .f(a),
    .g(b)
  );

endmodule
