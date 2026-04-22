"""List audio devices detected by sounddevice."""

import sounddevice as sd


def main() -> None:
    print("Dispositivos de áudio disponíveis:\n")
    print(sd.query_devices())
    print("\nDispositivo de entrada por defeito:")
    print(f"  {sd.default.device[0]} — {sd.query_devices(sd.default.device[0])['name']}")
    print("\nDispositivo de saída por defeito:")
    print(f"  {sd.default.device[1]} — {sd.query_devices(sd.default.device[1])['name']}")


if __name__ == "__main__":
    main()
