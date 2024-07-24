import numpy as np
import matplotlib.pyplot as plt
import io
from matplotlib.colors import LinearSegmentedColormap, Normalize, BoundaryNorm


def calculate_class_break_values(
    raster_array: np.ndarray, num_classes: int = 5, decimal_places: int = 4
) -> list[float]:
    """
    # Summary:
        Calculate class break values

    # Parameters:
        raster_array (np.ndarray): Array of values
        num_classes (int): Number of classes
        decimal_places (int): Decimal places

    # Returns:
        list[float]: List of class break values
    """

    valid_data = raster_array[~np.isnan(raster_array)]

    class_break_values = np.percentile(valid_data, np.linspace(0, 100, num_classes + 1))

    class_break_values = np.round(class_break_values, decimal_places)

    return class_break_values.tolist()


def generate_figure_save_and_show_5_normalized(
    index: np.ndarray,
    colormap: LinearSegmentedColormap,
    show: bool = False,
) -> io.BytesIO:
    """
    # Summary:
        Generate figure

    # Arguments:
        index (np.ndarray): Array of values
        class_labels (list[str]): List of class labels : example ["Área sin o Débil vegetación", "Vegetación escasa o Crecimiento inicial", "Vegetación moderada y saludable", "Vegetación densa y vigorosa", "Vegetación sobresaturada o de Alta densidad"]
        title (str): Title of the figure : example "Normalized Difference Vegetation Index (NDVI)"
        colormap (LinearSegmentedColormap): Colormap
        output_path_file_and_name (str): Name of the output file : example "C:/Users/A4agro/Desktop/ndvi-fig.png"
        show (bool): Show the figure
    """

    buf = io.BytesIO()
    min_val = np.nanmin(index)
    max_val = np.nanmax(index)

    norm = Normalize(vmin=min_val, vmax=max_val)

    # Create a figure and subplot for the plot
    fig, ax = plt.subplots(figsize=(10, 10), dpi=300)

    # Display index using imshow with colormap and normalization
    cbar_plot = ax.imshow(index, cmap=colormap, norm=norm)

    # Turn off axis labels
    ax.axis("off")

    # Set title for the plot

    # Save the plot as an image file
    fig.savefig(
        buf, format="png", pad_inches=0.1, bbox_inches="tight", transparent=True
    )

    if show == True:
        # Show the plot
        plt.show()

    plt.close(fig)
    buf.seek(0)

    return buf


def generate_figure_save_and_show(
    index: np.ndarray,
    colormap_norm: tuple[LinearSegmentedColormap, BoundaryNorm],
    show: bool = False,
) -> io.BytesIO:
    """
    # Summary:
        Generate figure

    # Arguments:
        index (np.ndarray): Array of values
        class_labels (list[str]): List of class labels : example ["Área sin o Débil vegetación", "Vegetación escasa o Crecimiento inicial", "Vegetación moderada y saludable", "Vegetación densa y vigorosa", "Vegetación sobresaturada o de Alta densidad"]
        title (str): Title of the figure : example "Normalized Difference Vegetation Index (NDVI)"
        colormap (LinearSegmentedColormap): Colormap
        output_path_file_and_name (str): Name of the output file : example "C:/Users/A4agro/Desktop/ndvi-fig.png"
        show (bool): Show the figure
    """
    colormap, norm = colormap_norm
    buf = io.BytesIO()

    # Create a figure and subplot for the plot
    fig, ax = plt.subplots(figsize=(10, 10), dpi=300)

    # add nearest
    # Display index using imshow with colormap and normalization
    cbar_plot = ax.imshow(index, cmap=colormap, norm=norm, interpolation="nearest")

    # Turn off axis labels
    ax.axis("off")

    # Save the plot as an image file
    fig.savefig(
        buf, format="png", pad_inches=0.1, bbox_inches="tight", transparent=True
    )

    if show == True:
        # Show the plot
        plt.show()

    plt.close(fig)
    buf.seek(0)

    return buf
