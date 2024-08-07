"""
:script: processing/preprocess/smooth_timeseries.py
:auth: Nathan T. Stevens
:email: ntsteven@uw.edu
:license: CC-BY-4.0
:purpose: Apply a gaussian smoothing kernel to timeseries data
        to remove high frequency noise arising from CRSD control systems'
        latency between measurements and servo response.

"""

import argparse, logging
import pandas as pd
import numpy as np

Logger = logging.getLogger('smooth_timeseries.py')

def main():
    parser = argparse.ArgumentParser(
        prog='smooth_timeseries.py',
        description='use a moving window z-score metric to remove anomalous spikes in data'
    )
    parser.add_argument(
        '-i',
        '--input',
        action='store',
        dest='input_file',
        default=None,
        help='path and filename of file to smooth',
        type=str
    )
    parser.add_argument(
        '-o',
        '--output',
        action='store',
        dest='output_file',
        default='tmp_smoothed_data.csv',
        help='path and filename of file to save results to',
        type=str
    )
    # parser.add_argument(
    #     '-n',
    #     '--niter',
    #     dest='niter',
    #     default=3,
    #     help='number of smoothing iterations to apply',
    #     type=int
    # )
    parser.add_argument(
        '-s',
        '--stdev',
        action='store',
        dest='std',
        default=75,
        help='standard deviation used to scale the gaussian weighting window for the rolling mean '+\
             'should be some positive scalar less than the window length (see --window).'+\
             'Defaults to 75',
        type=int
    )
    parser.add_argument(
        '-w',
        '--window',
        dest='window',
        help='smoothing window length in **samples**. Defaults to 600',
        default=600,
        type=int
    )
    args = parser.parse_args()
    Logger.info(f'loading data from: {args.input_file}')
    Logger.info(f'writing data to: {args.output_file}')
    Logger.info(f'using a window length of {args.window} sec')
    # Logger.info(f'running {args.niter} iterations of window-centered boxcar smoothing')
    # Load data
    df = pd.read_csv(args.input_file)
    # Populate Timestamp index
    df.index = pd.to_datetime(df.Epoch_UTC, unit='s')
    df = df.drop(['Epoch_UTC'], axis=1)
    Logger.info('data loaded')
    # Iterate for the number of smoothing passes
    # fields = [c_ for c_ in df.columns if c_ != 'Epoch_UTC']
    df_out = df.copy()
    Logger.info('running smoothing')
    # for _n in range(args.niter):
    # Logger.info(f'...iteration {_n+1}/{args.niter}...')
    df_out = df_out.rolling(
        window=args.window,
        center=True,
        win_type='gaussian',
        min_periods=3).mean(std=args.std)
    # df_out.index -= pd.Timedelta(args.window/2, unit='seconds')
    # df_out = df_out[(df_out.index >= df.index.min()) & 
    #                 (df_out.index <= df.index.max())]
    # Logger.info('getting window-centered epoch values')
    df_out = df_out.assign(Epoch_UTC = [x.timestamp() for x in df_out.index])
    # df_out = df_out.assign(epoch=lambda x: (x.index - pd.Timestamp('1970-1-1')).total_seconds())
    Logger.info('writing data to disk')
    df_out.to_csv(args.output_file, header=True, index=False)
    Logger.info('data written to disk - concluding main')


if __name__ == '__main__':
    ch = logging.StreamHandler()                                                            
    fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(fmt)
    Logger.addHandler(ch)
    Logger.setLevel(logging.INFO)
    main()