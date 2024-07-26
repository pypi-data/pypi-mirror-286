


import os
import gzip
import yaml
import numpy as np
import pandas as pd
from copy import deepcopy

from typing import List, Optional, Dict, Any, Union, Tuple, Iterable
try:
    from typing import Self  # Available in Python 3.11+
except ImportError:
    from typing_extensions import Self # Available in Python < 3.11


from target_approximation.target import Target
from target_approximation.filter import target_filter
from target_approximation.utils import state_plot_kwargs
from target_approximation.utils import finalize_plot
from target_approximation.utils import get_plot
from target_approximation.utils import get_plot_limits



class TargetSequence():

    def __init__(
            self,
            targets:
                Union[
                    Self,
                    Dict[ str, List[ Target ] ],
                    List[ List[ Target ] ],
                ],
            tiers: Optional[ List[ str ] ] = None,
            ):
        
        if isinstance( targets, TargetSequence ):
            if tiers is None:
                tiers = targets.tiers()
                targets = targets.targets
            else:
                # check if all tiers are in the target sequence
                if not all( [ tier in targets.tiers() for tier in tiers ] ):
                    raise ValueError(
                        f"""
                        Not all tiers in the tiers list are in the target sequence.
                        """
                        )
            tgs = dict()
            for tier in tiers:
                tgs[ tier ] = targets[ tier ]

        elif isinstance( targets, dict ):
            if tiers is None:
                tiers = list( targets.keys() )
                targets = targets
            else:
                # check if all tiers are in the target sequence
                if not all( [ tier in targets.keys() for tier in tiers ] ):
                    raise ValueError(
                        f"""
                        Not all tiers in the tiers list are in the target dict.
                        """
                        )
            tgs = dict()
            for tier in tiers:
                tgs[ tier ] = targets[ tier ]

        else:
            tgs = dict()
            if tiers is None:
                for idx, target in enumerate( targets ):
                    tgs[ idx ] = target
            else:
                if len( tiers ) != len( targets ):
                    raise ValueError(
                        f"""
                        The number of tier names ({len(tiers)}) must match
                        the number of tiers in targets: ({len(targets)}).
                        """
                        )
                for tier, target in zip( tiers, targets ):
                    tgs[ tier ] = target

        self.targets = tgs
        self.check_range()
        self.normalize()

        #self.onset_state

        return
    
    def __getitem__( self, index ):
        return self.targets[ index ]
    
    def __setitem__( self, index, value ):
        if isinstance( value, TargetSequence ):
            self.targets[ index ] = value[ index ]
        else:
            self.targets[ index ] = value
        return
    
    def __len__( self, ):
        return len( self.targets )
    
    def __iter__( self, ):
        return iter( self.targets )
    
    def __add__( self, other ):
        if set( self.tiers() ) != set( other.tiers() ):
            raise ValueError(
                f"""
                The tiers of the two target sequences do not match.
                """
                )
        new_tgs = [
            tgs + other.targets[ tier ]
            for tier, tgs in self.targets.items()
        ]
        return TargetSequence( new_tgs, tiers = self.tiers() )
    
    #def __radd__( self, other ):
    #    if set( self.tiers() ) != set( other.tiers() ):
    #        raise ValueError(
    #            f"""
    #            The tiers of the two target sequences do not match.
    #            """
    #            )
    #    new_tgs = [
    #        tgs + other.targets[ tier ]
    #        for tier, tgs in self.targets.items()
    #    ]
    #    return TargetSequence( new_tgs, tiers = self.tiers() )
    
    def __and__( self, other ):
        #print( other )
        tgs = deepcopy( self.targets )
        #print( tgs )
        tgs.update( other.targets )
        return TargetSequence( tgs.values(), tiers = tgs.keys() )
    
    #def __rand__( self, other ):
    #    tgs = deepcopy( other.targets )
    #    tgs.update( self.targets )
    #    return TargetSequence( tgs.values(), tiers = tgs.keys() )

    
    #def __mul__( self, other ):
    #    return TargetSequence( self.targets * other )
    
    #def __rmul__( self, other ):
    #    return TargetSequence( self.targets * other )
    
    #def __repr__( self, ):
    #    return str( self.targets )
    
    def __str__( self, ):
        columns = [
            'slope',
            'offset',
            'time_constant',
            'duration',
            ]
        string = []
        for tier, tgs in self.targets.items():
            tgs_df = pd.DataFrame( [
                    [
                        tg.m,
                        tg.b,
                        tg.tau,
                        tg.duration,
                        ]
                    for tg in tgs
                ],
                columns = columns,
                )
            string.append(
                f'{tier}:\n'+ tgs_df.to_string() + '\n'
                )

        return '\n'.join( string )
    
    @classmethod
    def from_offsets(
            cls,
            #m: np.ndarray = None,
            b: np.ndarray,
            tau: np.ndarray,
            duration: np.ndarray,
            tiers = None,
            ):
        # b should have shape (n_tiers, n_targets) or (n_targets,)
        # tau should have shape (n_tiers, n_targets) or (n_targets,) or (1,)
        # duration should have shape (n_tiers, n_targets) or (n_targets,)
        if not isinstance( b, np.ndarray ):
            try:
                b = np.array( b )
            except Exception as e:
                raise ValueError(
                    f"""
                    The arg b should be a numpy array,
                    or must be convertible to a numpy array.
                    """
                    )

        if len( b.shape ) == 1:
            b = b.reshape( 1, -1 )
        # broadcast tau to the shape of b if the dimensions require it
        #if isinstance( tau, ( int, float ) ):
        tau = np.broadcast_to( tau, b.shape )
        #if tau.shape == ( 1, ) or tau.shape == ( b.shape[ 1 ], ):
        #    tau = np.broadcast_to( tau, b.shape )
        # broadcast duration to the shape of b if the dimensions require it
        #if duration.shape == ( 1, ) or duration.shape == ( b.shape[ 1 ], ):
        duration = np.broadcast_to( duration, b.shape )
        m = np.zeros( b.shape )
        # concat m, b, tau and duration so that shape is ( n_tiers, 4, n_targets )
        data = np.stack( [ m, b, tau, duration ], axis = 1 )
        kwargs = dict(
            data = data,
            )
        if tiers is not None:
            kwargs[ 'tiers' ] = tiers
        return cls.from_numpy( **kwargs )

    @classmethod
    def from_numpy(
            cls,
            data: np.ndarray,
            onset_time: float = 0.0,
            onset_state: float = None,
            tiers = None,
            ):
        # data should have shape (n_tiers, 4, n_targets)
        if len( data.shape ) != 3:
            raise ValueError(
                f"""
                Data should have shape (n_tiers, n_channels, n_targets),
                but got shape {data.shape}.
                """
                )
        if data.shape[ 1 ] != 4:
            raise ValueError(
                f"""
                Dimension of n_channels must be 4 (m, b, tau, duration),
                but got dimension {data.shape[ 1 ]}.
                """
                )
        targets = []
        for tier in data:
            targets.append( [
                Target(
                    m = target_data[ 0 ],
                    b = target_data[ 1 ],
                    tau = target_data[ 2 ],
                    duration = target_data[ 3 ],
                    onset_state = onset_state,
                    )
                for target_data in tier.T
                ]
            )
        kwargs = dict(
            targets = targets,
            )
        if tiers is not None:
            kwargs[ 'tiers' ] = tiers
        return cls( **kwargs )
    
    @classmethod
    def from_dict( cls, x ):
        targets = dict()
        for tier, tgs in x.items():
            targets[ tier ] = [
                    Target( **tg )
                    for tg in tgs
                ]
        return cls( targets = targets )
    
    @classmethod
    def from_yaml( cls, file_path ):
        if file_path.endswith( '.yaml.gz' ):
            with gzip.open( file_path, 'rt' ) as f:
                x = yaml.load( f, Loader = yaml.FullLoader )
        else:
            with open( file_path, 'r' ) as f:
                x = yaml.load( f, Loader = yaml.FullLoader )
        return cls.from_dict( x )
    
    @classmethod
    def load(
            cls,
            file_path: str,
            ):
        if file_path.endswith( '.yaml' ):
            return cls.from_yaml( file_path )
        elif file_path.endswith( '.yaml.gz' ):
            return cls.from_yaml( file_path )
        else:
            raise ValueError(
                f"""
                The file extension should be .yaml or .yaml.gz,
                but got {file_path}.
                """
                )
        return
    
    def to_dict(
            self,
            ):
        x = dict()
        for tier, tgs in self.targets.items():
            x[ tier ] = [ tg.to_dict() for tg in tgs ]
        return x
    
    def to_numpy(
            self,
            sr: Union[ float, int ],
            file_path: Optional[ str ] = None,
            ):
        contour = self.contour( sr )
        x = np.array(
            [ c[ :, 1 ] for c in contour ]
        )
        if file_path is not None:
            if not os.path.exists(
                    os.path.dirname( file_path )
                    ):
                os.makedirs(
                    os.path.dirname( file_path ),
                    exist_ok=True,
                    )
            np.save( file_path, x )
        return x
    
    def to_series(
            self,
            sr: Optional[ float ] = None,
            ):
        x = TargetSeries.from_sequence( self, sr )
        return x
    
    def to_yaml(
            self,
            file_path,
            compress = False,
            ):
        x = self.to_dict()
        if compress:
            if not file_path.endswith( '.yaml.gz' ):
                file_path = file_path + '.yaml.gz'
            with gzip.open( file_path, 'wt' ) as f:
                yaml.dump( x, f, sort_keys=False )
        else:
            with open( file_path, 'w' ) as f:
                yaml.dump( x, f, sort_keys=False )
        return
        

    def boundaries(
            self,
            tier,
            ):
        tgs = self.targets[ tier ]
        boundaries = [ 0.0 ]
        for tg in tgs:
            boundaries.append(
                boundaries[ -1 ] + tg.duration
                )
        return boundaries

    def contour(
            self,
            sr: float = 500,
            sample_times = None,
            ):
        contour = []
        for tier, tgs in self.targets.items():
            contour.append(
                target_filter(
                    target_sequence = tgs,
                    sample_rate = sr,
                    onset_state = None,
                    sample_times = sample_times,
                    )
                )
        return contour

    def duration(
            self,
            tier = None,
            ):
        if tier is not None:
            duration = sum(
                [ tg.duration for tg in self.targets[ tier ] ]
                )
        else:
            duration = max(
                [ sum(
                    [ tg.duration for tg in tgs ] )
                    for _, tgs in self.targets.items()
                    ]
                )
        return duration
    
    def check_range(
            self,
            ):
        # tau should be > 0.0
        # duration should be > 0.0

        for tier, tgs in self.targets.items():
            for idx, tg in enumerate( tgs ):
                if tg.tau <= 0.0:
                    raise ValueError(
                        f"""
                        Time constant tau should be greater than 0.0,
                        but target {idx} in tier {tier} has a tau
                        value of {tg.tau}.
                        """
                        )
                if tg.duration <= 0.0:
                    raise ValueError(
                        f"""
                        Duration should alwasy be greater than 0.0,
                        but target {idx} in tier {tier} has a 
                        duration value of {tg.duration}.
                        """
                        )
        return
    
    def normalize(
            self,
            ):
        """
        This function checks if there are target sequences that are shorter
        than the longest target sequence. If a target sequence is shorter, a
        single target will be added to the end of the sequence with a duration
        so that the sequence has the same length as the longest sequence.
        The slope of that target will be 00 and the offset will be the last
        value of the previous target.
        """
        total_duration = self.duration()
        for tier, tgs in self.targets.items():
            tier_duration = self.duration( tier )
            if tier_duration < total_duration:
                tg = tgs[ -1 ]
                offset = tg.m * tg.duration + tg.b
                tgs.append(
                    Target(
                        m = 0.0,
                        b = offset,
                        tau = tg.tau,
                        duration = total_duration - tier_duration,
                        onset_state = None,
                        )
                    )
        return
        
    def plot(
            self,
            tiers = None,
            ax = None,
            plot_contours = True,
            plot_targets = True,
            **kwargs,
            ):
        if tiers is None:
            tiers = self.targets.keys()
        figure, ax = get_plot(
            n_rows = len(tiers),
            axs = ax
            )
        for idx, tier in enumerate( tiers ):
            tgs = self.targets[ tier ]
            if plot_targets:
                self.plot_targets( tgs, ax[ idx ] )
            if plot_contours:
                self.plot_contours( tgs, ax[ idx ] )
            ax[ idx ].set( ylabel = tier )
        # x label is Time [s], but only the last plot should have it
        ax[ -1 ].set( xlabel = 'Time [s]' )
        #ax[ 0 ].label_outer()
        finalize_plot(
            figure,
            ax,
            **kwargs,
            )
        return ax
    
    def plot_contours(
            self,
            tgs,
            ax,
            ):
        contour = target_filter(
            target_sequence = tgs,
            sample_rate = 500,
            onset_state = tgs[0].onset_state,
            )
        ax.plot(
            contour[ :, 0 ],
            contour[ :, 1 ],
            color = 'navy',
            )
        return ax

    def plot_targets(
            self,
            tgs,
            ax,
            ):
        onset_time = 0.0
        for tg in tgs:
            ax.axvline(
                onset_time,
                color = 'black',
                )
            x = [
                onset_time,
                onset_time + tg.duration,
                ]
            y = [
                tg.b,
                tg.m * tg.duration + tg.b,
                ]
            ax.plot(
                x,
                y,
                color = 'black',
                linestyle='--',
                )
            onset_time += tg.duration
        ax.axvline(
            onset_time,
            color = 'black',
            )
        return ax
    
    def m(
            self,
            x,
            tier = None,
            ):
        if tier is not None:
            tgs = self.targets[ tier ]
            for tg in tgs:
                tg.m = x
        else:
            for tgs in self.targets.values():
                for tg in tgs:
                    tg.m = x
        return

    def b(
            self,
            x,
            tier = None,
            ):
        if tier is not None:
            tgs = self.targets[ tier ]
            for tg in tgs:
                tg.b = x
        else:
            for tgs in self.targets.values():
                for tg in tgs:
                    tg.b = x
        return
    
    def tau(
            self,
            x,
            tier = None,
            ):
        if tier is not None:
            tgs = self.targets[ tier ]
            for tg in tgs:
                tg.tau = x
        else:
            for tgs in self.targets.values():
                for tg in tgs:
                    tg.tau = x
        return
    
    def extend(
            self,
            x,
            tier = None,
            padding = 'left',
            ):
        if padding == 'left':
            index = 0
        elif padding == 'right':
            index = -1
        else:
            raise ValueError(
                f"""
                Padding should be either 'left' or 'right',
                but got {padding}.
                """
                )
        def _pad( x, tier ):
            tg = Target(
                m = 0.0,
                b = self.targets[ tier ][ index ].b,
                tau = self.targets[ tier ][ index ].tau,
                duration = x,
                onset_state = None,
                )
            if padding == 'left':
                self.targets[ tier ].insert( 0, tg )
            else:
                self.targets[ tier ].append( tg )
            return
        if tier is not None:
            _pad( x, tier )
        else:
            for tier in self.targets.keys():
                _pad( x, tier )
        #self.normalize()
        return
    
    def save(
            self,
            file_path: str,
            ):
        if file_path.endswith( '.yaml' ):
            self.to_yaml( file_path )
        elif file_path.endswith( '.yaml.gz' ):
            self.to_yaml( file_path, compress=True )
        #elif file_path.endswith( '.npy' ):
        #    self.to_numpy( file_path )
        else:
            raise ValueError(
                f"""
                The file extension should be .yaml,
                but got {file_path}.
                """
                )
        return
    
    def tiers(
            self,
            ):
        return list( self.targets.keys() )



class TargetSeries():

    def __init__(
            self,
            series: Union[ Self, np.ndarray ],
            sr: float = None,
            tiers: List[ str ] = None,
            ):

        if isinstance( series, TargetSeries ):
            if tiers is not None:
                # check if all tiers are in the target series
                if not all( [ tier in series.tiers() for tier in tiers ] ):
                    raise ValueError(
                        f"""
                        Not all tiers in the tiers list are in the target series.
                        series.tiers: {series.tiers()}
                        tiers: {tiers}
                        """
                        )
            if sr is not None and sr != series.sr:
                raise ValueError(
                    f"""
                    The sampling rate of the target series does not
                    match the sampling rate provided as an argument.
                    """
                    )
            tiers = series.tiers()
            sr = series.sr
            series = series.to_numpy( transpose = False)
        
        elif not isinstance( series, np.ndarray ):
            try:
                series = np.array( series )
            except Exception as e:
                raise ValueError(
                    f"""
                    The arg series should be a numpy array,
                    or must be convertible to a numpy array.
                    """
                    )
        if len( series.shape ) == 1:
            series = series.reshape( -1, len( tiers ) )
        if tiers is None:
            tiers = [ f'tier_{i}' for i in range( series.shape[ -1 ] ) ]
        if len( set( tiers ) ) != len( tiers ):
            raise ValueError( 'tiers must be unique' )
        
        if len( tiers ) != series.shape[ -1 ]:
            raise ValueError(
                f"""
                The tiers and series must have the same length,
                but the tiers have length {len( tiers )} and the series
                has length {series.shape[ -1 ]}.
                """
                )
        self.series = pd.DataFrame( series, columns = tiers )
        self.sr = sr
        
        return
    
    def __len__( self, ):
        return len( self.series )
    
    def __iter__( self, ):
        return iter( self.series )
    
    #def __add__( self, other ):
    #    return TargetSequence( self.targets + other.targets )
    
    #def __radd__( self, other ):
    #    return TargetSequence( other.targets + self.targets )
    
    def __str__(self) -> str:
        return self.series.__str__()
    
    def __getitem__( self, index ):
        return self.series[ index ]
    
    def __setitem__( self, index, value ):
        self.series[ index ] = value
        return
    
    @classmethod
    def from_sequence(
            cls,
            sequence: TargetSequence,
            sr: float = None,
            tiers: List[ str ] = None,
            ):
        x = sequence.to_numpy( sr = sr )
        kwargs = dict(
            series = x.T,
            sr = sr,
            )
        if tiers is not None:
            kwargs[ 'tiers' ] = tiers
        return cls( **kwargs )
    
    def to_numpy(
            self,
            transpose = True,
            ):
        x = self.series.to_numpy()
        if transpose:
            x = x.T
        return x
    
    '''
    def plot(
            self,
            plot_type = 'trajectory',
            time = 'seconds',
            **kwargs,
            ):
        if plot_type in [ 'trajectory', 'trajectories', 'time' ]:
            return self.plot_trajectories( time = time, **kwargs )
        elif plot_type in [ 'distribution', 'distributions', 'dist', 'dists' ]:
            return self.plot_distributions( **kwargs )

    def plot_distributions(
            self,
            parameters = None,
            axs = None,
            n_columns = 5,
            plot_kwargs = state_hist_kwargs,
            **kwargs
            ):
        parameters = get_valid_tiers( parameters, self.tiers )
        n_rows = math.ceil( len( parameters ) / n_columns )
        figure, axs = get_plot(
            n_rows = n_rows,
            n_columns = n_columns,
            axs = axs,
            sharex = False,
            sharey = True,
            gridspec_kw = {},
            )
        index_row = 0
        index_col = 0
        for index, parameter in enumerate( parameters ):
            if index_col == n_columns:
                index_row += 1
                index_col = 0
            y = self[ parameter ]
            axs[ index_row, index_col ].hist( y, **plot_kwargs.get( parameter ) )
            axs[ index_row, index_col ].set( xlabel = parameter ) #, ylim = get_plot_limits( y ) )
            index_col += 1
        #for ax in axs:
        #    ax.label_outer()
        finalize_plot( figure, axs, hide_labels = False, **kwargs )
        return axs

    def plot_trajectories(
            self,
            parameters = None,
            axs = None,
            time = 'seconds',
            plot_kwargs = state_plot_kwargs,
            **kwargs,
            ):
        parameters = get_valid_tiers( parameters, self.tiers )
        #constants = vtl.get_constants()
        figure, axs = get_plot( n_rows = len( parameters ), axs = axs )
        for index, parameter in enumerate( parameters ):
            y = self[ parameter ]
            x = np.array( range( 0, len( y ) ) )
            if time == 'seconds':
                #x = x / constants[ 'samplerate_internal' ]
                x = x / (44100/110)
            axs[ index ].plot( x, y, **plot_kwargs.get( parameter ) )
            axs[ index ].set( ylabel = parameter, ylim = get_plot_limits( y ) )
        if time == 'seconds':
            plt.xlabel( 'Time [s]' )
        else:
            plt.xlabel( 'Frame' )
        #for ax in axs:
        #    ax.label_outer()
        finalize_plot( figure, axs, **kwargs )
        return axs
    '''
    
    def tiers( self ):
        return self.series.columns.tolist()