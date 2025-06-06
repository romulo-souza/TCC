# EIXO X EM SEGUNDOS
import subprocess
import time
import matplotlib.pyplot as plt
import pandas as pd

DURATION = 120  # Tempo total de coleta (segundos)
SAMPLE_INTERVAL = 0.4  # Intervalo entre amostras (segundos)


def get_cpu_usage(pid):
    # Executa o comando do ADB para obter o uso de CPU de determinado processo (PID especificado)
    command = f"adb shell top -p {pid} -n 1"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    output = result.stdout
    lines = output.splitlines()

    for line in lines:
        if str(pid) in line:
            parts = line.split()
            try:
                cpu_usage = float(parts[8])  # Extração do valor de CPU (Coluna %CPU)
                print(f"Linha de saída correspondente: {line}")
                print(f"Valor de CPU capturado: {cpu_usage}%\n")
                return cpu_usage
            except (IndexError, ValueError):
                pass
    return None


def plot_graph(cpu_data, timestamps):
    df = pd.DataFrame({"Tempo (s)": timestamps, "CPU": cpu_data})
    df["CPU_MME"] = (
        df["CPU"].ewm(alpha=0.3, adjust=False).mean()
    )  # Média Movel Exponencial (MME)

    # Média geral da MME (tendência suavizada)
    media_mme = df["CPU_MME"].mean()
    print(f"Média geral da MME durante o período: {media_mme:.2f}%")

    # Média dos valores brutos
    media_cpu_bruta = df["CPU"].mean()
    print(f"\nMédia dos valores brutos de consumo de CPU: {media_cpu_bruta:.2f}%")

    # Encontrar o pico de uso
    max_cpu = df["CPU"].max()
    max_index = df["CPU"].idxmax()
    print(f"Pico de uso de CPU: {max_cpu:.2f}%")

    # Configurações de fonte
    plt.rcParams["font.family"] = "Arial"
    plt.rcParams["font.size"] = 12

    # Plotagem das curvas
    plt.figure(figsize=(10, 5))
    plt.plot(
        df["Tempo (s)"],
        df["CPU"],
        label="Consumo de CPU (valores brutos)",
        linestyle="dotted",
        alpha=0.5,
        color="blue",
    )
    plt.plot(
        df["Tempo (s)"], df["CPU_MME"], label="MME do consumo de CPU", color="darkblue"
    )
    plt.plot(df["Tempo (s)"][max_index], max_cpu, "ro")
    plt.text(
        df["Tempo (s)"][max_index], max_cpu + 1, f"Pico: {max_cpu:.2f}%", color="red"
    )
    plt.ylabel("Consumo de CPU (%)")
    plt.xlabel("Tempo decorrido (s)")
    plt.title(f"Evolução do consumo de CPU")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.savefig("ExemploDeCapturaCPU.png", dpi=300, bbox_inches="tight")
    plt.show()


def main(pid):
    cpu_data = []
    timestamps = []

    start_time = time.perf_counter()
    while time.perf_counter() - start_time < DURATION:
        loop_start = time.perf_counter()
        cpu = get_cpu_usage(pid)

        elapsed_time = time.perf_counter() - start_time
        if cpu is not None:
            cpu_data.append(cpu)
            timestamps.append(elapsed_time)

        loop_duration = time.perf_counter() - loop_start
        remaining_time = SAMPLE_INTERVAL - loop_duration
        if remaining_time > 0:
            time.sleep(remaining_time)

    print(f"Duração total: {time.perf_counter() - start_time:.2f} segundos")
    print(f"Amostras coletadas: {len(cpu_data)}")
    plot_graph(cpu_data, timestamps)


if __name__ == "__main__":
    pid = input("Digite o PID do processo: ")
    main(pid)
