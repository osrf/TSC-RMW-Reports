#!/usr/bin/env python3

tests = [
    # RMW Hz, runs
    ('f', 80, 10),
    ('c', 80, 10),
    ('f', 100, 10),
    ('c', 100, 10),
    ('f', 120, 10),
    ('c', 120, 10),
]
rmw_names = {'f': 'FastRTPS', 'c': 'CycloneDDS'}
rmw_colors = {
    'f': [
        '#0000ff',
        '#0000ef',
        '#0000df',
        '#0000cf',
        '#0000bf',
        '#0000af',
        '#00009f',
        '#00008f',
        '#00007f',
        '#00006f',
    ],
    'c': [
        '#00ff00',
        '#00ef00',
        '#00df00',
        '#00cf00',
        '#00bf00',
        '#00af00',
        '#009f00',
        '#008f00',
        '#007f00',
        '#006f00',
    ]}
# data_by_frequency = {}
for rmw, frequency, runs in tests:
    rmw_name = rmw_names[rmw]
    print(rmw_name, 'with', frequency, 'hz', f'({runs} runs)')
    all_runs_sent = []
    all_runs_received = []
    for run in range(1, runs + 1):
        print('  run', run, '-', 'sent', 'vs', 'received')
        pub_file = f'{rmw}-p-{frequency}-{run}.txt'
        sub_file = f'{rmw}-s-{frequency}-{run}.txt'

        with open(pub_file, 'r') as h:
            pub_lines = h.read().splitlines()
        assert 'Topic name: Array60k' in pub_lines
        assert f'Publishing rate: {frequency}' in pub_lines
        assert 'Maximum runtime (sec): 30' in pub_lines
        assert 'Number of publishers: 1' in pub_lines
        assert 'Number of subscribers: 0' in pub_lines

        with open(sub_file, 'r') as h:
            sub_lines = h.read().splitlines()
        assert 'Topic name: Array60k' in sub_lines
        assert f'Publishing rate: {frequency}' in sub_lines
        assert 'Maximum runtime (sec): 30' in sub_lines
        assert 'Number of publishers: 0' in sub_lines
        assert 'Number of subscribers: 1' in sub_lines

        assert pub_lines[19].startswith('T_experiment,')
        assert pub_lines[49] == 'Maximum runtime reached. Exiting.'
        assert sub_lines[19].startswith('T_experiment,')
        assert sub_lines[49] == 'Maximum runtime reached. Exiting.'

        run_sent = []
        run_received = []
        for i in range(20, 49):
            pub_cols = pub_lines[i].split(',\t')
            sub_cols = sub_lines[i].split(',\t')
            # print(pub_cols[0], sub_cols[0])
            assert pub_cols[0].startswith('%d.' % (i - 18))
            assert sub_cols[0].startswith('%d.' % (i - 18))
            sent = pub_cols[3].strip()
            received = sub_cols[2].strip()
            print('   ', sent, received)
            run_sent.append(int(sent))
            run_received.append(int(received))
        all_runs_sent.append(run_sent)
        all_runs_received.append(run_received)

    import pandas
    data = {}
    for run in range(1, runs + 1):
        # data[f'Sent by Publisher #{run}'] = all_runs_sent[run - 1]
        # data[f'Received by Subscription #{run}'] = all_runs_received[run - 1]
        data[f'Run #{run}'] = all_runs_received[run - 1]
    tdf = pandas.DataFrame(data)
    tdf.index += 1  # Index from 1, since the index is really time in seconds
    ax = tdf.plot(kind='line', colors=rmw_colors[rmw])
    ax.set_title(
        f'Array60k @ {frequency} Hz - 1 to 1 Pub/Sub across wifi\n'
        f'{rmw_name}, reliable, volatile, keep_last@10')
    ax.set_xlabel('Time in Seconds')
    ax.set_ylabel('Number of Messages')
    ax.get_figure().savefig(f'{rmw}-{frequency}.png', bbox_inches='tight')

    print()
