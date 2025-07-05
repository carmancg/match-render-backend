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

def graficar_radar_rango_promedio_minimalista(home_team, away_team, teams_data):
    labels = ['Attack', 'Possession', 'Defense', 'Pressing', 'Speed']
    num_vars = len(labels)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    def procesar_equipo(data, color, nombre):
        stats = []
        for i in range(0, len(data), 2):
            partido = data[i]
            rival = data[i+1]
            atributos = calcular_atributos_partido(*(partido + rival))
            stats.append(atributos)

        stats = np.array(stats)
        min_vals = stats.min(axis=0).tolist() + [stats.min(axis=0)[0]]
        max_vals = stats.max(axis=0).tolist() + [stats.max(axis=0)[0]]
        avg_vals = stats.mean(axis=0).tolist() + [stats.mean(axis=0)[0]]

        ax.plot(angles, max_vals, color=color, linewidth=0.5, linestyle='dashed')
        ax.plot(angles, min_vals, color=color, linewidth=0.5, linestyle='dashed')
        ax.fill(angles, max_vals, color=color, alpha=0.15)
        ax.fill(angles, min_vals, color=color, alpha=1, zorder=2)
        ax.plot(angles, avg_vals, color=color, linewidth=2, label=nombre)

    procesar_equipo(teams_data[0], 'skyblue', home_team)
    procesar_equipo(teams_data[1], 'coral', away_team)

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_thetagrids(np.degrees(angles[:-1]), labels)

    ax.set_rgrids([])      # sin grillas radiales
    ax.set_yticklabels([]) # sin etiquetas radiales
    ax.set_xticks(angles[:-1])
    ax.grid(False)
    ax.set_frame_on(False)

    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color('black')
        spine.set_linewidth(1)

    ax.legend(loc='upper right')
    plt.tight_layout()
