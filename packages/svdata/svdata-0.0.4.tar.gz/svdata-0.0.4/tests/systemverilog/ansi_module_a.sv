module ansi_module_a (
  input var logic a,
  input var logic [1:0] b[2:0]
);

  logic c;
  wire  d;

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
