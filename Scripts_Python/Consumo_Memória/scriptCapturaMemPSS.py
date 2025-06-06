import subprocess
import time
import matplotlib.pyplot as plt
import pandas as pd

DURATION = 120  # Tempo total de coleta (segundos)
SAMPLE_INTERVAL = 0.4  # Intervalo entre amostras (segundos)


def get_pss_memory(package_name):
    # Executa o comando 'adb shell dumpsys meminfo' e retorna o PSS em MB
    command = f"adb shell dumpsys meminfo {package_name}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    output = result.stdout
    lines = output.splitlines()

    for line in lines:
        if "TOTAL PSS" in line:
            parts = line.split()
            try:
                pss_memory = float(parts[2]) / 1000  # PSS em MB
                print(f"\nComando executado: {command}")
                print(f"Linha de saída correspondente: {line}")
                print(f"PSS capturado: {pss_memory} MB")
                return pss_memory
            except (IndexError, ValueError):
                pass
    return None


def plot_graph(pss_data, timestamps):
    df = pd.DataFrame({"Tempo (s)": timestamps, "PSS": pss_data})
    df["PSS_MME"] = (
        df["PSS"].ewm(alpha=0.3, adjust=False).mean()
    )  # Média Movel Exponencial (MME)

    # Média geral da MME (tendência suavizada)
    media_pss_mme = df["PSS_MME"].mean()
    print(f"Média geral da MME durante o período: {media_pss_mme:.2f} MB")

    # Média dos valores brutos
    media_pss_bruto = df["PSS"].mean()
    print(f"\nMédia dos valores brutos de consumo de memória PSS: {media_pss_bruto:.2f} MB")

    # Encontrar o pico de uso
    max_pss = df["PSS"].max()
    max_index = df["PSS"].idxmax()
    print(f"Pico de uso de PSS: {max_pss:.2f} MB")

    # Configurações de fonte
    plt.rcParams["font.family"] = "Arial"
    plt.rcParams["font.size"] = 12

    # Plotagem das curvas
    plt.figure(figsize=(10, 5))
    plt.plot(
        df["Tempo (s)"],
        df["PSS"],
        label="Consumo de memória (valores brutos)",
        linestyle="dotted",
        alpha=0.5,
        color="blue",
    )
    plt.plot(
        df["Tempo (s)"],
        df["PSS_MME"],
        label="MME do consumo de memória",
        color="darkblue",
    )
    plt.plot(df["Tempo (s)"][max_index], max_pss, "ro")
    plt.text(
        df["Tempo (s)"][max_index], max_pss + 1, f"Pico: {max_pss:.2f} MB", color="red"
    )

    plt.ylabel("Consumo de Memória (MB)")
    plt.xlabel("Tempo decorrido (s)")
    plt.title(f"Evolução do consumo de memória (PSS)")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.savefig("ExemploDeCapturaMEM.png", dpi=300, bbox_inches="tight")
    plt.show()


def main(package_name):
    pss_data = []
    timestamps = []

    start_time = time.perf_counter()
    while time.perf_counter() - start_time < DURATION:
        loop_start = time.perf_counter()
        pss = get_pss_memory(package_name)

        elapsed_time = time.perf_counter() - start_time
        if pss is not None:
            pss_data.append(pss)
            timestamps.append(elapsed_time)

        loop_duration = time.perf_counter() - loop_start
        remaining_time = SAMPLE_INTERVAL - loop_duration
        if remaining_time > 0:
            time.sleep(remaining_time)

    print(f"\nDuração total: {time.perf_counter() - start_time:.2f} segundos")
    print(f"Amostras coletadas: {len(pss_data)}")
    plot_graph(pss_data, timestamps)


if __name__ == "__main__":
    package_name = input("Digite o nome do pacote do app (ex: com.instagram.android): ")
    main(package_name)
