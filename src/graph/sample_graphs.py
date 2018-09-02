import math

inf = math.inf
graph_a = {
    'nodes':
        {
            '0': ('1', '4'),
            '1': ('2'),
            '2': ('1', '3'),
            '3': (),
            '4': ()
        },
    'weights':
        {
            ('0', '1'): 99,
            ('0', '4'): 99,
            ('1', '2'): 15,
            ('2', '1'): 15,
            ('2', '3'): 10
        },
    'minpath':
        {
            '0': [0, 99, 114, 124, 99],
            '1': [inf, 0, 15, 25, inf],
            '2': [inf, 15, 0, 10, inf],
            '3': [inf, inf, inf, 0, inf],
            '4': [inf, inf, inf, inf, 0]

        },
    'avgpath': 62.625,
    'diameter': 124,
    'mode_path_length': (99, 2)
}
