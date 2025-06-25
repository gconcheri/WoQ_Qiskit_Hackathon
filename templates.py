## class for quantum circuit manipulation and simplification using templates matching
import re 
import numpy as np
from qiskit.qasm2 import dumps
from qiskit import QuantumCircuit
import matplotlib.pyplot as plt
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.quantum_info import SparsePauliOp
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import EstimatorV2 as Estimator



def find_3_2(qc_list):
    result = []
    new_temp = []
    N = len(qc_list)

    for n in range(N):
        skip_n = False
        qc_1 = qc_list[n]
        if qc_1[0] == "cx":
            j1 = qc_1[1]
            k1 = qc_1[2]

            for m in range(n + 1, N):
                qc_2 = qc_list[m]
                if qc_2[0] == "cx" and j1 not in qc_2 and k1 == qc_2[2]:
                    i2 = qc_2[1]

                    for l in range(m + 1, N):
                        qc_3 = qc_list[l]
                        if qc_3[0] == "cx" and i2 == qc_3[1] and j1 == qc_3[2]:
                            result.append([n, m, l])
                            new_temp.append(['cx', i2, j1])
                            new_temp.append(['cx', j1, k1])
                        elif i2 in qc_3 or j1 in qc_3:
                            skip_n = True
                            break
                        else: pass
                    if skip_n: break
                        
                elif j1 in qc_2 or k1 in qc_2:
                    break

                else: pass
            
    result = filter_triplets(result)

    return result, new_temp

def find_4_2(qc_list):
    result = []
    new_temp = []
    N = len(qc_list)

    for n in range(N):
        skip_n = False
        qc_1 = qc_list[n]
        if qc_1[0] == "ccx":
            i1 = qc_1[1]
            j1 = qc_1[2]
            k1 = qc_1[3]

            for m in range(n + 1, N):
                qc_2 = qc_list[m]
                if qc_2[0] == "cx" and i1 in qc_2[1:3] and j1 in qc_2[1:3]:

                    for l in range(m + 1, N):
                        qc_3 = qc_list[l]
                        if qc_3[0] == "ccx" and i1 in qc_3[1:3] and j1 in qc_3[1:3] and k1 == qc_3[3]:
                            result.append([n, m, l])
                            if i1 == qc_2[1]:
                                new_temp.append(['cx', i1, j1])
                                new_temp.append(['cx', i1, k1])
                            else:
                                new_temp.append(['cx', j1, i1])
                                new_temp.append(['cx', j1, k1])
                        elif i1 in qc_3 or j1 in qc_3 or k1 in qc_3:
                            skip_n = True
                            break
                        else: pass
                    if skip_n: break
                        
                elif i1 in qc_2 or j1 in qc_2 or k1 in qc_2:
                    break

                else: pass

    result = filter_triplets(result)
            
    return result, new_temp

def find_4_3(qc_list):
    result = []
    new_temp = []
    N = len(qc_list)

    for n in range(N):
        skip_n = False
        qc_1 = qc_list[n]
        if qc_1[0] == "ccx":
            i1 = qc_1[1]
            j1 = qc_1[2]
            k1 = qc_1[3]

            for m in range(n + 1, N):
                qc_2 = qc_list[m]
                if qc_2[0] == "x" and (i1 == qc_2[1] or j1 == qc_2[1]):

                    for l in range(m + 1, N):
                        qc_3 = qc_list[l]
                        if qc_3[0] == "ccx" and i1 == qc_3[1] and j1 == qc_3[2] and k1 == qc_3[3]:
                            result.append([n, m, l])
                            if i1 == qc_2[1]:
                                new_temp.append(['x', i1])
                                new_temp.append(['cx', j1, k1])
                            else:
                                new_temp.append(['x', j1])
                                new_temp.append(['cx', i1, k1])
                        elif i1 in qc_3 or j1 in qc_3 or k1 in qc_3:
                            skip_n = True
                            break
                        else: pass
                    if skip_n: break
                        
                elif i1 in qc_2 or j1 in qc_2 or k1 in qc_2:
                    break

                else: pass

    result = filter_triplets(result)
    
    return result, new_temp

    
def matching_template(circuit):
    qc_string = dumps(circuit)
    qc_list, num_qubit = string_to_list(qc_string)
    triplette1, new_temp1 = find_4_2(qc_list)
    circuit = list_to_circuit(triplette1, qc_list, new_temp1, num_qubit)

    qc_string = dumps(circuit)
    qc_list, num_qubit = string_to_list(qc_string)
    triplette2, new_temp2 = find_4_3(qc_list)
    circuit = list_to_circuit(triplette2, qc_list, new_temp2, num_qubit)

    qc_string = dumps(circuit)
    qc_list, num_qubit = string_to_list(qc_string)
    triplette3, new_temp3 = find_3_2(qc_list)
    circuit = list_to_circuit(triplette3, qc_list, new_temp3, num_qubit)

    return circuit

def filter_triplets(triplets):
    filtered = []
    prev_triplet = None
    for triplet in triplets:
        if prev_triplet is not None:
            # Controlla se c'è almeno un elemento in comune
            if set(triplet) & set(prev_triplet):
                continue  # Salta questa tripla, c'è sovrapposizione
        filtered.append(triplet)
        prev_triplet = triplet
    return filtered

def list_to_circuit(triplette, qc_list, new_temp, num_qubit):
    #list of type [[3,4,6], [7,8,9]]

    idx = 0
    for ot_indeces in triplette:
        qc_list[ot_indeces[0]] = new_temp[idx]
        qc_list[ot_indeces[1]] = new_temp[idx+1]
        qc_list[ot_indeces[2]] = []
        idx += 2

    # Remove empty lists
    qc_list = [item for item in qc_list if item]
    qc_string = list_to_string(qc_list, int(num_qubit))
    new_qc = QuantumCircuit.from_qasm_str(qc_string)
    return new_qc

def list_to_string(qc_list, num_qubit):
    lines = [
        "OPENQASM 2.0;",
        'include "qelib1.inc";',
        f"qreg q[{num_qubit}];"
    ]
    for item in qc_list:
        label = item[0]
        qubits = ",".join([f"q[{n}]" for n in item[1:]])
        lines.append(f"{label} {qubits};")
    return "\n".join(lines)

def string_to_list(string):
    third_line = string.splitlines()[2]
    num_qubit = third_line.split('[')[1].split(']')[0]

    lines = string.splitlines()[3:]  # Skip first three lines
    result = []
    # label_pattern = re.compile(r'^(\w+)\s*((?:q\[\d+\],?\s*)+);?$')
    label_pattern = re.compile(r'^(\w+(?:\([^)]+\))?)\s*((?:q\[\d+\],?\s*)+);?$')
    number_pattern = re.compile(r'q\[(\d+)\]')
    for line in lines:
        line = line.strip()
        if not line:
            continue
        match = label_pattern.match(line)
        if match:
            label = match.group(1)
            numbers = [int(n) for n in number_pattern.findall(match.group(2))]
            result.append([label] + numbers)
    return result, num_qubit

def plot_circuitdepth(namefakeprovider, qc, title):
   import qiskit_ibm_runtime.fake_provider as fake_provider
   fakeprov_class = getattr(fake_provider, namefakeprovider)
   backend = fakeprov_class()
   import time


   times = []
   depths = []
   ### WRITE YOUR CODE HERE ###
   # Sweep over different optimization levels
   optimization_levels = [0,1,2,3]
   for level in optimization_levels:
       pm = generate_preset_pass_manager(backend = backend, optimization_level=level, layout_method= "dense")
       ### YOUR CODE FINISHES HERE ###
       print('\033[1m' + f'Optimization level: {level}')
       start = time.time()
       isa_qc = pm.run(qc)
       dt = time.time() - start
       times.append(dt)
       depth = isa_qc.depth()
       depths.append(depth)


       print('Transpilation time (sec.):', dt)
       print('Circuit depth:', depth)
       print('---' * 50)


   # Plotting
   plt.figure(figsize=(10, 5))
   plt.suptitle(title, fontsize=16, fontweight='bold')

   plt.subplot(1, 2, 1)
   plt.bar([str(lvl) for lvl in optimization_levels], times, color='skyblue')
   plt.title('Transpilation Time')
   plt.xlabel('Optimization Level')
   plt.ylabel('Time (sec.)')


   plt.subplot(1, 2, 2)
   plt.bar([str(lvl) for lvl in optimization_levels], depths, color='salmon')
   plt.title('Circuit Depth')


def create_operatorstring(qubit_num):
    # ZZII...II, ZIZI...II, ... , ZIII...IZ
    n = int(qubit_num)  # Number of qubits

    operator_strings_Z = ["Z" + i * "I" + "Z" + "I" * (n - i - 2) for i in range(n - 1)]

    operators = [SparsePauliOp(operator) for operator in operator_strings_Z]

    return operators


def expectation_values(operators, namefakeprovider, qc, qc_reduced, num_qubit):

    import qiskit_ibm_runtime.fake_provider as fake_provider
    fakeprov_class = getattr(fake_provider, namefakeprovider)
    backend = fakeprov_class()

    # Create an Estimator instance
    estimator = Estimator(mode=backend)
    estimator.options.resilience_level = 1
    estimator.options.default_shots = 5000

    pm = generate_preset_pass_manager(backend=backend, optimization_level=2)
    isa_circuit = pm.run(qc) 

    isa_operators_list = [operator.apply_layout(isa_circuit.layout) for operator in operators]
    # Submit the circuit to Estimator
    job_1_err = estimator.run([(isa_circuit, isa_operators_list)])
    job_id1 = job_1_err.job_id()

    # data
    data = list(range(1, len(operators) + 1))  # Distance between the Z operators
    result_1_err = job_1_err.result()[0]
    values_1_err = result_1_err.data.evs  # Expectation value at each Z operator.
    values_1_err = [
        np.abs(v / values_1_err[0]) for v in values_1_err
    ]  # Normalize the expectation values to evaluate how they decay with distance.    

    pm = generate_preset_pass_manager(backend=backend, optimization_level=2)
    isa_circuit = pm.run(qc_reduced) 

    # Submit the circuit to Estimator
    job_2_err = estimator.run([(isa_circuit, isa_operators_list)])
    job_id_2= job_2_err.job_id()

    # data
    result_2_err = job_2_err.result()[0]
    values_2_err = result_2_err.data.evs  # Expectation value at each Z operator.
    values_2_err = [
        np.abs(v / values_2_err[0]) for v in values_2_err
    ]  # Normalize the expectation values to evaluate how they decay with distance.


    # Create a local simulator backend
    backend = AerSimulator()

    # Create an Estimator instance
    estimator = Estimator(mode=backend)
    estimator.options.resilience_level = 1
    estimator.options.default_shots = 5000

    pm = generate_preset_pass_manager(backend=backend, optimization_level=2)
    isa_circuit = pm.run(qc) 

    isa_operators_list = [operator.apply_layout(isa_circuit.layout) for operator in operators]
    # Submit the circuit to Estimator
    job_1 = estimator.run([(isa_circuit, isa_operators_list)])
    job_id1 = job_1.job_id()

    # data
    data = list(range(1, len(operators) + 1))  # Distance between the Z operators
    result_1 = job_1.result()[0]
    values_1 = result_1.data.evs  # Expectation value at each Z operator.
    values_1 = [
        np.abs(v / values_1[0]) for v in values_1
    ]  # Normalize the expectation values to evaluate how they decay with distance.

    pm = generate_preset_pass_manager(backend=backend, optimization_level=2)

    isa_circuit = pm.run(qc_reduced) 
    isa_operators_list = [operator.apply_layout(isa_circuit.layout) for operator in operators]
    # Submit the circuit to Estimator
    job_2 = estimator.run([(isa_circuit, isa_operators_list)])
    job_id_2 = job_2.job_id()

    # data
    result_2 = job_2.result()[0]
    values_2 = result_2.data.evs  # Expectation value at each Z operator.
    values_2 = [
        np.abs(v / values_2[0]) for v in values_2
    ]  # Normalize the expectation values to evaluate how they decay with distance.

    n = int(num_qubit)  # Number of qubits in the circuit

    # plotting graph
    plt.plot(data, values_1, marker="o", label=f"{n}-qubit naive circuit, no errors")
    plt.plot(data, values_2, marker="o", label=f"{n}-qubit reduced circuit, no errors")
    plt.plot(data, values_1_err, marker="o", label=f"{n}-qubit naive circuit, errors")
    plt.plot(data, values_2_err, marker="o", label=f"{n}-qubit reduced circuit, errors")
    plt.xlabel("Distance between qubits $i$")
    plt.ylabel(r"$\langle Z_i Z_0 \rangle / \langle Z_1 Z_0 \rangle $")
    plt.title(f"Expectation values for {n}-qubit circuit")
    plt.legend()
    plt.show()


