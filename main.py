import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, messagebox, ttk, Frame, Label, Button, Entry

def calcular():
    try:
        # Get tensor values from entry fields
        sigmaxx = float(entry_sigmaxx.get() or 0)
        sigmaxy = float(entry_sigmaxy.get() or 0)
        sigmaxz = float(entry_sigmaxz.get() or 0)
        sigmayy = float(entry_sigmayy.get() or 0)
        sigmayz = float(entry_sigmayz.get() or 0)
        sigmazz = float(entry_sigmazz.get() or 0)
        sigmac = float(entry_sigmac.get() or 0)

        # stress tensor matrix
        tensor = np.array([
            [sigmaxx, sigmaxy, sigmaxz],
            [sigmaxy, sigmayy, sigmayz],
            [sigmaxz, sigmayz, sigmazz]
        ])

        # invariants
        J1 = np.trace(tensor)  
        J2 = 0.5 * ((J1 ** 2) - np.sum(tensor ** 2))
        J3 = np.linalg.det(tensor)

        # eigenvalues (principal stresses)
        eigvals, eigvecs = np.linalg.eig(tensor)
        
        principais = sorted(eigvals, reverse=True)  

        sigma1, sigma2, sigma3 = principais[0], principais[1], principais[2]

        # Tresca and Von Mises criteria
        sigmaT = (sigma1 - sigma3) / 2
        critT = sigmac / 2

        sigmaVM = np.sqrt(((sigma1 - sigma2) ** 2 + (sigma2 - sigma3) ** 2 + (sigma1 - sigma3) ** 2) / 2)
        critVM = sigmac

        result_text = f"σ1: {sigma1:.2f} MPa\nσ2: {sigma2:.2f} MPa\nσ3: {sigma3:.2f} MPa"
        
        # Tresca result
        tresca_result = "✅ (OK)" if sigmaT < critT else "❌ (Exceeds)"
        result_text += f"\n\nTresca: σ_eq = {sigmaT:.2f} MPa | {tresca_result} (Critical = {critT:.2f} MPa)"

        # Von Mises result
        vonMises_result = "✅ (OK)" if sigmaVM < critVM else "❌ (Exceeds)"
        result_text += f"\n\nVon Mises: σ_eq = {sigmaVM:.2f} MPa | {vonMises_result} (Critical = {critVM:.2f} MPa)"

        result_label.config(text=result_text)

        plot_mohrs_circle_3d(sigma1, sigma2, sigma3, sigmac)

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for all fields.")




def plot_mohrs_circle_3d(sigma1, sigma2, sigma3, sigma_critical):

    tau_max_12 = abs(sigma1 - sigma2) / 2
    tau_max_23 = abs(sigma2 - sigma3) / 2
    tau_max_31 = abs(sigma3 - sigma1) / 2

    sigma_vm = np.sqrt(((sigma1 - sigma2)**2 + sigma1**2 + sigma2**2) / 2)

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect('equal')
    
    ax.set_xlim(min(sigma1, sigma2, sigma3) - 10, max(sigma1, sigma2, sigma3) + 10)
    ax.set_ylim(-max(tau_max_12, tau_max_23, tau_max_31) - 10, max(tau_max_12, tau_max_23, tau_max_31) + 10)

    # Circle 1 (σ1, σ2)
    center1 = (sigma1 + sigma2) / 2
    radius1 = abs(sigma1 - sigma2) / 2
    circle1 = plt.Circle((center1, 0), radius1, color='b', fill=False, linestyle='--', label="σ1 - σ2")
    ax.add_artist(circle1)

    # Circle 2 (σ2, σ3)
    center2 = (sigma2 + sigma3) / 2
    radius2 = abs(sigma2 - sigma3) / 2
    circle2 = plt.Circle((center2, 0), radius2, color='g', fill=False, linestyle='--', label="σ2 - σ3")
    ax.add_artist(circle2)

    # Circle 3 (σ3, σ1)
    center3 = (sigma3 + sigma1) / 2
    radius3 = abs(sigma3 - sigma1) / 2
    circle3 = plt.Circle((center3, 0), radius3, color='r', fill=False, linestyle='--', label="σ3 - σ1")
    ax.add_artist(circle3)

    # Plot the principal stresses (normal stress) as points on the x-axis (edges of each circle)
    ax.plot([sigma1, sigma2, sigma3], [0, 0, 0], 'ro', label="Principal Stresses (σ1, σ2, σ3)")

    ax.annotate(f'σ1 = {sigma1:.2f}', (sigma1, 0), textcoords="offset points", xytext=(0, 10), ha='center')
    ax.annotate(f'σ2 = {sigma2:.2f}', (sigma2, 0), textcoords="offset points", xytext=(0, 10), ha='center')
    ax.annotate(f'σ3 = {sigma3:.2f}', (sigma3, 0), textcoords="offset points", xytext=(0, 10), ha='center')

    # Plot shear stress points at maximum shear stress
    ax.plot([center1, center2, center3], [tau_max_12, tau_max_23, tau_max_31], 'bo', label="Max Shear Stresses (τ_max)")

    ax.annotate(f'τ12 = {tau_max_12:.2f}', (center1, tau_max_12), textcoords="offset points", xytext=(0, 10), ha='center')
    ax.annotate(f'τ23 = {tau_max_23:.2f}', (center2, tau_max_23), textcoords="offset points", xytext=(0, 10), ha='center')
    ax.annotate(f'τ31 = {tau_max_31:.2f}', (center3, tau_max_31), textcoords="offset points", xytext=(0, 10), ha='center')


    # Plot the Tresca criterion line 
    ax.axhline(sigma_critical / 2, color='orange', linestyle='--', label=f"Tresca Criterion: τ_max = {sigma_critical / 2:.2f}")


    ax.set_title("Mohr's Circle for 3D Stress with Von Mises and Tresca Criteria")
    ax.set_xlabel("Normal Stress (MPa)")
    ax.set_ylabel("Shear Stress (MPa)")
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)

    ax.legend(loc='best') 
    plt.grid(True)
    plt.show()


# Main window
root = Tk()
root.title("Plasticity Criteria")
root.geometry("600x700")
root.configure(bg="#2e2e2e")
style = ttk.Style()
style.configure("TLabel", foreground="white", background="#2e2e2e", font=("Helvetica", 12))
style.configure("TButton", font=("Helvetica", 12), padding=10)
style.configure("TEntry", padding=10)

input_frame = Frame(root, bg="#2e2e2e")
input_frame.pack(pady=20)

ttk.Label(input_frame, text="σxx", style="TLabel").grid(row=0, column=0, padx=10, pady=10)
entry_sigmaxx = ttk.Entry(input_frame)
entry_sigmaxx.grid(row=0, column=1)

ttk.Label(input_frame, text="σxy", style="TLabel").grid(row=1, column=0, padx=10, pady=10)
entry_sigmaxy = ttk.Entry(input_frame)
entry_sigmaxy.grid(row=1, column=1)

ttk.Label(input_frame, text="σxz", style="TLabel").grid(row=2, column=0, padx=10, pady=10)
entry_sigmaxz = ttk.Entry(input_frame)
entry_sigmaxz.grid(row=2, column=1)

ttk.Label(input_frame, text="σyy", style="TLabel").grid(row=3, column=0, padx=10, pady=10)
entry_sigmayy = ttk.Entry(input_frame)
entry_sigmayy.grid(row=3, column=1)

ttk.Label(input_frame, text="σyz", style="TLabel").grid(row=4, column=0, padx=10, pady=10)
entry_sigmayz = ttk.Entry(input_frame)
entry_sigmayz.grid(row=4, column=1)

ttk.Label(input_frame, text="σzz", style="TLabel").grid(row=5, column=0, padx=10, pady=10)
entry_sigmazz = ttk.Entry(input_frame)
entry_sigmazz.grid(row=5, column=1)

ttk.Label(input_frame, text="σc (Critical Stress)", style="TLabel").grid(row=6, column=0, padx=10, pady=10)
entry_sigmac = ttk.Entry(input_frame)
entry_sigmac.grid(row=6, column=1)

calculate_button = ttk.Button(root, text="Calculate", command=calcular)
calculate_button.pack(pady=20)

result_frame = Frame(root, bg="#2e2e2e", relief="solid", borderwidth=2)
result_frame.pack(pady=20, padx=20, fill="both", expand=True)

result_label = ttk.Label(result_frame, text="", style="TLabel", justify="left")
result_label.pack(fill="both", expand=True, padx=20, pady=20)


root.mainloop()
