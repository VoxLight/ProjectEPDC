from pyboy import PyBoy
from PIL import Image


def interact_with_rom(rom_path: str) -> bytes:
    """
    Interact with a ROM using PyBoy.

    Args:
        rom_path (str): The path to the ROM to interact with.
    """
    pyboy = PyBoy(rom_path)
    pyboy.set_emulation_speed(0)
    for i in range(1000):
        pyboy.tick()
    image = pyboy.botsupport_manager().screen().screen_ndarray()
    pil_image = Image.fromarray(image)
    pil_image.save("pokemon_red.png")
    # pil_image.tobytes()
    pyboy.stop()

    return pil_image