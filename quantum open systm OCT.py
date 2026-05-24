import numpy as np
import matplotlib.pyplot as plt
import qutip as qt
from scipy.optimize import minimize

def run_open_system_oct():
    print("---Running Open Quantum System OCT (Lindblad + Scipy)--- ")

    #1. System setup (Two-level Molecular Transition)
    H0 = qt.Qobj(np.zeros((2,2))) #Resonant drift Hamiltonian
    H_control = qt.sigmax() #Control Hamiltonian (Laser dipole coupling)

    #2. Environmental pure dephasing channel (Lindblad noise)
    gamma_phi = 0.3 #Dephasing rate
    c_ops = [np.sqrt(gamma_phi)*qt.sigmaz()]

    #3. Boundary Conditions as density matrices (rho)
    initial_rho = qt.fock_dm(2,0) #Ground state density matrix |0><0|
    target_rho = qt.fock_dm(2,1) #Target excited state density matrix |1><1|

    #4. Parameters (shorter time to let the pulse outrun dephasing time)
    n_steps = 40 #Number of time slices
    evo_time = 0.8 #Total time in ps (shortened to beat noise)
    times = np.linspace(0, evo_time,n_steps)
    init_amps = 3.0*np.sin(np.pi*times/evo_time) #Initial guess for the control pulse

    #5. Define the objective function (Infidelity to minimize)
    def objective_function(amps):
        H_dynamic = [H0,[H_control,amps]] #time-dependant Hamiltonian with piecewise amplitudes
        #Evolve the full mixed state using the Lindbland Master Equation
        result = qt.mesolve(H_dynamic,initial_rho,times,c_ops,[])
        final_rho = result.states[-1]
        #Target state is pure, so fidelity is simply: Tr(target_rho*final_rho)
        fidality = (target_rho*final_rho).tr().real
        return 1.0 - fidality
    
    #6. Run the optimization loop (BFGS gradient-style minimization)
    print("Optimizing pulse envolope fields...")
    opt_result = minimize(objective_function,init_amps,method='BFGS',options={'maxiter':50,'disp':True})

    optimized_pulse = opt_result.x    
    print(f"\nOptimization Finished!")
    print(f"Final Lindblad Infidelity Error:{opt_result.fun:.5f}")

    #7. Generate Final Trajectory for plotting
    H_final_dynamic = [H0,[H_control,optimized_pulse]]
    trajectory = qt.mesolve(H_final_dynamic,initial_rho,times,c_ops,[qt.sigmaz()])

    #Visiualization
    fig, (ax1,ax2)=plt.subplots(1,2,figsize=(13,5))

    #Left plot: Laser control amplitude
    ax1.step(times,optimized_pulse,where='mid',color='crimson',linewidth=2)
    ax1.set_title(r"Open System Optimized Control Pulse $\Omega(t)$",fontsize=11)
    ax1.set_xlabel("Time (ps)",fontsize=11)
    ax1.set_ylabel("Laser Amplitude (a.u.)",fontsize=11)
    ax1.grid(True,alpha=0.3)

    #Right Plot: Population Inversion Tracking
    ax2.plot(times,trajectory.expect[0],color='darkblue',linewidth=2,label=r'$\langle\sigma_z\rangle$')
    ax2.axhline(-1,color='green',linestyle=':',label=r'Target State $|1\rangle$')
    ax2.set_title(r"Open Quantum System Trajectory ($\rho_{00}-\rho_{11})$",fontsize=11)
    ax2.set_xlabel("Time(ps)",fontsize=11)
    ax2.set_ylabel("Population Inversion",fontsize=11)
    ax2.grid(True,alpha=0.3)
    ax2.legend()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_open_system_oct()