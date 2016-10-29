import json
import random

'''
    Attempt to generate a reasonable coloring of the world political map.

    My SVG map uses ccTLDs, my adjacency map uses these weird WAR codes,
    so first do some preprocessing to map between the two.

    Then (currently), greedily try to assign colors and see what happens.
    Turns out graph coloring is not a trivial problem - who knew.
'''


# grab TLD -> Name -> WAR mapping from CSV
names = {}
wars = {}
with open('filtered.csv') as f:
    for line in f:
        name, tld, war = [chunk.strip() for chunk in line.split(',')]
        wars[war] = tld
        names[tld] = name

# grab adjacencies
with open('country_adj.json') as f:
    war_adjacencies = json.load(f)

# convert to TLD adjacencies - some data is missing - oh well.
tld_adjacencies = {}
for key in war_adjacencies:
    if key not in wars:
        print 'ignoring', key
        continue

    tld = wars[key]
    tld_adjacencies[tld] = []
    for adjacent in war_adjacencies[key]:
        if adjacent in wars:
           tld_adjacencies[tld].append(wars[adjacent])


# Sanity check
print 'Adjacent to Canada:'
print ', '.join([names[tld] for tld in tld_adjacencies['.ca']])

print 'Adjacent to France:'
print ', '.join([names[tld] for tld in tld_adjacencies['.fr']])

colors = {
    '#FFCC32': set(),
    '#2BDF37': set(),
    '#FF3732': set(),
    '#4242D2': set(),
}
country_colors = {}

# shuffle the keys so we generate a new result each time
keys = tld_adjacencies.keys()
random.shuffle(keys)

# greedily attempt to color countries
for tld in keys:
    adjacents = tld_adjacencies[tld]
    neighbors_colors = set([country_colors[a] for a in adjacents if a in country_colors])
    if len(neighbors_colors) == len(colors):
        print 'impossible to color:', names[tld]
        print neighbors_colors
        print [names[a] for a in adjacents]
        continue

    color = next(iter(set(colors.keys()) - neighbors_colors))
    country_colors[tld] = color
    colors[color].add(tld)


# print out the resulting CSS styles
for c in colors:
    print '''
    {countries} {{
        fill: {color}
    }}
    '''.format(countries=', '.join(colors[c]), color=c)




