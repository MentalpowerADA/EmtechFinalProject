import time

def create_loading_bar(count):
    bar_length = 20
    progress = count / 20.0
    block = int(round(bar_length * progress))
    loading_bar = "|" + "█" * block + "-" * (bar_length - block) + "|"
    return loading_bar

for i in range(21):
    loading_bar = create_loading_bar(i)
    text = f"\r{loading_bar} {i}/20"
    time.sleep(0.1)
    print(text, end="")

# Add a newline at the end for a clean output
print()