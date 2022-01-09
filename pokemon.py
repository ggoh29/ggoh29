import pandas
import torch
import pandas as pd
import requests
from bs4 import BeautifulSoup
import itertools
import numpy as np
root_prefix = "~/Downloads"

pokemon_types = ['normal', 'fire' ,'water', 'grass', 'electric', 'ice', 'fighting', 'poison', 'ground', 'flying', 'psychic',
                 'bug', 'rock', 'ghost', 'dark', 'dragon', 'steel', 'fairy']
pokemon_type_map = {type : index for index, type in enumerate(pokemon_types)}

three_stage = [[0, 1, 2],
               [3, 4, 5],
               [6, 7, 8],
               [9, 10, 11],
               [12, 13, 14],
               [15, 16, 17],
               [171, 24, 25],
               [28, 29, 30],
               [31, 32, 33],
               [172, 34, 35],
               [173, 38, 39],
               [40, 41, 168],
               [42, 43, 44],
               [42, 43, 181],
               [59, 60, 61],
               [62, 63, 64],
               [65, 66, 67],
               [68, 69, 70],
               [73, 74, 75],
               [80, 81, 461],
               [91, 92, 93],
               [110, 111, 464],
               [439, 112, 241],
               [115, 117, 229],
               [438, 121, 865],
               [238, 124, 465],
               [239, 125, 466],
               [136, 232, 473],
               [146, 147, 148],
               [151, 152, 153],
               [154, 155, 156],
               [157, 158, 159],
               [174, 175, 467],
               [178, 179, 180],
               [297, 182, 183],
               [186, 187, 188],
               [219, 220, 472],
               [245, 246, 247],
               [251, 252, 253],
               [254, 255, 256],
               [257, 258, 259],
               [262, 263, 861],
               [264, 265, 266],
               [264, 267, 268],
               [269, 270, 271],
               [272, 273, 274],
               [279, 280, 281],
               [279, 280, 474],
               [286, 288, 289],
               [292, 293, 294],
               [303, 304, 305],
               [405, 314, 406],
               [327, 328, 329],
               [354, 355, 476],
               [362, 363, 364],
               [370, 371, 372],
               [373, 374, 375],
               [386, 387, 388],
               [389, 390, 391],
               [392, 393, 394],
               [395, 396, 397],
               [402, 403, 404],
               [442, 443, 444],
               [494, 495, 496],
               [497, 498, 499],
               [500, 501, 502],
               [505, 506, 507],
               [518, 519, 520],
               [523, 524, 525],
               [531, 532, 533],
               [534, 535, 536],
               [539, 540, 541],
               [542, 543, 544],
               [550, 551, 552],
               [573, 574, 575],
               [576, 577, 578],
               [581, 582, 583],
               [598, 599, 600],
               [601, 602, 603],
               [606, 607, 608],
               [609, 610, 611],
               [632, 633, 634],
               [649, 650, 651],
               [652, 653, 654],
               [655, 656, 657],
               [660, 661, 662],
               [663, 664, 665],
               [668, 669, 670],
               [678, 679, 680],
               [703, 704, 705],
               [721, 722, 723],
               [724, 725, 726],
               [727, 728, 729],
               [730, 731, 732],
               [735, 736, 737],
               [760, 761, 762],
               [781, 782, 783],
               [788, 789, 790],
               [788, 789, 791],
               [809, 810, 811],
               [812, 813, 814],
               [815, 816, 817],
               [820, 821, 822],
               [823, 824, 825],
               [836, 837, 838],
               [855, 856, 857],
               [858, 859, 860],
               [884, 885, 886]]

kanto = ['route-1', 'route-2', 'route-3', 'route-4', 'route-5', 'route-6', 'route-7', 'route-8', 'route-9', 'route-10',
         'route-11', 'route-12', 'route-13', 'route-14', 'route-15', 'route-16', 'route-17', 'route-18', 'route-19',
         'route-20', 'route-21', 'route-22', 'route-23', 'route-24', 'route-25', 'route-26', 'route-27', 'route-28',
         'berry-forest', 'bond-bridge', 'canyon-entrance', 'cape-brink', 'celadon-city', 'cerulean-cave', 'cerulean-city',
         'cinnabar-island', 'digletts-cave', 'five-island', 'five-isle-meadow', 'four-island', 'fuchsia-city',
         'green-path', 'icefall-cave', 'indigo-plateau', 'kindle-road', 'lavender-town', 'lost-cave', 'memorial-pillar',
         'mt-ember', 'mt-moon', 'navel-rock', 'one-island', 'outcast-island', 'pallet-town', 'pattern-bush', 'pewter-city',
         'pokemon-mansion', 'pokemon-tower', 'power-plant', 'resort-gorgeous', 'roaming', 'rock-tunnel',
         'ruin-valley', 'safari-zone', 'saffron-city', 'seafoam-islands', 'sevault-canyon', 'silph-co', 'tanoby-ruins',
         'three-isle-port', 'tohjo-falls', 'trainer-tower', 'treasure-beach', 'underground-path-5-6', 'vermilion-city',
         'victory-road', 'viridian-city', 'viridian-forest', 'water-labyrinth', 'water-path']

johto = ['route-29', 'route-30', 'route-31', 'route-32', 'route-33', 'route-34', 'route-35', 'route-36', 'route-37',
         'route-38', 'route-39', 'route-40', 'route-41', 'route-42', 'route-43', 'route-44', 'route-45', 'route-46',
         'route-47', 'route-48', 'azalea-town', 'bell-tower', 'blackthorn-city', 'burned-tower', 'cherrygrove-city',
         'cianwood-city', 'cliff-cave', 'cliff-edge-gate', 'dark-cave', 'dragons-den', 'ecruteak-city', 'embedded-tower',
         'goldenrod-city', 'ice-path', 'ilex-forest', 'lake-of-rage', 'mt-mortar', 'mt-silver', 'national-park',
         'new-bark-town', 'olivine-city', 'roaming', 'ruins-of-alph', 'safari-zone-gate', 'sinjoh-ruins',
         'slowpoke-well', 'sprout-tower', 'team-rocket-hq', 'tin-tower', 'union-cave', 'violet-city', 'whirl-islands']

hoenn = ['route-101', 'route-102', 'route-103', 'route-104', 'route-105', 'route-106', 'route-107', 'route-108',
         'route-109', 'route-110', 'route-111', 'route-112', 'route-113', 'route-114', 'route-115', 'route-116',
         'route-117', 'route-118', 'route-119', 'route-120', 'route-121', 'route-122', 'route-123', 'route-124',
         'route-125', 'route-126', 'route-127', 'route-128', 'route-129', 'route-130', 'route-131', 'route-132',
         'route-133', 'route-134', 'abandoned-ship', 'altering-cave', 'artisan-cave', 'battle-resort', 'battle-tower',
         'birth-island', 'cave-of-origin', 'desert-underpass', 'dewford-town', 'evergrande-city', 'faraway-island',
         'fiery-path', 'fortree-city', 'granite-cave', 'jagged-pass', 'lilycove-city', 'littleroot-town', 'marine-cave',
         'mauville-city', 'meteor-falls', 'mirage-island', 'mirage-spots', 'mirage-tower', 'mossdeep-city', 'mt-pyre',
         'new-mauville', 'pacifidlog-town', 'petalburg-city', 'petalburg-woods', 'roaming', 'rustboro-city',
         'rusturf-tunnel', 'safari-zone', 'scorched-slab', 'sea-mauville', 'seafloor-cavern', 'sealed-chamber',
         'shoal-cave', 'sky-pillar', 'slateport-city', 'sootopolis-city', 'southern-island', 'team-magma-aqua-hideout',
         'terra-cave', 'victory-road']

sinnoh = ['route-201', 'route-202', 'route-203', 'route-204', 'route-205', 'route-206', 'route-207', 'route-208',
          'route-209', 'route-210', 'route-211', 'route-212', 'route-213', 'route-214', 'route-215', 'route-216',
          'route-217', 'route-218', 'route-219', 'route-220', 'route-221', 'route-222', 'route-223', 'route-224',
          'route-225', 'route-226', 'route-227', 'route-228', 'route-229', 'route-230', 'acuity-lakefront',
          'big-bluff-cavern', 'bogsunk-cavern', 'canalave-city', 'celestic-town', 'dazzling-cave', 'distortion-world',
          'eterna-city', 'eterna-forest', 'floaroma-meadow', 'flower-paradise', 'fountainspring-cave', 'fuego-ironworks',
          'glacial-cavern', 'grassland-cave', 'great-marsh', 'hall-of-origin', 'icy-cave', 'iron-island', 'lake-acuity',
          'lake-valor', 'lake-verity', 'lost-tower', 'mt-coronet', 'newmoon-island', 'old-chateau', 'oreburgh-city',
          'oreburgh-gate', 'oreburgh-mine', 'pastoria-city', 'pokemon-league', 'ravaged-path', 'resort-area',
          'riverbank-cave', 'roaming', 'rocky-cave', 'maniac-tunnel', 'sandsear-cave', 'sendoff-spring',
          'snowpoint-city', 'snowpoint-temple', 'solaceon-ruins', 'spacious-cave', 'spear-pillar', 'stargleam-cavern',
          'stark-mountain', 'still-water-cavern', 'sunlit-cavern', 'sunyshore-city', 'swampy-cave', 'trophy-garden',
          'turnback-cave', 'twinleaf-town', 'typhlo-cavern', 'valley-windworks', 'valor-lakefront', 'veilstone-city',
          'victory-road', 'volcanic-cave', 'wayward-cave', 'whiteout-cave']

unova = ['route-1', 'route-2', 'route-3', 'route-4', 'route-5', 'route-6', 'route-7', 'route-8', 'route-9', 'route-10',
         'route-11', 'route-12', 'route-13', 'route-14', 'route-15', 'route-16', 'route-17', 'route-18', 'route-19',
         'route-20', 'route-21', 'route-22', 'route-23', 'abundant-shrine', 'accumula-town', 'aspertia-city',
         'castelia-city', 'castelia-sewers', 'celestial-tower', 'challengers-cave', 'chargestone-cave', 'clay-tunnel',
         'cold-storage', 'desert-resort', 'dragonspiral-tower', 'dreamyard', 'driftveil-city', 'driftveil-drawbridge',
         'floccesy-ranch', 'giant-chasm', 'humilau-city', 'icirrus-city', 'liberty-island', 'lostlorn-forest',
         'marvelous-bridge', 'mistralton-cave', 'moor-of-icirrus', 'ns-castle', 'nacrene-city', 'nature-preserve',
         'nature-sanctuary', 'nuvema-town', 'p2-laboratory', 'pinwheel-forest', 'relic-castle', 'relic-passage',
         'reversal-mountain', 'roaming', 'seaside-cave', 'strange-house', 'striaton-city', 'twist-mountain',
         'undella-bay', 'undella-town', 'underground-ruins', 'victory-road', 'village-bridge', 'virbank-city',
         'virbank-complex', 'wellspring-cave', 'white-forest']

kalos =['route-2', 'route-3', 'route-4', 'route-5', 'route-6', 'route-7', 'route-8', 'route-9', 'route-10', 'route-11',
        'route-12', 'route-13', 'route-14', 'route-15', 'route-16', 'route-17', 'route-18', 'route-19', 'route-20',
        'route-21', 'route-22', 'ambrette-town', 'aquacorde-town', 'azure-bay', 'camphrier-town', 'connecting-cave',
        'coumarine-city', 'cyllage-city', 'frost-cavern', 'geosenge-town', 'glittering-cave', 'laverre-city', 'lost-hotel',
        'lumiose-city', 'parfum-palace', 'pokemon-village', 'reflection-cave', 'roaming', 'santalune-city',
        'santalune-forest', 'sea-spirits-den', 'shalour-city', 'snowbelle-city', 'team-flare-hq', 'terminus-cave',
        'tower-of-mastery', 'unknown-dungeon', 'vaniville-town', 'victory-road']

alola = ['route-1', 'route-2', 'route-3', 'route-4', 'route-5', 'route-6', 'route-7', 'route-8', 'route-9', 'route-10',
         'route-11', 'route-12', 'route-13', 'route-14', 'route-15', 'route-16', 'route-17', 'aether-paradise',
         'akala-outskirts', 'altar-of-the-moone', 'altar-of-the-sunne', 'ancient-poni-path', 'berry-fields',
         'blush-mountain', 'brooklet-hill', 'digletts-tunnel', 'dividing-peak-tunnel', 'exeggutor-island',
         'haina-desert', 'hano-beach', 'hauoli-cemetery', 'hauoli-city', 'heahea-beach', 'heahea-city', 'iki-town',
         'kalae-bay', 'konikoni-city', 'lake-of-the-moone', 'lake-of-the-sunne', 'lush-jungle', 'mahalo-trail',
         'malie-city', 'malie-garden', 'melemele-meadow', 'melemele-sea', 'memorial-hill', 'mount-hokulani',
         'mount-lanakila', 'paniola-ranch', 'paniola-town', 'poke-pelago', 'poni-breaker-coast', 'poni-coast',
         'poni-gauntlet', 'poni-grove', 'poni-meadow', 'poni-plains', 'poni-wilds', 'resolution-cave', 'royal-avenue',
         'ruins-of-abundance', 'ruins-of-conflict', 'ruins-of-hope', 'ruins-of-life', 'sandy-cave', 'seafolk-village',
         'seaward-cave', 'secluded-shore', 'tapu-village', 'team-rockets-castle', 'ten-carat-hill', 'thrifty-megamart',
         'ula-ula-beach', 'ulaula-meadow', 'ultra-megalopolis', 'ultra-space', 'ultra-space-wilds', 'vast-poni-canyon',
         'verdant-cavern', 'wela-volcano-park']

galar = ['route-1', 'route-2', 'route-3', 'route-4', 'route-5', 'route-6', 'route-7', 'route-8', 'route-9', 'route-10',
         'axews-eye', 'ballimere-lake', 'brawlers-cave', 'bridge-field', 'challenge-beach', 'challenge-road',
         'courageous-cavern', 'dappled-grove', 'dusty-bowl', 'east-lake-axewell', 'fields-of-honor', 'forest-of-focus',
         'frigid-sea', 'frostpoint-field', 'galar-mine', 'galar-mine-no-2', 'giants-bed', 'giants-cap', 'giants-foot',
         'giants-mirror', 'giants-seat', 'glimwood-tangle', 'hammerlocke-hills', 'honeycalm-island', 'honeycalm-sea',
         'hulbury', 'insular-sea', 'lake-of-outrage', 'lakeside-cave', 'loop-lagoon', 'motostoke', 'motostoke-outskirts',
         'motostoke-riverbank', 'north-lake-miloch', 'old-cemetery', 'path-to-the-peak', 'potbottom-desert', 'roaring-sea-caves',
         'rolling-fields', 'slippery-slope', 'slumbering-weald', 'snowslide-slope', 'soothing-wetlands', 'south-lake-miloch',
         'stepping-stone-sea', 'stony-wilderness', 'three-point-pass', 'training-lowlands', 'tunnel-to-the-top', 'warm-up-tunnel',
         'watchtower-ruins', 'west-lake-axewell', 'workout-sea']

class GraphObject:

    def __init__(self, x, edge_index, edge_features, tri_index, y, train_mask, val_mask, test_mask):
        self.x = x
        self.edge_index = edge_index
        self.edge_features = edge_features
        self.tri_index = tri_index
        self.y = y
        self.train_mask = train_mask
        self.val_mask = val_mask
        self.test_mask = test_mask

def find_specific(string, prefix, suffix):
    s_i = string.index(prefix)
    string = string[s_i + len(prefix):]
    s_j = string.index(suffix)
    return string[:s_j]

def repair_sparse(matrix, ideal_shape):
    # Only use this if last few cols/rows are empty and were removed in sparse operation
    i_x, i_y = ideal_shape
    m_x, m_y = matrix.shape[0], matrix.shape[1]
    indices = matrix.coalesce().indices()
    values = matrix.coalesce().values()
    if i_x > m_x or i_y > m_y:
        additional_i = torch.tensor([[i_x - 1], [i_y - 1]], dtype=torch.float)
        additional_v = torch.tensor([0], dtype=torch.float)
        indices = torch.cat([indices, additional_i], dim=1)
        values = torch.cat([values, additional_v], dim=0)
    return torch.sparse_coo_tensor(indices, values)

"""Code to download moves"""
def get_moves():
    URL = "https://pokemondb.net/move/all"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="moves")
    move_name = []
    for result in results:
        try:
            moves = result.findAll("td", {"class": "cell-name"})
            for move in moves:
                move = str(move)
                # Dynamax-cannon is a legitimate move, the rest are max moves which are a gimmick
                if len(move) <= 1 or "-max-" in move or "/max-" in move:
                    continue
                move = find_specific(move, "/move/", '"')
                move_name.append(move)
        except AttributeError:
            continue

    df = {"move_name" : move_name}
    df = pd.DataFrame(df)
    df.to_csv(f"{root_prefix}/moves.csv")

"""code to get pokemon"""
def get_pokemon():
    URL = "https://pokemondb.net/pokedex/national"
    page = requests.get(URL)

    pokemon_list = []
    type_list_1 = []
    type_list_2 = []

    soup = BeautifulSoup(page.content, "html.parser")
    soup = soup.find("main", {"class" : "main-content grid-container"})
    soup = soup.findAll("div" , {"class" : "infocard-list infocard-list-pkmn-lg"})
    for index, gen in enumerate(soup):
        for pokemon in gen:
            p = str(pokemon)
            if len(p) <= 1:
                continue
            pokemon_name = find_specific(p, "/pokedex/", '"')
            pokemon_primary_type = find_specific(p, "/type/", '"')
            p_secondary = p[p.index("/type/") + 6:]
            if p_secondary.find("/type/") == -1:
                pokemon_secondary_type = pokemon_primary_type
            else:
                pokemon_secondary_type = find_specific(p_secondary, "/type/", '"')
            pokemon_list.append(pokemon_name)
            type_list_1.append(pokemon_primary_type)
            type_list_2.append(pokemon_secondary_type)


    df = {"name" : pokemon_list, "type_1" : type_list_1, "type_2" : type_list_2}
    df = pd.DataFrame(df)
    df.to_csv(f"{root_prefix}/pokemon.csv")


def get_pokemon_gen():
    pokemon = pd.read_csv(f"{root_prefix}/pokemon.csv")

    names = pokemon['name']
    pokemon_names_dct = {names[i] : i for i in range(len(names))}
    game_list = ["red-blue-yellow", "gold-silver-crystal" , "ruby-sapphire-emerald", "diamond-pearl", "black-white", "x-y", "sun-moon", "sword-shield"]
    pokemon_games_dct = {game_name : [0 for _ in range(len(names))] for game_name in game_list}

    for game in game_list:
        URL = f"https://pokemondb.net/pokedex/game/{game}"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.findAll("div" , {"class" : "infocard-list infocard-list-pkmn-lg"})
        for result in results:
            for name in result:
                n = str(name)
                if len(n) <= 1:
                    continue
                name = find_specific(n, "/pokedex/", '"')
                index = pokemon_names_dct[name]
                pokemon_games_dct[game][index] = 1

    df = pd.DataFrame(pokemon_games_dct)
    df = df.rename(columns={game_list[i] : i for i in range(8)})
    result = pd.concat([pokemon, df], axis=1, ignore_index=True)

    result.to_csv(f"{root_prefix}/pokemon_half.csv")


def get_pokemon_egg_move():

    moves = pd.read_csv(f"{root_prefix}/moves.csv")[["move_name"]]
    pokemon = pd.read_csv(f"{root_prefix}/pokemon_half.csv").drop(columns = ['Unnamed: 0', '0'])
    pokemon = pokemon.rename(columns = {'1' : 'name'})
    names = pokemon['name']
    moves = moves['move_name']
    pokemon_moves_index_dct = {moves[i] : i for i in range(len(moves))}
    pokemon_moves_dct = {name : [0 for _ in range(len(moves))] for name in names}
    for pokemon_name in names:
        URL = f"https://pokemondb.net/pokedex/{pokemon_name}/egg"
        page = requests.get(URL)

        soup = BeautifulSoup(page.content, "html.parser")
        soup = soup.find("main", {"class": "main-content grid-container"})
        soup = soup.find("div", {"class" : "grid-col span-md-4"})
        move_set = set()
        for move_str in soup:
            move_str = str(move_str)
            if len(move_str) <= 1:
                continue
            key_prefix = "#move-"
            while move_str.find(key_prefix) != -1:
                move = find_specific(move_str, key_prefix, '"')
                move_set.add(move)
                move_str = move_str[move_str.index(key_prefix) + 5 :]
        for move in move_set:
            pokemon_moves_dct[pokemon_name][pokemon_moves_index_dct[move]] = 1

    df = pd.DataFrame(pokemon_moves_dct).transpose().reset_index(drop = True)
    df = pd.concat([pokemon[['name']], df], axis=1, ignore_index=True)
    df.to_csv(f"{root_prefix}/pokemon_egg_moves.csv")


def get_pokemon_level_move():

    moves = pd.read_csv(f"{root_prefix}/moves.csv")[["move_name"]]
    pokemon = pd.read_csv(f"{root_prefix}/pokemon.csv") [['name', 'type_1', 'type_2']]
    pokemon = pokemon.rename(columns = {'1' : 'name'})
    names = pokemon['name']
    moves = moves['move_name']
    pokemon_moves_dct = {moves[i]: i for i in range(len(moves))}
    pokemon_names_dct = {name : [0 for _ in range(len(moves))] for name in names}

    for pokemon_name in names:
        URL = f"https://pokemondb.net/pokedex/{pokemon_name}"
        page = requests.get(URL)

        soup = BeautifulSoup(page.content, "html.parser")
        soup = soup.find("main", {"class" : "main-content grid-container"})
        soup = soup.findAll("div", {"class" : "grid-col span-lg-6"})
        move_set = set()
        if len(soup) == 0:
            continue
        move_str = str(soup[0])
        key_prefix = "/move/"
        while move_str.find(key_prefix) != -1:
            move = find_specific(move_str, key_prefix, '"')
            move_set.add(move)
            move_str = move_str[move_str.index(key_prefix) + 6:]

        for move in move_set:
            pokemon_names_dct[pokemon_name][pokemon_moves_dct[move]] = 1

    two_stage_evos = get_two_stage_evolutions()
    three_stage_name = [*map(lambda lst: [*map(lambda item: names.iloc[item], lst)], three_stage)]

    for first_evo, second_evo in two_stage_evos:
        first_evo_list = pokemon_names_dct[first_evo]
        second_evo_list = pokemon_names_dct[second_evo]

        combined = [int(x or y) for x, y in zip(first_evo_list, second_evo_list)]
        pokemon_names_dct[second_evo] = combined

    for x, y, z in three_stage_name:
        for first_evo, second_evo in [(x, y), (y, z)]:
            first_evo_list = pokemon_names_dct[first_evo]
            second_evo_list = pokemon_names_dct[second_evo]

            combined = [int(x or y) for x, y in zip(first_evo_list, second_evo_list)]
            pokemon_names_dct[second_evo] = combined

    df = pd.DataFrame(pokemon_names_dct).transpose().reset_index(drop = True)
    result = pd.concat([pokemon, df], axis=1, ignore_index=True)
    df.astype(float)
    result.to_csv(f"{root_prefix}/pokemon_level_moves.csv")


def get_pokemon_get_compatible_breeds():
    pokemon = pd.read_csv(f"{root_prefix}/pokemon_half.csv").drop(columns = ['Unnamed: 0', '0'])
    pokemon = pokemon.rename(columns = {'1' : 'name'})
    names = pokemon['name']
    pokemon_name_dct = {names[i]: i for i in range(len(names))}
    pokemon_moves_dct = {name: [0 for _ in range(len(names))] for name in names}
    for pokemon_name in names:
        URL = f"https://pokemondb.net/pokedex/{pokemon_name}/egg"
        page = requests.get(URL)

        soup = BeautifulSoup(page.content, "html.parser")
        soup = soup.find("main", {"class": "main-content grid-container"})
        soup = soup.findAll("div", {"class": "infocard-list infocard-list-pkmn-sm"})
        compatible_pokemon = set()
        for s in soup:
            for div in s.findAll("a", {"class": "infocard"}):
                compatible = find_specific(str(div), "/pokedex/", '"')
                compatible_pokemon.add(compatible)

        for pkm in compatible_pokemon:
            index = pokemon_name_dct[pkm]
            pokemon_moves_dct[pokemon_name][index] = 1

    two_stage_evos = [*map(lambda lst: [*map(lambda item: pokemon_name_dct[item], lst)], get_two_stage_evolutions())]
    three_stage_evos = three_stage

    for i in range(len(names)):
        pokemon_moves_dct[names.loc[i]][i] = 0

    for x, y in two_stage_evos:
        pokemon_moves_dct[names.loc[x]][y] = 0
        pokemon_moves_dct[names.loc[y]][x] = 0

    for x, y, z in three_stage_evos:
        pokemon_moves_dct[names.loc[x]][y] = 0
        pokemon_moves_dct[names.loc[y]][x] = 0
        pokemon_moves_dct[names.loc[z]][y] = 0
        pokemon_moves_dct[names.loc[y]][z] = 0
        pokemon_moves_dct[names.loc[x]][z] = 0
        pokemon_moves_dct[names.loc[z]][x] = 0

    df = pd.DataFrame(pokemon_moves_dct)
    df = pd.concat([pokemon[['name']], df], axis=1, ignore_index=True)
    df.to_csv(f"{root_prefix}/pokemon_compatible_breeds.csv")


def get_two_stage_evolutions():
    pokemon = pd.read_csv(f"{root_prefix}/pokemon.csv").rename(columns = {'1' : 'name'})
    names = pokemon['name']
    three_stage_starter_set = [*map(lambda lst : {*map(lambda item : names.iloc[item], lst)}, three_stage)]
    three_stage_starter_set = set().union(*three_stage_starter_set)

    URL = "https://pokemondb.net/evolution"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    soup = soup.find("main", {"class": "main-content grid-container"})
    soup = soup.findAll("div", {"infocard-list-evo"})
    two_stage_evo_list = []
    for pkm in soup:
        starter = pkm.find("div", {"class": "infocard"})
        first_evo = find_specific(str(starter), "/pokedex/", '"')
        if first_evo in three_stage_starter_set:
            continue
        for p in pkm.findAll("div", {"class": "infocard"}):
            two_stage_evo = [first_evo]
            second_evo = find_specific(str(p), "/pokedex/", '"')
            if first_evo == second_evo:
                continue
            two_stage_evo.append(second_evo)
            two_stage_evo_list.append(two_stage_evo)
    two_stage_evo_list.sort()
    two_stage_evo_list = list(k for k, _ in itertools.groupby(two_stage_evo_list))

    return two_stage_evo_list


def get_pokemon_moves_one_hot():
    moves = pd.read_csv(f"{root_prefix}/moves.csv")[["move_name"]]
    pokemon = pd.read_csv(f"{root_prefix}/pokemon.csv") [['name', 'type_1', 'type_2']]
    pokemon = pokemon.rename(columns = {'1' : 'name'})
    names = pokemon['name']
    moves = moves['move_name']
    pokemon_moves_dct = {moves[i]: i for i in range(len(moves))}
    pokemon_names_dct = {name : [0 for _ in range(len(moves))] for name in names}

    for pokemon_name in names:
        URL = f"https://pokemondb.net/pokedex/{pokemon_name}"
        page = requests.get(URL)

        soup = BeautifulSoup(page.content, "html.parser")
        soup = soup.find("main", {"class" : "main-content grid-container"})
        soup = soup.findAll("div", {"class" : "grid-col span-lg-6"})
        move_set = set()
        for moves_table in soup:
            move_str = str(moves_table)
            key_prefix = "/move/"
            while move_str.find(key_prefix) != -1:
                move = find_specific(move_str, key_prefix, '"')
                move_set.add(move)
                move_str = move_str[move_str.index(key_prefix) + 6:]

        for move in move_set:
            pokemon_names_dct[pokemon_name][pokemon_moves_dct[move]] = 1

    two_stage_evos = get_two_stage_evolutions()
    three_stage_name = [*map(lambda lst: [*map(lambda item: names.iloc[item], lst)], three_stage)]

    for first_evo, second_evo in two_stage_evos:
        first_evo_list = pokemon_names_dct[first_evo]
        second_evo_list = pokemon_names_dct[second_evo]

        combined = [int(x or y) for x, y in zip(first_evo_list, second_evo_list)]
        pokemon_names_dct[second_evo] = combined

    for x, y, z in three_stage_name:
        for first_evo, second_evo in [(x, y), (y, z)]:
            first_evo_list = pokemon_names_dct[first_evo]
            second_evo_list = pokemon_names_dct[second_evo]

            combined = [int(x or y) for x, y in zip(first_evo_list, second_evo_list)]
            pokemon_names_dct[second_evo] = combined

    df = pd.DataFrame(pokemon_names_dct).transpose().reset_index(drop = True)
    result = pd.concat([pokemon, df], axis=1, ignore_index=True)
    result.to_csv(f"{root_prefix}/pokemon_full.csv")


def get_pokemon_egg_group():
    groups = ['amorphous', 'bug', 'dragon', 'fairy', 'field', 'flying', 'grass', 'human-like', 'mineral', 'monster',
              'water-1', 'water-2', 'water-3', 'undiscovered']
    pokemon_df = pd.read_csv(f"{root_prefix}/pokemon.csv")[['name', 'type_1', 'type_2']]
    names = pokemon_df['name']
    group_dct = {group : [0 for _ in range(len(names))] for group in groups}
    pokemon_name_dct = {names[i]: i for i in range(len(names))}
    for group in groups:
        URL = f"https://pokemondb.net/egg-group/{group}"
        page = requests.get(URL)

        soup = BeautifulSoup(page.content, "html.parser")
        soup = soup.find("main", {"class": "main-content grid-container"})
        soup = soup.find("div", {"class": "grid-col span-md-8 span-lg-6"})
        key_prefix = "/pokedex/"
        group_str = str(soup)
        while group_str.find(key_prefix) != -1:
            pokemon = find_specific(group_str, key_prefix, '"')
            group_str = group_str[group_str.index(key_prefix) + len(key_prefix):]
            group_dct[group][pokemon_name_dct[pokemon]] = 1

    size = len(names)
    adj_indices = torch.triu_indices(size, size, offset=1).T

    egg_group_dataset = pd.DataFrame(group_dct)[group_dct.keys()].to_numpy()
    egg_group_dataset = torch.tensor(egg_group_dataset)

    egg_group_features_in, egg_group_features_out = egg_group_dataset[adj_indices[:, 0]], egg_group_dataset[adj_indices[:, 1]]
    egg_group_features_common = torch.logical_and(egg_group_features_in, egg_group_features_out).float()
    egg_group_features_flag = torch.sum(egg_group_features_common, dim=1) > 0

    adj_indices = adj_indices[egg_group_features_flag]

    adj = torch.zeros((size, size))
    adj = adj.index_put_(tuple(adj_indices.T), torch.ones(1)).numpy()

    two_stage_evos = [*map(lambda lst: [*map(lambda item: pokemon_name_dct[item], lst)], get_two_stage_evolutions())]
    three_stage_evos = three_stage


    for i in range(len(names)):
        adj[i, i] = 0

    for x, y in two_stage_evos:
        adj[x, y] = 0
        adj[y, x] = 0

    for x, y, z in three_stage_evos:
        adj[x, y] = 0
        adj[y, x] = 0
        adj[z, y] = 0
        adj[y, z] = 0
        adj[x, z] = 0
        adj[z, x] = 0

    df = pd.DataFrame(adj, columns = [list(names)])

    df = pd.concat([pokemon_df[['name']], df], axis=1, ignore_index=True)
    df.to_csv(f"{root_prefix}/pokemon_egg_groups.csv")



def get_pokemon_locations():
    location_dct = {'kanto' : kanto, 'johto' : johto, 'hoenn' : hoenn, 'sinnoh' : sinnoh,
                    'unova' : unova, 'kalos' : kalos, 'alola' : alola, 'galar' : galar}
    starters = {'kanto' : ['bulbasaur', 'charmander', 'squirtle'],
                'johto' : ['chikorita', 'cyndaquil', 'totodile'],
                'hoenn' : ['treecko', 'torchic', 'mudkip'],
                'sinnoh' :['turtwig', 'chimchar', 'piplup'],
                'unova' : ['snivy', 'tepig', 'oshawott'],
                'kalos' : ['chespin', 'fennekin', 'froakie'],
                'alola' : ['rowlet', 'litten', 'popplio'],
                'galar' : ['grookey', 'scorbunny', 'sobble']}

    no_prefix_urls = {"galar-ballimere-lake", "galar-frigid-sea", "galar-frostpoint-field", "galar-giants-bed",
                      "galar-giants-foot", "galar-path-to-the-peak", "galar-old-cemetery", "galar-roaring-sea-caves",
                      "galar-slippery-slope", "galar-three-point-pass", 'galar-tunnel-to-the-top', 'galar-snowslide-slope',
                      "galar-lakeside-cave"}

    pokemon = pd.read_csv(f"{root_prefix}/pokemon.csv")
    names = pokemon['name']
    nodes = len(names)
    pokemon_names_dct = {names[i]: i for i in range(nodes)}

    dct = {}
    for location in location_dct:
        for sub_location in location_dct[location]:
            dct[f"{location}-{sub_location}"] = [0 for _ in range(nodes)]

    for location in location_dct:
        for index, sub_location in enumerate(location_dct[location]):
            seen_set = set()
            location_str = f"{location}-{sub_location}"
            if location_str in no_prefix_urls:
                location_str = sub_location
            # if index == 0:
            #     seen_set.update(starters[location])
            URL = f"https://pokemondb.net/location/{location_str}"
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, "html.parser")
            soup = soup.find("main", {"class": "main-content grid-container"})
            soup = soup.findAll("td", {"class": "cell-fixed cell-name"})
            for s in soup:
                pokemon_name = find_specific(str(s), '/pokedex/', '"')
                seen_set.add(pokemon_name)
            for pokemon_name in seen_set:
                pokemon_index = pokemon_names_dct[pokemon_name]
                dct[f"{location}-{sub_location}"][pokemon_index] = 1

    df = pd.DataFrame(dct)
    df = pandas.concat([pokemon, df], axis=1, ignore_index=True)
    df.to_csv(f"{root_prefix}/pokemon-regions.csv")


def create_graph_by_game_and_egg_group():

    move_index = [str(i) for i in range(3, 792)]
    labels_per_class = 5

    move_dataset = pd.read_csv(f"{root_prefix}/pokemon_full.csv")
    names = move_dataset['0']
    pokemon_name_dct = {names[i]: i for i in range(len(names))}

    egg_move_dataset = pd.read_csv(f"{root_prefix}/pokemon_egg_moves.csv")[[str(i) for i in range(1, 790)]].to_numpy()
    level_move_dataset = pd.read_csv(f"{root_prefix}/pokemon_level_moves.csv")[[str(i) for i in range(3, 792)]].to_numpy()
    gen_group_dataset = pd.read_csv(f"{root_prefix}/pokemon_half.csv")[[str(i) for i in range(4, 12)]].to_numpy()
    egg_group_edges = pd.read_csv(f"{root_prefix}/pokemon_egg_groups.csv")[[str(i) for i in range(1, 899)]].to_numpy()

    egg_move_dataset = torch.tensor(egg_move_dataset)
    level_move_dataset = torch.tensor(level_move_dataset)
    gen_group_dataset = torch.tensor(gen_group_dataset)
    egg_group_edges = torch.tensor(egg_group_edges)

    adj_indices = torch.nonzero(torch.triu(egg_group_edges))

    gen_features_in, gen_features_out = gen_group_dataset[adj_indices[:, 0]], gen_group_dataset[adj_indices[:, 1]]
    gen_features_common = torch.logical_and(gen_features_in, gen_features_out).float()
    gen_features_flag = torch.sum(gen_features_common, dim=1) > 0

    edges = adj_indices[gen_features_flag]

    learnt_moves = torch.logical_or(egg_move_dataset, level_move_dataset).float()
    node_features = learnt_moves

    egg_moves, parent_moves = learnt_moves[edges[:,0]], learnt_moves[edges[:,1]]
    moves = torch.logical_and(egg_moves, parent_moves).float()
    edge_features = moves

    edges_lst = list(edges)
    edge_set = [{(i.item(), j.item()), (j.item(), i.item())} for i, j in edges_lst]
    seen_set = set().union(*edge_set)

    edge_lst = []
    feature_lst = []

    two_stage_evos = [*map(lambda lst: [*map(lambda item: pokemon_name_dct[item], lst)], get_two_stage_evolutions())]
    three_stage_name = [*map(lambda lst: [*map(lambda item: names.iloc[item], lst)], three_stage)]
    three_stage_evos = three_stage

    for i in range(node_features.shape[0]):
        edge_lst.append([i, i])
        features = torch.logical_and(egg_move_dataset[i], level_move_dataset[i]).float()
        feature_lst.append(features)
        seen_set.add((i, i))

    for x, y in two_stage_evos:
        if (x, y) not in seen_set:
            edge_lst.append([x, y])
            features = (level_move_dataset[y] - level_move_dataset[x]) + egg_move_dataset[x]
            feature_lst.append(features)
            seen_set.add((x, y))


    for x, y, z in three_stage_evos:
        for i, j in [(x, y), (y, z), (x, z)]:
            if (i, j) not in seen_set:
                edge_lst.append([i, j])
                features = (level_move_dataset[j] - level_move_dataset[i]) + egg_move_dataset[i]
                feature_lst.append(features)
                seen_set.add((i, j))

    edge_lst = torch.tensor(edge_lst)
    feature_lst = torch.stack(feature_lst, dim=0)

    edges = torch.cat([edges, edge_lst], dim=0)
    edge_features = torch.cat([edge_features, feature_lst], dim=0)

    adj = torch.zeros((node_features.shape[0], node_features.shape[0]))
    adj = adj.index_put_(tuple(edges.T), torch.ones(1))

    adj_flag_0 = torch.sum(adj, dim=0) > 1
    adj_flag_1 = torch.sum(adj, dim=1) > 1
    adj_flag = torch.logical_or(adj_flag_0, adj_flag_1)

    edge_index = torch.tensor([(i + 1) for i in range(edge_features.shape[0])])
    edge_matrix = torch.sparse_coo_tensor(edges.T, edge_index,
                                          (node_features.shape[0], node_features.shape[0])).to_dense()

    edge_matrix = edge_matrix[adj_flag]
    edge_matrix = edge_matrix[:, adj_flag].to_sparse(2)

    edges = edge_matrix.coalesce().indices()
    edge_index = edge_matrix.coalesce().values() - 1
    edge_features = edge_features[edge_index]

    adj_flag_np = adj_flag.numpy()

    node_features = node_features[adj_flag]

    pokemon_nodes = list(names[adj_flag_np])
    pokemon_nodes_dct = {pokemon_nodes[i]: i for i in range(len(pokemon_nodes))}
    three_stage_index = [*map(lambda lst: [*map(lambda item: pokemon_nodes_dct[item], lst)], three_stage_name)]
    # three_stage_index = three_stage
    three_stage_index = torch.tensor(three_stage_index)

    dataset = move_dataset[['0', '1']][adj_flag_np].reset_index(drop=True)
    dataset_ordered = dataset.sort_values(by=['0'])

    train_index = {pkm_type: [] for pkm_type in pokemon_types}
    test_index = []
    val_index = []

    train_size = 0
    val_size = 0
    test_size = 0

    for index, row in dataset_ordered.iterrows():
        type = row['1']
        if len(train_index[type]) < labels_per_class:
            train_index[type].append(index)
            train_size += 1
        elif val_size < 150:
            val_index.append(index)
            val_size += 1
        else:
            test_index.append(index)
            test_size += 1
        if train_size == (len(pokemon_types) * labels_per_class) and val_size == 150 and test_size == 500:
            break

    s = len(node_features)

    train_index = [train_index[pkm_type] for pkm_type in pokemon_types]
    train_index = torch.tensor([item for sublist in train_index for item in sublist])
    train_mask = torch.zeros(s)
    train_mask.index_fill_(0, train_index, 1)
    train_mask = train_mask > 0

    test_mask = torch.zeros(s)
    test_index = torch.tensor(test_index)
    test_mask.index_fill_(0, test_index, 1)
    test_mask = test_mask > 0

    val_mask = torch.zeros(s)
    val_index = torch.tensor(val_index)
    val_mask.index_fill_(0, val_index, 1)
    val_mask = val_mask > 0

    # labels = [*map(lambda label: pokemon_type_map[label], list(move_dataset['1']))]
    labels = [*map(lambda label: pokemon_type_map[label], list(dataset['1']))]
    label_dataset = torch.tensor(labels)

    assert (node_features.shape[0] == label_dataset.shape[0])
    assert (edges.shape[1] == edge_features.shape[0])
    assert (node_features.shape[0] == train_mask.shape[0])
    assert (node_features.shape[0] == val_mask.shape[0])
    assert (node_features.shape[0] == test_mask.shape[0])

    g = GraphObject(node_features, edges, edge_features, three_stage_index, label_dataset, train_mask, val_mask,
                    test_mask)
    return g


def create_graph_by_moves():

    move_index = [str(i) for i in range(3, 792)]
    labels_per_class = 5

    move_dataset = pd.read_csv(f"{root_prefix}/pokemon_full.csv")
    names = move_dataset['0']
    pokemon_name_dct = {names[i]: i for i in range(len(names))}

    breed_dataset = pd.read_csv(f"{root_prefix}/pokemon_compatible_breeds.csv")[[str(i) for i in range(1,899)]].to_numpy()
    egg_move_dataset = pd.read_csv(f"{root_prefix}/pokemon_egg_moves.csv")[[str(i) for i in range(1,790)]].to_numpy()
    level_move_dataset = pd.read_csv(f"{root_prefix}/pokemon_level_moves.csv")[[str(i) for i in range(3,792)]].to_numpy()

    # node_features = move_dataset[move_index].to_numpy()
    # node_features = torch.tensor(node_features, dtype=torch.float)

    edge_adj = torch.triu(torch.tensor(breed_dataset).T + torch.tensor(breed_dataset))
    # edge_adj = torch.tensor(breed_dataset).T
    edges = list(torch.nonzero(edge_adj))
    edge_set = [{(i.item(), j.item()), (j.item(), i.item())} for i, j in edges]
    seen_set = set().union(*edge_set)

    edges = torch.nonzero(edge_adj)
    egg_move_dataset = torch.tensor(egg_move_dataset)
    level_move_dataset = torch.tensor(level_move_dataset)

    learnt_moves = torch.logical_or(egg_move_dataset, level_move_dataset).float()
    node_features = learnt_moves

    egg_moves, parent_moves = learnt_moves[edges[:,0]], learnt_moves[edges[:,1]]
    moves_0 = torch.logical_and(egg_moves, parent_moves).float()
    egg_moves, parent_moves = learnt_moves[edges[:, 1]], learnt_moves[edges[:, 0]]
    moves_1 = torch.logical_and(egg_moves, parent_moves).float()
    moves = torch.logical_or(moves_0, moves_1).float()
    moves_flag = torch.sum(moves, dim = 1) > 0
    edges = edges[moves_flag]
    edge_features = moves[moves_flag]

    two_stage_evos = [*map(lambda lst: [*map(lambda item: pokemon_name_dct[item], lst)], get_two_stage_evolutions())]
    three_stage_name = [*map(lambda lst: [*map(lambda item: names.iloc[item], lst)], three_stage)]
    three_stage_evos = three_stage

    edge_lst = []
    feature_lst = []

    for i in range(node_features.shape[0]):
        edge_lst.append([i, i])
        features = torch.logical_and(egg_move_dataset[i], level_move_dataset[i]).float()
        feature_lst.append(features)
        seen_set.add((i, i))

    for x, y in two_stage_evos:
        if (x, y) not in seen_set:
            edge_lst.append([x, y])
            features = (level_move_dataset[y] - level_move_dataset[x]) + egg_move_dataset[x]
            feature_lst.append(features)
            seen_set.add((x, y))


    for x, y, z in three_stage_evos:
        # lst = [x, y, z]
        # lst.sort()
        # x, y, z = lst
        for i, j in [(x, y), (y, z), (x, z)]:
            if (i, j) not in seen_set:
                edge_lst.append([i, j])
                features = (level_move_dataset[j] - level_move_dataset[i]) + egg_move_dataset[i]
                feature_lst.append(features)
                seen_set.add((i, j))

    edge_lst = torch.tensor(edge_lst)
    feature_lst = torch.stack(feature_lst, dim = 0)

    edges = torch.cat([edges, edge_lst], dim = 0)
    edge_features = torch.cat([edge_features, feature_lst], dim=0)

    adj = torch.zeros((node_features.shape[0], node_features.shape[0]))
    adj = adj.index_put_(tuple(edges.T), torch.ones(1))

    adj_flag_0 = torch.sum(adj, dim=0) > 1
    adj_flag_1 = torch.sum(adj, dim=1) > 1
    adj_flag = torch.logical_or(adj_flag_0, adj_flag_1)

    edge_index = torch.tensor([(i + 1) for i in range(edge_features.shape[0])])
    edge_matrix = torch.sparse_coo_tensor(edges.T, edge_index, (node_features.shape[0], node_features.shape[0])).to_dense()

    edge_matrix = edge_matrix[adj_flag]
    edge_matrix = edge_matrix[:, adj_flag].to_sparse(2)

    edges = edge_matrix.coalesce().indices()
    edge_index = edge_matrix.coalesce().values() - 1
    edge_features = edge_features[edge_index]

    adj_flag_np = adj_flag.numpy()

    node_features = node_features[adj_flag]

    pokemon_nodes = list(names[adj_flag_np])
    pokemon_nodes_dct = {pokemon_nodes[i] : i for i in range(len(pokemon_nodes))}
    three_stage_index = [*map(lambda lst: [*map(lambda item: pokemon_nodes_dct[item], lst)], three_stage_name)]
    # three_stage_index = three_stage
    three_stage_index = torch.tensor(three_stage_index)

    dataset = move_dataset[['0', '1']][adj_flag_np].reset_index(drop = True)
    dataset_ordered = dataset.sort_values(by=['0'])

    train_index = {pkm_type: [] for pkm_type in pokemon_types}
    test_index = []
    val_index = []

    train_size = 0
    val_size = 0
    test_size = 0

    for index, row in dataset_ordered.iterrows():
        type = row['1']
        if len(train_index[type]) < labels_per_class:
            train_index[type].append(index)
            train_size += 1
        elif val_size < 150:
            val_index.append(index)
            val_size += 1
        else:
            test_index.append(index)
            test_size += 1
        if train_size == (len(pokemon_types) * labels_per_class) and val_size == 150 and test_size == 500:
            break

    s = len(node_features)

    train_index = [train_index[pkm_type] for pkm_type in pokemon_types]
    train_index = torch.tensor([item for sublist in train_index for item in sublist])
    train_mask = torch.zeros(s)
    train_mask.index_fill_(0, train_index, 1)
    train_mask = train_mask > 0

    test_mask = torch.zeros(s)
    test_index = torch.tensor(test_index)
    test_mask.index_fill_(0, test_index, 1)
    test_mask = test_mask > 0

    val_mask = torch.zeros(s)
    val_index = torch.tensor(val_index)
    val_mask.index_fill_(0, val_index, 1)
    val_mask = val_mask > 0

    # labels = [*map(lambda label: pokemon_type_map[label], list(move_dataset['1']))]
    labels = [*map(lambda label: pokemon_type_map[label], list(dataset['1']))]
    label_dataset = torch.tensor(labels)

    assert(node_features.shape[0] == label_dataset.shape[0])
    assert(edges.shape[1] == edge_features.shape[0])
    assert (node_features.shape[0] == train_mask.shape[0])
    assert (node_features.shape[0] == val_mask.shape[0])
    assert (node_features.shape[0] == test_mask.shape[0])

    g = GraphObject(node_features, edges, edge_features, three_stage_index, label_dataset, train_mask, val_mask, test_mask)
    return g

if __name__ == "__main__":
    get_pokemon_egg_group()
