import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# =============================================================================
# 1. Planar Brownian motion in ℝ² (reference implementation)
# =============================================================================

def brownian_plane(n_steps: int = 20_000,
                   dt: float = 1e-4,
                   x0: tuple[float, float] = (0.0, 0.0),
                   seed: int | None = None) -> np.ndarray:
    """Simulate a planar Brownian motion in ℝ²."""
    rng = np.random.default_rng(seed)
    increments = rng.normal(scale=np.sqrt(dt), size=(n_steps, 2))
    path = np.empty((n_steps + 1, 2))
    path[0] = x0
    path[1:] = x0 + np.cumsum(increments, axis=0)
    return path


# =============================================================================
# 2. Brownian motion on the flat torus [0,L)×[0,L)  (kept for completeness)
# =============================================================================

def brownian_flat_torus(n_steps: int = 20_000,
                        dt: float = 1e-4,
                        L: float = 1.0,
                        x0: tuple[float, float] | None = None,
                        seed: int | None = None) -> np.ndarray:
    """Simulate Brownian motion on the flat torus T² = [0,L)×[0,L)."""
    rng = np.random.default_rng(seed)
    if x0 is None:
        x0 = rng.uniform(0.0, L, size=2)
    increments = rng.normal(scale=np.sqrt(dt), size=(n_steps, 2))
    path = np.empty((n_steps + 1, 2))
    path[0] = np.asarray(x0) % L
    for k in range(1, n_steps + 1):
        path[k] = (path[k - 1] + increments[k - 1]) % L
    return path


# =============================================================================
# 3. Brownian motion in an annulus with *absorbing* boundaries (first‑exit time)
# =============================================================================

def brownian_annulus_first_exit(dt: float = 1e-4,
                                R_outer: float = 1.0,
                                R_inner: float = 0.5,
                                x0: tuple[float, float] | None = None,
                                seed: int | None = None,
                                max_steps: int = 1_000_000) -> tuple[np.ndarray, str]:
    """Simulate planar Brownian motion until it hits one of two concentric circles.

    Parameters
    ----------
    dt : float
        Time increment.
    R_outer : float
        Radius of the outer absorbing circle (must be > R_inner).
    R_inner : float
        Radius of the inner absorbing circle.
    x0 : tuple | None
        Optional starting point. If *None*, a point is chosen uniformly in area.
    seed : int | None
        RNG seed for reproducibility.
    max_steps : int
        Safety cap on the number of steps.

    Returns
    -------
    path : (n, 2) ndarray
        Path up to and including the boundary hit.
    hit : str
        'outer' if the outer circle was hit, 'inner' if the inner was hit, or
        'none' if *max_steps* was reached first.
    """
    if R_inner <= 0 or R_outer <= 0 or R_inner >= R_outer:
        raise ValueError("Require 0 < R_inner < R_outer.")

    rng = np.random.default_rng(seed)

    # --- choose start uniformly in area of annulus --------------------------------
    if x0 is None:
        u = rng.random()
        r0 = np.sqrt(u * (R_outer**2 - R_inner**2) + R_inner**2)
        theta0 = rng.uniform(0.0, 2 * np.pi)
        x0 = (r0 * np.cos(theta0), r0 * np.sin(theta0))
    else:
        if not (R_inner <= np.linalg.norm(x0) <= R_outer):
            raise ValueError("x0 must lie inside the annulus.")

    pos = np.array(x0, dtype=float)
    path = [pos.copy()]

    for _ in range(max_steps):
        step = rng.normal(scale=np.sqrt(dt), size=2)
        new = pos + step
        dist = np.linalg.norm(new)

        # --- check whether boundary is crossed -----------------------------------
        if dist >= R_outer:
            new *= R_outer / dist  # project onto boundary for nice plot
            path.append(new.copy())
            return np.vstack(path), "outer"
        elif dist <= R_inner:
            new *= R_inner / dist
            path.append(new.copy())
            return np.vstack(path), "inner"

        pos = new
        path.append(pos.copy())

    # safety exit
    return np.vstack(path), "none"


# =============================================================================
# 4. Interactive visualisation: multiple paths via a matplotlib Button
# =============================================================================

def interactive_annulus(dt: float = 1e-4,
                        R_outer: float = 1.0,
                        R_inner: float = 0.5,
                        seed: int | None = None,
                        max_steps: int = 1_000_000) -> None:
    """Launch an interactive plot in which a button adds new Brownian paths.

    Each click on *Neuer Pfad* simulates a fresh Brownian motion with a new
    RNG seed but **identical start position** and draws it into the same axes.
    """
    rng = np.random.default_rng(seed)

    # --- choose a common start position -----------------------------------------
    u = rng.random()
    r0 = np.sqrt(u * (R_outer**2 - R_inner**2) + R_inner**2)
    theta0 = rng.uniform(0.0, 2 * np.pi)
    x0 = (r0 * np.cos(theta0), r0 * np.sin(theta0))

    fig, ax = plt.subplots(figsize=(6, 6))
    fig.canvas.manager.set_window_title("Brownian annulus – mehrere Pfade")

    # Boundaries (always the same)
    ax.add_patch(plt.Circle((0.0, 0.0), R_outer, fill=False, linestyle="--", color="k", alpha=0.6))
    ax.add_patch(plt.Circle((0.0, 0.0), R_inner, fill=False, linestyle="--", color="k", alpha=0.6))

    ax.scatter(*x0, marker="o", s=40, label="Start", zorder=3)
    ax.set_aspect("equal")
    ax.set_xlim(-1.1 * R_outer, 1.1 * R_outer)
    ax.set_ylim(-1.1 * R_outer, 1.1 * R_outer)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Ringgebiet: Klikke auf *Neuer Pfad* für weitere Läufe")

    # colour cycle for successive paths
    colours = plt.cm.tab10.colors
    counter = {"n": 0}

    def add_new_path(event=None):
        counter["n"] += 1
        seed_local = rng.integers(0, 2 ** 32 - 1)
        path, hit = brownian_annulus_first_exit(dt=dt,
                                                R_outer=R_outer,
                                                R_inner=R_inner,
                                                x0=x0,
                                                seed=seed_local,
                                                max_steps=max_steps)
        colour = colours[(counter["n"] - 1) % len(colours)]
        ax.plot(path[:, 0], path[:, 1], lw=0.7, color=colour,
                label=f"Pfad {counter['n']} ({hit})")
        ax.legend(loc="upper right", fontsize="small")
        fig.canvas.draw_idle()

    # first path is drawn automatically
    add_new_path()

    # --- Button ---------------------------------------------------------------
    button_ax = fig.add_axes([0.78, 0.02, 0.18, 0.06])  # x0, y0, w, h
    button = Button(button_ax, "Neuer Pfad")
    button.on_clicked(add_new_path)

    plt.tight_layout()
    plt.show()


# =============================================================================
# 5. If run as a script: launch interactive viewer
# =============================================================================

if __name__ == "__main__":
    interactive_annulus()
    #test