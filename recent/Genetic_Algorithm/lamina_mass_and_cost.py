import numpy as np

composite_material_property = {
        'fiber_volume_fraction': 0.7,
        }
fiber_property = {
        'specific_gravity':1.8
        }
matrice_property = {
        'specific_gravity':1.2
        }
density_of_water = 3.6127*0.01


def get_graphite_epoxy_lamina_mass(volume):
    density = fiber_property['specific_gravity'] * density_of_water * \
              composite_material_property['fiber_volume_fraction'] + \
              matrice_property['specific_gravity'] * density_of_water * \
              (1 - composite_material_property['fiber_volume_fraction'])
    return volume * density



if __name__ == "__main__":
    volume = np.pi * 6 * 12 * 35 * 0.005
    mass = get_graphite_epoxy_lamina_mass(volume)
    print(mass)
