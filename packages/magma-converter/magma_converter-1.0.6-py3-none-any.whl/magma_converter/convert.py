import os
import pandas as pd

from datetime import datetime, timedelta
from obspy import read, Stream, UTCDateTime
from typing import Any, Dict, List, Self
from .sds import SDS
from .utilities import (
    validate_date,
    validate_directory_structure,
    trimming_trace
)


class Convert:
    def __init__(self, input_dir: str, directory_structure: str, network: str = 'VG',
                 min_completeness: float = 70, station: str = '*', channel: str = '*',
                 location: str = '*', output_directory: str = None,):
        """Seismic convert class

        Convert CVGHM various seismic data structure into Seiscomp Data Structure (SDS)

        Args:
            input_dir (str): input directory path
            directory_structure (str): input directory structure
            network (str): input network name
            station (str): input station name
            channel (str): input channel name
            location (str): input location name
        """
        self.input_dir = input_dir
        self.directory_structure = validate_directory_structure(directory_structure)
        self.output_dir = output_directory
        self.network = network
        self.station = station
        self.channel = channel
        self.location = location
        self.select = {
            'network': network,
            'station': station,
            'location': location,
            'component': channel,
        }

        self.new_channel: str | None = None
        self.min_completeness: float = min_completeness
        self.success: list[Dict[str, Any]] = []
        self.failed: list[Dict[str, Any]] = []

    def one_day(self, date_str: str) -> Self:
        """Convert one day of data.

        Args:
            date_str (str): Date format in yyyy-mm-dd

        Returns:
            Self
        """
        validate_date(date_str)
        self.run(date_str)
        return self

    def between_dates(self, start_date: str, end_date: str) -> Self:
        """Convert seismic between two range of dates.

        Args:
            start_date (str): start date in yyyy-mm-dd
            end_date (str): end date in yyyy-mm-dd

        Returns:
            Self
        """
        dates = pd.date_range(start_date, end_date)

        for _date in dates:
            date_str: str = _date.strftime('%Y-%m-%d')
            self.one_day(date_str)

        return self

    def run(self, date_str: str, **kwargs) -> None:
        """Convert for specific date.

        Args:
            date_str (str): Date format in yyyy-mm-dd
            **kwargs (dict): Keyword arguments save in Obspy

        Returns:
            None
        """
        min_completeness = self.min_completeness
        stream = self.search(date_str)
        for trace in stream:

            if trace.stats.channel[0] not in ['M', 'O']:
                sds: SDS = SDS(
                    output_dir=self.output_dir,
                    directory_structure=self.directory_structure,
                    trace=trace,
                    date_str=date_str,
                    channel=self.channel,
                    station=self.station,
                    location=self.location,
                    network=self.network,
                )

                if sds.save(min_completeness=min_completeness, **kwargs):
                    self.success.append(sds.results)
                else:
                    self.failed.append(sds.results)

    def merged(self, stream: Stream, date_str: str) -> Stream:
        """Merging seismic data into daily seismic data.

        Args:
            stream (Stream): Stream object
            date_str (str): Date in yyyy-mm-dd format

        Returns:
            Stream: Stream object
        """
        start_time: UTCDateTime = UTCDateTime(date_str)
        end_time: UTCDateTime = UTCDateTime(date_str) + timedelta(days=1)
        return trimming_trace(stream, start_time, end_time)

    def sac(self, date_str: str) -> Stream:
        """Read SAC data structure.

        <earthworm_dir>/ContinuousSAC/YYYYMM/YYYYMMDD_HHMM00_MAN/<per_channel>

        Args:
            date_str (str): Date format in yyyy-mm-dd

        Returns:
            Stream: Stream object
        """
        import warnings
        warnings.filterwarnings("error")

        channels: List[str] = [self.channel]
        if (self.channel == '*') or (self.channel is None):
            channels: List[str] = ['H*', 'EH*']

        date_str: str = date_str.replace('-', '')
        date_str = f"{date_str}*"
        date_yyyy_mm: str = date_str[0:6]

        stream: Stream = Stream()

        for channel in channels:
            seismic_dir: str = os.path.join(self.input_dir, date_yyyy_mm, date_str, f"*{channel}*")
            try:
                temp_stream: Stream = read(seismic_dir)
                stream = stream + temp_stream
            except Exception as e:
                print(f'⛔ {date_str} - self.sac() with channel: {channel}:: {e}')
                pass

        return stream

    def seisan(self, date_str: str) -> Stream:
        """Read seisan data structure.

        Args:
            date_str (str): Date format in yyyy-mm-dd

        Returns:
            Stream: Stream object
        """
        import warnings
        warnings.filterwarnings("error")

        wildcard: str = "{}*".format(date_str)
        seismic_dir: str = os.path.join(self.input_dir, wildcard)

        try:
            stream: Stream = read(seismic_dir)
            stream = stream.select(**self.select)
            return stream
        except Exception as e:
            print(f'⛔ {date_str} - self.seisan():: {e}')
            return Stream()

    def ijen(self, date_str: str) -> Stream:
        """Read Ijen seismic directory

        <seismic_dir>/YYYY/YYYYMMDD/Set00/<per_channel>

        Args:
            date_str (str): Date format in yyyy-mm-dd

        Returns:
            Stream: Stream object
        """
        input_dir = self.input_dir
        stream = Stream()

        current_day_obj = datetime.strptime(date_str, '%Y-%m-%d')
        current_year: str = current_day_obj.strftime('%Y')
        current_yyyymmdd: str = current_day_obj.strftime('%Y%m%d')

        seismic_dir: str = os.path.join(input_dir, current_year, current_yyyymmdd)

        if os.path.exists(seismic_dir):
            try:
                current_dir: str = os.path.join(seismic_dir, '*', '{}*'.format(date_str))
                stream: Stream = read(current_dir)
            except Exception as e:
                print(f'⛔ {date_str} - self.ijen():: {e}')
                return stream

        if stream.count() > 0:
            next_day_obj = current_day_obj + timedelta(days=1)
            next_day_year: str = next_day_obj.strftime('%Y')
            next_day_yyyymmdd: str = next_day_obj.strftime('%Y%m%d')

            try:
                next_dir: str = os.path.join(input_dir, next_day_year, next_day_yyyymmdd,
                                             '*', '{}-2350-*'.format(date_str))
                next_stream = read(next_dir)
                stream: Stream = stream + next_stream
            except:
                return stream

        return stream

    def search(self, date_str: str) -> Stream:
        """Search seismic data structure.

        Args:
            date_str (str): Date format in yyyy-mm-d

        Returns:
            Stream: Stream object
        """
        stream: Stream = Stream()
        directory_structure: str = self.directory_structure

        if directory_structure in ['ijen']:
            stream = self.ijen(date_str)

        if directory_structure in ['seisan', 'ibu', 'tambora']:
            stream = self.seisan(date_str)

        if directory_structure in ['sac', 'bromo']:
            stream = self.sac(date_str)

        print(f"👍 {date_str} :: Total {stream.count()} traces found.")

        return self.merged(stream, date_str)

    def fix_channel_to(self, new_channel: str) -> Self:
        """Fix channel name

        Args:
            new_channel (str): new channel name

        Returns:
            Self: Convert class
        """
        self.new_channel = new_channel
        return self
