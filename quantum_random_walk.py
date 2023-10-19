from qiskit import *
from qiskit.circuit import QuantumCircuit
from qiskit.circuit.library.standard_gates import XGate
import numpy as np
import csv
import matplotlib.pyplot as plt
from qiskit.extensions import UnitaryGate
from qiskit.quantum_info.operators import Operator

def binToData(dict, n, data):
    shift_val = 0
    for key in dict.keys():
        val = int(key[::-1],2)
        if val > 2 ** (n - 1):
            shift_val = val - 2 ** (n)
        else:
            shift_val = val
        
        # key = shift_val
        data[shift_val + (2 ** (n-1) -1)] = dict[key]

def Y():
    matrix = np.array(
            [
                [1/np.sqrt(2),1.j/np.sqrt(2)],
                [1.j/np.sqrt(2),1/np.sqrt(2)]
            ],
            dtype = complex
        )
    return UnitaryGate(Operator(matrix), label = 'Y')

class QuantumRandomWalk:
    def __init__(self,steps,size):
        self.steps=steps
        self.size=size # size does NOT include coin
    
    
    def addGate(self):
        circuit = QuantumCircuit(self.size, name="Add.")

        for i in np.arange(self.size-1,0,-1):
            circuit.append(XGate().control(int(i)),\
                            list(np.arange(self.size-1,self.size - (i+2),-1)))

        circuit.x([self.size-1])

        add_gate = circuit.to_gate()

        return add_gate

    def subGate(self):
        circuit = QuantumCircuit(self.size, name="Sub.")
        
        circuit.x([self.size-1])
        
        for i in np.arange(1,self.size):
            circuit.append(XGate().control(int(i)),\
                            list(np.arange(self.size-1,self.size - (i+2),-1)))

        sub_gate = circuit.to_gate()

        return sub_gate
    
    def ctrlAddGate(self):
        return self.addGate().control(1)
    
    def ctrlSubGate(self):
        return self.subGate().control(1,None,'0')
    
    def shiftGate(self, name):        
        qc=QuantumCircuit(1+self.size,name="Step {}".format(name))
        
        qc.h(0)
        qc.append(self.ctrlAddGate(),[i for i in range(1+self.size)])
        qc.append(self.ctrlSubGate(),[i for i in range(1+self.size)])
        
        shift_gate = qc.to_gate()
        
        return shift_gate
    
    def walkCircuit(self):        
        qc=QuantumCircuit(1+self.size,name="QRW")
        for step in range(self.steps):
            qc.append(self.shiftGate(name=step+1),[i for i in range(1+self.size)])
        
        return qc
    
    def walkData(self):
        qc=QuantumCircuit(1+self.size,self.size,name="Sim")

        qc.append(self.walkCircuit(),[i for i in range(1+self.size)])

        qc.measure(range(1,self.size+1),range(self.size))
        
        backend_sim = Aer.get_backend('qasm_simulator')

        job_sim = backend_sim.run(transpile(qc, backend_sim), shots=1024)

        result_sim = job_sim.result()
        counts = result_sim.get_counts(qc)

        pos_data = [i for i in range(- 2 ** (self.size - 1) + 1, 2 ** (self.size - 1))]
        freq_data = [0 for i in range(2 ** self.size - 1)]

        binToData(counts, self.size, freq_data)

        return pos_data, freq_data
    
    def walkPlot(self):
        return plt.plot(self.walkData()[0], self.walkData()[1])
    
    def exportToCSV(self, name='quantum_randomwalk_data'):
        data = [(a, x, y) for a, (x, y) in enumerate(zip(self.walkData()[0], self.walkData()[1]))]

        file = "{}.csv".format(name)

        with open(file, mode="w", newline="") as f:
            writer = csv.writer(f)

            writer.writerow(["a", "pos_x", "freq_y"])

            writer.writerows(data)

        return "Data saved to {}".format(file)
