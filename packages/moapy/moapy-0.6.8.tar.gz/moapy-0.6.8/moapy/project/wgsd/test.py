import matplotlib.pyplot as plt

def plot_material_data(json_data):
    material_data = json_data['moapy.project.wgsd.wgsd_flow.MaterialConcrete']

    curve_uls = material_data['curve_uls']
    curve_sls = material_data['curve_sls']

    stress_uls = [point['stress'] for point in curve_uls]
    strain_uls = [point['strain'] for point in curve_uls]

    stress_sls = [point['stress'] for point in curve_sls]
    strain_sls = [point['strain'] for point in curve_sls]

    plt.plot(strain_uls, stress_uls, label='Curve ULS')
    plt.plot(strain_sls, stress_sls, label='Curve SLS')

    plt.xlabel('Strain')
    plt.ylabel('Stress')
    plt.title('Material Concrete Stress-Strain Curve')
    plt.legend()

    plt.show()

# Usage
json_data = {'moapy.project.wgsd.wgsd_flow.MaterialConcrete': {'grade': {'design_code': 'ACI318M-19', 'grade': 'C12'}, 'curve_uls': [{'stress': 0, 'strain': 0}, {'stress': 0, 'strain': 0.0004500000000000001}, {'stress': 10.2, 'strain': 0.0004500000000000001}, {'stress': 10.2, 'strain': 0.003}], 'curve_sls': [{'stress': 0, 'strain': 0}, {'stress': 12, 'strain': 0.003}]}}

plot_material_data(json_data)