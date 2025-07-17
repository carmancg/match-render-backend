# Reejecutamos el código tras el reset del entorno

import matplotlib.pyplot as plt
import numpy as np

def calcular_atributos_partido(
    goles, remates, remates_arco, posesion, pases, prec_pases, faltas, offsides,
    goles_rival, remates_rival, remates_arco_rival, posesion_rival, pases_rival,
    prec_pases_rival, faltas_rival, offsides_rival
):
    pases_precisos = (prec_pases / 100) * pases
    pases_precisos_rival = (prec_pases_rival / 100) * pases_rival
    porteria = 100 - ((100 / remates_arco_rival) * goles_rival) if remates_arco_rival else 0
    prec_def = 100 - ((100 / pases_precisos_rival) * remates_rival) if pases_precisos_rival else 0
    disc_def = 100 - ((100 / (remates_rival + offsides_rival)) * remates_rival) if (remates_rival + offsides_rival) else 0
    poss_advances = pases_precisos + faltas
    poss_advances_rival = pases_precisos_rival + faltas_rival
    match_poss_adv = poss_advances + poss_advances_rival

    attack = (100 / remates_arco) * goles if remates_arco else 0
    possession = (prec_pases * 2 + posesion * 1) / 3
    defense = (prec_def + disc_def + porteria) / 3
    pressing = (100 / match_poss_adv) * poss_advances if match_poss_adv else 0
    speed = 20 * ((100 / pases_precisos) * remates) if pases_precisos else 0

    return [round(attack, 2), round(possession, 2), round(defense, 2),
            round(pressing, 2), round(speed, 2)]

def graficar_5_radares_datos_crudos(teams_data, team_a_name, team_b_name):
    etiquetas = ['Attack', 'Possession', 'Defense', 'Pressing', 'Speed']
    num_vars = len(etiquetas)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    def cerrar(valores):
        return valores + valores[:1]

    fig, axs = plt.subplots(4, 2, figsize=(10, 16), subplot_kw=dict(polar=True))
    colores = ['skyblue', 'coral']
    features_por_equipo = [[], []]

    for equipo_id in [0, 1]:
        for j in range(0, 6, 2):
            stats = calcular_atributos_partido(*(teams_data[equipo_id][j] + teams_data[1 - equipo_id][j + 1]))
            rival_stats = calcular_atributos_partido(*(teams_data[1 - equipo_id][j + 1] + teams_data[equipo_id][j]))

            features_por_equipo[equipo_id].append(stats)

            partido_c = cerrar(stats)
            rival_stats_c = cerrar(rival_stats)

            ax = axs[j // 2, equipo_id]
            ax.plot(angles, partido_c, color=colores[equipo_id], linewidth=2)
            ax.fill(angles, partido_c, color=colores[equipo_id], alpha=0.2)

            ax.plot(angles, rival_stats_c, color='gray', linewidth=1.5)
            ax.fill(angles, rival_stats_c, color='gray', alpha=0.2)

            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(etiquetas)
            ax.set_yticklabels([])
            ax.grid(color='gray', linewidth=0.2)
            ax.spines['polar'].set_color('gray')
            ax.spines['polar'].set_linewidth(0.2)

        # Rango + Promedio (Fila 4)
        data = np.array(features_por_equipo[equipo_id])
        mins = cerrar(np.min(data, axis=0).tolist())
        maxs = cerrar(np.max(data, axis=0).tolist())
        proms = cerrar(np.mean(data, axis=0).tolist())

        ax = axs[3, equipo_id]
        ax.plot(angles, mins, color=colores[equipo_id], linewidth=0.2)
        ax.plot(angles, maxs, color=colores[equipo_id], linewidth=0.2)
        ax.plot(angles, proms, color=colores[equipo_id], linewidth=2)
        ax.fill_between(angles, mins, maxs, color=colores[equipo_id], alpha=0.2)

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(etiquetas)
        ax.set_yticklabels([])
        ax.grid(color='gray', linewidth=0.2)
        ax.spines['polar'].set_color('gray')
        ax.spines['polar'].set_linewidth(0.2)
        ax.set_title(" ", fontsize=10)

    # Comparativo final
    fig_comp, ax_comp = plt.subplots(figsize=(4, 4), subplot_kw=dict(polar=True))
    for equipo_id in [0, 1]:
        data = np.array(features_por_equipo[equipo_id])
        mins = cerrar(np.min(data, axis=0).tolist())
        maxs = cerrar(np.max(data, axis=0).tolist())
        proms = cerrar(np.mean(data, axis=0).tolist())

        ax_comp.plot(angles, mins, color=colores[equipo_id], linewidth=0.2)
        ax_comp.plot(angles, maxs, color=colores[equipo_id], linewidth=0.2)
        ax_comp.plot(angles, proms, color=colores[equipo_id], linewidth=2)
        ax_comp.fill_between(angles, mins, maxs, color=colores[equipo_id], alpha=0.2)

    ax_comp.set_xticks(angles[:-1])
    ax_comp.set_xticklabels(etiquetas)
    ax_comp.set_yticklabels([])
    ax_comp.grid(color='gray', linewidth=0.2)
    ax_comp.spines['polar'].set_color('gray')
    ax_comp.spines['polar'].set_linewidth(0.2)
    ax_comp.set_title(" ", fontsize=10)

    plt.tight_layout()
    plt.show()
