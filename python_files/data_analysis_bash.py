import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from CoolProp.CoolProp import PropsSI
import matplotlib
matplotlib.use('Agg')


diameters = ["d2", "d3", "d4", "d5"]
rpms = ["5k", "10k", "15k", "20k", "25k", "30k", "35k", "40k", "45k", "50k", "55k", "60k", "65k", "70k"]

skip_cases = [
    ("d5", "70k"),
    ("d5", "65k"),
    ("d5", "60k"),
    ("d5", "55k"),
    ("d5", "50k"),
    ("d4", "70k"),
    ("d4", "65k"),
    ("d4", "60k"),
    ("d4", "55k"),
    ("d3", "70k"),
    ("d3", "65k"),
    ("d2", "70k"),
]

fluid = "Methane"

results = []

base_path = r"/scratch/24cr60r06/dhairya/data_files/extracted_data"
extracted_base = "/scratch/24cr60r06/dhairya/data_files/extracted_data/data_analysis"

output_csv = os.path.join(extracted_base,"power_efficiency_results.csv")
nsds_chart = os.path.join(extracted_base,"ns_ds_chart.png")
performance_chart = os.path.join(extracted_base,"power_vs_efficiency.png")
enthalpy_chart = os.path.join(extracted_base,"enthalpy_drop_vs_efficiency.png")
pi1_chart = os.path.join(extracted_base,"efficiency_vs_flow_coefficient.png")
pi2_chart = os.path.join(extracted_base,"efficiency_vs_loading_coefficient.png")
pi3_chart = os.path.join(extracted_base,"efficiency_vs_pressure_coefficient.png")
pi3_chart_rpm = os.path.join(extracted_base,"efficiency_vs_pressure_coefficient_rpm.png")
pi4_chart = os.path.join(extracted_base,"efficiency_vs_rotational_reynolds_number.png")
pi1_vs_pi2_chart = os.path.join(extracted_base,"flow_coefficient_vs_loading_coefficient.png")


# Variables to plot
variables_to_plot = [
    "Pressure",
    "Velocity (mwa)",
    "Temperature",
    "Entropy",
    "Density (mwa)",
    "Mach Number (mwa)"
]



for diameter in diameters:

    for rpm in rpms:
    
      if (diameter, rpm) in skip_cases:
            continue
      
      filename_sp = f"{base_path}/statepoint_data/rotation_{diameter}_{rpm}_state_point_data.csv"

      # Rotor diameter map
      diameter_map = {
          "d2": 0.017711374999993368 * 2,
          "d3": 0.02102387500000713 * 2,
          "d4": 0.024020000000021437 * 2,
          "d5": 0.026768000000034556 * 2
      }
      
      D = diameter_map[diameter]
      D_mean = (D + 0.02) / 2
      
      try:
          df_sp = pd.read_csv(filename_sp)
          diameter_value = float(diameter.replace("d","")) / 1000
          rpm_value = float(rpm.replace("k", "")) * 1000
      
          mdot = abs(df_sp["mdot"][0])
      
          vin = df_sp["vin"][0]
          vout = df_sp["vout"][0]
      
          Pin = df_sp["Pin"][0]
          Pout = df_sp["Pout"][0]
      
          P0in = df_sp["P0in"][0]
          P0out = df_sp["P0out"][0]
      
          Tin = df_sp["Tin"][0]
          Tout = df_sp["Tout"][0]
      
          T0in = df_sp["T0in"][0]
          T0out = df_sp["T0out"][0]
      
          htin = df_sp["htin"][0]
          htout = df_sp["htout"][0]
      
          hin = df_sp["hin"][0]
          hout = df_sp["hout"][0]
      
          sin = df_sp["sin"][0]
          sout = df_sp["sout"][0]
      
          muin = df_sp["muin"][0]
          muout = df_sp["muout"][0]
      
          rhoin = df_sp["rhoin"][0]
          rhoout = df_sp["rhoout"][0]
          
          Min = df_sp["Min"][0]
          Mout = df_sp["Mout"][0]
      
          Tx = df_sp["Tx"][0]
          Ty = df_sp["Ty"][0]
          Tz = df_sp["Tz"][0]
      
          Fx = df_sp["Fx"][0]
          Fy = df_sp["Fy"][0]
          Fz = df_sp["Fz"][0]
      
          # isentropic outlet enthalpy
          h_out_s = PropsSI('H', 'P', Pout, 'S', sin, fluid)
          h_out_ts = PropsSI('H', 'P', P0out, 'S', sin, fluid)
      
          # enthalpy drops
          delta_h_actual = htin - htout
          delta_h_isentropic_ts = htin - h_out_s
          delta_h_isentropic_tt = htin - h_out_ts
      
          # efficiency
          eta_ts = delta_h_actual / delta_h_isentropic_ts
          eta_tt = delta_h_actual / delta_h_isentropic_tt
      
          # Torque magnitude
          torque_t = abs(Tz)
      
          # Force  and torque magnitude
          force = abs(Fz)
          torque_f = force * D / 2
      
          # Angular velocity
          omega = 2 * np.pi * rpm_value / 60
      
          # Shaft power
          shaft_work_t = torque_t * omega
          shaft_work_f = torque_f * omega
      
          # Fluid power
          fluid_work = mdot * (htin - htout)
      
          # Efficiency
          eff_t = shaft_work_t / fluid_work
          eff_f = shaft_work_f / fluid_work
      
          # Volume flow rate
          Q = mdot / rhoin
      
          # Specific enthalpy drop
          delta_ht = htin - htout
      
          # Specific speed
          Ns = omega * np.sqrt(Q) / (delta_ht ** 0.75)
      
          # Specific diameter
          Ds = D_mean * (delta_ht ** 0.25) / np.sqrt(Q)
      
          # Blade Speed / Channel speed
          U = omega * (D_mean / 2)
      
          # Relative Velocity
          win = vin - U
          wout = vout - U
      
          # Blade speed ratio
          Bin = U / vin
          Bout = U / vout
      
          # Total Pressure drop
          delta_pt = P0in - P0out
      
          # Static Pressure Drop
          delta_p = Pin - Pout
      
          # Total Temperature drop
          delta_t0 = T0in - T0out
      
          # Static Temperature Drop
          delta_t = Tin - Tout
      
          # Buckingham pi terms
          # Flow coefficient
          pi1 = mdot / ((D_mean**3) * omega * rhoin)
      
          # Loading coefficient
          pi2 = delta_ht / ((D_mean**2) * omega**2)
      
          # Expansion coefficient or non-dimensional pressure drop
          pi3 = delta_pt / ((D_mean**2) * omega**2 * rhoin)
      
          # Inverse rotational Reynolds number
          pi4 = muin / ((D_mean**2) * omega * rhoin)
      
          # Store results
          results.append({
              "Mdot": mdot,
              "Diameter": diameter,
              "RPM": rpm,
              "Diameter_value": diameter_value,
              "RPM_value": rpm_value,
              "Omega": omega,
              "Mean Radius": D_mean / 2,
              "Inlet Absolute Velocity": vin,
              "Outlet Absolute Velocity": vout,
              "Inlet Relative Velocity": win,
              "Outlet Relative Velocity": wout,
              "Blade Speed": U,
              "Inlet Mach Number": Min,
              "outlet Mach Number": Mout,
              "Torque_t (Nm)": torque_t,
              "Torque_f (Nm)": torque_f,
              "Power_t (W)": shaft_work_t,
              "Power_f (W)": shaft_work_f,
              "Fluid Power (W)": fluid_work,
              "Shaft_efficiency_t": eff_t,
              "Shaft_efficiency_f": eff_f,
              "Efficiency Total-to-Static": eta_ts,
              "Efficiency Total-to-Total": eta_tt,
              "Ns": Ns,
              "Ds": Ds,
              "Total Pressure drop": delta_pt,
              "Static Pressure drop": delta_p,
              "Total temperature drop": delta_t0,
              "Static Temperature drop": delta_t,
              "Total Enthalpy drop": delta_ht,
              "pi1": pi1,
              "pi2": pi2,
              "pi3": pi3,
              "pi4": pi4
          })
      
      
      except FileNotFoundError:
          print(f"File not found: {filename_sp}")
          
          
results_df = pd.DataFrame(results)
results_df.to_csv(output_csv,index=False)




# ----------------------------------------
# Ns-Ds plot
# ----------------------------------------
plt.figure(figsize=(8,6))

# Different markers for each diameter
marker_map = {
    "d2": "o",
    "d3": "s",
    "d4": "^",
    "d5": "D"
}

for diameter in results_df["Diameter"].unique():

    subset = results_df[results_df["Diameter"] == diameter]

    # Sort by RPM for proper connection
    #subset = subset.sort_values("RPM")

    plt.plot(
        subset["Ns"],
        subset["Ds"],
        marker=marker_map[diameter],
        linewidth=1.5,
        markersize=7,
        label=diameter
    )

    # Add text near each point
    for _, row in subset.iterrows():

        # Efficiency label
        plt.text(
            row["Ns"] - 0.002,
            row["Ds"],
            f'{row["Efficiency Total-to-Total"]*100:.1f}%',
            fontsize=8,
            ha='right',
            va='center'
        )

        # RPM label
        plt.text(
            row["Ns"] + 0.002,
            row["Ds"],
            f'{row["RPM"]}',
            fontsize=8,
            ha='left',
            va='top'
        )

plt.xlabel("Specific Speed (Ns)")
plt.ylabel("Specific Diameter (Ds)")
plt.title("Ns-Ds Chart")

plt.grid(True)
plt.legend(title="Diameter")

plt.savefig(
    nsds_chart,
    dpi=300,
    bbox_inches='tight',
    pad_inches=0.3
)
plt.close()



# ----------------------------------------
# Power vs Efficiency 
# ----------------------------------------
plt.figure(figsize=(8,6))

# Different markers for each diameter
marker_map = {
    "d2": "o",   # circle
    "d3": "s",   # square
    "d4": "^",   # triangle
    "d5": "D"    # diamond
}

for diameter in results_df["Diameter"].unique():

    subset = results_df[results_df["Diameter"] == diameter]

    plt.plot(
        subset["Efficiency Total-to-Total"] * 100,
        subset["Power_f (W)"],
        marker=marker_map[diameter],
        markersize=8,
        linewidth=1.5,
        label=diameter
    )
    
    
    # Add RPM labels
    for _, row in subset.iterrows():

        plt.text(
            row["Efficiency Total-to-Total"],
            row["Power_f (W)"],
            f'{row["RPM"]}',
            fontsize=8,
            ha='left',
            va='bottom'
        )


plt.xlabel("Efficiency Total-to-Total (%)")
plt.ylabel("Power (W)")
plt.title("Power vs Efficiency")

plt.grid(True)
plt.legend(title="Diameter")

plt.savefig(
    performance_chart,
    dpi=300,
    bbox_inches='tight',
    pad_inches=0.3
)
plt.close()



# ----------------------------------------
# Enthalpy drop vs Efficiency
# ----------------------------------------
plt.figure(figsize=(8,6))

# Different markers for each diameter
marker_map = {
    "d2": "o",   # circle
    "d3": "s",   # square
    "d4": "^",   # triangle
    "d5": "D"    # diamond
}

for diameter in results_df["Diameter"].unique():

    subset = results_df[results_df["Diameter"] == diameter]

    plt.plot(
        subset["Efficiency Total-to-Total"] * 100,
        subset["Total Enthalpy drop"],
        marker=marker_map[diameter],
        markersize=8,
        linewidth=1.5,
        label=diameter
    )
    
    
    # Add RPM labels
    for _, row in subset.iterrows():

        plt.text(
            row["Efficiency Total-to-Total"],
            row["Total Enthalpy drop"],
            f'{row["RPM"]}',
            fontsize=8,
            ha='left',
            va='bottom'
        )


plt.xlabel("Efficiency Total-to-Total (%)")
plt.ylabel("Total Enthalpy drop")
plt.title("Total Enthalpy drop vs Efficiency")

plt.grid(True)
plt.legend(title="Diameter")

plt.savefig(
    enthalpy_chart,
    dpi=300,
    bbox_inches='tight',
    pad_inches=0.3
)
plt.close()


# ----------------------------------------
# Efficiency vs Flow Coefficient (pi1)
# ----------------------------------------
plt.figure(figsize=(8,6))

# Different markers for each diameter
marker_map = {
    "d2": "o",
    "d3": "s",
    "d4": "^",
    "d5": "D"
}

for diameter in results_df["Diameter"].unique():

    subset = results_df[
        results_df["Diameter"] == diameter
    ]

    # Optional: sort by RPM
    subset = subset.sort_values("RPM_value")

    plt.plot(
        subset["Efficiency Total-to-Total"] * 100,
        subset["pi1"],
        marker=marker_map[diameter],
        linewidth=1.5,
        markersize=7,
        label=diameter
    )

    # Add RPM labels
    for _, row in subset.iterrows():

        plt.text(
            row["pi1"],
            row["Efficiency Total-to-Total"] * 100,
            f'{row["RPM"]}',
            fontsize=8,
            ha='left',
            va='bottom'
        )

plt.ylabel("Flow Coefficient ($\\pi_1$)")
plt.xlabel("Efficiency Total-to-Total (%)")
plt.title("Efficiency vs Flow Coefficient")


equation_text = (
    r"$\pi_1 = \frac{\dot{m}}{d^3 \, \omega \, \rho_{in}}$"
)

plt.text(
    0.15, 0.95,                # x,y in axes coordinates
    equation_text,
    transform=plt.gca().transAxes,
    fontsize=14,
    verticalalignment='top',
    bbox=dict(
        boxstyle="round",
        facecolor="white",
        alpha=1
    )
)

plt.grid(True)
plt.legend(title="Diameter")

plt.savefig(
    pi1_chart,
    dpi=300,
    pad_inches=0.3
)

plt.close()


# ----------------------------------------
# Efficiency vs Loading Coefficient (pi2)
# ----------------------------------------
plt.figure(figsize=(8,6))

# Different markers for each diameter
marker_map = {
    "d2": "o",
    "d3": "s",
    "d4": "^",
    "d5": "D"
}

for diameter in results_df["Diameter"].unique():

    subset = results_df[
        results_df["Diameter"] == diameter
    ]

    # Optional: sort by RPM
    subset = subset.sort_values("RPM_value")

    plt.plot(
        subset["Efficiency Total-to-Total"] * 100,
        subset["pi2"],
        marker=marker_map[diameter],
        linewidth=1.5,
        markersize=7,
        label=diameter
    )

    # Add RPM labels
    for _, row in subset.iterrows():

        plt.text(
            row["Efficiency Total-to-Total"] * 100,
            row["pi2"],
            f'{row["RPM"]}',
            fontsize=8,
            ha='left',
            va='bottom'
        )

plt.ylabel("Loading Coefficient ($\\pi_2$)")
plt.xlabel("Efficiency Total-to-Total (%)")
plt.title("Efficiency vs Loading Coefficient")


equation_text = (
    r"$\pi_2 = \frac{\Delta h_0}{d^2 \, \omega^2}$"
)

plt.text(
    0.15, 0.95,                # x,y in axes coordinates
    equation_text,
    transform=plt.gca().transAxes,
    fontsize=14,
    verticalalignment='top',
    bbox=dict(
        boxstyle="round",
        facecolor="white",
        alpha=1
    )
)

plt.grid(True)
plt.legend(title="Diameter")

plt.savefig(
    pi2_chart,
    dpi=300,
    pad_inches=0.3
)

plt.close()

# ----------------------------------------
# Efficiency vs Pressure Coefficient (pi3)
# ----------------------------------------
plt.figure(figsize=(8,6))

# Different markers for each diameter
marker_map = {
    "d2": "o",
    "d3": "s",
    "d4": "^",
    "d5": "D"
}

for diameter in results_df["Diameter"].unique():

    subset = results_df[
        results_df["Diameter"] == diameter
    ]

    # Optional: sort by RPM
    subset = subset.sort_values("RPM_value")

    plt.plot(
        subset["Efficiency Total-to-Total"] * 100,
        subset["pi3"],
        marker=marker_map[diameter],
        linewidth=1.5,
        markersize=7,
        label=diameter
    )
    
    plt.yscale("log")

    # Add RPM labels
    for _, row in subset.iterrows():

        plt.text(
            row["Efficiency Total-to-Total"] * 100,
            row["pi3"],
            f'{row["RPM"]}',
            fontsize=8,
            ha='left',
            va='bottom'
        )

plt.ylabel("Pressure Coefficient ($\\pi_3$)")
plt.xlabel("Efficiency Total-to-Total (%)")
plt.title("Efficiency vs Pressure Coefficient")


equation_text = (
    r"$\pi_3 = \frac{\Delta P_0}{d^2 \, \omega^2 \, \rho_{in}}$"
)

plt.text(
    0.15, 0.95,                # x,y in axes coordinates
    equation_text,
    transform=plt.gca().transAxes,
    fontsize=14,
    verticalalignment='top',
    bbox=dict(
        boxstyle="round",
        facecolor="white",
        alpha=1
    )
)

plt.grid(True)
plt.legend(title="Diameter")

plt.savefig(
    pi3_chart,
    dpi=300,
    pad_inches=0.3
)

plt.close()


# ----------------------------------------
# Efficiency vs Rotational Reynolds number (pi4)
# ----------------------------------------
plt.figure(figsize=(8,6))

# Different markers for each diameter
marker_map = {
    "d2": "o",
    "d3": "s",
    "d4": "^",
    "d5": "D"
}

for diameter in results_df["Diameter"].unique():

    subset = results_df[
        results_df["Diameter"] == diameter
    ]

    # Optional: sort by RPM
    subset = subset.sort_values("RPM_value")

    plt.plot(
        subset["Efficiency Total-to-Total"] * 100,
        subset["pi4"]**(-1),
        marker=marker_map[diameter],
        linewidth=1.5,
        markersize=7,
        label=diameter
    )
    plt.yscale("log")

    # Add RPM labels
    for _, row in subset.iterrows():

        plt.text(
            row["Efficiency Total-to-Total"] * 100,
            row["pi4"]**(-1),
            f'{row["RPM"]}',
            fontsize=8,
            ha='left',
            va='bottom'
        )

plt.ylabel("Rotational Reynolds number ($\\pi_4^{-1}$)")
plt.xlabel("Efficiency Total-to-Total (%)")
plt.title("Efficiency vs Rotational Reynolds number")

equation_text = (
    r"$\pi_4^{-1} = \frac{D_{mean}^2 \, \omega \, \rho}{\mu}$"
)

plt.text(
    0.15, 0.95,                # x,y in axes coordinates
    equation_text,
    transform=plt.gca().transAxes,
    fontsize=14,
    verticalalignment='top',
    bbox=dict(
        boxstyle="round",
        facecolor="white",
        alpha=1
    )
)

plt.grid(True)
plt.legend(title="Diameter")

plt.savefig(
    pi4_chart,
    dpi=300,
    pad_inches=0.3
)

plt.close()



# ----------------------------------------
# Flow Coefficient (pi1) vs Loading Coefficient (pi2)
# ----------------------------------------
plt.figure(figsize=(8,6))

# Different markers for each diameter
marker_map = {
    "d2": "o",
    "d3": "s",
    "d4": "^",
    "d5": "D"
}

for diameter in results_df["Diameter"].unique():

    subset = results_df[
        results_df["Diameter"] == diameter
    ]

    # Optional: sort by RPM
    subset = subset.sort_values("RPM_value")

    plt.plot(
        subset["pi1"],
        subset["pi2"],
        marker=marker_map[diameter],
        linewidth=1.5,
        markersize=7,
        label=diameter
    )

    # Add RPM labels
    for _, row in subset.iterrows():

        plt.text(
            row["pi1"],
            row["pi2"],
            f'{row["RPM"]}',
            fontsize=8,
            ha='left',
            va='bottom'
        )

plt.ylabel("Flow Coefficient ($\\pi_1$)")
plt.xlabel("Loading Coefficient ($\\pi_2$)")
plt.title("Flow Coefficient vs Loading Coefficient")

plt.grid(True)
plt.legend(title="Diameter")

plt.savefig(
    pi1_vs_pi2_chart,
    dpi=300,
    pad_inches=0.3
)

plt.close()





# ----------------------------------------
# Efficiency vs Pressure Coefficient (pi3)
# grouped by RPM
# ----------------------------------------
plt.figure(figsize=(8,6))

# Marker map for RPMs
marker_map = {
    5000.0: "o",
    10000.0: "s",
    15000.0: "^",
    20000.0: "D",
    25000.0: "v",
    30000.0: "P",
    35000.0: "X",
    40000.0: "*",
    45000.0: "<",
    50000.0: ">",
    55000.0: "h",
    60000.0: "H",
    65000.0: "8",
    70000.0: "p"
}

for rpm in results_df["RPM_value"].unique():

    subset = results_df[
        results_df["RPM_value"] == rpm
    ]

    # Sort by diameter
    subset = subset.sort_values("Diameter_value")

    plt.plot(
        subset["Efficiency Total-to-Total"] * 100,
        subset["pi3"],
        marker=marker_map[rpm],
        linewidth=1.5,
        markersize=7,
        label=f"{int(rpm/1000)}k"
    )

    # Add diameter labels
    for _, row in subset.iterrows():

        plt.text(
            row["Efficiency Total-to-Total"] * 100,
            row["pi3"],
            f'{row["Diameter"]}',
            fontsize=8,
            ha='left',
            va='bottom'
        )

# Log scale for pi3 axis
plt.yscale("log")

plt.ylabel("Pressure Coefficient ($\\pi_3$)")
plt.xlabel("Efficiency Total-to-Total (%)")
plt.title("Efficiency vs Pressure Coefficient")

# Equation textbox
equation_text = (
    r"$\pi_3 = \frac{\Delta P_0}{D^2 \, \omega^2 \, \rho_{in}}$"
)

plt.text(
    0.15, 0.95,
    equation_text,
    transform=plt.gca().transAxes,
    fontsize=14,
    verticalalignment='top',
    bbox=dict(
        boxstyle="round",
        facecolor="white",
        alpha=1
    )
)

plt.grid(True)
plt.legend(title="RPM")

plt.savefig(
    pi3_chart_rpm,
    dpi=300,
    pad_inches=0.3
)

plt.close()
