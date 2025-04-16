import flet as ft  # type: ignore
from components import navbar, appbar

def generar_script_flexsim(modelo: str, parametros: tuple) -> str:
    """
    Genera el script de FlexSim basado en el modelo y sus parámetros.
    """
    if modelo == "norm":
        mu, sigma = parametros
        return f"normal({mu:.4f}, {sigma:.4f})"

    elif modelo == "expon":
        loc, scale = parametros
        return f"{loc:.4f} + exponential({scale:.4f})"

    elif modelo == "gamma":
        a, loc, scale = parametros
        return f"{loc:.4f} + gamma({scale:.4f}, {a:.4f})"

    elif modelo == "weibull_min":
        c, loc, scale = parametros
        return f"{loc:.4f} + weibull({scale:.4f}, {c:.4f})"

    elif modelo == "weibull_max":
        c, loc, scale = parametros
        return f"{loc:.4f} + weibull_max({scale:.4f}, {c:.4f})"

    elif modelo == "lognorm":
        s, loc, scale = parametros
        return f"{loc:.4f} + lognormal({scale:.4f}, {s:.4f})"

    elif modelo == "beta":
        a, b, loc, scale = parametros
        return f"{loc:.4f} + beta({scale:.4f}, {a:.4f}, {b:.4f})"

    elif modelo == "t":
        df, loc, scale = parametros
        return f"{loc:.4f} + student({df:.4f}, {scale:.4f})"

    elif modelo == "cauchy":
        loc, scale = parametros
        return f"{loc:.4f} + cauchy({scale:.4f})"

    elif modelo == "pareto":
        b, loc, scale = parametros
        return f"{loc:.4f} + pareto({scale:.4f}, {b:.4f})"

    elif modelo == "loglaplace":
        c, loc, scale = parametros
        return f"{loc:.4f} + loglaplace({scale:.4f}, {c:.4f})"

    elif modelo == "gompertz":
        c, loc, scale = parametros
        return f"{loc:.4f} + gompertz({scale:.4f}, {c:.4f})"

    elif modelo == "logistic":
        loc, scale = parametros
        return f"logistic({loc:.4f}, {scale:.4f})"

    elif modelo == "invgauss":
        mu, loc, scale = parametros
        return f"{loc:.4f} + invgauss({scale:.4f}, {mu:.4f})"

    elif modelo == "genextreme":
        c, loc, scale = parametros
        return f"{loc:.4f} + genextreme({scale:.4f}, {c:.4f})"

    elif modelo == "genpareto":
        c, loc, scale = parametros
        return f"{loc:.4f} + {scale:.4f} * ((rand() ^ {abs(c):.4f}) - 1) / {c:.4f}"

    elif modelo == "triang":
        c, loc, scale = parametros
        return f"{loc:.4f} + triang({scale:.4f}, {c:.4f})"

    elif modelo == "powerlaw":
        a, loc, scale = parametros
        return f"{loc:.4f} + powerlaw({scale:.4f}, {a:.4f})"

    else:
        return f"No se ha definido el script para el modelo: {modelo}"


def ApplicationsScreen(page):
    modelo = page.best_model
    parametros = page.best_model_params

    # Generar el script para FlexSim
    script_flexsim = generar_script_flexsim(modelo, parametros)

    return ft.View(
        "/applications",
        [
            appbar.appBar(page, "Aplicaciones"),
            ft.Container(
                content=ft.Text(
                    f"Modelo seleccionado: {modelo}\n\nScript para FlexSim:\n\n{script_flexsim}",
                    text_align=ft.TextAlign.CENTER,
                    size=20,
                    selectable=True
                ),
                alignment=ft.alignment.center,
                padding=30,
                expand=True,
            ),
            navbar.NavigationBar(page)
        ]
    )
