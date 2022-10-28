# !/usr/bin/python3
# coding=utf-8


import itertools
from pydoc import cli


def hamming_distance(s1, s2):
    return sum(ch1 != ch2 for ch1, ch2 in zip(s1, s2))


def find_clusters(E, n, k):
    """
    Finner k klynger ved hjelp av kantene i E. Kantenen i E er på
    formatet (i, j, avstand), hvor i og j er indeksen til noden (dyret)
    kanten knytter sammen og avstand er Hamming-avstanden mellom
    gensekvensen til dyrene. Funksjonen returnerer en liste av k
    lister. Hvor de indre listene representerer en klynge og består av
    indeksene til nodene (dyrene). F.eks. har vi tre dyr som skal
    i to klynger, hvor dyr 0 og 2 ender i samme klynge returnerer
    funksjonen [[0, 2], [1]].

    :param E: Kanter i grafen på formatet (i, j, avstand). i og j er
              indeksen til dyrene kanten går mellom.
    :param n: Antall noder
    :param k: Antall klynger som ønskes
    :return: En liste av k lister.
    """

    print("-----------------------")

    E.sort(key=lambda x: x[2])

    print("E: ", E)
    print("n: ", n)
    print("k: ", k)

    mst = []
    nodes = [i for i in range(n)]

    nodes_in_mst = set()
    for i in range(min(n - 1, len(E))):
        u, v, w = E[i]
        if u not in nodes_in_mst or v not in nodes_in_mst or True:
            mst.append((u, v, w))
            nodes_in_mst.add(u)
            nodes_in_mst.add(v)

    print("mst: ", mst)

    for i in range(k - 1):
        mst.pop()

    print("mst: ", mst)
    print("nodes: ", nodes)

    clusters = []
    for edge in mst:
        u, v, _ = edge
        flatten = list(itertools.chain(*clusters))
        if u not in flatten and v not in flatten:
            clusters.append([u, v])
        elif u in flatten and v not in flatten:
            for cluster in clusters:
                if u in cluster:
                    cluster.append(v)
        elif u not in flatten and v in flatten:
            for cluster in clusters:
                if v in cluster:
                    cluster.append(u)

    flatten = list(itertools.chain(*clusters))

    for node in nodes:
        if node not in flatten:
            clusters.append([node])

    print("clusters: ", clusters)

    return clusters


def find_animal_groups(animals, k):
    # Lager kanter basert på Hamming-avstand
    E = []
    for i in range(len(animals)):
        for j in range(i + 1, len(animals)):
            E.append((i, j, hamming_distance(animals[i][1], animals[j][1])))

    # Finner klynger
    clusters = find_clusters(E, len(animals), k)

    # Gjøre om fra klynger basert på indekser til klynger basert på dyrenavn
    animal_clusters = [
        [animals[i][0] for i in cluster] for cluster in clusters
    ]
    return animal_clusters


tests = [
    (
        [
            ("Ugle", "CGAAGTTA"),
            ("Hauk", "CGATGTTA"),
            ("Hamster", "AAAATCAC"),
            ("Mus", "AAAATGAC"),
        ],
        2,
        6,
    ),
    ([("Ugle", "AGTC"), ("Ørn", "AGTA")], 2, 1),
    ([("Ugle", "CGGCACGT"), ("Elg", "ATTTGACA"), ("Hjort", "AATAGGCC")], 2, 8),
    (
        [("Ugle", "ATACTCAT"), ("Hauk", "AGTCTCAT"), ("Hjort", "CATGGCCG")],
        2,
        6,
    ),
    (
        [
            ("Ugle", "CAAACGAT"),
            ("Spurv", "CAGTCTAA"),
            ("Mus", "TCTGGACG"),
            ("Hauk", "CGAACTAT"),
        ],
        2,
        8,
    ),
    (
        [
            ("Ugle", "ATAACTCC"),
            ("Hauk", "TTACCTCC"),
            ("Hjort", "AGTGAACC"),
            ("Mus", "GTAGGACC"),
            ("Spurv", "ATGTCCCA"),
        ],
        3,
        4,
    ),
    (
        [
            ("Hauk", "CCTACTGATGACGCGC"),
            ("Ugle", "CCTAGTGATGAAGCAC"),
            ("Hjort", "ACTTTAACATCGCGGG"),
            ("Spurv", "ACGACTGATGAAGCAC"),
            ("Mus", "GTTAGACAATGGAGTG"),
            ("Rotte", "GTCGTACAATTGAGTG"),
        ],
        3,
        9,
    ),
    (
        [
            ("Ugle", "GGAGACCGGCTTCCTA"),
            ("Marsvin", "GCTACCTTGCTCACGT"),
            ("Hauk", "CGAGACCAGCTGCTGG"),
            ("Hjort", "GACATCTCTGTTCGGC"),
            ("Spurv", "GGAGACCGGCTTCCTG"),
            ("Rotte", "ACTACCTTGCGCACGA"),
            ("Mus", "TCTACCTTGCCCACGA"),
        ],
        3,
        10,
    ),
    (
        [
            ("Spurv", "TAGCAGTTCCTGAGAA"),
            ("Hjort", "ATGCATATCAGACGAT"),
            ("Ugle", "TAGCGATTTCAGAATT"),
            ("Rotte", "GACGGATTATTCCCCA"),
            ("Marsvin", "GAGGAATGGTAATCGC"),
            ("Hauk", "GATCGGTATCAGAACT"),
            ("Elg", "ATTCGTATAACCAAAG"),
            ("Mus", "GAGGGATGCTCCTCCC"),
        ],
        3,
        9,
    ),
    (
        [
            ("Katt", "CCGTGGTATCAAATAA"),
            ("Hjort", "TTACAGGCGGGCGTTC"),
            ("Hauk", "GGGAAATGAGCTTTCT"),
            ("Rotte", "ATCCTATAATGACCCT"),
            ("Elg", "TTGCATGCGGGCGATT"),
            ("Marsvin", "TTCGGCGGAGGTTCTA"),
            ("Mus", "ATCGGAGGAGGATCTC"),
            ("Ugle", "GGCTAGTGCGCTTTTT"),
            ("Spurv", "TGCCAGTCCGCTTTAT"),
        ],
        4,
        9,
    ),
    (
        [
            ("Hjort", "GATTACCCATGCTGGA"),
            ("Leopard", "TTTTCCTACCTAGTTA"),
            ("Ugle", "TCCCGGGAAGGGGATG"),
            ("Hauk", "TCCCAGCAAGGGGCTG"),
            ("Rotte", "CGCAGGACCGGAGGCA"),
            ("Spurv", "TCACGTGACGGGGGTG"),
            ("Katt", "TTTTCCTAACGGGTTA"),
            ("Mus", "CGCCGGAGCGAAACTA"),
            ("Elg", "GTATAGCTGTGCAGGA"),
            ("Marsvin", "AGCTGGGGCGTCAAGA"),
        ],
        4,
        9,
    ),
    (
        [
            ("Spurv", "AATCCCTGTAACGCGT"),
            ("Rotte", "CACCAGTCCGAGGAAC"),
            ("Leopard", "CACCCTATATCAAAGG"),
            ("Hauk", "AAATTGTCTCACGGGG"),
            ("Mus", "CACCACTCCTAGGAAC"),
            ("Elg", "ATGAGAGAGAGCTCCT"),
            ("Hjort", "ATGCTAGTGGGCCGCT"),
            ("Elefant", "TTTGAACAGTTTTAAT"),
            ("Marsvin", "AAGCCCTCAGAGCAAC"),
            ("Nesehorn", "TTTGACCAGTATTAAC"),
            ("Ugle", "AAAATGTCTAACGAGG"),
            ("Katt", "CACCCTATACCAAAGG"),
        ],
        5,
        9,
    ),
]

failed = False

for animals, k, optimal in tests:
    clusters = find_animal_groups(animals[:], k)

    test = "(animals={:}, k={:})".format(animals, k)
    if type(clusters) != list:
        print(
            "find_animal_groups skal returnere en liste av klynger. For testen "
            + "{:} gjorde ikke implementasjonen din dette. Den ".format(test)
            + "returnerte heller {:}.".format(clusters)
        )
        failed = True
        break

    if len(clusters) != k:
        print(
            "Implementasjonen din lage ikke riktig antall klynger for testen "
            + "{:}. Du lagde {:} klynger.".format(test, len(clusters))
        )
        failed = True
        break

    cluster_animals = [animal for cluster in clusters for animal in cluster]
    if len(cluster_animals) > len(animals):
        print(
            "Klyngene dine inneholder flere elementer enn det som finnes. "
            + "Du returnerte {:} for testen {:}.".format(clusters, test)
        )
        failed = True
        break

    if len(cluster_animals) > len(set(cluster_animals)):
        print(
            "Klyngene dine inneholder duplikater. Du returnerte "
            + "{:} for testen {:}.".format(clusters, test)
        )
        failed = True
        break

    if set(name for name, _ in animals) != set(cluster_animals):
        print(
            "Klyngene dine inneholder ikke alle dyrene eller inneholder også "
            + " andre dyr. Du returnerte "
            + "{:} for testen {:}.".format(clusters, test)
        )
        failed = True
        break

    lookup = {
        animal: index
        for index, cluster in enumerate(clusters)
        for animal in cluster
    }
    def t(x): return x[0] != x[1]
    sep_dist = min(
        sum(map(t, zip(a1[1], a2[1])))
        for a1, a2 in itertools.combinations(animals, 2)
        if lookup[a1[0]] != lookup[a2[0]]
    )
    if sep_dist < optimal:
        print(
            "Klyngene har ikke maksimal separasjonsavstand. Den maksimale "
            + "seperasjonsavstanden er {:}, men koden ".format(optimal)
            + "resulterte i en seperasjonsavstand på {:} ".format(sep_dist)
            + "for testen {:}".format(test)
        )
        failed = True
        break

if not failed:
    print("Koden fungerte for alle eksempeltestene.")
