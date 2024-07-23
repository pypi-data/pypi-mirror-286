#!/usr/bin/env python

import os
import sys
import itertools
from datetime import datetime
from collections import defaultdict

import toml
import click
from tabulate import tabulate
from click import confirm, style

import numpy as np

from nenucal import __version__, msutils
from nenucal import datahandler

from libpipe import worker, futils

t_file = click.Path(exists=True, dir_okay=False)

ms_file_to_check = 'table.info'


@click.group()
@click.version_option(__version__)
def main():
    ''' NenuFAR-CD data management utilities ...'''


@main.command('list')
@click.argument('obs_ids', type=str)
@click.option('--config', '-c', help='Data handler configuration file', type=t_file, default='data_handler.toml')
def list(obs_ids, config):
    ''' List all obs_ids '''
    dh = datahandler.DataHandler.from_file(config)

    header = ['Obs_id'] + [*dh.get_levels()]
    data = []

    for obs_id in dh.get_obs_ids(obs_ids):
        o = [obs_id]
        for level in dh.get_levels():
            counts = []
            for sw in dh.get_spectral_windows():
                mss = dh.get_ms_path(obs_id, level, sw)
                n_mss = len(mss)
                n_mss_exists = sum([os.path.exists(ms + f'/{ms_file_to_check}') for ms in mss])
                if n_mss == n_mss_exists:
                    counts.append(style(f'{n_mss}', fg='green'))
                elif n_mss_exists > 0:
                    counts.append(style(f'{n_mss_exists}', fg='yellow'))
                else:
                    counts.append(style(f'0', fg='red'))
            o.append(','.join(counts))
        data.append(o)

    print(tabulate(data, header))


@main.command('add')
@click.argument('obs_id', type=str)
@click.argument('nodes_distribution_id', type=str)
@click.option('--config', '-c', help='Data handler configuration file', type=t_file, default='data_handler.toml')
def add(obs_id, nodes_distribution_id, config):
    ''' Add obs_id '''
    dh = datahandler.DataHandler.from_file(config)

    if nodes_distribution_id not in dh.get_nodes_distribution():
        print(f'Error: nodes distribution ID {nodes_distribution_id} does not exist.')
        sys.exit(0)

    if obs_id in dh.get_obs_ids():
        print(f'Error: observation ID {obs_id} already exist.')
        sys.exit(0)

    nodes = dh.get_nodes_distribution()[nodes_distribution_id]

    if confirm(f'Adding {obs_id} with nodes {",".join(nodes)}'):
        s = toml.load(config, _dict=defaultdict)
        s['obs_ids'][obs_id] = nodes
        f = f'{config}.{datetime.now().strftime("%Y%m%d")}'
        backup_config = f
        i = 1
        while os.path.exists(backup_config):
            backup_config = f'{f}.{i}'
            i += 1

        os.rename(config, backup_config)

        with open(config, mode='w') as f:
            toml.dump(dict(s), f)

        print('Done !')

@main.command('add_all')
@click.argument('obs_ids', type=str, nargs=-1)
@click.option('--config', '-c', help='Data handler configuration file', type=t_file, default='data_handler.toml')
@click.option('--skip_existing', '-s', help='Skip existing OBS_ID', is_flag=True)
def add_all(obs_ids, config, skip_existing):
    ''' Add all obs_id '''
    dh = datahandler.DataHandler.from_file(config)
    s = toml.load(config, _dict=defaultdict)
    all_obs_ids = dh.get_obs_ids()

    for obs_id, nodes_distribution_id in zip(obs_ids, itertools.cycle(dh.get_nodes_distribution().keys())):
        if obs_id in all_obs_ids:
            print(f'Error: observation ID {obs_id} already exist.')
            if not skip_existing:
                sys.exit(0)

        nodes = dh.get_nodes_distribution()[nodes_distribution_id]
        print(f'Adding {obs_id} with nodes {",".join(nodes)} (ID: {nodes_distribution_id})')
        s['obs_ids'][obs_id] = nodes

    if len(obs_ids) > 0:
        if confirm('Confirm update ?'):
            f = f'{config}.{datetime.now().strftime("%Y%m%d")}'
            backup_config = f
            i = 1
            while os.path.exists(backup_config):
                backup_config = f'{f}.{i}'
                i += 1

            os.rename(config, backup_config)

            with open(config, mode='w') as f:
                toml.dump(dict(s), f)

            print('Done !')
        else:
            print('Changes discarded.')


@main.command('get_obs_ids')
@click.argument('obs_ids', type=str)
@click.option('--config', '-c', help='Data handler configuration file', type=t_file, default='data_handler.toml')
def get_obs_ids(obs_ids, config):
    ''' List all obs_ids (without existence check) '''
    dh = datahandler.DataHandler.from_file(config)

    print('\n'.join(dh.get_obs_ids(obs_ids)))


@main.command('get_ms')
@click.argument('level', type=str)
@click.argument('obs_ids', type=str)
@click.option('--config', '-c', help='Data handler configuration file', type=t_file, default='data_handler.toml')
@click.option('--sws', '-s', help='Spectral windows', type=str, default='all')
@click.option('--post_path', '-p', help='Add post_path to the path of the MS', type=str, default='')
def get_ms(level, obs_ids, config, sws, post_path):
    ''' Return a list of all MS corresponding to given OBS_IDS and SWS '''
    dh = datahandler.DataHandler.from_file(config)

    if post_path and not post_path.startswith('/'):
        post_path = '/' + post_path

    if sws == 'all':
        sws = dh.get_spectral_windows()
    else:
        sws = [k.upper() for k in sws.split(',')]

    for obs_id in dh.get_obs_ids(obs_ids):
        for sw in sws:
            print(f' '.join([f'{k}/{post_path}' for k in dh.get_ms_path(obs_id, level, sw)]), end=' ')


@main.command('remove')
@click.argument('level', type=str)
@click.argument('obs_ids', type=str)
@click.option('--config', '-c', help='Data handler configuration file', type=t_file, default='data_handler.toml')
@click.option('--sws', '-s', help='Spectral windows', type=str, default='all')
def remove(level, obs_ids, config, sws):
    ''' Remove all MS corresponding to given OBS_IDS and SWS '''
    dh = datahandler.DataHandler.from_file(config)

    if sws == 'all':
        sws = dh.get_spectral_windows()
    else:
        sws = [k.upper() for k in sws.split(',')]

    obs_ids = dh.get_obs_ids(obs_ids)

    if confirm(style(f'Removing obs_ids {",".join(obs_ids)} for SW {",".join(sws)} ?', fg='yellow')):
        for obs_id in obs_ids:
            for sw in sws:
                for ms in dh.get_ms_path(obs_id, level, sw):
                    futils.rm_if_exist(ms, verbose=True)
    else:
        print('No changes made.')


@main.command('retrieve')
@click.argument('remote_host', type=str)
@click.argument('obs_ids', type=str)
@click.option('--config', '-c', help='Data handler configuration file', type=t_file, default='data_handler.toml')
@click.option('--dry_run', help='Run in dry mode', is_flag=True)
@click.option('--run_on_host', help='Run rsync on specified host', type=str, default='target_host')
@click.option('--sws', '-s', help='Spectral windows', type=str, default='all')
def retrieve(obs_ids, remote_host, config, dry_run, run_on_host, sws):
    ''' Return a list of all MS corresponding to given OBS_IDS and SWS '''
    dh = datahandler.DataHandler.from_file(config)
    assert remote_host in dh.get_remote_hosts(), f'Remote host {remote_host} needs to be defined in {config}'

    target_level = dh.get_remote_level(remote_host)
    target_host = dh.get_remote_host(remote_host)

    assert target_level in dh.get_levels(), f'{target_level} data level can be retrieved'

    all_hosts = dh.get_all_hosts()
    if run_on_host != 'target_host' and run_on_host not in all_hosts:
        all_hosts.append(run_on_host)

    if sws == 'all':
        sws = dh.get_spectral_windows()
    else:
        sws = [k.upper() for k in sws.split(',')]

    w = worker.WorkerPool(all_hosts, name='Transfert', max_tasks_per_worker=1, debug=dry_run, dry_run=dry_run)

    for obs_id in dh.get_obs_ids(obs_ids, include_n2_obs_ids=False):
        date = obs_id.split('_')[0]
        year = date[:4]
        month = date[4:6]

        remote_path = dh.get_remote_data_path(remote_host).replace('%YEAR%', year).replace('%MONTH%', month)
        remote_path = remote_path.replace('%OBS_ID%', obs_id)

        for sw in sws:
            files = ' '.join([f'{target_host}:{remote_path}/SB{sb}.MS' for sb in dh.get_sbs(sw)])
            target = dh.get_dir_path(obs_id, target_level, sw)
            if run_on_host =='target_host':
                node = dh.get_node(obs_id, sw)
            else:
                node = run_on_host

            for i in range(100):
                log_file = f'{target}/transfert_{i}.log'
                if not os.path.exists(log_file):
                    break

            if not os.path.exists(target):
                os.makedirs(target)

            cmd = f'rsync --progress -v -am {files} {target}'

            w.add(cmd, run_on_host=node, output_file=log_file)

    w.execute()


@main.command('l1_to_l2')
@click.argument('level', type=str)
@click.argument('obs_ids', type=str)
@click.option('--config', '-c', help='Data handler configuration file', type=t_file, default='data_handler.toml')
@click.option('--force', help='Force overwrite data if already exists', is_flag=True)
@click.option('--l1_level', help='L1 level name', type=str, default='L1')
@click.option('--max_concurrent', '-m', help='Maximum concurrent tasks on a node', type=int, default=1)
@click.option('--dry_run', help='Do not do anything', is_flag=True)
@click.option('--env_file', help='Environment file', type=str, default='~/.bashrc')
@click.option('--timeslot_multiple', help='Specify the multiple for time slots', type=int, default=5)
@click.option('--hosts', help='Lists of hosts', type=str, default=None)
def l1_to_l2(level, obs_ids, config, force, l1_level, max_concurrent, dry_run, env_file, timeslot_multiple, hosts):
    ''' Create L2 data (at level LEVEL) from L1 data for the given OBS_IDS'''
    dh = datahandler.DataHandler.from_file(config)
    assert 'L1' in dh.get_levels(), f'L1 data level needs to be defined'
    assert level in dh.get_levels(), f'{level} data level needs to be defined'

    env_file = os.path.expanduser(env_file)
    if not os.path.exists(env_file):
        env_file = None

    dppp_file = dh.get_l1_to_l2_config(level)

    if hosts is None:
        hosts = dh.get_all_hosts()
    else:
        hosts = worker.get_hosts(hosts)

    w = worker.WorkerPool(hosts, name='L1 to L2', max_tasks_per_worker=max_concurrent,
                          debug=dry_run, dry_run=dry_run, env_source_file=env_file)

    obs_ids, sws = dh.get_obs_ids_and_spectral_windows(obs_ids)

    for obs_id in obs_ids:
        for sw in sws:
            msins_list = dh.get_ms_path(obs_id, l1_level, sw)
            msins = ','.join(msins_list)
            spec_ms_process = []

            if dh.is_n2_obs_id(obs_id):
                ms_info = msutils.get_info_from_ms_files(msins_list)
                nodes = dh.get_n2_nodes(obs_id)
                msouts = dh.get_ms_path(obs_id, level, sw)
                n = len(nodes)
                if l1_level.upper().startswith('L2'):
                    spec_ms_process = zip(nodes, msins_list, msouts, [0] * n, [0] * n)
                else:
                    n_slots = (ms_info['end_time'] - ms_info['start_time']) // ms_info['int_time']

                    # Calculate approximate number of slots per node
                    approx_slots_per_node = n_slots // n

                    # Adjust to make it a multiple of timeslot_multiple
                    adjusted_slots_per_node = (approx_slots_per_node // timeslot_multiple) * timeslot_multiple

                    # Create starttimeslots, ensuring multiples of timeslot_multiple, except for the last one
                    starttimeslots = [0]
                    for i in range(1, n):
                        starttimeslot = starttimeslots[-1] + adjusted_slots_per_node
                        starttimeslots.append(starttimeslot)

                    # Ensure the last end time is correctly set
                    starttimeslots.append(n_slots)

                    n_times_slices = np.diff(starttimeslots)
                    starttimeslots = starttimeslots[:-1]
                    spec_ms_process = zip(nodes, [msins] * n, msouts, starttimeslots, n_times_slices)
            else:
                msout = dh.get_ms_path(obs_id, level, sw)[0]
                node = dh.get_node(obs_id, sw)
                spec_ms_process.append((node, msins, msout, 0, 0))

            for node, msins, msout, starttimeslot, ntimes in spec_ms_process:
                target, msout_name = os.path.split(msout)

                if os.path.exists(msout):
                    if force:
                        print(f'Warning: {msout} already exists')
                    else:
                        print(f'Error: {msout} already exists')
                        return 1

                if not os.path.exists(target):
                    os.makedirs(target)

                for i in range(1000):
                    log_file = f'{target}/l2_to_l1_{msout_name}_{i}.log'
                    if not os.path.exists(log_file):
                        break

                cmd = f'DP3 {os.path.abspath(dppp_file)} msin=[{msins}] msout={msout} msout.overwrite=true'
                if starttimeslot!= 0 or ntimes != 0:
                    cmd += f' msin.starttimeslot={int(starttimeslot)} msin.ntimes={int(ntimes)}'

                w.add(cmd, run_on_host=node, output_file=log_file)

    w.execute()


@main.command('make_ms_list')
@click.argument('level', type=str)
@click.argument('obs_ids', type=str)
@click.option('--config', '-c', help='Data handler configuration file', type=t_file, default='data_handler.toml')
@click.option('--target', help='Target directory', default='ms_lists')
def make_ms_list(level, obs_ids, config, target):
    ''' Make MS list for all OBS_IDS at level LEVEL '''
    dh = datahandler.DataHandler.from_file(config)
    assert level in dh.get_levels(), f'{level} data level needs to be defined'

    if not os.path.exists(target):
        os.makedirs(target)

    for obs_id in dh.get_obs_ids(obs_ids):
        for sw in dh.get_spectral_windows():
            ms = ' '.join(dh.get_ms_path(obs_id, level, sw))
            filepath = os.path.join(target, f'{obs_id}_{level}_{sw}')

            with open(filepath, 'w') as f:
                f.write(f'{ms}\n')
