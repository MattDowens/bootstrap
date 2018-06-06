## Contents

* [SDPB](#sdpb)
* [Installation and Usage](#installation-and-usage)
* [Changelog](#changelog)
* [Attribution](#attribution)
* [Acknowledgements](#acknowledgements)
* [Works Using SDPB](#works-using-sdpb)

# SDPB

SDPB is an open-source, arbitrary-precision, parallelized semidefinite
program solver, designed for the conformal bootstrap. It solves the following problem:

![maximize:  b_0 + \sum_n b_n y_n over (y_1,...,y_N), such that: M_{0j}(x) + \sum_n y_n M_{nj}(x) is positive semidefinite for all x >= 0 and 1 <= j <= J, where each M_{nj}(x) is a polynomial matrix in x.](/docs/SDPB-PMP-Description.png?raw=true)

For more information, see [A Semidefinite Program Solver for the Conformal Bootstrap](http://arxiv.org/abs/1502.02033)
and [the manual](/docs/SDPB-Manual.pdf).

Author: David Simmons-Duffin (davidsd@gmail.com). As of February 2015, I am
supported by DOE grant number DE-SC0009988 and a William D. Loughlin Membership
at the [Institute for Advanced Study](http://sns.ias.edu).

## Installation and Usage

Installation instructions for Linux, Mac OS X, and Windows (using Cygwin)
 can be found in [Install.md](Install.md).

Type `sdpb --help` for the syntax and a list of options.

The input format for SDPB is XML-based and described in
[the manual](/docs/SDPB-Manual.pdf).
The Mathematica file `SDPB.m` includes code to export semidefinite
programs in this format, along with some examples. An example input
file `test.xml` is included with the source code.

Two python wrappers for SDPB are also available:

- [PyCFTBoot](https://github.com/cbehan/pycftboot) by Connor Behan ([arXiv:1602.02810](http://arxiv.org/abs/arXiv:1602.02810))
- [cboot](https://github.com/tohtsky/cboot) by Tomoki Ohtsuki ([arXiv:1602.07295](http://arxiv.org/abs/arXiv:1602.07295)).

## Attribution

If you use SDPB in work that results in publication, please cite

- D. Simmons-Duffin, "A Semidefinite Program Solver for the
  Conformal Bootstrap", [arXiv:1502.02033 \[hep-th\]](http://arxiv.org/abs/1502.02033).

Depending on how SDPB is used, the following other sources might be relevant:

The first use of semidefinite programming in the bootstrap:

- D. Poland, D. Simmons-Duffin and A. Vichi, "Carving Out the Space of
  4D CFTs," JHEP 1205, 110 (2012) [arXiv:1109.5176 \[hep-th\]](http://arxiv.org/abs/1109.5176).

The generalization of semidefinite programming methods to arbitrary
spacetime dimension:

- F. Kos, D. Poland and D. Simmons-Duffin, "Bootstrapping the O(N)
  Vector Models," JHEP 1406, 091 (2014) [arXiv:1307.6856 \[hep-th\]](http://arxiv.org/abs/1307.6856).

The generalization of semidefinite programming methods to arbitrary
systems of correlation functions:

- F. Kos, D. Poland and D. Simmons-Duffin, "Bootstrapping Mixed
  Correlators in the 3D Ising Model," [arXiv:1406.4858 \[hep-th\]](http://arxiv.org/abs/1406.4858).

## Acknowledgements

- SDPB Makes extensive use of [MPACK](http://mplapack.sourceforge.net/), the multiple precision linear algebra library written by Nakata Maho.  Several source files from MPACK are included in the SDPB source tree (see the license at the top of those files).

- SDPB uses Lee Thomason's [tinyxml2](http://www.grinninglizard.com/tinyxml2/) library (included in the source tree) for parsing.

- The design of SDPB was partially based on the solvers [SDPA](http://sdpa.sourceforge.net/) and SDPA-GMP, which were essential sources of inspiration and examples.

- Thanks to Filip Kos, David Poland, and Alessandro Vichi for collaboration in developing semidefinite programming methods for the conformal bootstrap and assistance testing SDPB.

- Thanks to Amir Ali Ahmadi, Hande Benson, Pablo Parrilo, and Robert Vanderbei for advice and discussions about semidefinite programming.

- Thanks also to Noah Stein, who first suggested the idea of semidefinite programming to me in [this Math Overflow question](http://mathoverflow.net/questions/33242/continuous-linear-programming-estimating-a-solution).

## Works Using SDPB

- D. Simmons-Duffin,
  "A Semidefinite Program Solver for the Conformal Bootstrap",
  [arXiv:1502.02033 [hep-th]](http://arxiv.org/abs/1502.02033).

- F. Kos, D. Poland, D. Simmons-Duffin and A. Vichi,
  "Bootstrapping the O(N) Archipelago,"
  [arXiv:1504.07997 [hep-th]](http://arxiv.org/abs/1504.07997).

- S. M. Chester, S. Giombi, L. V. Iliesiu, I. R. Klebanov, S. S. Pufu and R. Yacoby,
  "Accidental Symmetries and the Conformal Bootstrap,"
  [arXiv:1507.04424 [hep-th]](http://arxiv.org/abs/1507.04424).

- C. Beem, M. Lemos, L. Rastelli and B. C. van Rees,
  "The (2,0) superconformal bootstrap,"
  [arXiv:1507.05637 [hep-th]](http://arxiv.org/abs/1507.05637).

- L. Iliesiu, F. Kos, D. Poland, S. S. Pufu, D. Simmons-Duffin and R. Yacoby,
  "Bootstrapping 3D Fermions,"
  [arXiv:1508.00012 [hep-th]](http://arxiv.org/abs/1508.00012).

- D. Poland and A. Stergiou,
  "Exploring the Minimal 4D N=1 SCFT,"
  [arXiv:1509.06368 [hep-th]](http://arxiv.org/abs/1509.06368).

-  M. Lemos and P. Liendo,
  "Bootstrapping N=2 chiral correlators,"
  [arXiv:1510.03866 [hep-th]](http://arxiv.org/abs/1510.03866).

- Y. H. Lin, S. H. Shao, D. Simmons-Duffin, Y. Wang and X. Yin,
  "N=4 Superconformal Bootstrap of the K3 CFT,"
  [arXiv:1511.04065 [hep-th]](http://arxiv.org/abs/arXiv:1511.04065)

- S. M. Chester, L. V. Iliesiu, S. S. Pufu and R. Yacoby,
  "Bootstrapping O(N) Vector Models with Four Supercharges in 3 <= d <= 4,"
  [arXiv:1511.07552 [hep-th]](http://arxiv.org/abs/arXiv:1511.07552)

- S. M. Chester and S. S. Pufu,
  "Towards Bootstrapping QED_3,"
  [arXiv:1601.03476 [hep-th]](http://arxiv.org/abs/arXiv:1601.03476)

- C. Behan,
  "PyCFTBoot: A flexible interface for the conformal bootstrap,"
  [arXiv:1602.02810 [hep-th]](http://arxiv.org/abs/arXiv:1602.02810)

- Y. Nakayama and T. Ohtsuki,
  "Conformal Bootstrap Dashing Hopes of Emergent Symmetry,"
  [arXiv:1602.07295 [cond-mat.str-el]](http://arxiv.org/abs/arXiv:1602.07295)

- H. Iha, H. Makino and H. Suzuki,
  "Upper bound on the mass anomalous dimension in many-flavor gauge theories -- a conformal bootstrap approach"
  [arXiv:1603.01995 [hep-th]](http://arxiv.org/abs/1603.01995)

- F. Kos, D. Poland, D. Simmons-Duffin, and A. Vichi,
  "Precision Islands in the Ising and O(N) Models"
  [arXiv:1603.04436 [hep-th]](http://arxiv.org/abs/1603.04436)

- Z. Komargodski and D. Simmons-Duffin,
  "The Random-Bond Ising Model in 2.01 and 3 Dimensions"
  [arXiv:1603.04444 [hep-th]](http://arxiv.org/abs/1603.04444)

- Y. Nakayama,
  "Bootstrap bound for conformal multi-flavor QCD on lattice"
  [arXiv:1605.04052 [hep-th]](https://arxiv.org/abs/1605.04052)

- M. Paulos, J. Penedones, J. Toledo, B. van Rees, P. Vieira,
  "The S-matrix Bootstrap I: QFT in AdS"
  [arXiv:1607.06109 [hep-th]](http://arxiv.org/abs/1607.06109)

- Z. Li, N. Su,
  "Bootstrapping Mixed Correlators in the Five Dimensional Critical O(N) Models"
  [arXiv:1607.07077 [hep-th]](https://arxiv.org/abs/1607.07077)

- S. Collier, Y.H. Lin, X. Yin,
  "Modular Bootstrap Revisited"
  [arXiv:1608.06241 [hep-th]](https://arxiv.org/abs/1608.06241)

- Y. Pang, J. Rong, N. Su,
  "φ3  theory with F4 flavor symmetry in 6−2ε dimensions: 3-loop renormalization and conformal bootstrap"
  [arXiv:1609.03007 [hep-th]](https://arxiv.org/abs/1609.03007)

- Y.H. Lin, S.H. Shao, Y. Wang, X. Yin,
  "(2,2) Superconformal Bootstrap in Two Dimensions"
  [arXiv:1610.05371 [hep-th]](https://arxiv.org/abs/1610.05371)
  
- J.B. Bae, K. Lee, S. Lee,
  "Bootstrapping Pure Quantum Gravity in AdS3"
  [arXiv:1610.05814 [hep-th]](https://arxiv.org/abs/1610.05814)

- J.B. Bae, D. Gang, J. Lee,
  "3d N=2 minimal SCFTs from Wrapped M5-branes"
  [arXiv:1610.09259 [hep-th]](https://arxiv.org/abs/1610.09259)

- C. Beem, L. Rastelli, B. C. van Rees,
  "More N=4 superconformal bootstrap"
  [arXiv:1612.02363 [hep-th]](https://arxiv.org/abs/1612.02363)

- M. Lemos, P. Liendo, C. Meneghelli, V. Mitev,
  "Bootstrapping N=3 superconformal theories"
  [arXiv:1612.01536 [hep-th]](https://arxiv.org/abs/1612.01536)

- D. Simmons-Duffin,
  "The Lightcone Bootstrap and the Spectrum of the 3d Ising CFT"
  [arXiv:1612.08471 [hep-th]](https://arxiv.org/abs/1612.08471)

- D. Li, D. Meltzer, A. Stergiou,
  "Bootstrapping Mixed Correlators in 4D N=1 SCFTs"
  [arXiv:1702.00404 [hep-th]](https://arxiv.org/abs/1702.00404)
  
- S. Collier, P. Kravchuk, Y.-H. Lin, X. Yin,
  "Bootstrapping the Spectral Function: On the Uniqueness of Liouville and the Universality of BTZ"
  [arXiv:1702.00423 [hep-th]](https://arxiv.org/abs/1702.00423)
  
- M. Cornagliotto, M. Lemos, V. Schomerus,
  "Long Multiplet Bootstrap"
  [arXiv:1702.05101 [hep-th]](https://arxiv.org/abs/1702.05101)

- Y. Nakayama,
  "Bootstrap experiments on higher dimensional CFTs"
  [arXiv:1705.02744 [hep-th]](https://arxiv.org/abs/1705.02744)

- L. Iliesiu, F. Kos, D. Poland, S. S. Pufu, D. Simmons-Duffin,
  "Bootstrapping 3D Fermions with Global Symmetries"
  [arXiv:1705.03484 [hep-th]](https://arxiv.org/abs/1705.03484)

- A. Dymarsky, J. Penedones, E. Trevisani, A. Vichi,
  "Charting the space of 3D CFTs with a continuous global symmetry"
  [arXiv:1705.04278 [hep-th]](https://arxiv.org/abs/1705.04278)

- C.-M. Chang, Y.-H. Lin,
  "Carving Out the End of the World or (Superconformal Bootstrap in Six Dimensions)"
  [arXiv:1705.05392 [hep-th]](https://arxiv.org/abs/1705.05392)

- M. Cho, S. Collier, X. Yin,
  "Genus Two Modular Bootstrap"
  [arXiv:1705.05865 [hep-th]](https://arxiv.org/abs/1705.05865)
  
- A. Dymarsky, F. Kos, P. Kravchuk, D. Poland, D. Simmons-Duffin,
  "The 3d Stress-Tensor Bootstrap"
  [arXiv:1708.05718 [hep-th]](https://arxiv.org/abs/1708.05718)

- M. F. Paulos, J. Penedones, J. Toledo, B. C. van Rees, P. Vieira,
  "The S-matrix Bootstrap III: Higher Dimensional Amplitudes"
  [arXiv:1708.06765 [hep-th]](https://arxiv.org/abs/1708.06765)
  
- J.-B. Bae, S. Lee, J. Song,
  "Modular Constraints on Conformal Field Theories with Currents"
  [arXiv:1708.08815 [hep-th]](https://arxiv.org/abs/1708.08815)

(Please let me know if you would like your paper to be included in this list!)
