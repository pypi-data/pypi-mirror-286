from enum import Enum
from typing import Iterable, Union

import numpy as np

__all__ = [
    "AggregationMethod",
    "auc",
    "copy_docstring_from",
    "check_confusion_matrix_entries",
    "onehot_encode",
]


def copy_docstring_from(source):
    """
    Decorator to copy the docstring from one function to another.

    Parameters
    ----------
    source : function
        The function from which to copy the docstring.

    Returns
    -------
    function
        The decorated function with the copied docstring.
    """

    def decorator(target):
        target.__doc__ = source.__doc__
        return target

    return decorator


class AggregationMethod(Enum):
    """
    Enumeration for specifying the method of aggregating metrics in
    multi-class classification.

    Attributes:
    ----------
    MICRO : str
        Micro-averaging method, which aggregates contributions from all classes
        to compute the average metric.
    MACRO : str
        Macro-averaging method, which computes the metric independently for
        each class and then takes the average.
    ONE_VS_ALL : str
        One-vs-all method, which treats (subsequently) each class as the
        positive class and all others as negative, computing metrics for
        each class in this manner.
    """

    MICRO = "MICRO"
    MACRO = "MACRO"
    ONE_VS_ALL = "ONE_VS_ALL"


def _all_equal(iterable: Iterable):
    """
    Check if all elements in the iterable are equal.

    Parameters:
    ----------
    iterable : iterable
        An iterable containing elements to be compared.

    Returns:
    -------
    bool
        True if all elements in the iterable are equal or if the
        iterable is empty.
        False otherwise.

    """
    iterator = iter(iterable)
    try:
        first = next(iterator)
    except StopIteration:
        return True
    return all(element == first for element in iterator)


def check_confusion_matrix_entries(*args):
    """
    Validate that input confusion matrix arrays are 2D, have the same shape,
    and are non-negative.

    Parameters:
    ----------
    *args : np.ndarray
        Variable number of input arrays representing confusion matrix entries.

    Raises:
    ------
    AssertionError
        If input arrays are not 2D, do not have the same shape, or contain
        negative values.
    """
    assert _all_equal(
        [arg.ndim for arg in args]
    ), "Inputs arrays must be of two-dimensional."
    assert _all_equal(
        [arg.shape for arg in args]
    ), "Inputs arrays must have same the shape."
    assert all(
        [np.min(arg) >= 0 for arg in args]
    ), "Input arrays must be non-negative."


def auc(vals_x: np.ndarray, vals_y: np.ndarray) -> Union[np.ndarray, float]:
    """
    Compute the approximate area under the curve.

    This is a weak wrapper around np.trapz, ensuring that the integral is
    always positive, i.e. making it ignore the sorting order of the input
    numpy array.

    Parameters
    ----------
    vals_x : np.ndarray
        Must be squeezable to shape (-1,) or (-1, n_classes).
    vals_y : np.ndarray
        Must be squeezable to shape (-1,) or (-1, n_classes).

    Returns
    -------
    Union[np.ndarray, float]
        Approximate AUC value. Either single float or np.ndarray of shape
        (vals_x.shape[1],).
    """
    vals_x = np.squeeze(vals_x)
    vals_y = np.squeeze(vals_y)

    if vals_x.ndim == 1:
        return np.abs(np.trapz(x=vals_x, y=vals_y))
    elif vals_x.ndim == 2:
        return np.array(
            [
                np.trapz(x=vals_x[..., i], y=vals_y[..., i])
                for i in range(vals_x.shape[-1])
            ]
        )
    else:
        raise NotImplementedError("Inputs must be 1 or 2 dimensional.")


def onehot_encode(int_masks: np.ndarray, num_classes: int) -> np.ndarray:
    """
    Convert integer masks to one-hot encoded masks.
    Optimized methods that does not explode in memory for larger input arrays.

    Parameters
    ----------
    int_masks : np.ndarray
        An array of integer class labels.
        Each element in the array is an integer
        representing a class label.
    num_classes : int
        The number of distinct classes. This will determine the depth
        of the one-hot
        encoded dimension.

    Returns
    -------
    np.ndarray
        A one-hot encoded array with shape (n, num_classes), where n is
        the number of
        elements in `int_masks`. Each row in the output corresponds to
        a one-hot
        encoded version of the respective element in `int_masks`.

    """
    # Number of classes (0-5, so we have 6 classes)

    # Initialize the output array with zeros and the correct shape
    # (n, w, h, 6) where 6 is the number of classes

    new_mask = int_masks

    one_hot_encoded = np.zeros(
        new_mask.squeeze().shape[:] + (num_classes,), dtype=bool
    )

    # Flatten the labels array to use for indexing, labels are assumed to
    # be within the correct range
    indices = new_mask.flatten()
    # Calculate the linear indices in the flattened array which corresponds
    # to the position of 1s for one-hot encoding
    linear_indices = np.arange(indices.size) * num_classes + indices

    # Use flat indexing to set the appropriate elements to 1
    one_hot_encoded.ravel()[linear_indices] = 1
    return one_hot_encoded
