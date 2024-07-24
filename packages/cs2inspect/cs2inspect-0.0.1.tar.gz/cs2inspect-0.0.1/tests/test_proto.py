__author__ = "Lukas Mahler"
__version__ = "0.0.0"
__date__ = "19.07.2024"
__email__ = "m@hler.eu"
__status__ = "Development"

import cs2inspect


def test_masked():
    base_block = cs2inspect.Builder(
        defindex=7,
        paintindex=1035,
        paintseed=144,
        paintwear=0.14680618047714233,
        rarity=4,
        stickers=[
            {'slot': 0, 'sticker_id': 3952, 'wear': 1},
            {'slot': 0, 'sticker_id': 4687, 'wear': 1},
            {'slot': 3, 'sticker_id': 4687, 'wear': 1},
            {'slot': 3, 'sticker_id': 4687, 'wear': 1},
            {'slot': 1, 'sticker_id': 4687, 'wear': 1}
        ]
    )

    try:
        data_block = base_block.build()
    except Exception as e:
        print(f"Build failed: {e}")
        exit(1)

    hex_str = cs2inspect.to_hex(data_block)
    data_block = cs2inspect.from_hex(hex_str)
    link_str = cs2inspect.link(data_block)
    gen_str = cs2inspect.gen(data_block)

    print(data_block)
    print(hex_str)
    print(link_str)
    print(gen_str)


def test_unmasked():
    data_link = {
        'asset_id': '38350177019',
        'class_id': '9385506221951591925',
        'owner_id': '76561198066322090'
    }

    data_gen = {
        'defindex': 7,
        'paintindex': 1035,
        'paintseed': 144,
        'paintwear': 0.14680618047714233,
        'stickers': [
            {'slot': 0, 'sticker_id': 3952, 'wear': 1},
            {'slot': 0, 'sticker_id': 4687, 'wear': 1},
            {'slot': 3, 'sticker_id': 4687, 'wear': 1},
            {'slot': 3, 'sticker_id': 4687, 'wear': 1},
            {'slot': 1, 'sticker_id': 4687, 'wear': 1}
        ]
    }

    link_str = cs2inspect.link(data_link)
    gen_str = cs2inspect.gen(data_gen)

    print(link_str)
    print(gen_str)


def test_simple():

    # Example usage
    proto_base = cs2inspect.Builder(
        defindex=7,
        paintindex=941,
        paintseed=2,
        paintwear=0.22540508210659027,
        rarity=5,
    )

    proto_base.stickers.append({'slot': 2, 'sticker_id': 7203, 'wear': 0})

    try:
        protobuf = proto_base.build()
    except Exception as e:
        print(f"Build failed: {e}")
        exit(1)

    link_str = cs2inspect.link(protobuf)
    gen_str = cs2inspect.gen(protobuf)

    print(link_str)  # =
    print(gen_str)


def main():
    # Test masked
    test_masked()
    print()
    test_unmasked()
    print()
    test_simple()


if __name__ == '__main__':
    main()
