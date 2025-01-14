# src/utils/barrier_conditions.py

def check_knock_out_barrier(current_path, barrier_level, barrier_type):
    """
    Example: for an up-and-out barrier, if the path ever goes above 'barrier_level',
    the option is knocked out.
    """
    if barrier_type == "up-and-out":
        return any(price > barrier_level for price in current_path)
    # Additional logic for other barrier types
    return False
