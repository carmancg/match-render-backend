import matplotlib.pyplot as plt
import numpy as np

def calcular_atributos_partido(
    goles, remates, remates_arco, posesion, pases, prec_pases, faltas, offsides,
    goles_rival, remates_rival, remates_arco_rival, posesion_rival, pases_rival, prec_pases_rival, faltas_rival, offsides_rival
):
    pases_precisos = (prec_pases / 100) * pases
    pases_precisos_rival = (prec_pases_rival / 100) * pases_rival
    porteria = 100 - ((100 / remates_arco_rival) * goles_rival) if remates_arco_rival else 0
    prec_def = 100 - ((100 / pases_precisos_rival) * remates_rival) if pases_precisos_rival else 0
    disc_def = 100 - ((100 / (remates_rival + offsides_rival)) * remates_rival) if remates_rival + offsides_rival else 0
    poss_advances = pases_precisos + faltas
    poss_advances_rival = pases_precisos_rival + faltas_rival
    match_poss_adv = poss_advances + poss_advances_rival

    attack = (100 / remates_arco) * goles if remates_arco else 0
    possession = (prec_pases * 2 + posesion * 1) / 3
    defense = (prec_def + disc_def + porteria) / 3
    pressing = (100 / match_poss_adv) * poss_advances if match_poss_adv else 0
    speed = 20 * ((100 / pases_precisos) * remates) if pases_precisos else 0

    return [round(attack, 2), round(possession, 2), round(defense, 2), round(pressing, 2), round(speed, 2)]


def graficar_radar_rango_promedio_minimalista(team_a_name, team_b_name, teams_data):
    labels = ['Attack', 'Possession', 'Defense', 'Pressing', 'Speed']
    num_vars = len(labels)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))

    def calcular_min_max_avg(team_data):
        valores = []
        for i in range(0, len(team_data), 2):
            atributos = calcular_atributos_partido(*(team_data[i] + team_data[i+1]))
            valores.append(atributos)
        valores = np.array(valores)
        min_vals = valores.min(axis=0).tolist()
        max_vals = valores.max(axis=0).tolist()
        avg_vals = valores.mean(axis=0).tolist()
        return (
            min_vals + [min_vals[0]],
            max_vals + [max_vals[0]],
            avg_vals + [avg_vals[0]]
        )

    min_a, max_a, avg_a = calcular_min_max_avg(teams_data[0])
    min_b, max_b, avg_b = calcular_min_max_avg(teams_data[1])

    # Team A
    ax.fill_between(angles, min_a, max_a, color='skyblue', alpha=0.2, label=f'{team_a_name}')
    ax.plot(angles, max_a, color='skyblue', linewidth=0.1)
    ax.plot(angles, min_a, color='skyblue', linewidth=0.1)
    ax.plot(angles, avg_a, color='deepskyblue', linestyle='-', linewidth=1.5, label=f'{team_a_name} (avg)')

    # Team B
    ax.fill_between(angles, min_b, max_b, color='coral', alpha=0.2, label=f'{team_b_name}')
    ax.plot(angles, max_b, color='coral', linewidth=0.1)
    ax.plot(angles, min_b, color='coral', linewidth=0.1)
    ax.plot(angles, avg_b, color='orangered', linestyle='-', linewidth=1.5, label=f'{team_b_name} (avg)')

    # Estética minimalista
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_thetagrids(np.degrees(angles[:-1]), labels, fontsize=11)

    ax.set_yticklabels([])        # ❌ sin etiquetas radiales
    ax.set_rgrids([])             # ❌ sin líneas de grilla radial
    ax.set_xticks(angles[:-1])    # ✅ mantener etiquetas de features
    ax.grid(False)                # ❌ sin grid
    ax.set_frame_on(False)        # ❌ sin borde polar

    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.legend(loc='upper right', bbox_to_anchor=(1.35, 1.1))
    plt.tight_layout()
    plt.show()
