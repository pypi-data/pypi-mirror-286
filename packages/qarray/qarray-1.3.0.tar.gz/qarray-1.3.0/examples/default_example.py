import matplotlib.pyplot as plt
import numpy as np

from qarray import DotArray, GateVoltageComposer

# Create a quantum dot with 2 gates, specifying the capacitance matrices in their maxwell form.

model = DotArray(
    Cdd=np.array([
        [0, 0.1],
        [0.1, 0]
    ]),
    Cgd=np.array([
        [1., 0.1],
        [0.1, 1]
    ]),
    algorithm='default',
    implementation='rust',
    charge_carrier='h', T=0.,
)

model.run_gui()

# a helper class designed to make it easy to create gate voltage arrays for nd sweeps
voltage_composer = GateVoltageComposer(n_gate=model.n_gate, n_dot=model.n_dot)
voltage_composer.virtual_gate_matrix = -np.linalg.pinv(model.cdd_inv @ model.cgd)
voltage_composer.virtual_gate_origin = np.zeros(model.n_gate)

# defining the min and max values for the dot voltage sweep
# defining the min and max values for the dot voltage sweep
vx_min, vx_max = -5, 5
vy_min, vy_max = -5, 5

# using the dot voltage composer to create the dot voltage array for the 2d sweep
vg = voltage_composer.do2d('P1', vy_min, vx_max, 400, 'P2', vy_min, vy_max, 400)

# run the simulation with the quantum dot array open such that the number of charge carriers is not fixed
n_open = model.ground_state_open(vg)  # n_open is a (100, 100, 2) array encoding the
# number of charge carriers in each dot for each gate voltage
# run the simulation with the quantum dot array closed such that the number of charge carriers is fixed to 2
n_closed = model.ground_state_closed(vg, n_charges=2)  # n_closed is a (100, 100, 2) array encoding the
# number of charge carriers in each dot for each gate voltage

# importing a function which dots the charge occupation with the charge state contrast to yield a z value for plotting by imshow.
from qarray import charge_state_contrast

charge_state_contrast_array = [0.8, 1.2]

# creating arrays that encode when the dot occupation changes
z_open = charge_state_contrast(n_open, charge_state_contrast_array)
z_closed = charge_state_contrast(n_closed, charge_state_contrast_array)

# plot the results
fig, ax = plt.subplots(1, 2, figsize=(10, 5))
ax[0].imshow(z_open, extent=(vx_min, vx_max, vy_min, vy_max), origin='lower', cmap='Blues')
ax[0].set_title('Open Dot Array')
ax[0].set_xlabel('e1_2')
ax[0].set_ylabel('U1_2')
ax[1].imshow(z_closed, extent=(vx_min, vx_max, vy_min, vy_max), origin='lower', cmap='Blues')
ax[1].set_title('Closed Dot Array')
ax[1].set_xlabel('e1_2')
ax[1].set_ylabel('U1_2')
plt.tight_layout()
plt.savefig('../docs/source/figures/getting_started_example_plunger_plunger.jpg')


# using the dot voltage composer to create the dot voltage array for the 2d sweep
vg = voltage_composer.do2d('e1_2', vy_min, vx_max, 400, 'U1_2', vy_min, vy_max, 400)

# run the simulation with the quantum dot array open such that the number of charge carriers is not fixed
n_open = model.ground_state_open(vg)  # n_open is a (100, 100, 2) array encoding the
# number of charge carriers in each dot for each gate voltage
# run the simulation with the quantum dot array closed such that the number of charge carriers is fixed to 2
n_closed = model.ground_state_closed(vg, n_charges=2)  # n_closed is a (100, 100, 2) array encoding the
# number of charge carriers in each dot for each gate voltage

# importing a function which dots the charge occupation with the charge state contrast to yield a z value for plotting by imshow.
from qarray import charge_state_contrast

charge_state_contrast_array = [0.8, 1.2]

# creating arrays that encode when the dot occupation changes
z_open = charge_state_contrast(n_open, charge_state_contrast_array)
z_closed = charge_state_contrast(n_closed, charge_state_contrast_array)

# plot the results
fig, ax = plt.subplots(1, 2, figsize=(10, 5))
ax[0].imshow(z_open, extent=(vx_min, vx_max, vy_min, vy_max), origin='lower', cmap='Blues')
ax[0].set_title('Open Dot Array')
ax[0].set_xlabel('e1_2')
ax[0].set_ylabel('U1_2')
ax[1].imshow(z_closed, extent=(vx_min, vx_max, vy_min, vy_max), origin='lower', cmap='Blues')
ax[1].set_title('Closed Dot Array')
ax[1].set_xlabel('e1_2')
ax[1].set_ylabel('U1_2')
plt.tight_layout()
plt.savefig('../docs/source/figures/getting_started_example_detuning_onsite.jpg')
