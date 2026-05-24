import numpy as np
import matplotlib.pyplot as plt
import qutip as qt
import qutip_qtrl.pulseoptim as cpo

def run_oct_simulation():
    print("---Phase 1: Running Quantum Optimal Control (GRAPE)---")

    #1. System setup (Two level molecular transition)
    #H0 is the molecular Hamiltonian on resonance in the rotating frame (0)
    H0 = qt.Qobj(np.zeros((2,2)))
    #The laser couples via Pauli-X operator to drive the transition
    H_control = qt.sigmax()

    #2. Define initial and target state
    U_initial = qt.basis(2,0) #Ground State
    U_target = qt.basis(2,1) #Excited State

    #3. Discretized time grid for the pulse
    n_steps = 100 #slice the pulse into 100 constant steps
    evo_time = 3.0 #Total pulse duration (e,h., 3 picoseconds)

    #4. Optimization Targets
    fid_err_targ = 1e-5 #Stop when target accuracy is 99.999%
    max_iter = 200 #Safety limit for iterations

    #5. Run the GRAPE Optimization loop
    result = cpo.optimize_pulse_unitary(H0,[H_control],U_initial,U_target,n_steps,evo_time,fid_err_targ=fid_err_targ,max_iter=max_iter,init_pulse_type="SINE", gen_stats=True)

    print(f"\nOptimization Finished!")
    print(f"Final Success Fidelity: {1.0-result.fid_err:.5f}")

    #6. Extract the Optimized Pulse Shape
    optimized_pulse = result.final_amps[:,0]
    time_grid = result.time

    #7. Step 2: Track Quantum trajectory 
    #We take the calculated pulse and feed it into our standard time-solver to find how
    #the population actually shifted at every step
    #We construct a time-dependant Hamiltonian array: [H0,[H_control, pulse_amplitudes]]
    H_dynamic = [H0,[H_control,optimized_pulse]]

    #Solve the Master Equation to track state population (via Pauli-Z)
    times_for_solver=time_grid[:-1] #Match dimensions for piecewise amplitudes
    trajectory = qt.mesolve(H_dynamic,U_initial,times_for_solver,[],[qt.sigmaz()])

    #8. Visualization: Side by Side subplots
    fig, (ax1,ax2)=plt.subplots(1,2,figsize=(13,5))

    #Left Plot: The Control Variable (The laser pulse shape)
    ax1.step(time_grid[:-1],optimized_pulse,where='post',color='crimson',linewidth=2)
    ax1.set_title("GRAPE Optimized Control Variable $\Omega(t)$",fontsize=12)
    ax1.set_xlabel("Time(ps)",fontsize=11)
    ax1.set_ylabel("Laser Amplitude/Rabi Frequency (a.u.)",fontsize=11)
    ax1.grid(True,alpha=0.3)

    #Right Plot: The System State (Population Inversion Tracking)
    ax2.plot(times_for_solver,trajectory.expect[0],color='darkblue',linewidth=2,label=r"$\langle\sigma_z\rangle$")
    ax2.axhline(-1,color='green',linestyle=':',label=r"Target state $|1\rangle$")
    ax2.set_title("Quantum State Trajectory",fontsize=11)
    ax2.set_xlabel("Time (ps)",fontsize=11)
    ax2.set_ylabel("Population Inversion (Ground vs Excited)",fontsize=11)
    ax2.grid(True,alpha=0.3)
    ax2.legend()

    plt.tight_layout()
    plt.show()

if __name__=="__main__":
    run_oct_simulation()