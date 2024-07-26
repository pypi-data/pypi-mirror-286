


class Target():
    """
    Implementation of an articulatory target

    Parameters
    ----------

    m : float
        The linear slope parameter of the target.

    b : float
        The linear offset parameter of the target.

    tau : float
        The time constant of the target (in seconds).
        Describes the rate at which the target is approached.

    duration : float
        The target duration (in seconds).

    onset_state : float
        Describes the target contour onset. This values should be set only if the contour should
        start from a different value than the respective target value. The contour will then
        approach the target instead of following it exactly.


    Attributes
    ----------
    to_dict : dict
        Returns a dictionary representation of the target object.

    """ 
    def __init__(
        self,
        m: float = 0.0, 
        b: float = 1.0, 
        tau: float = 0.015,
        duration: float = 1.0, 
        onset_state: float = None,
        ):
        if tau <= 0.0:
            raise ValueError(
                f"""
                Time constant tau should be greater than 0.0,
                but a tau value of {tau} was passed.
                """
                )
        if duration <= 0.0:
            raise ValueError(
                f"""
                Duration should alwasy be greater than 0.0,
                but a duration value of {duration} was passed.
                """
                )
        self.m = m
        self.b = b
        self.tau = tau
        self.duration = duration
        self.onset_state = onset_state
        return
    
    def __str__(self) -> str:
        x = self.to_dict()
        return str( x )
    
    def to_dict(self):
        return {
            "m": float( self.m ),
            "b": float( self.b ),
            "tau": float( self.tau ),
            "duration": float( self.duration ),
            #"onset_state": self.onset_state,
        }