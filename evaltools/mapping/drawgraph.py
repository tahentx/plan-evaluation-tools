
import matplotlib.pyplot as plt
import networkx as nx


def drawgraph(
        G, ax=None, x="INTPTLON20", y="INTPTLAT20", components=False, node_size=1,
        **kwargs
    ):
    """
    Draws a gerrychain Graph object. Returns a single Axes object (for dual
    graphs drawn whole) and lists of `(Figure, Axes)` pairs for graphs drawn
    component-wise.

    Args:
        G: The dual graph to draw.
        ax: Optional; `matplotlib.axes.Axes` object. If not passed, one is created.
        x: Optional; vertex property used as the horizontal (E-W) coordinate.
        y: Optional; vertex property used as the vertical (N-S) coordinate.
        components: Optional; if `True`, the graph is assumed to have more than
            one connected component (e.g. Michigan) and is drawn component-wise
            and rather than return a single `Axes` object, return a list of
            `(Figure, Axes)` pairs. If something is passed to `ax`, the same
            Axes instance is used for each new Figure.
        node_size: Optional; specifies the default size of a vertex.
        kwargs: Optional; arguments to be passed to `nx.draw()`.

    Returns:
        A tuple of `matplotlib` `(Figure, Axes)` objects, or if `components` is
        `True`, returns a list of `(Figure, Axes)` objects corresponding to each
        component.
    """
    # Create a mapping from identifiers to positions.
    positions = {
        v: (properties[x], properties[y])
        for v, properties in G.nodes(data=True)
    }

    # If `components` is true, plot the graph component-wise. Otherwise plot
    # normally. First, set some properties common to both graphs.
    properties = {"pos": positions, "node_size": node_size }

    # Initialize `pairs` to None.
    pairs = None

    if not components:
        if not ax: axes = plt.axes()
        else: axes = ax
        nx.draw(G, ax=axes, **properties, **kwargs)
    else:
        # Create lists for figures and axes.
        pairs = []

        connected_components = [c for c in nx.connected_components(G)]
        for component in connected_components:
            # Create a new Figure object for each component.
            fig = plt.figure()
            if not ax: ax = plt.axes()

            # Plot the graph.
            subgraph = G.subgraph(component)
            nx.draw(subgraph, ax=ax, **properties, **kwargs)

            # Add them to their respective lists.
            pairs.append((fig, ax))

    return pairs if pairs else axes
