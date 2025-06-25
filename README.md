# Qiskit Hackaton - LamaLab project

![lama_logo](https://github.com/giorgiostucchi/QiskitMunich/blob/main/logo.pdf)

This project realizes a three-staged enhancement of qiskit standard transpilation of quantum circuits. The stages act, respectively, at the pre-transpilation, transpilation, and post-transpilation level.

---

## What’s inside?

```
.
├── assembled.ipynb   # ← the star of the show
├── LICENSE             # license inherited from the original author
├── README.md           # you’re reading it
├── my_ddd.py           # libraries
├── my_lib.py
├── my_rem.py
├── logo.pdf            # advertise us!
└── zxpass              # functions from https://github.com/dlyongemallo/qiskit-zx-transpiler
```

---

## Local setup

```bash
git clone https://github.com/giorgiostucchi/QiskitMunich/tree/main

```

---

## Dependencies

```
numpy
qiskit
qiskit-ibm-runtime (with IBM account)
```


---

## Acknowledgements

Big thanks to the QISKIT hackaton organizers!

We adapted and took some code from [dlyongemallo](https://github.com/dlyongemallo/qiskit-zx-transpiler) and [ZX Calculus Projects](https://github.com/Quantomatic/pyzx/blob/master/circuits/Fast/mod5_4_before), which should be mentioned when referncing the current repository.

---
