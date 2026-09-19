# Carry Local Protocol

Parallel word-level carry protocol for arbitrary-precision addition.
Companion code for the paper:

> **"Local Carry Decision and Informational Irrelevance in Large-Base
> Positional Arithmetic"**
> Marlon Javier Muñoz Muñoz and Javier Fernando Botía Valderrama —
> Universidad de Antioquia, Colombia
> Preprint: arXiv:XXXX.XXXXX · Submitted to IEEE Latin America Transactions

## What is this?

A hardware protocol in which each compute nucleus adds one word (32/64 bits)
independently and exchanges a single binary flag (+c / −c) with its immediate
neighbor. Because the carry dependency is confined to the frontier set
F = {(a,b) : a+b = B−1} with measure μ(F) = 1/B, at word-level bases
(B = 2³², 2⁶⁴) the dependency is statistically negligible: nuclei decide
their outgoing carry without waiting, and only frontier cells stall and
forward the flag. The design is homogeneous, asynchronous (no global clock),
race-free by construction, and scales with linear area O(m).


## Note on the clock in the RTL

The Verilog model in `verilog/` is a **synchronous behavioral model intended
for functional verification**: the `clk` signal discretizes the protocol
phases (local sum and classification, flag emission, reception and
correction) into simulation cycles. It does **not** constitute a physical
global-clock requirement of the protocol. Inter-nucleus coordination relies
exclusively on the flag handshake (`flag_out`/`flag_ready`,
`flag_in`/`flag_valid`), a two-wire completion-signaling primitive that can
be realized without any shared time base — e.g., self-timed completion
detection, GALS integration, or bundled-data asynchronous logic. The
clock-free claim refers to the protocol specification; the clocked RTL is
one convenient verification vehicle for it.

## Repository structure

- `verilog/` — RTL: `carry_nucleus.v` (cell), `carry_chain.v` (chain of N
  nuclei), `ripple_ref.v` (sequential reference), `tb_comparison.v`
  (testbench with LFSR random stimuli and CSV export).
- `python/` — `cross_validate.py` (verifies Verilog output against Python
  big-integer arithmetic), `figures.py` (regenerates Figs. 1–5 of the paper),
  `statistics.py` (frontier-measure statistics), `requirements.txt`.

## Prerequisites

- [Icarus Verilog](http://iverilog.icarus.com/) (`iverilog`, `vvp`)
- Python 3.8+ with `numpy` and `matplotlib`:
  `pip install -r python/requirements.txt`

## Running the simulation

    cd verilog
    iverilog -o tb tb_comparison.v
    vvp tb > output.txt

Runs 5 seeds × 60 words of 32 bits (1920-bit numbers), comparing the parallel
chain (N = 15, 30, 60) against the sequential ripple reference.

## Cross-validation

    python ../python/cross_validate.py output.txt

Expected: `Total: 5/5 passed` (parallel result identical to ripple and to
Python big-integer addition).

## Reproducing the paper figures

    python python/figures.py

Generates `fig1.png` … `fig5.png` (decay of μ(F), empirical frontier
frequency, chain-length distribution, independent-nuclei fraction,
scalability).

## Results summary

- Parallel chain completes in 2–4 protocol cycles, independent of N.
- Ripple reference: N cycles (60 for N = 60).
- Results identical between parallel, ripple, and Python reference.
- No frontier chains of length ≥ 2 observed in 5×10⁵ samples for k ≥ 9.

## Citation

If you use this code in your research, please cite the companion manuscript:

> **"Local Carry Decision and Informational Irrelevance in Large-Base Positional Arithmetic"**
> Marlon Javier Muñoz Muñoz and Javier Fernando Botía Valderrama, 2026.
> Companion code: https://github.com/marlonmunozm-ui/carry-local-protocol

```bibtex
@misc{munoz2026carrylocal,
  author       = {Munoz, Marlon Javier and Bot\'{i}a Valderrama, Javier Fernando},
  title        = {Carry Local Protocol: parallel word-level carry protocol
                  for arbitrary-precision arithmetic},
  year         = {2026},
  publisher    = {GitHub},
  journal      = {GitHub repository},
  howpublished = {\url{https://github.com/marlonmunozm-ui/carry-local-protocol}},
  note         = {Companion code for the manuscript \textit{Local Carry
                  Decision and Informational Irrelevance in Large-Base
                  Positional Arithmetic} (Munoz and Bot\'{i}a Valderrama, 2026)}
}
